import React, { Component } from "react";
import styles from "./TaskList.css";

export default class SubSubTask extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div>
        <div className={styles.subSubTask}>
          <span className={styles.subSubTaskName}>
            {this.props.subSubTask.name}
          </span>
          <span className={styles.subSubTaskInput}>
            <input type="checkbox" />
          </span>
        </div>
      </div>
    );
  }
}
