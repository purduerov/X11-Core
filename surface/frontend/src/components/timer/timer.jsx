import React, { Component } from 'react';
import styles from './timer.css';

export default class timer extends Component {
    constructor(props) {
        super(props);

        this.state = {

          isUpdating: true
        };

        /*setInterval(() => {
            if (this.state.isUpdating) {
                this.setState({
                  ph: parseFloat((10 * Math.random()).toFixed(2)),
                  temperature: parseFloat((100 * Math.random()).toFixed(2))
                });
            }
        }, 500);*/

        //console.log(props.variable);
        this.displayInfo = this.displayInfo.bind(this);
        this.start = this.freeze.bind(this);
        this.pause = this.pause.bind(this);
        this.reset = this.reset.bind(this);
    }

    displayInfo() {
        return (
            <h4>Get time somehow...</h4>
        )
    }

    start() {

    }

    pause() {
        this.setState({
          isUpdating: !this.state.isUpdating
        });
    }

    reset() {

    }

    render() {
        // also disable start button unless reset has been pressed?
        // if time < 2, render with red, else, render with green (??)
        return (
            <div className={styles.container}>
                <h3>Time</h3>
                {this.displayInfo()}
                <button onClick={this.start}>Start</button>
                <button onClick={this.pause}>Pause</button>
                <button onClick={this.reset}>Reset</button>
            </div>
        );
    }
}
