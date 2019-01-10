import React, { Component } from 'react';
import styles from "./Telemetry.css";

export default class Telemetry extends Component {
  constructor(props) {
    super(props);
    this.state = {horizontal: 0, vertical: 0, depth: 0}
  }


  componentWillMount() {
    <div>
      <canvas width="300" height="200" id="canvas">Oof, I don't work yet</canvas>
      <input type="text" id="title" placeholder="heckin frick"/>
    </div>
  }


/*  componentWillReceiveProps(nextProps) {
    if(nextProps.gp!==this.props.gp) {
      //update state
      var canvas = document.getElementById('canvas'),
          ctx = canvas.getContext('2d');
      ctx.fillStyle = '#0e70d1'; //blue, will graduate to blue background and draw on transparent canvas over it
      //arrow function that updates writing
      ctx.save();
      ctx.clearRect(0,0, canvas.width, canvas.height);
      ctx.fillText("Fuck IU", 15, canvas.height / 2 + 35);
      ctx.restore();
    }
  } */

  update() {
    var canvas = document.getElementById('canvas'),
    ctx = canvas.getContext('2d');
    ctx.fillStyle = '#0e70d1';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    document.getElementById('title').addEventListener('keyup', function() {
    	ctx.save();
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    	var stringTitle = document.getElementById('title').value;
      ctx.fillStyle = '#fff';
      ctx.font = '60px sans-serif';
      ctx.fillText(stringTitle, 15, canvas.height / 2 + 35);
      ctx.restore();
    });
  }

  render() {
    return (
      <div>
      </div>
    );
  }

} //class
