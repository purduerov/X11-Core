const { shell, app, ipcRenderer } = window.require('electron');

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */

    /*
        IPC Connection Section
    */
    setInterval(() => {
        var sending = {
            config: where.state.config,
            invertThrust: where.state.dearflask.thrusters.inverted_thrusters,
        };

        ipcRenderer.send('config-from-win2', sending);
    }, 50);
};
