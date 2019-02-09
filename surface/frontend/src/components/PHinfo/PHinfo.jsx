import React, { Component } from 'react';
import styles from './PHinfo.css';

export default class PHinfo extends Component {
    constructor(props) {
        super(props);

        this.ph;
        this.temperature;
        this.isUpdating = true;

        setInterval(() => {
            if (this.isUpdating) {
                this.ph = Math.random();
                this.temperature = Math.random();
            }
        }, 500);

        //console.log(props.variable);
        this.displayInfo = this.displayInfo.bind(this);
        this.freeze = this.freeze.bind(this);
    }

    displayInfo() {
        return (
            <ul>
                <li>pH: {this.ph}</li>
                <li>Temperature: {this.temperature}</li>
            </ul>
        )
    }

    freeze() {
        this.isUpdating = !this.isUpdating;
    }

    render() {
        return (
            <div className={styles.container}>
                <h3>pH and Temperature</h3>
                {this.displayInfo()}
                <button onClick={this.freeze}>Freeze/Unfreeze Display</button>
            </div>
        );
    }
}
