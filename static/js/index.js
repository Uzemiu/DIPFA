(function initAxios(){
  axios.interceptors.response.use(
    function(response) {
      console.log(response);
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
    images: [],
    inCrop: false,
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
      '噪声滤波'
    ],
    currentCollapseName: '',
    selectedAsideMenu: 0,
  },
  methods: {
    selectAsideCollapse(index){
      this.selectedAsideMenu = index;
    },
    switchImage(index){
      this.inCrop = false;
      this.currentImage = index;
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
    },
    confirmAction(){
      if(this.inCrop){
        this.endCrop();
        return;
      }
    },
    //---collapse---
    onCollapseChange(newCollapse){
      if(newCollapse !== '' && newCollapse !== 'adjust-01'){
        this.cancelCrop();
      }
      console.log(newCollapse);
    },
    //---api---
    process(files, command, args={}){
      const param = new FormData();
      files.forEach((file,i) => {
        param.append('files', file, new Date().getTime() + '' + i);
      })
      param.append('command', command);
      param.append('args', JSON.stringify(args));
      axios.post('/process', param, {
        'Content-Type': 'multipart/form-data'
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
    }
  },
  computed: {
    multiInput(){
      return this.currentCollapseName.indexOf('[mul]') >= 0;
    }
  }
});