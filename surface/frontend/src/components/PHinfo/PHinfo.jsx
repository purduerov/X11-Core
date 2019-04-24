import React, { Component } from 'react';
import styles from './PHinfo.css';

export default class PHinfo extends Component {
    constructor(props) {
        super(props);

        this.state = {
          ph: 7,
          temperature: 20,
          isUpdating: true
        };

        setInterval(() => {
            if (this.state.isUpdating) {
                this.setState({
                  ph: parseFloat((10 * Math.random()).toFixed(2)),
                  temperature: parseFloat((100 * Math.random()).toFixed(2))
                });
            }
        }, 500);

        //console.log(props.variable);
        this.displayInfo = this.displayInfo.bind(this);
        this.freeze = this.freeze.bind(this);
    }

    displayInfo() {
        return (
            <ul>
                <li>pH: {this.state.ph}</li>
                <li>Temperature: {this.state.temperature}</li>
            </ul>
        )
    }

    freeze() {
        this.setState({
          isUpdating: !this.state.isUpdating
        });
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
