// const sleep = require('sleep');

function track(start_pos, end_pos) {
  /* start_pos 点击的坐标
  * end_pos 结束的坐标
  * */
  const s_time = new Date().getTime();
  const distance = end_pos[0] - start_pos[0] + 68
  let a = 0.00035, // 加速度
    current = 0, //当前位移
    t = 0.02, //计算间隔
    v = 0, //初速度
    mid = distance * 4 / 5; //  减速阈值
  while (current < distance) {
    v0 = v; //初速度v0
    v = v0 + a * t; //当前速度
    move = v0 * t + 1 / 2 * a * t * t; // 移动距离
    // console.log("每次移动: ", move)
    if (parseInt(move) > 0) {
      current += parseInt(move); //当前位移
      if (current < mid) {
        if (current % (parseInt(Math.random() * 5)) == 0) {
          console.log("当前位移: ", current);
        }
      } else {
        console.log("当前位移: ", current);
      }
    }
  }
  const e_time = new Date().getTime();
  console.log('花费时间: ', e_time - s_time);
}

track([62, 286], [280, 298]);