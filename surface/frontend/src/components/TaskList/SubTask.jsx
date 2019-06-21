import React, { Component } from "react";
import PropTypes from "prop-types";
import styles from "./TaskList.css";
import SubSubTask from "./SubSubTask.jsx";

export default class SubTask extends Component {
  constructor(props) {
    super(props);
    this.toggleCheckbox = this.toggleCheckbox.bind(this);
  }

  toggleCheckbox(sstNum) {
    return () => this.props.funcs.toggleCheckbox(this.props.stNum, sstNum);
  }

  render() {
    const funcs = { toggleCheckbox: this.toggleCheckbox };
    let sST, sSTArray;
    if ((sST = this.props.subTask.subSubTasks)) {
      sSTArray = sST.map((val, idx) => (
        <SubSubTask key={idx} sstNum={idx} subSubTask={val} funcs={funcs} />
      ));
    }
    return (
      <SubTaskHeader toggleCheckbox={this.toggleCheckbox} {...this.props}>
        <div>{sSTArray ? sSTArray : ""}</div>
      </SubTaskHeader>
    );
  }
}

class SubTaskHeader extends Component {
  render() {
    return (
      <div className={styles.subTask}>
        <PlusMinus {...this.props} />
        <span
          className={styles.subTaskName}
          onClick={this.props.funcs.toggleSubtaskDisplay(this.props.stNum)}
        >
          {this.props.subTask.name}
        </span>
        <input
          type="checkbox"
          checked={this.props.subTask.checked}
          onChange={this.props.toggleCheckbox(null)}
        />

        <div
          className={styles.panel}
          style={{ display: this.props.subTask.display }}
        >
          {this.props.children}
        </div>
      </div>
    );
  }
}

function PlusMinus(props) {
  if (props.subTask.subSubTasks) {
    return (
      <span
        className={styles.openClose}
        onClick={props.funcs.toggleSubtaskDisplay(props.stNum)}
      >
        {props.subTask.display === "block" ? "-" : "+"}
      </span>
    );
  } else {
    return <span className={styles.openCloseSpacer} />;
  }
}
