const { shell, app, ipcRenderer } = window.require('electron');
var keyBind = require('./keyBind.js');


module.exports = (where, socketHost) => {
    var buddy = None;
    /*
        Socket Connection Section
    */

    /*
        IPC Connection Section
    */
    ipcRenderer.on('update-info-from', (event, data) => {
        where.setState({
            dearclient: data,
        });
    });

    /*
      Keyboard controls section
    */

    buddy = new keyBind(where);
}; // end export
