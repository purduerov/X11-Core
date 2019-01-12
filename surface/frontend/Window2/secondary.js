const { shell, app, ipcRenderer } = window.require('electron');

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */

    /*
        IPC Connection Section
    */
    ipcRenderer.on('second-window-message', (event, data) => {
        console.log("Here's the response to the button click");
        console.log(data);
    });

};
