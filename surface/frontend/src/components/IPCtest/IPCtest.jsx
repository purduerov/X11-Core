import React, { Component } from 'react';
import styles from './IPCtest.css';

const { ipcRenderer } = window.require('electron');


export default class IPCtest extends Component {
    constructor(props) {
        super(props);

        console.log(props.variable);
        this.testIPC = this.testIPC.bind(this);
    }

    testIPC() {
        console.log("Button clicked in window");
        let text = $("."+styles.textarea+this.props.variable).val();
        ipcRenderer.send('button-clicked', text);
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
                <textarea rows="2" cols="20"  className={styles.textarea+this.props.variable}>
                </textarea>
                <button onClick={this.testIPC}>TEST</button>
            </div>
        );
    }
}
