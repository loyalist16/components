// const battery = require('battery');
// console.log(battery);
// (async () => {
//   const {level, charging} = await battery();
//
//   console.log(level);
//   //=> 0.8
//
//   console.log(charging);
//   //=> true
// })();

var navigator = {};

navigator.getBattery = function () {
  let num = 0.6;
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      num > 0.5 ? resolve({level: 1, charging: true}) : reject(num);
    }, 1000);
  })
};

var u = navigator.getBattery

function o(v) {
  console.log('这是o函数: ', v);
}
var e = 0, i='lalala';
u.call(navigator).then(
  function (n) {
    o(e = n)
  },
  function () {
    e = i
  })

console.log(e)
// u.call(navigator).then(val => {
//   console.info(`Status switches to fulfilled, and the value is ${val.level}`);
// }, val => {
//   console.info(`Status switches to reject, and the value is ${val}`);
// })