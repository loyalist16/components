const { Canvas } = require('canvas');
// let c = require('canvas');

Canvas.prototype.getContext = function (v) {
    if (v === '2d'){
        return this.getContext('2d');
    }else {
        return {
            canvas: this,
            getExtension: function (v) {
                return {
                    UNMASKED_RENDERER_WEBGL: 37446,
                };
            },
            getParameter: function (v) {
                return "ANGLE (Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0)";
            }
        }
    }
}
canvas = new Canvas(300, 150);
n = canvas.getContext('webgl');
e = "0";
o = n.getExtension('s');
console.log(o);
u = n.getParameter(o.UNMASKED_RENDERER_WEBGL);
console.log(u)