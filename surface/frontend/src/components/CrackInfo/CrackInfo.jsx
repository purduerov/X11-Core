import React, { Component } from "react";
import Modal from './Modal.jsx';

import './CrackInfo.css';

export default class ModalWrapper extends Component {
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
        <button className="open-modal-btn" onClick={this.openModalHandler}>
          Open Modal
        </button>

        <Modal
          className="modal"
          show={this.state.showing}
          close={this.closeModalHandler}
        >
        </Modal>
      </div>
    );
  }
}

// <CrackMap height="500" width="500" crackSquare="A2" length="12.4" />
