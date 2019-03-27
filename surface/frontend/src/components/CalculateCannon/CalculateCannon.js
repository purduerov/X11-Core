const math = require('math.js');


var r1 = args.r1;
var r2 = args.r2;
var r3 = args.r3;
var height = args.height;
var volume = (Math.PI / 3) * (Math.pow(r1,2) + r1 * r3 + Math.pow(r3,2)) * height;
volume -= Math.PI * Math.pow(r2,2) * height;

console.log(JSON.stringify({ }))
