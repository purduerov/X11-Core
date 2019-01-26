import React from 'react';
import { render } from 'react-dom';
import styles from './main.css';
import packet from '../src/packets.js';
const { shell, app, ipcRenderer } = window.require('electron');

import Card from '../src/components/Card/Card.jsx';
import Titlebar from '../src/components/Titlebar/Titlebar.jsx';
import BuddyControls from '../src/components/BuddyControls/BuddyControls.jsx';
import IPCtest from '../src/components/IPCtest/IPCtest.jsx'

const socketHost = 'ws://localhost:5001';

/* These should be done in a component, or the js file for this window

const socket = io.connect(socketHost, { transports: ['websocket'] });
const { shell, app, ipcRenderer } = window.require('electron');
*/


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = require('../src/packets.js'); //= $.extend(true, {}, packets);

        this.state.directions = { x: 0, y: 0 };
        this.state.config = {
            thrust_scales: {
                master: 50,
                velX: 100,
                velY: 100,
                velZ: 100,
                pitch: 100,
                roll: 100,
                yaw: 100,
            },
            thrust_invert: {
                master: 1,
                velX: 1,
                velY: 1,
                velZ: 1,
                pitch: 1,
                roll: 1,
                yaw: 1,
            },
            thruster_control: [ // invert is -1/1 for easy multiplication
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
                { power: 100, invert: -1 }, { power: 100, invert: 1 },
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
            ],
            tool_scales: {
                manipulator: {
                    master: 0.25,
                    open: 1,
                    close: 1,
                    invert: 1,
                },
            },
        };


        this.flaskcpy = this.state.dearflask;
        this.clientcpy = this.state.dearclient;
        this.confcpy = this.state.config;
    }

    componentDidMount() {
        var signals = require('./main.js');
        window.react = this;

        signals(this, socketHost);

        ipcRenderer.on('second-window-message', (event, message) => {
          console.log('Received message from second window');
        });
    }

    render() {
        return (
            <div className="main">
                <div className="titlebar">
                    <Titlebar title="Purdue ROV Primary Screen" />
                </div>
                <div className="main-container">
                    <div className="camera-width full-height center" />
                    <div className="data-width full-height">
                        <div className="data-column">
                            <Card>
                              <BuddyControls
                                buddyDirections={this.state.directions}
                              />
                            </Card>
                        </div>
                        <div className="data-column">
                            <Card />
                        </div>
                        <div className="data-column">
                            <Card />
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

render(<App />, document.getElementById('app'));
