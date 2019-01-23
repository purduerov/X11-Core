const { shell, app, ipcRenderer } = window.require('electron');

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */
    const socket = io.connect(socketHost, { transports: ['websocket'] });

    // upon new data, save it locally
    socket.on('dearclient', (data) => { // Updates the data sent back from the server
        this.clientcpy = data;

        this.setState({
            dearclient: this.clientcpy,
        });
    });

    // request new data
    setInterval(() => {
        socket.emit('dearclient');
    }, 50);

    // send new data
    setInterval(() => { // Sends a message down to the server with updated surface info
        socket.emit('dearflask', where.state.dearflask);
    }, 50);


    /*
        IPC Connection Section
    */

    ipcRenderer.on('other-main-window-message', (event, data) => {
      console.log("other-main-window-message received, the message was: " + data);
    });
};
