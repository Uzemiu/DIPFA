(function initAxios(){
  axios.defaults.baseURL = 'http://127.0.0.1:5000';
  axios.interceptors.response.use(
    function(response) {
      return Promise.resolve(response.data);
    },
    function(error) {
      return Promise.reject(error);
    }
  );
})();


const app = new Vue({
  el: '#app',
  data: {
    currentImage: null,
    secondImage: null,
    resultImage: [],
    disableReplace: false,
    images: [],
    inCrop: false,
    loading: false,
    command: '',
    // cropper
    cropper:{
      width: 200,
      height: 200
    },
    displayCropperWidth: 200,
    displayCropperHeight: 200,
    // ui
    asideMenu: [
      '图像调整',
      '基本计算',
      '边缘检测',
      '图像增强',
      '形态学操作',
      '噪声滤波',
      '其他'
    ],
    currentCollapseName: '',
    selectedAsideMenu: 0,
    // popup
    dialogVisible: false,
    // aside menu中具体项目
    logicOp: [
      ['and', '与运算'],
      ['or', '或运算'],
      ['not', '非运算']
    ],
    arthimaticOp: [
      ['add', '加运算'],
      ['subtract', '减运算'],
      ['multiply', '乘运算'],
      ['divide', '除运算']
    ],
    geometricOp: [
      ['scale', '缩放'],
      ['translate', '平移'],
      ['rotate', '旋转'],
    ],
    geometricOpArgs: {
      x: 0,
      y: 0,
      xArg: 0,
      yArg: 0,
      deg: 0
    },
    flipOp: [
      ['flipHor', '水平翻转'],
      ['flipVer', '垂直翻转']
    ],
    affineOp: [
      ['affine', '仿射变换']
    ],
    affineArgs: {
      post1: [[0,0],[0,0],[0,0]],
      post2: [[0,0],[0,0],[0,0]],
    },
    // 边缘检测
    edgeOp: [
      ['roberts', 'Roberts'],
      ['sobel', 'Sobel'],
      ['laplacian', 'Laplacian'],
      ['LoG', 'LoG'],
      ['canny', 'Canny']
    ],
    edgeArgs: {
      blurSize: 3,
      ksize: 3,
      threshold1: 50,
      threshold2: 150
    },
    houghOp: [
      ['hough', '霍夫变换'],
      ['houghP', '概率霍夫变换']
    ],
    houghArgs: {
      blurSize: 3,
      cannyThreshold1: 50,
      cannyThreshold2: 150,
      houghThreshold: 120,
      minLineLength: 120,
      maxLineGap: 15
    },
    // 噪声
    noiseOp: [
      ['spNoise', '椒盐噪声'],
      ['gaussianNoise', '高斯噪声'],
    ],
    noiseArgs: {
      svp: 0.5,
      amount: 0.04,
      mean: 0,
      sigma: 25
    },
    // 滤波01
    blurOp: [
      ['maxBlur', '最大值滤波'],
      ['avgBlur', '均值滤波'],
      ['minBlur', '最小值滤波'],
      ['medBlur', '中值滤波'],
      ['gaussianBlur', '高斯滤波'],
      ['geometricBlur', '几何均值滤波'],
      ['harmonicBlur', '谐波均值滤波']
    ],
    blurArgs: {
      x: 3,
      y: 3,
      ksize: 3
    },
    // 滤波02
    selectiveOp: [
      ['lowPass', '低通滤波'],
      ['highPass', '高通滤波'],
      ['bandPass', '带通滤波'],
      ['bandStop', '带阻滤波'],
    ],
    selectiveArgs: {
      threshold1: 0,
      threshold2: 255
    },
    // 形态学操作
    morphOp: [
      ['morphOpen', '开操作'],
      ['morphClose', '闭操作'],
      ['morphErode', '腐蚀'],
      ['morphDilate', '膨胀'],
    ],
    morphArgs: {
      kernelSize: 5,
      kernelType: 'morph rect'
    },
    // 频域的平滑/频域的锐化
    filterOp1: [
      ['lpFilter', '理想低通滤波'],
      ['hpFilter', '理想高通滤波'],
      ['blpFilter', '巴特沃兹低通滤波'],
      ['bhpFilter', '巴特沃兹高通滤波'],
      ['glpFilter', '高斯低通滤波'],
      ['ghpFilter', '高斯高通滤波'],
    ],
    filterArgs1: {
      d0: 50,
      n: 2
    },
    // 空域的平滑
    filterOp2: [
      ['robertsGrad', 'Roberts算子'],
      ['sobelGrad', 'Sobel算子'],
      ['prewittGrad', 'Prewitt算子'],
      ['laplacianGrad', 'Laplacian算子'],
    ],
    // 其他
    otherOp: [
      ['hist', '直方图统计'],
      ['getRGB', 'RGB'],
      ['getHSV', 'HSV']
    ]
  },
  methods: {
    selectAsideCollapse(index){
      this.selectedAsideMenu = index;
      this.command = ''; // clear command
    },
    switchImage(index){
      this.inCrop = false;
      this.currentImage = index;
    },
    setCommand(command){
      this.command = command;
    },
    replaceResultImage(){
      this.images[this.currentImage] = this.resultImage[0];
      this.dialogVisible = false;
    },
    addResultImage(){
      this.images.push(...this.resultImage);
      this.dialogVisible = false;
    },
    //---crop---
    startCrop(){
      if(this.currentImage !== null){
        this.inCrop = true;
      }
    },
    cancelCrop(){
      this.inCrop = false;
    },
    endCrop(){
      this.$refs.cropper.getCropData(data => {
        this.images[this.currentImage] = data;
        this.inCrop = false;
      })
    },
    onCropperMove(preview){
      this.displayCropperHeight = preview.h >> 0;
      this.displayCropperWidth = preview.w >> 0;
    },
    setCropperSize(){
      this.cropper.width = this.displayCropperWidth;
      this.cropper.height = this.displayCropperHeight;
    },
    //---command---
    cancelAction(){
      if(this.inCrop){
        this.cancelCrop();
        return;
      }
      // cancel request
      this.controller.abort();
    },
    confirmAction(args){
      if(this.loading){
        this.$message.warning('正在进行其他处理操作')
        return;
      }
      if(this.inCrop){
        this.endCrop();
        return;
      }
      if(!this.command){
        this.$message.warning('未选择操作');
        return;
      }
      if(this.currentImage === null){
        this.$message.warning('未选择图片');
        return;
      }
      const files = [this.images[this.currentImage]];
      if(this.multiInput){
        if(!this.secondImage){
          this.$message.warning('未选择第二张图片')
          return;
        }
        files.push(this.secondImage)
      }
      this.process(files, this.command, args);
    },
    //---collapse---
    onCollapseChange(newCollapse){
      if(newCollapse !== '' && newCollapse !== 'adjust-01'){
        this.cancelCrop();
      }
    },
    //---api---
    process(base64Images, command, args={}){
      function dataURLtoBlob(dataurl) {
        var arr = dataurl.split(','),
        mime = arr[0].match(/:(.*?);/)[1],
        bstr = atob(arr[1]),
        n = bstr.length,
        u8arr = new Uint8Array(n);
        while (n--) {
            u8arr[n] = bstr.charCodeAt(n);
        }
        return new Blob([u8arr], {
            type: mime
        });
      }

      this.loading = true;
      this.controller = new AbortController();

      const param = new FormData();
      base64Images.forEach((img,i) => {
        param.append('files', dataURLtoBlob(img),new Date().getTime() + '' + i);
      })
      param.append('command', command);
      param.append('args', JSON.stringify(args));
      return axios.post('/process', param, {
        'Content-Type': 'multipart/form-data',
        signal: this.controller.signal
      }).then(data => {
        this.resultImage = data.data.map(e => 'data:image/jpeg;base64,' + e);
        this.dialogVisible = true;
      }).catch(e => {
        console.error(e);
        if(e.response){
          const msg = e.response.data.message;
          this.$message.error(msg);
        }
      }).finally(() => {
        this.loading = false;
      });
    },
    uploadImage(file, onload){
      const reader = new FileReader();
      reader.onload = onload || (e => {
        this.images.push(e.target.result);
        if(this.currentImage === null){
          this.currentImage = 0;
        }
      });
      reader.readAsDataURL(file);
      return false;
    },
    uploadSecondImage(file){
      this.uploadImage(file, e => {
        this.secondImage = e.target.result;
      })
      return false;
    },
  },
  computed: {
    multiInput(){
      return this.currentCollapseName.indexOf('[mul]') >= 0 && this.command !== 'not';
    },
  }
});