import React from 'react';
import { render } from 'react-dom';
import styles from './main.css';

import Card from '../src/components/Card/Card.jsx';
import CameraScreen from '../src/components/CameraScreen/CameraScreen.jsx';
import Titlebar from '../src/components/Titlebar/Titlebar.jsx';
import PHinfo from '../src/components/PHinfo/PHinfo.jsx'
import BuddyControlsShow from '../src/components/BuddyControlsShow/BuddyControlsShow.jsx';
import FreezeGp from '../src/components/FreezeGp/FreezeGp.jsx';
import betterlayouts from '../src/gamepad/betterlayouts.js';
import ThrusterInfo from '../src/components/ThrusterInfo/ThrusterInfo.jsx';
import Gpinfo from '../src/components/Gpinfo/Gpinfo.jsx';
import ShowObject from '../src/components/ShowObject/ShowObject.jsx'
import PacketView from '../src/components/PacketView/PacketView.jsx';
import Timer from '../src/components/Timer/Timer.jsx';
import CVview from '../src/components/CVview/CVview.jsx';
import CrackInfo from '../src/components/CrackInfo/CrackInfo.jsx';

const socketHost = 'ws://localhost:5001';

/* These should be done in a component, or the js file for this window

const socket = io.connect(socketHost, { transports: ['websocket'] });
const { shell, app, ipcRenderer } = window.require('electron');
*/


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = require("../src/packets.json");
        this.state.gp = require('../src/gamepad/bettergamepad.js');

        this.state.gp = require ("../src/gamepad/bettergamepad.js");
        this.gp = require('../src/gamepad/bettergamepad.js');


        this.state.directions = { x: 0, y: 0 };
        this.state.freeze = 0;
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
            thrust_invert: this.state.dearflask.thrusters.inv_6dof,
            thruster_control: [ // invert is -1/1 for easy multiplication
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
                { power: 100, invert: 1 }, { power: 100, invert: 1 },
            ],
        };

        this.state.config.thruster_control.map((cur, index, arr) => {
            arr[index].invert = this.state.dearflask.thrusters.inverted[index];
        });


        this.flaskcpy = this.state.dearflask;
        this.clientcpy = this.state.dearclient;
        this.confcpy = this.state.config;

        this.setFreeze = this.setFreeze.bind(this);
        this.changeDisabled = this.changeDisabled.bind(this);
    }

    componentDidMount() {
        var signals = require('./main.js');
        window.react = this;

        signals(this, socketHost);

        setInterval(() => {
            if (this.state.freeze) {
                this.flaskcpy.thrusters.desired_thrust = [0.0, 0.0, -0.1, 0.0, 0.0, 0.0];
            }

            this.setState({
                dearflask: this.flaskcpy,
            });
        }, 50);
    }

    setFreeze(value) {
        this.setState({
            freeze: value,
        });
    }

    changeDisabled(dis) {
        this.flaskcpy.thrusters.disable_thrusters = dis;
    }

    render() {
        return (
            <div className="main">
                <div className="titlebar">
                    <Titlebar title="Purdue ROV Primary Screen" />
                </div>
                <div className="main-container">
                    <div className="camera-width full-height center">
                        <CameraScreen
                            next={this.state.gp.buttons.left}
                            prev={this.state.gp.buttons.right}
                        />
                    </div>
                    <div className="data-width full-height">
                        <div className="data-column">
                            <Card>
                                <PHinfo />
                            </Card>
                            <Card>
                                <CrackInfo
                                    length={-27.6}
                                    crackSquare="D3"
                                />
                            </Card>
                            <Card title="Line Graph Component" />
                        </div>
                        <div className="data-column">
                            <Card>
                                <FreezeGp
                                    maybeFreeze={this.state.freeze}
                                    rend={this.setFreeze}
                                />
                            </Card>
                            <Card>
                                <ShowObject
                                    obj={this.state.dearclient.sensors.imu}
                                />
                            </Card>
                            <Card>
                                <ThrusterInfo
                                    thrusters={this.state.dearclient.thrusters}
                                    disabled={this.state.dearflask.thrusters.disable_thrusters}
                                    manipulator={this.state.dearflask.tools.manipulator}
                                    rend={this.changeDisabled}
                                />
                            </Card>
                            <Card title="Desired Force Vector" />
                        </div>
                        <div className="data-column">
                            <Card>
                                <ShowObject obj={this.state.dearclient.sensors.esc.temperatures} />
                            </Card>
                            <Card title="Computer Vision Stuff" />
                            <Card title="CV view window">
                                <CVview desc={"Purdo good, Purdon't let Eric make messages"} tdist={[0.0, 0.1, 0.2, 0.4, 0.7, 0.8]} />
                            </Card>
                            <Card title="Time">
                                <Timer />
                            </Card>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}

render(<App />, document.getElementById('app'));
