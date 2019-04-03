const s = require('net').Socket();

const packet = require('../frontend/src/packets.json');

s.setEncoding("utf-8");

let t1 = null;
let t2 = null;

function connect() {
    s.connect(5001, 'localhost');
}

s.on('connect', () => {
    console.log('Connected!');

    t1 = setTimeout(() => {
        s.write("end");
    }, 5000);

    t2 = setInterval(() => {
        s.write(JSON.stringify(packet));
    }, 500);
});

s.on('data', (d) => {
    console.log(d.toString());
});

s.on('error', (e) => {
    console.log(e.toString());
    setTimeout(connect, 500);
});

s.on('end', (d) => {
    console.log('Connection closed');
    s.end();
    clearInterval(t2);
    clearInterval(t1);
});


connect()
