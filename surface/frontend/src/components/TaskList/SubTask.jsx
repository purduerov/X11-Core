import React, { Component } from "react";
import PropTypes from "prop-types";
import styles from "./TaskList.css";
import SubSubTask from "./SubSubTask.jsx";

export default class SubTask extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <SubTaskHeader {...this.props}>
        <SubSubTasksRender {...this.props} />
      </SubTaskHeader>
    );
  }
}

function SubTaskHeader(props) {
  return (
    <div
      className={styles.subTask}
      onClick={props.funcs.toggleSubtaskDisplay(props.sTNum)}
    >
      <span className={styles.openClose}>
        {props.subTask.display === "block" ? "-" : "+"}
      </span>
      {""}
      <span>{props.subTask.name}</span>
      <div className={styles.panel} style={{ display: props.subTask.display }}>
        {props.children}
      </div>
    </div>
  );
}

function SubSubTasksRender(props) {
  let sST;
  if ((sST = props.subTask.subSubTasks)) {
    const sSTArray = sST.map((val, idx) => (
      <SubSubTask key={idx} subSubTask={val} />
    ));
    return <div>{sSTArray}</div>;
  } else {
    return "";
  }
}
