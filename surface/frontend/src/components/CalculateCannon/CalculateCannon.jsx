import React, { Component } from 'react';
import styles from './CalculateCannon.css';

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
      var pi = 3.14159265359;
      var volume = (pi / 3) * (r1 * r1 + r1 * r3 + r3 * r3) * height;
      volume -= pi * r2 * r2 * height;
      volume = volume.toFixed(2);

      this.props.rend(volume);

      this.setState({
          calc: false
      }, () => {
          $("#cannonResults").text("The volume is approximately "+volume+" cm^3");
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
            <div className={styles.halfLeft} >
              <p>Open end radius r1 (cm)</p>
              <input id="openRadius" defaultValue="5.3" />
              <p>Bore Radius r2 (cm)</p>
              <input id="boreRadius" defaultValue="2.8" />
            </div>
            <div className={styles.halfRight} >
              <p>Wide/Closed end radius r3 (cm)</p>
              <input id="wideRadius" defaultValue="7.7" />
              <p>Length (cm)</p>
              <input id="length" defaultValue="46" />
            </div>
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
