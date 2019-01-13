import React from 'react';
import { render } from 'react-dom';
import 'font-awesome/css/font-awesome.min.css';
import 'bootstrap-css-only/css/bootstrap.min.css';
import 'mdbreact/dist/css/mdb.css';
import CVview from '../src/components/CVview/CVview.jsx';

// import styles from './main.css';
import packet from '../src/packets.js';

// import Card from '../src/components/Card/Card.jsx';
// import Titlebar from '../src/components/Titlebar/Titlebar.jsx';
import { MDBContainer, Row, Col, Navbar, NavbarBrand, Card, CardBody, CardImage, CardTitle, CardText, Fa } from 'mdbreact';

const socketHost = 'ws://localhost:5001';

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
        this.state = require('../src/packets.js'); //= $.extend(true, {}, packets);

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
            <MDBContainer fluid className="elegant-color" style={styles}>
                <Row>
                    <Navbar className="mb-3" color="indigo" dark expand="md" style={nav}>
                        <NavbarBrand>
                            <strong className="white-text">Purdue IEEE ROV</strong>
                        </NavbarBrand>
                    </Navbar>
                </Row>
                <Row>
                    <Col size="6">

                    </Col>
                    <Col size="3">
                        <Card>
                            
                            <CardBody className="elegant-color white-text rounded-bottom">
                                <CardTitle>Card Title</CardTitle>
                                <hr className="hr-light" />
                                <CardText className="white-text">
                                    Some quick example text to build on the card title and make
                                    up the bulk of the card&apos;s content.
              </CardText>
                                <a href="#!" className="black-text d-flex justify-content-end" >
                                    <h5 className="white-text">
                                        Read more <Fa icon="angle-double-right" />
                                    </h5>
                                </a>
                            </CardBody>
                        </Card>
                    </Col>
                    <Col size="3">

                    </Col>
                </Row>
            </MDBContainer>
        );
    }
}

render(<App />, document.getElementById('app'));
