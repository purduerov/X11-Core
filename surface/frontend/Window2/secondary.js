const { shell, app, ipcRenderer } = window.require('electron');

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */

    /*
        IPC Connection Section
    */
    ipcRenderer.on('update-info-from', (event, data) => {
      where.setState({
        where.dearclient: data
      });
    });
    
};
