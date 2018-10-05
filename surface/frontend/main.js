let socketHost = `ws://raspberrypi.local:5000`;
let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');


module.exports = (where) => {
    // upon new data, save it locally
    socket.on("dearclient", (data) => {    //Updates the data sent back from the server
        this.clientcpy = data;
        
        this.setState({
          dearclient: this.clientcpy
        });
    });

    // request new data
    setInterval(() => {
        socket.emit("dearclient");
    }, 50);

    // send new data
    setInterval(() => {             //Sends a message down to the server with updated surface info
        socket.emit("dearflask", where.state.dearflask);
    }, 50);
}
