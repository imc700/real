// 页面完全加载完成所耗时间----最重要!!!
var mytiming = window.performance.timing;
var result = mytiming.responseStart - mytiming.navigationStart;
console.log('ari:', result);