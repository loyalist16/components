// 一些常用的hook函数

// 打印调用堆栈
function printStack() {
    send(Java.use("android.util.Log").getStackTraceString(Java.use("Java.lang.Exception").$new()));
}

// bytesArray 转 string
function array2string(bytesArray) {
    var buffer = Java.array('byte', bytesArray);
    var result = "";
    for (var i = 0; i < buffer.length; i++) {
        result += (String.fromCharCode(buffer[i]))
    }
}