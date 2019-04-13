import React, { Component } from "react";
import PropTypes from "prop-types";
import styles from "./TaskList.css";
import SubTask from "./SubTask.jsx";

export default class Task extends Component {
  constructor(props) {
    super(props);
    this.state = {
      pointsEarned: 0
    };
  }

  render() {
    return (
      <div>
        <div className={styles.titleContainer}>
          <div className={styles.title}>{this.props.task.taskDesc}</div>
        </div>

        <div className={styles.stats}>
          {`${this.state.pointsEarned} out of ${
            this.props.task.pointTotal
          } points earned`}
        </div>

        <div className={styles.subTaskContainer}>
          {this.props.task.subTasks.map((sT, idx) => (
            <SubTask key={idx} subTask={sT} />
          ))}
        </div>
      </div>
    );
  }
}

Task.propTypes = {
  task: PropTypes.shape({
    taskNum: PropTypes.number.isRequired,
    taskDesc: PropTypes.string.isRequired,
    pointTotal: PropTypes.number.isRequired,
    subTasks: PropTypes.arrayOf(PropTypes.object).isRequired
  }).isRequired
};
