// not used
// require('./betterlayouts.js');
var bind = require('./bindfunc.js');

var gp = {
    buttons: {},
    axes: {},
    prevBut: {},
    initTrigs: {}, // For the rock candycontroller's madness
    up: 0,
    down: 0,
    selID: 0,
    select(rate) { // prints id of activated gamepad
        gp.selID = setInterval(gp.selectController, rate);
    },
    gamepadIndex: -1, // the index that goes with navigator.getGamepads
    layoutKey: -1, // the name of the controller
    ready: false,
    butFunc: {},
    axFunc: {},

    selectController() {
        var cur = navigator.getGamepads();
        Object.keys(cur).forEach((key, i) => {
            if (key != 'length') {
                if (cur[key] != null) {
                    if (cur[key].buttons[1] != undefined) {
                        cur[key].buttons.forEach((keyB, i) => {
                            if (cur[key].buttons[i].pressed) {
                                // console.log(cur[key].id);
                                gp.map(key, cur[key].id);
                            }
                        });
                    }
                }
            }
        });
    },

    map(key, id) { // id is the id in chrome driver
        var b = 10; // random number of possible ids, not important
        Object.keys(layouts).forEach((keyGp, iGp) => {
            for (var a = 0; a < b; a++) { // loops through ids of betterlayouts
                if (id.startsWith(layouts[keyGp].idMatch[a])) { // For loop through idMatch rather than using just the first one
                    b = a;
                    clearInterval(gp.selID);
                    gp.selID = -1;
                    Object.keys(layouts[keyGp]).forEach((gpAx, i) => {
                        if (gpAx != 'idMatch') {
                            var cur = navigator.getGamepads()[key];
                            for (var j = 0; j < layouts[keyGp][gpAx].length; j++) {
                                if (gpAx == 'buttons') {
                                    if (layouts[keyGp][gpAx][j].name.endsWith('trigger')) { // #triggered
                                        // console.log(layouts[keyGp][gpAx][j].name+" initializing at "+cur[layouts[keyGp][gpAx][j].where][layouts[keyGp][gpAx][j].indx].value);
                                        gp.initTrigs[layouts[keyGp][gpAx][j].name] = cur[layouts[keyGp][gpAx][j].where][layouts[keyGp][gpAx][j].indx].value;
                                    }
                                    gp.buttons[layouts[keyGp][gpAx][j].name] = { pressed: 0, released: 0, curVal: 0 };
                                    gp.butFunc[layouts[keyGp][gpAx][j].name] = { pressed: null, released: null, curVal: null };
                                    gp.prevBut[layouts[keyGp].buttons[j].name] = 0;
                                    // console.log(layouts[keyGp].buttons[j].name+": "+gp.buttons[layouts[keyGp].buttons[j].name]); //eventually remove
                                } else {
                                    if (layouts[keyAp][gpAx][j].name.endsWith('trigger')) { // #triggered
                                        // console.log(layouts[keyGp][gpAx][j].name+" initializing at "+cur[layouts[keyGp][gpAx][j].where][layouts[keyGp][gpAx][j].indx]);
                                        gp.initTrigs[layouts[keyGp][gpAx][j].name] = cur[layouts[keyGp][gpAx][j].where][layouts[keyGp][gpAx][j].indx];
                                    }
                                    gp.axes[layouts[keyGp][gpAx][j].name] = {
                                        changed: 0, curVal: 0, constant: 0, past: 0,
                                    };
                                    gp.axFunc[layouts[keyGp][gpAx][j].name] = { curVal: null };
                                }
                            }
                        }
                    });
                    gp.gamepadIndex = key;
                    gp.layoutKey = keyGp;
                    gp.zero();
                    bind.activate(gp);
                    gp.ready = true;
                }
            }
        });
    },

    update() {
        var cur = navigator.getGamepads()[gp.gamepadIndex];
        // console.log(layouts[gp.layoutKey]+" "+gp.layoutKey);
        var lay = layouts[gp.layoutKey];
        for (var i = 0; i < lay.buttons.length; i++) {
            var name = lay.buttons[i].name;
            var buttn = lay.buttons[i];
            var val = cur[buttn.where][buttn.indx];
            if (lay.buttons[i].where == 'buttons') {
                val = val.value;
            }
            val = val == lay.buttons[i].pressed ? val : 0;
            if (name.endsWith('trigger') && val == gp.initTrigs[name]) {
                // console.log(name+" is at "+val);
                val = lay.buttons[i].notpressed;
            } else {
                gp.initTrigs[name] = lay.buttons[i].notpressed;
            }
            // should adjust the intput to a 1-0 scale:
            // console.log(name+" "+val+" "+lay.buttons[i].notpressed+" "+lay.buttons[i].pressed)
            gp.buttons[name].curVal = (val - lay.buttons[i].notpressed) / (lay.buttons[i].pressed - lay.buttons[i].notpressed);
            gp.pressRelease(name);

            if (gp.butFunc[name].pressed && gp.buttons[name].pressed) { // runs bindfunc
                gp.butFunc[name].pressed();
            }
            if (gp.butFunc[name].released && gp.buttons[name].released) {
                gp.butFunc[name].released();
            }
            if (gp.butFunc[name].curVal) {
                gp.butFunc[name].curVal();
            }
        }
        for (var i = 0; i < lay.axes.length; i++) {
            var name = lay.axes[i].name;
            var val = cur[lay.axes[i].where][lay.axes[i].indx];
            if (lay.axes[i].where == 'buttons') {
                val = val.value;
            }
            if (lay.axes[i].name.endsWith('trigger')) {
                // console.log(cur[lay.axes[i].where][lay.axes[i].indx].value);
                // console.log(gp.adjust(i, val))
                // console.log(lay.axes[i].name)
                // console.log("val: "+val+" min: "+lay.axes[i].min+" max: "+lay.axes[i].max)
                // console.log(val+" "+lay.axes[i].min+" "+lay.axes[i].max)
                // console.log(val+" vs "+gp.initTrigs[name]);
                if (val == gp.initTrigs[name]) {
                    val = lay.axes[i].min;
                } else {
                    gp.initTrigs[name] = lay.axes[i].min;
                }
                gp.axes[name].curVal = (val - lay.axes[i].min) / (lay.axes[i].max - lay.axes[i].min);
            } else if (Math.abs(gp.adjust(i, val)) > 0.15) {
                gp.axes[lay.axes[i].name].curVal = gp.adjust(i, val);
            } else {
                gp.axes[lay.axes[i].name].curVal = 0;
            }
            if (gp.axFunc[name].curVal) { // runs bindfunc
                gp.axFunc[name].curVal();
            }
        }
    },

    pressRelease(butName) {
        if (gp.prevBut[butName] < gp.buttons[butName].curVal) {
            gp.buttons[butName].pressed = 1;
            gp.buttons[butName].released = 0;
        } else if (gp.prevBut[butName] > gp.buttons[butName].curVal) {
            gp.buttons[butName].released = 1;
            gp.buttons[butName].pressed = 0;
        } else {
            gp.buttons[butName].released = 0;
            gp.buttons[butName].pressed = 0;
        }
        gp.prevBut[butName] = gp.buttons[butName].curVal;
    },

    zero() { // gets values of constants
        var cur = navigator.getGamepads()[gp.gamepadIndex];
        var lay = layouts[gp.layoutKey];

        for (var i = 0; i < lay.axes.length; i++) // copy of the function in update, but sets constants
        {
            gp.axes[lay.axes[i].name].constant = cur.axes[i];
        }
    },

    adjust(index, cur) {
        // var cur = navigator.getGamepads()[gp.gamepadIndex];
        var lay = layouts[gp.layoutKey];
        let newVal = cur - gp.axes[lay.axes[index].name].constant;
        if (newVal > 0) {
            newVal /= (1 - gp.axes[lay.axes[index].name].constant);
        } else if (newVal < 0) {
            newVal /= (1 + gp.axes[lay.axes[index].name].constant);
        }
        return (newVal);
    },

    btnBind(piece, which, func) {
        gp.butFunc[piece][which] = func;
    },

    axesBind(piece, which, func) {
        gp.axFunc[piece][which] = func;
    },

};// end gp
module.exports = gp;
