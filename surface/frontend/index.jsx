import React from 'react';
import {render} from 'react-dom';
import styles from './index.css';
import packet from './src/packets.js';


import Titlebar from './src/components/Titlebar/Titlebar.jsx';

//var packets = require("./src/packets.js");
let socketHost = `ws://localhost:5001`;

let socket = io.connect(socketHost, {transports: ['websocket']});
let {shell, app, ipcRenderer} = window.require('electron');


class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = require("./src/packets.js"); //= $.extend(true, {}, packets);

    this.state.config = {
            thrust_scales: {
                master: 50, velX: 100, velY: 100,
                velZ: 100, pitch: 100,
                roll: 100, yaw: 100,
            },
            thrust_invert: {
                master: 1, velX: 1, velY: 1,
                velZ: 1, pitch: 1,
                roll: 1, yaw: 1,
            },
            thruster_control: [   //invert is -1/1 for easy multiplication
                {power: 100, invert:  1}, {power: 100, invert:  1}, {power: 100, invert: -1}, {power: 100, invert:  1},
                {power: 100, invert:  1}, {power: 100, invert:  1}, {power: 100, invert:  1}, {power: 100, invert:  1}
            ],
            tool_scales: {
                manipulator: {
                    master: .25,
                    open: 1,
                    close: 1,
                    invert: 1
                }
            }
        }


    this.flaskcpy = this.state.dearflask;
    this.clientcpy = this.state.dearclient;
    this.confcpy = this.state.config;
  }

  render () {
    return (
      <div className="main">
          <div className="titlebar">
          <Titlebar/>
          </div>
          <div className="main-container">
              <div className="camera-width full-height center">
              </div>
              <div className="data-width full-height">
                  <div className="data-column">
                  </div>
                  <div className="data-column">
                  </div>
                  <div className="data-column">

                  </div>
              </div>
          </div>
      </div>
    );
  }

  componentDidMount() {
    window.react = this;
    
    var signals = require("./main.js");

    signals(this);
  }
}

render(<App/>, document.getElementById('app'));
