const { shell, app, ipcRenderer } = window.require('electron');

//object for buddy's control status
var rocketcpy = { 37: 0, 38: 0, 39: 0, 40: 0 };

module.exports = (where, socketHost) => {
    /*
        Socket Connection Section
    */

    /*
        IPC Connection Section
    */

    /*
      Keyboard controls section
    */
    $("body").keydown(function(event) {
      var key = event.which;
      if (key == 37 || key == 38 || key == 39 || key == 40) {
        console.log(key + "pressed");
        pocketrocket[key] = 1;
        console.log(pocketrocket);
      }
    });

    $("body").keyup(function(event) {
      var key = event.which;
      if (key == 37 || key == 38 || key == 39 || key == 40) {
        console.log(key + "released");
        pocketrocket[key] = 0;
        console.log(pocketrocket[key]);
      }
    });
};
