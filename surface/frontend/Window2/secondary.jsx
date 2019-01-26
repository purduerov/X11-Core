import React from 'react';
import { render } from 'react-dom';
<<<<<<< HEAD
// import styles from './secondary.css';
import packet from '../src/packets.js';
=======
import styles from './secondary.css';
import packet from '../src/packets.json';
>>>>>>> bb1c4835e27d61d84b90f5d9eca85903f409361e

import Panel from '../src/components/Panel/Panel.jsx';
import Titlebar from '../src/components/Titlebar/Titlebar.jsx';
import { MDBContainer, Row, Col, Navbar, NavbarBrand } from 'mdbreact';


const styles = {
    height: '100vh'
}

const nav = {
    width: '100vw'
}

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
            <MDBContainer fluid className="elegant-color-dark" style={styles}>
                <small>
                    <Row>
                        <Navbar className="mb-3" color="primary-color-dark" dark expand="md" style={nav}>
                            <NavbarBrand>
                                <strong className="white-text">Purdue ROV Secondary Screen</strong>
                            </NavbarBrand>
                        </Navbar>
                    </Row>
                    <Row>
                        <Col size="5">
                            <Panel title="Camera Vision will be here.">

                            </Panel>
                        </Col>
                        <Col size="7">
                            <Row>
                                <Col size="4">
                                    <Panel />
                                </Col>
                                <Col size="4">
                                    <Panel />
                                </Col>
                                <Col size="4">
                                    <Panel />
                                </Col>
                            </Row>
                        </Col>
                    </Row>
                </small>
            </MDBContainer>

        );
    }
}

render(<App />, document.getElementById('app'));
