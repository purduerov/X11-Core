import React, { Component } from 'react';
import styles from './BuddyControlsShow.css';

export default class BuddyControlsShow extends Component {
    constructor(props) {
        super(props);

        this.readyToRender = this.readyToRender.bind(this);
    }

    readyToRender() {
        var axis = ['x', 'y'];
        return axis.map((val, index) => (
            <li key={`axis${val}`}>
                {axis[index]}: {this.props.buddyDirections[val]}
            </li>
        ));
    }

    render() {
        return (
            <div container={styles.container}>
                <h1> Buddy's Controls</h1>
                <hr />
                <div className={styles.container}>
                    {this.readyToRender()}
                </div>
            </div>
        );
    }

}
