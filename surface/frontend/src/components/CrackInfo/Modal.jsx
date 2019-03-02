import React, { Component } from "react";
import Graph from "./Graph.jsx";

import "./CrackInfo.css";

const ESCAPE_KEY = 27;

export default class Modal extends Component {
  constructor(props) {
    super(props);
    this.handleEscape = this.handleEscape.bind(this);
  }

  handleEscape(event) {
    if(event.keyCode === ESCAPE_KEY){
      this.props.close();
    }
  }

  componentWillUpdate(nextProps) {
    if(nextProps.show) {
      document.addEventListener("keydown", this.handleEscape)
    } else {
      document.removeEventListener("keydown", this.handleEscape);
    }
  }
  render() {
    return (
      <div>
        <div
          className="modal-wrapper"
          style={{
            transform: this.props.show ? "translateY(0vh)" : "translateY(-100vh)",
            opacity: this.props.show ? "1" : "0"
          }}
        >
          <div className="modal-header">
            <span className="close-modal-btn" onClick={this.props.close}>
              ×
            </span>
          </div>
          <div className="modal-body">
            <Graph height={500} width={500} crackSquare="A2" length={12.4} />
          </div>
        </div>
      </div>
    );
  }
}