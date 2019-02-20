require('./betterlayouts.js');
var bind = require('./bindfunc.js');

var gp = {
    buttons: {},
    axes: {},
    prev_but: {},
    init_trigs: {}, // For the rock candycontroller's madness
    up: 0,
    down: 0,
    selID: 0,
    select(rate) { // prints id of activated gamepad
        gp.selID = setInterval(gp.selectController, rate);
    },
    gamepadIndex: -1, // the index that goes with navigator.getGamepads
    layoutKey: -1, // the name of the controller
    ready: false,
    but_func: {},
    ax_func: {},

    selectController() {
        var cur = navigator.getGamepads();
        Object.keys(cur).forEach((key, i) => {
            if (key != 'length') {
                if (cur[key] != null) {
                    if (cur[key].buttons[1] != undefined) {
                        cur[key].buttons.forEach((key_b, i) => {
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
        Object.keys(layouts).forEach((key_gp, i_gp) => {
            for (var a = 0; a < b; a++) { // loops through ids of betterlayouts
                if (id.startsWith(layouts[key_gp].idMatch[a])) { // For loop through idMatch rather than using just the first one
                    b = a;
                    clearInterval(gp.selID);
                    gp.selID = -1;
                    Object.keys(layouts[key_gp]).forEach((gp_ax, i) => {
                        if (gp_ax != 'idMatch') {
                            var cur = navigator.getGamepads()[key];
                            for (var j = 0; j < layouts[key_gp][gp_ax].length; j++) {
                                if (gp_ax == 'buttons') {
                                    if (layouts[key_gp][gp_ax][j].name.endsWith('trigger')) { // #triggered
                                        // console.log(layouts[key_gp][gp_ax][j].name+" initializing at "+cur[layouts[key_gp][gp_ax][j].where][layouts[key_gp][gp_ax][j].indx].value);
                                        gp.init_trigs[layouts[key_gp][gp_ax][j].name] = cur[layouts[key_gp][gp_ax][j].where][layouts[key_gp][gp_ax][j].indx].value;
                                    }
                                    gp.buttons[layouts[key_gp][gp_ax][j].name] = { pressed: 0, released: 0, curVal: 0 };
                                    gp.but_func[layouts[key_gp][gp_ax][j].name] = { pressed: null, released: null, curVal: null };
                                    gp.prev_but[layouts[key_gp].buttons[j].name] = 0;
                                    // console.log(layouts[key_gp].buttons[j].name+": "+gp.buttons[layouts[key_gp].buttons[j].name]); //eventually remove
                                } else {
                                    if (layouts[key_gp][gp_ax][j].name.endsWith('trigger')) { // #triggered
                                        // console.log(layouts[key_gp][gp_ax][j].name+" initializing at "+cur[layouts[key_gp][gp_ax][j].where][layouts[key_gp][gp_ax][j].indx]);
                                        gp.init_trigs[layouts[key_gp][gp_ax][j].name] = cur[layouts[key_gp][gp_ax][j].where][layouts[key_gp][gp_ax][j].indx];
                                    }
                                    gp.axes[layouts[key_gp][gp_ax][j].name] = {
                                        changed: 0, curVal: 0, constant: 0, past: 0,
                                    };
                                    gp.ax_func[layouts[key_gp][gp_ax][j].name] = { curVal: null };
                                }
                            }
                        }
                    });
                    gp.gamepadIndex = key;
                    gp.layoutKey = key_gp;
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
            if (name.endsWith('trigger') && val == gp.init_trigs[name]) {
                // console.log(name+" is at "+val);
                val = lay.buttons[i].notpressed;
            } else {
                gp.init_trigs[name] = lay.buttons[i].notpressed;
            }
            // should adjust the intput to a 1-0 scale:
            // console.log(name+" "+val+" "+lay.buttons[i].notpressed+" "+lay.buttons[i].pressed)
            gp.buttons[name].curVal = (val - lay.buttons[i].notpressed) / (lay.buttons[i].pressed - lay.buttons[i].notpressed);
            gp.pressRelease(name);

            if (gp.but_func[name].pressed && gp.buttons[name].pressed) { // runs bindfunc
                gp.but_func[name].pressed();
            }
            if (gp.but_func[name].released && gp.buttons[name].released) {
                gp.but_func[name].released();
            }
            if (gp.but_func[name].curVal) {
                gp.but_func[name].curVal();
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
                // console.log(val+" vs "+gp.init_trigs[name]);
                if (val == gp.init_trigs[name]) {
                    val = lay.axes[i].min;
                } else {
                    gp.init_trigs[name] = lay.axes[i].min;
                }
                gp.axes[name].curVal = (val - lay.axes[i].min) / (lay.axes[i].max - lay.axes[i].min);
            } else if (Math.abs(gp.adjust(i, val)) > 0.15) {
                gp.axes[lay.axes[i].name].curVal = gp.adjust(i, val);
            } else {
                gp.axes[lay.axes[i].name].curVal = 0;
            }
            if (gp.ax_func[name].curVal) { // runs bindfunc
                gp.ax_func[name].curVal();
            }
        }
    },

    pressRelease(but_name) {
        if (gp.prev_but[but_name] < gp.buttons[but_name].curVal) {
            gp.buttons[but_name].pressed = 1;
            gp.buttons[but_name].released = 0;
        } else if (gp.prev_but[but_name] > gp.buttons[but_name].curVal) {
            gp.buttons[but_name].released = 1;
            gp.buttons[but_name].pressed = 0;
        } else {
            gp.buttons[but_name].released = 0;
            gp.buttons[but_name].pressed = 0;
        }
        gp.prev_but[but_name] = gp.buttons[but_name].curVal;
    },

    zero() { // gets values of constants
        var cur = navigator.getGamepads()[gp.gamepadIndex];
        var lay = layouts[gp.layoutKey];

        for (var i = 0; i < lay.axes.length; i++) // copy of the function in update, but sets constants
        {
            gp.axes[lay.axes[i].name].constant = cur.axes[i];
        }
    },

    adjust(index_2, cur) {
        // var cur = navigator.getGamepads()[gp.gamepadIndex];
        var lay = layouts[gp.layoutKey];
        let newVal = cur - gp.axes[lay.axes[index_2].name].constant;
        if (newVal > 0) {
            newVal /= (1 - gp.axes[lay.axes[index_2].name].constant);
        } else if (newVal < 0) {
            newVal /= (1 + gp.axes[lay.axes[index_2].name].constant);
        }
        return (newVal);
    },

    btn_bind(piece, which, func) {
        gp.but_func[piece][which] = func;
    },

    axes_bind(piece, which, func) {
        gp.ax_func[piece][which] = func;
    },

};// end gp
module.exports = gp;
