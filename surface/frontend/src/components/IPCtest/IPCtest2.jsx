import React, { Component } from 'react';
import styles from './IPCtest.css';

const { ipcRenderer } = window.require('electron');


export default class IPCtest extends Component {
    constructor(props) {
        super(props);
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
                <textarea rows="2" cols="20" id="textarea">
                </textarea>
            </div>
        );
    }
}
