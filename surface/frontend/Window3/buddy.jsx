import React from 'react';
import { render } from 'react-dom';
import styles from './buddy.css';
import packet from '../src/packets.json';

import Card from '../src/components/Card/Card.jsx';
import Titlebar from '../src/components/Titlebar/Titlebar.jsx';

/* These should be done in a component, or the js file for this window

const socket = io.connect(socketHost, { transports: ['websocket'] });
const { shell, app, ipcRenderer } = window.require('electron');
*/


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = require("../src/packets.json");

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


        this.flaskcpy = $.extend(true, {}, this.state.dearflask);
        this.clientcpy = $.extend(true, {}, this.state.dearclient);
        this.confcpy = $.extend(true, {}, this.state.config);
    }

    componentDidMount() {
        var signals = require('./buddy.js');
        window.react = this;

        signals(this);
    }

    render() {
        return (
            <div className="main">
                <div className="titlebar">
                    <Titlebar title="Purdue ROV's Buddy Screen" />
                </div>
                <div className="main-container">
                    <div className="camera-width full-height center" />
                    <div className="data-width full-height">
                        <div className="data-column">
                            <Card />
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
