import React, { Component } from "react";
import Task from "./Task.jsx";
import styles from "./TaskList.css";
import Nav from "./Nav.jsx";
import * as TaskManifest from "./TaskManifest.json";

export default class TaskList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTab: 1,
      tasks: TaskManifest
    };

    this.switchTab = this.switchTab.bind(this);
    this.pointsEarned = this.pointsEarned.bind(this);
    this.toggleSubtaskDisplay = this.toggleSubtaskDisplay.bind(this);
  }

  switchTab(tabNum) {
    return () => this.setState({ activeTab: tabNum });
  }

  pointsEarned(taskNum, addPoints) {
    const tasks = this.state.tasks;
    tasks[taskNum - 1].pointsEarned += addPoints;
    this.setState({ tasks });
  }

  toggleSubtaskDisplay(taskNum, sTNum) {
    let tasks = this.state.tasks;
    const display = tasks[taskNum - 1].subTasks[sTNum].display;
    tasks[taskNum - 1].subTasks[sTNum].display =
      display === "none" ? "block" : "none";
    this.setState({ tasks });
  }

  render() {
    const funcs = {
      pointsEarned: this.pointsEarned,
      toggleSubtaskDisplay: this.toggleSubtaskDisplay
    };
    return (
      <div className={styles.container}>
        <Nav active={this.state.activeTab} switchTab={this.switchTab} />
        <div className={styles.body}>
          <Task
            task={this.state.tasks[this.state.activeTab - 1]}
            funcs={funcs}
          />
        </div>
      </div>
    );
  }
}
