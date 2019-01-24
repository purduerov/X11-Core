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
const files = ['frontend/Window1/main.html', 'frontend/Window2/secondary.html', 'frontend/Window3/buddy.html'];

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
            if (i == 2) {
              webContents.sendInputEvent({
    type: 'keydown',
    keyCode: key,
});
webContents.sendInputEvent({
    type: 'keyup',
    keyCode: key,
});
webContents.sendInputEvent({
    type: 'char',
    keyCode: key,
});
            }
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

/*
ipcMain.on('button-clicked', (event, file) => {
    console.log('Received button-clicked')
    event.sender.send('button-clicked-response', 'This is some data from button clicked response')
});
*/

/*ipcMain.on('button-clicked', (event, message) => {
    windows[1].webContents.send('window-message', 'Second window is sending a message');
    console.log('One of the windows is sending a message: ' + message);
});

ipcMain.on('reply', (event, message) => {
    console.log('reply received')
    windows[0].webContents.send('main-window-message', 'Main window is sending a message');
    console.log('Main window is sending a message')
});*/

ipcMain.on('button-clicked', (event, message) => {
    windows[0].webContents.send('other-main-window-message', message);
    console.log('Main window is sending a message: ' + message);
});

/*
    Here we are saying that every time our node application receives data from the python process
    output stream(on 'data'), we want to convert that received data into a string and append it to
    the overall dataString.
*/
py.stdout.on('data', (data) => {
    dataString = data.toString();
});

/* Once the stream is done (on 'end') we want to simply log the received data to the console. */
py.stdout.on('end', () => {
    console.log('Sum of numbers=', dataString);
});

/* We have to stringify the data first otherwise our python process wont recognize it */
py.stdin.write(JSON.stringify(data));

/* Sending the 'end' signal to the python process */
py.stdin.end();
