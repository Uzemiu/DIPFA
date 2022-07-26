# flaskProject

### 说明

本项目使用flask作为后端，采用网页的形式进行展示，交互

### 环境

python3.7+

### 开始

```
pip install -r requirements.txt
python app.py # 默认在 127.0.0.1:5000
```
如果打算使用 GPU，由于 cuda 版本不同，pytorch 和 torchvision 需要自行下载，建议从以下网站找到对应版本下载 whl 文件安装 \
https://download.pytorch.org/whl/torch/
https://download.pytorch.org/whl/torchvision/
```python
import torch
torch.cuda.is_available() # 返回 True 才能使用 GPU
```

#### 风格迁移说明
<code>models</code>下包含风格迁移的模型文件下载地址，需运行 models.bat 和 myModels.bat 下载 \
其中，models.bat 下载固定风格任意内容的模型，myModels.bat 下载任意风格任意内容的模型。\
任意风格任意内容迁移的代码、研究与报告见 ./style_transfer/。
```
- models
  - style_transfer
    - COCO2014_1000
      - *.png
    - metanet_base32_style300000.0_tv1e-06_tagnohvd.pth
    - metanet_base32_style300000.0_tv1e-06_tagnohvd_transform_net.pth
  - candy.t7
  - feathers.t7
  - *.t7
```
myModels.bat 受限于服务器带宽，下载所有文件需要约 30 min。\
为了减少下载时间:
1. 如果本地已经有完整的 COCO2014，可以运行 genCOCO2014_1000.py 脚本生成数据集 \
如果没有，可以运行 getCOCO2014_1000.bat 下载， \
也可以从[这里](http://images.cocodataset.org/zips/train2014.zip)下载，解压并运行 genCOCO2014_1000.py 脚本 \
需要将 genCOCO2014_1000.py 的这行改成自己数据集的路径
```python
src = "../../COCO2014/train2014"
```
2. 目前已经将 vgg19 改成了 pretrained=True，通过 torchvision 下载，所以项目初次运行会先进行下载。 \
如果下载不了的话可以找其他的源下载，并修改代码，\
或者运行 getVgg19.bat 从服务器获取，享受极(慢)速(度)(约 20 min)
```python
vgg19 = models.vgg19(pretrained=False)
vgg19.load_state_dict(torch.load(${模型路径}))
```

![style transfer](./images/style_transfer.png)
如图，左侧为内容图，右侧为风格图。对于一张风格图，第一次运行会花费额外的时间（取决于设备）。
之后风格图不变，更换内容图，进行迁移需要约 5-8s。