/* global react */

/*
button template:
  btn: {
    value: {
      params: undefined,
      func: null,
    },
    pressed: {
      params: undefined,
      func: null,
    },
    released: {
      params: undefined,
      func: null,
    },
  },

axes template:
  side: {
      params: undefined,
      func: null,
        },

        // a:{
        //   value: {
        //     func: function() {
        //       react.flaskcpy.thrusters.desiredThrust = gp.buttons.a.curVal
        //     }
        //   },
        // },
        // up: {
        //   pressed: {
        //     func: function() {
        //       react.flaskcpy.thrusters.desiredThrust =
        //     }
        //
        //   },
        //   released: {
        //
        //   },
        // },

  */

var bind = {
    btn: {
        lb: { // roll counterclockwise
            pressed: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    react.flaskcpy.thrusters.desiredThrust[3] = inv.master * inv.roll *
                              -react.gp.buttons.lb.curVal * stuff.master * stuff.roll / 10000;
                },
            },
            released: {
                func() {
                    var inv = react.state.config.thrustInvert;
                    if (react.flaskcpy.thrusters.desiredThrust[3] * inv.master * inv.roll < 0) {
                        react.flaskcpy.thrusters.desiredThrust[3] = 0;
                    }
                },
            },
        },
        rb: { // roll clockwise
            pressed: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    react.flaskcpy.thrusters.desiredThrust[3] = inv.master * inv.roll *
                                react.gp.buttons.rb.curVal * stuff.master * stuff.roll / 10000;
                },
            },
            released: {
                func() {
                    var inv = react.state.config.thrustInvert;
                    if (react.flaskcpy.thrusters.desiredThrust[3] * inv.master * inv.roll > 0) {
                        react.flaskcpy.thrusters.desiredThrust[3] = 0;
                    }
                },
            },
        },
        a: { // open manipulator
            pressed: {
                func() {
                    var stuff = react.state.config.toolScales.manipulator;
                    react.flaskcpy.manipulator.power = react.gp.buttons.a.curVal *
                                stuff.master * stuff.open * stuff.invert;
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.toolScales.manipulator;
                    if (react.flaskcpy.manipulator.power * stuff.invert > 0) {
                        react.flaskcpy.manipulator.power = 0;
                    }
                },
            },
        },
        b: { // close manipulator
            pressed: {
                func() {
                    var stuff = react.state.config.toolScales.manipulator;
                    // console.log(-react.gp.buttons.lb.curVal+" "+stuff.master+" "+
                        // stuff.close+" "+stuff.invert)
                    // console.log(react.flaskcpy.manipulator.power)
                    react.flaskcpy.manipulator.power = -react.gp.buttons.b.curVal *
                                stuff.master * stuff.close * stuff.invert;
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.toolScales.manipulator;
                    if (react.flaskcpy.manipulator.power * stuff.invert < 0) {
                        react.flaskcpy.manipulator.power = 0;
                    }
                },
            },
        },
        right: { // obs leveler power right increment
            pressed: {
                func() {
                    var stuff = react.state.config.toolScales.obsTool;
                    if (react.flaskcpy.obsTool.power * stuff.invert < 0.0) {
                        react.flaskcpy.obsTool.power = 0.0;
                    } else {
                        react.flaskcpy.obsTool.power += 0.02 * stuff.invert;
                    }
                },
            },
        },
        left: { // obs leveler power left increment
            pressed: {
                func() {
                    var stuff = react.state.config.toolScales.obsTool;
                    if (react.flaskcpy.obsTool.power * stuff.invert > 0.0) {
                        react.flaskcpy.obsTool.power = 0.0;
                    } else {
                        react.flaskcpy.obsTool.power -= 0.02 * stuff.invert;
                    }
                },
            },
        },
        up: { // rotate main camera up
            pressed: {
                func() {
                    react.flaskcpy.maincamAngle += 2.5;
                },
            },
        },
        down: { // rotate main camera down
            pressed: {
                func() {
                    react.flaskcpy.maincamAngle -= 2.5;
                },
            },
        },
        start: { // Toggle electromagnet
            pressed: {
                func() {
                    react.flaskcpy.magnet = !react.flaskcpy.magnet;
                },
            },
        },
        select: { // Toggle transmitter (audio tools)
            pressed: {
                func() {
                    react.flaskcpy.transmitter = !react.flaskcpy.transmitter;
                },
            },
        },
        lpress: {
            pressed: {
                func() {
                    react.confcpy.thrustScales.master = 60;

                    react.setState({
                        config: react.confcpy,
                    });
                },
            },
        },
        rpress: {
            pressed: {
                func() {
                    react.confcpy.thrustScales.master = 35;

                    react.setState({
                        config: react.confcpy,
                    });
                },
            },
        },

    }, // end btn

    axes: {
        LstickXaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    react.flaskcpy.thrusters.desiredThrust[1] = inv.master * inv.velY *
                          react.gp.axes.LstickXaxis.curVal * stuff.master * stuff.velY / 10000;
                },
            },
        },
        LstickYaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    react.flaskcpy.thrusters.desiredThrust[0] = inv.master * inv.velX *
                            -react.gp.axes.LstickYaxis.curVal * stuff.master * stuff.velX / 10000;
                },
            },
        },
        RstickXaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    react.flaskcpy.thrusters.desiredThrust[5] = inv.master * inv.yaw *
                              react.gp.axes.RstickXaxis.curVal * stuff.master * stuff.yaw / 10000;
                },
            },
        },
        RstickYaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    react.flaskcpy.thrusters.desiredThrust[4] = inv.master * inv.pitch *
                            -react.gp.axes.RstickYaxis.curVal * stuff.master * stuff.pitch / 10000;
                },
            },
        },
        /*
          THESE ARE A DELICATE BALANCE
          Only change the weird up/down referencing if you've REALLY thought through what you're doing
          I spent too much time on this late at night when I would have rather been at the cactus.
          Please don't make it for naught...
          -- Ian

          Allows for the last trigger pressed to take dominace over whether the ROV is going up,
          or down
        */
        Ltrigger: { // descend
            curVal: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    if (react.gp.axes.Ltrigger.curVal != 0) {
                        if (react.gp.up < 2) {
                            // console.log("Ltrigger: "+react.gp.axes.Ltrigger.curVal+" "+
                                // stuff.master+" "+stuff.velZ);
                            react.flaskcpy.thrusters.desiredThrust[2] = inv.master * inv.velZ *
                                -react.gp.axes.Ltrigger.curVal * stuff.master * stuff.velZ / 10000;
                            react.gp.down = 1 + react.gp.up;
                        }
                    } else {
                        react.gp.down = 0;
                    }
                    if (react.gp.down == react.gp.up) {
                        react.flaskcpy.thrusters.desiredThrust[2] = 0;
                    }
                },
            },
        },
        Rtrigger: { // ascend
            curVal: {
                func() {
                    var stuff = react.state.config.thrustScales;
                    var inv = react.state.config.thrustInvert;
                    if (react.gp.axes.Rtrigger.curVal != 0) {
                        if (react.gp.down < 2) {
                            react.flaskcpy.thrusters.desiredThrust[2] = inv.master * inv.velZ
                              * react.gp.axes.Rtrigger.curVal * stuff.master * stuff.velZ / 10000;
                            react.gp.up = 1 + react.gp.down;
                        }
                    } else {
                        react.gp.up = 0;
                    }
                    if (react.gp.down == react.gp.up) {
                        react.flaskcpy.thrusters.desiredThrust[2] = 0;
                    }
                },
            },
        },
    },

    activate(gp) {
        // console.log(gp)
        Object.keys(bind).forEach((btnAx, i) => { // goes through btn or ax
            if (btnAx != 'activate') {
                Object.keys(bind[btnAx]).forEach((piece, j) => {
                        // goes through buttons or left and right axes
                    Object.keys(bind[btnAx][piece]).forEach((which, k) => {
                            // goes through the individual functions
                        // console.log(btnAx+"Bind: "+piece+", "+which);
                        gp[`${btnAx}Bind`](piece, which, bind[btnAx][piece][which].func);
                    });
                });
            }
        });
    },

}; // end bind
module.exports = bind;
