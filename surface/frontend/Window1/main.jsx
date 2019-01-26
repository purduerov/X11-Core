import React from 'react';
import { render } from 'react-dom';
import styles from './main.css';
import packet from '../src/packets.js';


import CVview from '../src/components/CVview/CVview.jsx';
import ESCinfo from '../src/components/ESCinfo/ESCinfo.jsx';
import Card from '../src/components/Card/Card.jsx';
import CameraScreen from '../src/components/CameraScreen/CameraScreen.jsx';
import ForceScales from '../src/components/ForceScales/ForceScales.jsx';
import Titlebar from '../src/components/Titlebar/Titlebar.jsx';
import ThrusterInfo from '../src/components/ThrusterInfo/ThrusterInfo.jsx';
import ThrusterScales from '../src/components/ThrusterScales/ThrusterScales.jsx';
import Gpinfo from '../src/components/Gpinfo/Gpinfo.jsx';
import ShowObject from '../src/components/ShowObject/ShowObject.jsx'
import ToolView from '../src/components/ToolView/ToolView.jsx';
import PacketView from '../src/components/PacketView/PacketView.jsx';
import betterlayouts from '../src/gamepad/betterlayouts.js';

const socketHost = 'ws://localhost:5001';

/* These should be done in a component, or the js file for this window

const socket = io.connect(socketHost, { transports: ['websocket'] });
const { shell, app, ipcRenderer } = window.require('electron');
*/


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = require('../src/packets.js'); //= $.extend(true, {}, packets);
        this.state.gp = require('../src/gamepad/bettergamepad.js');

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
    }

    render() {
        return (
            <div className="main">
                <div className="titlebar">
                    <Titlebar title="Purdue ROV Primary Screen" />
                </div>
                <div className="main-container">
                    <div className="camera-width full-height center">
                    <CameraScreen next={this.state.gp.buttons.left} prev={this.state.gp.buttons.right} />
                    </div>
                    <div className="data-width full-height">
                        <div className="data-column">
                            <Card>
                                <ThrusterInfo
                                  thrusters={this.state.dearclient.thrusters}
                                  disabled={this.state.dearflask.thrusters.disabled_thrusters}
                                  manipulator={this.state.dearflask.manipulator.power}
                                  obs_tool={this.state.dearflask.obs_tool.power}
                                  rend={this.changeDisabled}
                                />
                            </Card>
                            <Card title="CV view window">
                                <CVview desc={"Purdo good, Purdon't let Eric make messages"} tdist={[0.0, 0.1, 0.2, 0.4, 0.7, 0.8]} />
                            </Card>
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
                            <Card title="ESC readings">
                                <ESCinfo
                                  currents={this.state.dearclient.sensors.esc.currents}
                                  temp={this.state.dearclient.sensors.esc.temperatures}
                                  />
                            </Card>
                            <Card>
                                <ToolView 
                                  manipulator={this.state.dearflask.manipulator.power}
                                  obs_tool={this.state.dearflask.obs_tool.power}
                                  servo={this.state.dearflask.maincam_angle}
                                  transmitter={this.state.dearflask.transmitter}
                                  magnet={this.state.dearflask.magnet}
                                  conf={this.state.config.tool_scales}
                                  rend={this.rendTools}
                                  />
                            </Card>
                            <Card title="Object Display">
                                <ShowObject
                                  obj={this.state.dearclient.sensors.obs}
                                  />
                            </Card>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

render(<App />, document.getElementById('app'));
