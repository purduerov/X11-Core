import React, { Component } from 'react';
import styles from './CalculateThrust.css';

export default class CalculateThrust extends Component {
  constructor(props) {
    super(props);

    this.state = {calc: true};
    this.resetCalc = this.resetCalc.bind(this);
    this.calcThrust = this.calcThrust.bind(this);
  }

  calcThrust() {
    var btn = $("thrustCalcStart>button");
    if(btn.text() != "Please wait...") {
      btn.text("Please wait...");

      var volume = this.props.volume / (1000000); //volume (cm^3 to m^3)
      var waterMass = volume * (1000); // volume(m^3) * density of water (kg/m^3)
      var fBuoyancy = waterMass * 9.7991; //F = mg
      var objectDensity = Number($("#specGrav").val()); //kg/m^3
      var objectWeight = objectDensity * volume * 9.7991; //kg/m^3 * m^3 * g to get N
      var apparent = objectWeight - fBuoyancy;
      apparent = apparent.toFixed(3);


      this.setState({
          calc: false
      }, () => {
          $("#thrustResults").text("The apparent weight of the cannon is "+apparent+" N");
      });
    }
  }

  resetCalc() {
    this.setState({
      calc: true
    }, () => {
      $("#thrustCalcStart>button").text("Calculate Apparent Weight");
    });
  }

  render() {
    return (
      <div className={styles.container}>
        {this.state.calc && <div id="thrustCalcStart">
          <div className={styles.innerRow}>
            <div className={styles.halfLeft} >
              <p>Specific Gravity (kg/m^3)</p>
              <input id="specGrav" defaultValue="10" />
            </div>
            <div className={styles.halfRight} >
              <p>Thrust (N)</p>
              <input id="thrust" defaultValue="46" />
            </div>
          </div>
          <button onClick={this.calcThrust} >Calculate Apparent Weight</button>
        </div>}
        {!this.state.calc && <div id="thrustResultsContainer">
          <p id="thrustResults" />
          <button onClick={this.resetCalc}>Reset Calculation</button>
        </div>}
      </div>
    );
  }
}
