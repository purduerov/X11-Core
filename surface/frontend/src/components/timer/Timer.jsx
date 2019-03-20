import React, { Component } from 'react';
import styles from './Timer.css';

export default class Timer extends Component {
    constructor(props) {
        super(props);

        this.state = {
            timeAtStart: 0, // units: ms
            timeOffset: 0, // units: ms
            curtime: 0, // units: ms
            isUpdating: false
        };

        this.displayInfo = this.displayInfo.bind(this);
        this.start = this.start.bind(this);
        this.pause = this.pause.bind(this);
        this.reset = this.reset.bind(this);

        this.interval = setInterval(() => {
            // console.log(this.state);
            if (this.state.isUpdating) {
                this.setState({
                    curtime: Date.now(),
                });
            }
        }, 50);
    }

    displayInfo() {
        var timeDisplay;
        if (this.state.isUpdating) {
            timeDisplay = 15 * 60 -(this.state.curtime - this.state.timeAtStart + this.state.timeOffset) / 1000;
        } else {
            timeDisplay = 15 * 60 - this.state.timeOffset / 1000;
        }

        if (timeDisplay <= 0) {
            return (<h4>00:00</h4>);
        }

        var minutes = Math.floor(timeDisplay / 60);
        var seconds = Math.floor(timeDisplay % 60);

        return (
             // both minutes and seconds always display to 2 places
            <h4>{`${("0" + minutes).slice(-2)}:${("0" + seconds).slice(-2)}`}</h4>
        );
    }

    start() { // TODO: fix clicking start after pause causing time to flicker, displaying 2nd to last time for a fraction of a second
        if (!this.state.isUpdating) {
            this.setState({
                isUpdating: true,
                timeAtStart: Date.now()
            });
        }
    }

    pause() {
        if (this.state.isUpdating) {
            this.setState({
                isUpdating: false,
                timeAtStart: 0,
                timeOffset: Date.now() - this.state.timeAtStart + this.state.timeOffset
            });
        }

    }

    reset() {
        this.setState({
            timeAtStart: 0,
            timeOffset: 0,
            curtime: 0,
            isUpdating: false
        });
    }

    render() {
        var timeDisplay;
        if (this.state.isUpdating) {
            timeDisplay = 15 * 60 - (this.state.curtime - this.state.timeAtStart + this.state.timeOffset) / 1000;
        } else {
            timeDisplay = 15 * 60 - this.state.timeOffset / 1000;
        }

        var colorNumbers;
        if (timeDisplay / 60 < 2) {
            colorNumbers = { color: "red"};
        } else if (timeDisplay / 60 < 5) {
            colorNumbers = { color: "orange"};
        } else {
            colorNumbers = { color: "inherit"};
        }

        return (
            <div className={styles.container} style={colorNumbers}>
                <h3>Time</h3>
                {this.displayInfo()}
                <button onClick={this.start}>Start</button>
                <button onClick={this.pause}>Pause</button>
                <button onClick={this.reset}>Reset</button>
            </div>
        );
    }
}
