import React, { Component } from 'react';
import styles from './PHinfo.css';

export default class PHinfo extends Component {
    constructor(props) {
        super(props);

        this.displayInfo = this.displayInfo.bind(this);
        this.freeze = this.freeze.bind(this);
    }

    displayInfo() {
        return (
            <ul>
                <li>pH: {this.props.ph}</li>
                <li>Temperature: {this.props.temp}</li>
            </ul>
        );
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
