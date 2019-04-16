import React, { Component } from "react";
import PropTypes from "prop-types";
import Modal from "./Modal.jsx";

export default class CrackInfo extends Component {
  constructor() {
    super();
    this.state = {
      showing: false
    };
    this.openModalHandler = this.openModalHandler.bind(this);
    this.closeModalHandler = this.closeModalHandler.bind(this);
  }

  openModalHandler() {
    this.setState({
      showing: true
    });
  }

  closeModalHandler() {
    this.setState({
      showing: false
    });
  }

  render() {
    return (
      <div>
        <div>
          <div>Length:</div>
          {this.props.length} cm
        </div>
        {this.state.showing ? (
          <button onClick={this.closeModalHandler}>Close Graph</button>
        ) : (
          <button onClick={this.openModalHandler}>Display Graph</button>
        )}
        {this.state.showing ? (
          <Modal
            close={this.closeModalHandler}
            crackSquare={this.props.crackSquare}
            length={this.props.length}
          />
        ) : (
          ""
        )}
      </div>
    );
  }
}

CrackInfo.propTypes = {
  crackSquare: PropTypes.string.isRequired,
  length: PropTypes.number.isRequired
};
