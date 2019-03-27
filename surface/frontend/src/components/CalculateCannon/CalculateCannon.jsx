import React, { Componenet } from 'react';
import styles from '.CalculateCannon.css';
const { ipcRenderer } = window.require('electron');
const math = require('mathjs');

export default class CalculateCannon extends Component {
  constructor(props) {
    super(props);

    this.state = {calc: true};
    this.resetCalc = this.resetCalc.bind(this);
    this.calcCannon = this.calcCannon.bind(this);
  }

  calcCannon() {
    var btn = $("cannonCalcStart>button");
    if(btn.text() != "Please wait...") {
      btn.text("Please wait...");

      var r1 = Number($("#openRadius").val());
      var r2 = Number($("#boreRadius").val());
      var r3 = Number($("#wideRadius").val());
      var height = Number($("#length").val());

      var volume = (Math.PI / 3) * (Math.pow(r1,2) + r1 * r3 + Math.pow(r3,2)) * height;
      volume -= Math.PI * Math.pow(r2,2) * height;

      this.setState({
          calc: false
      }, () => {
          $("#cannonResults").text("The volume is approximately "+data.mag.toFixed(3)+" cm^3");
      });
    }
  }

  resetCalc() {
    this.setState({
      calc: true
    }, () => {
      $("#cannonCalcStart>button").text("Calculate Cannon Volume");
    });
  }

  render() {
    return (
      <div className={styles.container}>
        {this.state.calc && <div id="cannonCalcStart">
          <div className={styles.innerRow}>
            <p>Open end radius</p>
            <input id="openRadius" defaultValue="6 inches" />
            <p>Bore Radius</p>
            <input id="boreRadius" defaultValue="6 inches" />
            <p>Wide/Closed end radius</p>
            <input id="wideRadius" defaultValue="thicc as shit" />
            <p>Length</p>
            <input id="length" defaultValue="3 inches :(" />
          </div>
          <button onClick={this.calcCannon} >Calculate Cannon Volume</button>
        </div>}
        {!this.state.calc && <div id="cannonResultsContainer">
          <p id="cannonResults" />
          <button onClick={this.resetCalc}>Reset Calculation</button>
        </div>}
      </div>
    );
  }
}
