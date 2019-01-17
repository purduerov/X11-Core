const { shell, app, ipcRenderer } = window.require('electron');

class keyBind {
  constructor(where) {
      this.directionscpy = {x: 0, y: 0};

      this.goodkeys = {
        37: this.blankFunc('y', -1),
        38: this.blankFunc('x', 1),
        39: this.blankFunc('y', 1),
        40: this.blankFunc('x', -1)
      };
      console.log(this.goodkeys);

      $("body").keydown((event) => {
        var key = event.which;
        if (this.goodkeys[key] != undefined) {
          this.goodkeys[key](1);
        }
      });

      $("body").keyup((event) => {
        var key = event.which;
        if (this.goodkeys[key] != undefined) {
          this.goodkeys[key](0);
        }
      });

      setInterval(() => {
        where.setState({
          directions: this.directionscpy
        });
      }, 50);

  }

  blankFunc(key, posneg) {
    // called like "blankFunc('x', -1)" or "blankFunc('y', 1)"
    return (value) => {
      if(!(this.directionscpy[key]) || this.directionscpy[key] == posneg) {
        this.directionscpy[key] = value * posneg;
        console.log(this.directionscpy[key]);
      }
    }
  }
}

//object for buddy's control status
//var rocketcpy = { 37: 0, 38: 0, 39: 0, 40: 0 };

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

  /*  $("body").keydown(function(event) {
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
    }); */
    const buddy = new keyBind(where);
}; // end export
