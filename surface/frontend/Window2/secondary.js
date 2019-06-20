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
            invertThrust: where.state.dearflask.thrusters.inverted,
        };

        ipcRenderer.send('config-from-win2', sending);
    }, 50);

    ipcRenderer.on('update-info-from', (event, data) => {
        where.setState({
            dearclient: data,
        });
    });
};
