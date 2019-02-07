const { ipcRenderer } = window.require('electron');

module.exports = class keyBind {
    constructor(where) {
        this.directionscpy = { x: 0, y: 0 };

        this.goodkeys = {
            37: this.blankFunc('y', -1),
            38: this.blankFunc('x', 1),
            39: this.blankFunc('y', 1),
            40: this.blankFunc('x', -1)
        };
        // console.log(this.goodkeys);

        $('body').keydown((event) => {
            var key = event.which;
            if (this.goodkeys[key] !== undefined) {
                this.goodkeys[key](1);
            }
        });

        $('body').keyup((event) => {
            var key = event.which;
            if (this.goodkeys[key] != undefined) {
                this.goodkeys[key](0);
            }
        });

        setInterval(() => {
            where.setState({
                directions: this.directionscpy,
            });
            ipcRenderer.send('buddy-controls-from-win-3', this.directionscpy);
        }, 50);
    }

    blankFunc(key, posneg) {
        // called like "blankFunc('x', -1)" or "blankFunc('y', 1)"
        return (value) => {
            if (value && (!(this.directionscpy[key]) || this.directionscpy[key] === -posneg)) {
                this.directionscpy[key] = value * posneg;
                // console.log(this.directionscpy[key]);
            } else if (!value && this.directionscpy[key] === posneg) {
                this.directionscpy[key] = value;
            }
        };
    }
};
