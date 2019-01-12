import React, { Component } from 'react';
import styles from './IPCtest.css';

const { ipcRenderer } = window.require('electron');


export default class IPCtest extends Component {
    constructor(props) {
        super(props);
    }

    testIPC() {
        console.log("Testing IPC...");
        ipcRenderer.send('calc-crash', "Test");
    }

    componentDidMount() {
        ipcRenderer.on('crash-found', (event, data) => {
            console.log("Test response came through");
        });
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
