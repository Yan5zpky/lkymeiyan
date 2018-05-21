//index.js
//获取应用实例
const app = getApp()

Page({
  data: {
    motto: 'Hello World',
    userInfo: {},
    hasUserInfo: false,
    canIUse: wx.canIUse('button.open-type.getUserInfo'),
    beautyFilePath: '',
    originFilePath: '',
    hideView: "display:block;",
    showView: "display:none"
  },
  //事件处理函数
  bindViewTap: function() {
    wx.navigateTo({
      url: '../logs/logs'
    })
  },
  onLoad: function () {
    if (app.globalData.userInfo) {
      this.setData({
        userInfo: app.globalData.userInfo,
        hasUserInfo: true
      })
    } else if (this.data.canIUse){
      // 由于 getUserInfo 是网络请求，可能会在 Page.onLoad 之后才返回
      // 所以此处加入 callback 以防止这种情况
      app.userInfoReadyCallback = res => {
        this.setData({
          userInfo: res.userInfo,
          hasUserInfo: true
        })
      }
    } else {
      // 在没有 open-type=getUserInfo 版本的兼容处理
      wx.getUserInfo({
        success: res => {
          app.globalData.userInfo = res.userInfo
          this.setData({
            userInfo: res.userInfo,
            hasUserInfo: true
          })
        }
      })
    }
  },
  getUserInfo: function(e) {
    console.log(e)
    app.globalData.userInfo = e.detail.userInfo
    this.setData({
      userInfo: e.detail.userInfo,
      hasUserInfo: true
    })
  },
  // 上传图片
  makeupImage: function() {
    var _this = this; 
    wx.chooseImage({
      sizeType: ['compressed'],
      success: function (res) {
        var tempFilePaths = res.tempFilePaths
        wx.uploadFile({
          url: 'http://182.254.214.99/makeup?sunglass=1', 
          filePath: tempFilePaths[0],
          name: 'file',
          formData: {

          },
          success: function (res) {
            var data = res.data
            var obj = JSON.parse(data);
            _this.setData({
              beautyFilePath: "http://182.254.214.99/static/" + obj.beautifulpath,
              originFilePath: obj.originpath,
              hideView: "display:none;",
              showView: "display:block;"
            })
            
          }
        })
      }
    })
  },
  //保存图片
  saveImage: function(e) {
    wx.downloadFile({
      url: e.target.dataset.imageurl,
      success: function (res) {
        wx.saveImageToPhotosAlbum({
          filePath: res.tempFilePath,
          success: function (res) {
            console.log(res)
          },
          fail: function (res) {
            console.log(res)
            console.log('fail')
          }
        })
      },
      fail: function () {
        console.log('fail')
      }
    }) 
  },
  //去掉墨镜
  removeSunglass: function (e) {
    var _this = this;
    wx.chooseImage({
      sizeType: ['compressed'],
      success: function (res) {
        var tempFilePaths = res.tempFilePaths
        wx.uploadFile({
          url: 'http://182.254.214.99/makeup?sunglass=0',
          filePath: tempFilePaths[0],
          name: 'file',
          formData: {

          },
          success: function (res) {
            var data = res.data
            var obj = JSON.parse(data);
            _this.setData({
              beautyFilePath: "http://182.254.214.99/static/" + obj.beautifulpath,
              originFilePath: obj.originpath,
              hideView: "display:none;",
              showView: "display:block;"
            })

          }
        })
      }
    })
  },
  // 滤镜1
  countour: function (e) {
    var _this = this;
    wx.chooseImage({
      sizeType: ['compressed'],
      success: function (res) {
        var tempFilePaths = res.tempFilePaths
        wx.uploadFile({
          url: 'http://182.254.214.99/makeup?sunglass=0&filterType=2',
          filePath: tempFilePaths[0],
          name: 'file',
          formData: {

          },
          success: function (res) {
            var data = res.data
            var obj = JSON.parse(data);
            _this.setData({
              beautyFilePath: "http://182.254.214.99/static/" + obj.beautifulpath,
              originFilePath: obj.originpath,
              hideView: "display:none;",
              showView: "display:block;"
            })

          }
        })
      }
    })
  },
  //滤镜2
  //去掉墨镜
  emboss: function (e) {
    var _this = this;
    wx.chooseImage({
      sizeType: ['compressed'],
      success: function (res) {
        var tempFilePaths = res.tempFilePaths
        wx.uploadFile({
          url: 'http://182.254.214.99/makeup?sunglass=0&filterType=6',
          filePath: tempFilePaths[0],
          name: 'file',
          formData: {

          },
          success: function (res) {
            var data = res.data
            var obj = JSON.parse(data);
            _this.setData({
              beautyFilePath: "http://182.254.214.99/static/" + obj.beautifulpath,
              originFilePath: obj.originpath,
              hideView: "display:none;",
              showView: "display:block;"
            })

          }
        })
      }
    })
  }
})
