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
        //       react.flaskcpy.thrusters.desired_thrust = gp.buttons.a.curVal
        //     }
        //   },
        // },
        // up: {
        //   pressed: {
        //     func: function() {
        //       react.flaskcpy.thrusters.desired_thrust =
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
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    react.flaskcpy.thrusters.desired_thrust[3] = inv.master * inv.roll * -react.gp.buttons.lb.curVal * stuff.master * stuff.roll / 10000;
                },
            },
            released: {
                func() {
                    var inv = react.state.config.thrust_invert;
                    if (react.flaskcpy.thrusters.desired_thrust[3] * inv.master * inv.roll < 0) {
                        react.flaskcpy.thrusters.desired_thrust[3] = 0;
                    }
                },
            },
        },
        rb: { // roll clockwise
            pressed: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    react.flaskcpy.thrusters.desired_thrust[3] = inv.master * inv.roll * react.gp.buttons.rb.curVal * stuff.master * stuff.roll / 10000;
                },
            },
            released: {
                func() {
                    var inv = react.state.config.thrust_invert;
                    if (react.flaskcpy.thrusters.desired_thrust[3] * inv.master * inv.roll > 0) {
                        react.flaskcpy.thrusters.desired_thrust[3] = 0;
                    }
                },
            },
        },
        x: { // activate groutTrout
            pressed: {
                func() {
                    var stuff = react.state.config.tool_scales.groutTrout;
                    // console.log(-react.gp.buttons.x.curVal+" "+stuff.master+" "+stuff.close+" "+stuff.invert)
                    // console.log(react.flaskcpy.groutTrout.power)
                    react.flaskcpy.groutTrout.power = react.gp.buttons.x.curVal * stuff.master * stuff.close * stuff.invert;
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.tool_scales.groutTrout;
                    if (react.flaskcpy.groutTrout.power * stuff.invert > 0) {
                        react.flaskcpy.groutTrout.power = 0;
                    }
                },
            },
        },
        y: { // activate marker
            pressed: {
                func() {
                    var stuff = react.state.config.tool_scales.marker;
                    // console.log(-react.gp.buttons.y.curVal+" "+stuff.master+" "+stuff.close+" "+stuff.invert)
                    // console.log(react.flaskcpy.marker.power)
                    react.flaskcpy.marker.power = react.gp.buttons.y.curVal * stuff.master * stuff.close * stuff.invert;
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.tool_scales.marker;
                    if (react.flaskcpy.marker.power * stuff.invert > 0) {
                        react.flaskcpy.marker.power = 0;
                    }
                },
            },
        },
        a: { // open manipulator
            pressed: {
                func() {
                    var stuff = react.state.config.tool_scales.manipulator;
                    react.flaskcpy.manipulator.power = react.gp.buttons.a.curVal * stuff.master * stuff.open * stuff.invert;
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.tool_scales.manipulator;
                    if (react.flaskcpy.manipulator.power * stuff.invert > 0) {
                        react.flaskcpy.manipulator.power = 0;
                    }
                },
            },
        },
        b: { // close manipulator
            pressed: {
                func() {
                    var stuff = react.state.config.tool_scales.manipulator;
                    // console.log(-react.gp.buttons.lb.curVal+" "+stuff.master+" "+stuff.close+" "+stuff.invert)
                    // console.log(react.flaskcpy.manipulator.power)
                    react.flaskcpy.manipulator.power = -react.gp.buttons.b.curVal * stuff.master * stuff.close * stuff.invert;
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.tool_scales.manipulator;
                    if (react.flaskcpy.manipulator.power * stuff.invert < 0) {
                        react.flaskcpy.manipulator.power = 0;
                    }
                },
            },
        },
        start: { // open liftBag if right is pressed
            pressed: {
                func() {
                    var stuff = react.state.config.tool_scales.liftBag;
                    // console.log(-react.gp.buttons.lb.curVal+" "+stuff.master+" "+stuff.close+" "+stuff.invert)
                    // console.log(react.flaskcpy.liftBag.power)
                    if(react.gp.buttons.right.curVal > 0) {
                        react.flaskcpy.liftBag.power = react.gp.buttons.start.curVal * stuff.master * stuff.close * stuff.invert;
                    }
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.tool_scales.liftBag;
                    if (react.flaskcpy.liftBag.power * stuff.invert > 0) {
                        react.flaskcpy.liftBag.power = 0;
                    }
                },
            },
        },
        right: { // close liftBag if start is pressed
            pressed: {
                func() {
                    var stuff = react.state.config.tool_scales.liftBag;
                    // console.log(-react.gp.buttons.lb.curVal+" "+stuff.master+" "+stuff.close+" "+stuff.invert)
                    // console.log(react.flaskcpy.liftBag.power)
                    if(react.gp.buttons.start.curVal > 0) {
                        react.flaskcpy.liftBag.power = react.gp.buttons.right.curVal * stuff.master * stuff.close * stuff.invert;
                    }
                },
            },
            released: {
                func() {
                    var stuff = react.state.config.tool_scales.liftBag;
                    if (react.flaskcpy.liftBag.power * stuff.invert > 0) {
                        react.flaskcpy.liftBag.power = 0;
                    }
                },
            },
        },
        up: { // rotate main camera up
            pressed: {
                func() {
                    react.flaskcpy.maincam_angle += 2.5;
                },
            },
        },
        down: { // rotate main camera down
            pressed: {
                func() {
                    react.flaskcpy.maincam_angle -= 2.5;
                },
            },
        },
        lpress: {
            pressed: {
                func() {
                    react.confcpy.thrust_scales.master = 35;
                },
            },
        },
        rpress: {
            pressed: {
                func() {
                    react.confcpy.thrust_scales.master = 60;
                },
            },
        },

    }, // end btn

    axes: {
        LstickXaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    react.flaskcpy.thrusters.desired_thrust[1] = inv.master * inv.velY * react.gp.axes.LstickXaxis.curVal * stuff.master * stuff.velY / 10000;
                },
            },
        },
        LstickYaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    react.flaskcpy.thrusters.desired_thrust[0] = inv.master * inv.velX * -react.gp.axes.LstickYaxis.curVal * stuff.master * stuff.velX / 10000;
                },
            },
        },
        RstickXaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    react.flaskcpy.thrusters.desired_thrust[5] = inv.master * inv.yaw * react.gp.axes.RstickXaxis.curVal * stuff.master * stuff.yaw / 10000;
                },
            },
        },
        RstickYaxis: {
            curVal: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    react.flaskcpy.thrusters.desired_thrust[4] = inv.master * inv.pitch * -react.gp.axes.RstickYaxis.curVal * stuff.master * stuff.pitch / 10000;
                },
            },
        },
        /*
          THESE ARE A DELICATE BALANCE
          Only change the weird up/down referencing if you've REALLY thought through what you're doing
          I spent too much time on this late at night when I would have rather been at the cactus.
          Please don't make it for naught...
          -- Ian

          Allows for the last trigger pressed to take dominace over whether the ROV is going up, or down
        */
        Ltrigger: { // descend
            curVal: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    if (react.gp.axes.Ltrigger.curVal != 0) {
                        if (react.gp.up < 2) {
                            // console.log("Ltrigger: "+react.gp.axes.Ltrigger.curVal+" "+stuff.master+" "+stuff.velZ);
                            react.flaskcpy.thrusters.desired_thrust[2] = inv.master * inv.velZ * -react.gp.axes.Ltrigger.curVal * stuff.master * stuff.velZ / 10000;
                            react.gp.down = 1 + react.gp.up;
                        }
                    } else {
                        react.gp.down = 0;
                    }
                    if (react.gp.down == react.gp.up) {
                        react.flaskcpy.thrusters.desired_thrust[2] = 0;
                    }
                },
            },
        },
        Rtrigger: { // ascend
            curVal: {
                func() {
                    var stuff = react.state.config.thrust_scales;
                    var inv = react.state.config.thrust_invert;
                    if (react.gp.axes.Rtrigger.curVal != 0) {
                        if (react.gp.down < 2) {
                            react.flaskcpy.thrusters.desired_thrust[2] = inv.master * inv.velZ * react.gp.axes.Rtrigger.curVal * stuff.master * stuff.velZ / 10000;
                            react.gp.up = 1 + react.gp.down;
                        }
                    } else {
                        react.gp.up = 0;
                    }
                    if (react.gp.down == react.gp.up) {
                        react.flaskcpy.thrusters.desired_thrust[2] = 0;
                    }
                },
            },
        },
    },

    activate(gp) {
        // console.log(gp)
        Object.keys(bind).forEach((btn_ax, i) => { // goes through btn or ax
            if (btn_ax != 'activate') {
                Object.keys(bind[btn_ax]).forEach((piece, j) => { // goes through buttons or left and right axes
                    Object.keys(bind[btn_ax][piece]).forEach((which, k) => { // goes through the individual functions
                        // console.log(btn_ax+"_bind: "+piece+", "+which);
                        gp[`${btn_ax}_bind`](piece, which, bind[btn_ax][piece][which].func);
                    });
                });
            }
        });
    },

}; // end bind
module.exports = bind;
