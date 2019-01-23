import React, { Component } from 'react';
import styles from './IPCtest.css';

const { ipcRenderer } = window.require('electron');


export default class IPCtest extends Component {
    constructor(props) {
        super(props);
    }

    testIPC() {
        console.log("Button clicked in window");
        ipcRenderer.send('button-clicked', "Test Data 1");
    }

    componentDidMount() {
/*
        ipcRenderer.on('button-clicked-response', (event, data) => {
            console.log("Here's the response to the button click");
            console.log(data)
        });
*/
    }

    render() {
        return (
            <div className={styles.container}>
                <h3> Test IPC </h3>
                <p id="testwrite"></p>
                <button id="teststart" onClick={this.testIPC}>TEST</button>
            </div>
        );
    }
}
