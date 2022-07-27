# -*- coding: utf-8 -*- 
""" 
@File : myTransfer.py.py 
@Author: csc
@Date : 2022/7/24
"""
import os

# os.environ['CUDA_VISIBLE_DEVICES'] = '5'

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import torchvision
import torchvision.transforms as transforms
import torchvision.models as models

import random
import shutil
from glob import glob
from tqdm import tqdm
from PIL import Image
import imagehash
import copy

from utils import *
from models import *

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# device = 'cpu'


class MetaNet(nn.Module):
    def __init__(self, param_dict):
        super(MetaNet, self).__init__()
        self.param_num = len(param_dict)
        self.hidden = nn.Linear(1920, 128 * self.param_num)
        self.fc_dict = {}
        for i, (name, params) in enumerate(param_dict.items()):
            self.fc_dict[name] = i
            setattr(self, 'fc{}'.format(i + 1), nn.Linear(128, params))

    # ONNX 要求输出 tensor 或者 list，不能是 dict
    def forward(self, mean_std_features):
        hidden = F.relu(self.hidden(mean_std_features))
        filters = {}
        for name, i in self.fc_dict.items():
            fc = getattr(self, 'fc{}'.format(i + 1))
            filters[name] = fc(hidden[:, i * 128:(i + 1) * 128])
        return list(filters.values())

    def forward2(self, mean_std_features):
        hidden = F.relu(self.hidden(mean_std_features))
        filters = {}
        for name, i in self.fc_dict.items():
            fc = getattr(self, 'fc{}'.format(i + 1))
            filters[name] = fc(hidden[:, i * 128:(i + 1) * 128])
        return filters


backbone = models.vgg19(pretrained=True)
backbone = VGG19(backbone.features[:30]).to(device).eval()

base = 32

# 可视化
width = 256
data_transform = transforms.Compose([
    transforms.RandomResizedCrop(width, scale=(256 / 480, 1), ratio=(1, 1)),
    transforms.ToTensor(),
    tensor_normalizer
])

style_weight = 3e5
content_weight = 1
tv_weight = 1e-6
batch_size = 8

content_dataset = torchvision.datasets.ImageFolder('./models/COCO2014_1000/', transform=data_transform)
content_data_loader = torch.utils.data.DataLoader(content_dataset, batch_size=batch_size, shuffle=True)

# style buffer
buffer = {}


def style_transfer(style_img, content_img):
    transform_net = TransformNet(base, residuals='resnext').to(device)
    metanet = MetaNet(transform_net.get_param_dict()).to(device)
    # 每次都加载一次来实现类似深拷贝的效果
    transform_net.load_state_dict(torch.load('./models/metanet_base32_style300000.0_tv1e-06_tagnohvd_transform_net.pth'))
    metanet.load_state_dict(torch.load('./models/metanet_base32_style300000.0_tv1e-06_tagnohvd.pth'))

    trainable_params = {}
    trainable_param_shapes = {}
    for model in [backbone, transform_net, metanet]:
        for name, param in model.named_parameters():
            if param.requires_grad:
                trainable_params[name] = param
                trainable_param_shapes[name] = param.shape

    optimizer = optim.Adam(trainable_params.values(), 1e-3)

    # hash
    key = imagehash.phash(Image.fromarray(style_img), hash_size=8, highfreq_factor=4)

    style_img = image_to_tensor(style_img, 256)
    content_img = image_to_tensor(content_img, 256)
    style_image = style_img.to(device)
    content_image = content_img.to(device)

    if key in buffer:
        _transform_net = buffer[key]
        transformed_images = _transform_net(content_image)
    else:
        style_features = backbone(style_image)
        style_mean_std = mean_std(style_features)

        n_batch = 20
        with tqdm(enumerate(content_data_loader), total=n_batch) as pbar:
            for batch, (content_images, _) in pbar:
                x = content_images.cpu().numpy()
                if (x.min(-1).min(-1) == x.max(-1).max(-1)).any():
                    continue

                optimizer.zero_grad()

                # 使用风格图像生成风格模型
                weights = metanet.forward2(mean_std(style_features))
                transform_net.set_weights(weights, 0)

                # 使用风格模型预测风格迁移图像
                content_images = content_images.to(device)
                transformed_images = transform_net(content_images)

                # 使用 vgg19 计算特征
                content_features = backbone(content_images)
                transformed_features = backbone(transformed_images)
                transformed_mean_std = mean_std(transformed_features)

                # content loss
                content_loss = content_weight * F.mse_loss(transformed_features[2], content_features[2])

                # style loss
                style_loss = style_weight * F.mse_loss(transformed_mean_std,
                                                       style_mean_std.expand_as(transformed_mean_std))

                # total variation loss
                y = transformed_images
                tv_loss = tv_weight * (torch.sum(torch.abs(y[:, :, :, :-1] - y[:, :, :, 1:])) +
                                       torch.sum(torch.abs(y[:, :, :-1, :] - y[:, :, 1:, :])))

                # 求和
                loss = content_loss + style_loss + tv_loss

                loss.backward()
                optimizer.step()

                if batch > n_batch:
                    break

        buffer[key] = transform_net
        transformed_images = transform_net(content_image)

    transformed_images_vis = torch.cat([x for x in transformed_images], dim=-1)

    return recover_image(transformed_images_vis)

