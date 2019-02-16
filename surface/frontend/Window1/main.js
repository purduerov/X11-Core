const { shell, app, ipcRenderer } = window.require('electron');

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */
    const socket = io.connect(socketHost, { transports: ['websocket'] });

    // upon new data, save it locally
    socket.on('dearclient', (data) => { // Updates the data sent back from the server
        where.clientcpy = data;

        where.setState({
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

    ipcRenderer.on('buddy-controls-from-win-1', (event, data) => {
        where.setState({
          directions: data
        });
    });


    //updating the gamepad
    setInterval(() => {
      if(where.gp.ready === false) {
//        console.log("not yet");
        where.gp.selectController();
      }
      if((where.gp.ready === true) && (where.state.freeze === 0)) {
        where.gp.update();
//        console.log('success');
} else if (where.state.freeze === 1){
        this.gp.freeze();
      }

      where.setState({                           //Initiates rendering process
        gp: where.gp,
        dearflask: where.flaskcpy
      });
    }, 100);


};
