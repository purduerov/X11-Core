import React, { Component } from "react";
import PropTypes from "prop-types";
import Graph from "./Graph.jsx";

import styles from "./CrackInfo.css";

const ESCAPE_KEY = 27;

export default class Modal extends Component {
  constructor(props) {
    super(props);
    this.handleEscape = this.handleEscape.bind(this);
  }

  handleEscape(event) {
    if (event.keyCode === ESCAPE_KEY) {
      this.props.close();
    }
  }

  componentDidMount() {
    document.addEventListener("keydown", this.handleEscape);
  }

  componentWillUnmount() {
    document.removeEventListener("keydown", this.handleEscape);
  }

  render() {
    return (
      <div className={styles.modalWrapper}>
        <div className={styles.modalHeader}>
          <h5>Identified Crack Length and Location</h5>
          <button className={styles.closeModalBtn} onClick={this.props.close}>
            Close Graph
          </button>
        </div>
        <Graph height={500} width={500} crackSquare={this.props.crackSquare} length={this.props.length} />
      </div>
    );
  }
}

Modal.propTypes = {
  close: PropTypes.func.isRequired,
  crackSquare: PropTypes.string.isRequired,
  length: PropTypes.number.isRequired
};
