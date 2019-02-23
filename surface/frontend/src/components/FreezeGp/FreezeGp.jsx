import React, { Component } from 'react';
import styles from './FreezeGp.css';

export default class FreezeGp extends Component {
  constructor(props) {
    super(props);

    this.freezeFunc = this.freezeFunc.bind(this);
    this.unfreezeFunc = this.unfreezeFunc.bind(this);
  }

  freezeFunc() {
    this.props.rend(1); //maybeFreeze = 1 - maybeFreeze
  }

  unfreezeFunc() {
    this.props.rend(0);
  }

  render() {
    return (
      <div>
        <h1>GamePad Locking</h1>

        <button onClick={this.freezeFunc} id="freezeButton" className="button">Freeze</button>

        <button onClick={this.unfreezeFunc} id="unfreezeButton" className="button">Unfreeze</button>
      </div>
    );
  }


}
