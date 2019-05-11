import React, { Component } from "react";
import styles from "./TaskList.css";

export default class SubSubTask extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div>
        <div className={styles.subSubTask}>{this.props.subSubTask.name}</div>
      </div>
    );
  }
}
