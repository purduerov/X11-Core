import React from 'react';
import { render } from 'react-dom';
import styles from './secondary.css';
import packet from '../src/packets.json';

import Card from '../src/components/Card/Card.jsx';
import Titlebar from '../src/components/Titlebar/Titlebar.jsx';

import ThrusterScales from '../src/components/ThrusterScales/ThrusterScales.jsx';
import ForceScales from '../src/components/ForceScales/ForceScales.jsx';
import ToolView from '../src/components/ToolView/ToolView.jsx';
import ESCinfo from '../src/components/ESCinfo/ESCinfo.jsx';

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


        this.flaskcpy = this.state.dearflask;
        this.clientcpy = this.state.dearclient;
        this.confcpy = this.state.config;
    }

    componentDidMount() {
        var signals = require('./secondary.js');
        window.react = this;

        signals(this);
    }

    render() {
        return (
            <div className="main">
                <div className="titlebar">
                    <Titlebar title="Purdue ROV Secondary Screen" />
                </div>
                <div className="main-container">
                    <div className="camera-width full-height center" />
                    <div className="data-width full-height">
                        <div className="data-column">
                            <Card title="Cannon Calculator" />
                            <Card>
                                <ToolView
                                    manipulator={this.state.dearflask.manipulator.power}
                                    servo={this.state.dearflask.maincam_angle}
                                    transmitter={this.state.dearflask.transmitter}
                                    magnet={this.state.dearflask.magnet}
                                    conf={this.state.config.tool_scales}
                                    rend={this.rendTools}
                                />
                            </Card>
                            <Card title="Task List View" />
                        </div>
                        <div className="data-column">
                            <Card title="Directional Control">
                                <ForceScales
                                    rend={this.changeForceScales}
                                    scales={this.state.config.thrust_scales}
                                    invert={this.state.config.thrust_invert}
                                />
                            </Card>
                            <Card title="Thruster Control">
                                <ThrusterScales
                                    rend={this.changeThrustScales}
                                    scales={this.state.config.thruster_control}
                                />
                            </Card>
                        </div>
                        <div className="data-column">
                            <Card title="pH and Temp readout" />
                            <Card title="ESC readings">
                                <ESCinfo
                                    currents={this.state.dearclient.sensors.esc.currents}
                                    temp={this.state.dearclient.sensors.esc.temperatures}
                                />
                            </Card>
                            <Card title="Other Sensor Info" />
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

render(<App />, document.getElementById('app'));
