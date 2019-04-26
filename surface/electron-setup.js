const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const url = require('url');
const spawn = require('child_process').spawn;

// Keep a global reference of the window object, if you don't, the window will
// be closed automatically when the JavaScript object is garbage collected.
const cvbin = './pakfront/bin/';
var cvspawns = {};
var cvref = {};

// TODO: webpack.config.js needs to be configured to work with multiple input files
const files = ['frontend/Window1/main.html', 'frontend/Window2/secondary.html']; //, 'frontend/Window3/buddy.html'];

const windows = [null, null, null];

// Spawning process variables, for proof of concept only currently
var py = spawn('python', [`${cvbin}print.py`]);

var data = [1, 2, 3, 4, 5, 6, 7, 8, 9];
var dataString = '';

// ----------------------------------------------------------------------------------------
// Importing this adds a right-click menu with 'Inspect Element' option [worth it]
require('electron-context-menu')({
    prepend: (params, browserWindow) => [{
        label: 'Rainbow',
        // Only show it when right-clicking images
        visible: params.mediaType === 'image',
    }],
});
// ----------------------------------------------------------------------------------------

function closeWin(i) {
    return () => {
        // Dereference the window object, usually you would store windows
        // in an array if your app supports multi windows, this is the time
        // when you should delete the corresponding element.
        windows[i] = null;
    };
}

function createWindow() {
    var i;

    // Create the browser window.

    for (i = 0; i < files.length; i++) {
        // Curious if a macOS works better this way with multi-windows...
        if (windows[i] == null) {
            windows[i] = new BrowserWindow({ width: 1600, height: 1200 });

            // and load the index.html of the app.
            windows[i].loadURL(url.format({
                pathname: path.join(__dirname, files[i]),
                protocol: 'file:',
                slashes: true,
            }));

            // Open the DevTools.
            windows[i].webContents.openDevTools();

            // Emitted when the window is closed.
            windows[i].on('closed', closeWin(i));
        }
    }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.on('ready', createWindow);

// Quit when all windows are closed.
app.on('window-all-closed', () => {
    // On macOS it is common for applications and their menu bar
    // to stay active until the user quits explicitly with Cmd + Q
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    createWindow();
});

ipcMain.on('timer-parameters', (event, message) => {
    for (let i = 0; i < windows.length; i++) {
        if (windows[i] != null) {
            windows[i].webContents.send('timer-parameters-from-main', message);
        }
    }
});

ipcMain.on('buddy-controls-from-win-3', (event, message) => {
    if (windows[0] != null) {
        windows[0].webContents.send('buddy-controls-to-win-1', message);
    }
});

ipcMain.on('config-from-win2', (event, configs) => {
    if (windows[0] != null) {
        windows[0].webContents.send('config-from-win2', configs);
    }
});

ipcMain.on('update-info-to', (event, message) => {
    if (windows[1] != null) {
        windows[1].webContents.send('update-info-from', message);
    }
    if (windows[2] != null) {
        windows[2].webContents.send('update-info-from', message);
    }
});
