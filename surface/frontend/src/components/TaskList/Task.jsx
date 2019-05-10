import React, { Component } from 'react';
import styles from './TaskList.css';

export default class Task extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div className={styles.titleContainer}>
          <div className={styles.title}>{this.props.task.taskDesc}</div>
        </div>

        <div className={styles.stats}>
          {`${this.props.task.pointsEarned} out of ${
            this.props.task.pointTotal
          } points earned`}
        </div>

        <div className={styles.subTaskContainer}>{/* <SubTask /> */}</div>
      </div>
    );
  }
}
