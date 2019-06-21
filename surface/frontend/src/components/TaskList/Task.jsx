import React, { Component } from "react";
import styles from "./TaskList.css";
import SubTask from "./SubTask.jsx";

export default class Task extends Component {
  constructor(props) {
    super(props);
    this.toggleSubtaskDisplay = this.toggleSubtaskDisplay.bind(this);
    this.toggleCheckbox = this.toggleCheckbox.bind(this);
  }

  toggleSubtaskDisplay(stNum) {
    return () =>
      this.props.funcs.toggleSubtaskDisplay(this.props.task.taskNum, stNum);
  }

  toggleCheckbox(stNum, sstNum) {
    this.props.funcs.toggleCheckbox(this.props.task.taskNum, stNum, sstNum);
  }

  render() {
    const funcs = {
      toggleSubtaskDisplay: this.toggleSubtaskDisplay,
      toggleCheckbox: this.toggleCheckbox
    };
    return (
      <div>
        <div className={styles.titleContainer}>
          <div className={styles.title}>{this.props.task.taskDesc}</div>
        </div>

        {/* <div className={styles.stats}>
          {`${this.props.task.pointsEarned} out of ${
            this.props.task.pointTotal
          } points earned`}
        </div> */}

        <div className={styles.subTaskContainer}>
          {this.props.task.subTasks.map((sT, idx) => (
            <SubTask subTask={sT} key={idx} stNum={idx} funcs={funcs} />
          ))}
        </div>
      </div>
    );
  }
}
