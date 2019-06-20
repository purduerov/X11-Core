const { shell, app, ipcRenderer } = window.require('electron');
const net = window.require('net');

const base_packet = require("../src/packets.json");

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */
    const socket = io.connect(socketHost, { transports: ['websocket'] });

    // upon new data, save it locally
    socket.on('dearclient-response', (data) => { // Updates the data sent back from the server

        ipcRenderer.send('update-info-to', data); //send data to window 2

        where.setState({
            dearclient: data,
        });

    });

    // send new data
    setInterval(() => { // Sends a message down to the server with updated surface info
        socket.emit('dearRos', where.state.dearflask);
    }, 50);


    /*
        IPC Connection Section
    */

    ipcRenderer.on('buddy-controls-to-win-1', (event, data) => {
        where.setState({
            directions: data,
        });
    });

    ipcRenderer.on('config-from-win2', (event, data) => {
        var flaskcpy = where.flaskcpy;
        flaskcpy.thrusters.inverted = data.invertThrust;

        where.setState({
            config: data.config,
            dearflask: flaskcpy,
        });
    });
    /*
    this.bigCopy = where.dearclient;
    setInterval(() => { //update window 2 info
      where.setState({
        clientStuff = this.bigCopy
      });
      ipcRenderer.send('update-info-to', this.bigCopy)
    }, 50); */


    // updating the gamepad
    setInterval(() => {
        if (where.gp.ready === false) {
        //        console.log("not yet");
            where.gp.selectController();
        }
        if ((where.gp.ready === true) && (where.state.freeze === 0)) {
            where.gp.update();
        //        console.log('success');
        } /* else if (where.state.freeze === 1) {
            where.gp.freeze();
        } */

        where.setState({ // Initiates rendering process
            gp: where.gp,
            dearflask: where.flaskcpy,
        });
    }, 100);


};
