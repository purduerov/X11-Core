const { shell, app, ipcRenderer } = window.require('electron');

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */

    /*
        IPC Connection Section
    */
    ipcRenderer.on('window-message', (event, data) => {
        console.log("window-message received");
        ipcRenderer.send('reply', "This is a reply sending from window 2")
        console.log(data);
    });
    
};
