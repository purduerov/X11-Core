import React, { Component } from 'react';
import styles from './PocketRocket.css';

export default class PocketRocket extends Component {
  constructor(props) {
    super(props);

    this.state = this.
  }

}

var key_pressed = false;

$("body").keydown(function(event) {
  var key = event.which;
  if (!key_pressed) {
    console.log("key pressed");
    console.log(key);
    key_pressed = true;
  }
});

$("body").keyup(function(event) {
  key_pressed = false;
  console.log('key released');
});
