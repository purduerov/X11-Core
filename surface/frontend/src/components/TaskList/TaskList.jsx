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
    this.toggleCheckbox = this.toggleCheckbox.bind(this);
  }

  switchTab(tabNum) {
    return () => this.setState({ activeTab: tabNum });
  }

  pointsEarned(taskNum, addPoints) {
    const tasks = this.state.tasks;
    tasks[taskNum - 1].pointsEarned += addPoints;
    this.setState({ tasks });
  }

  toggleSubtaskDisplay(taskNum, stNum) {
    let tasks = this.state.tasks;
    const display = tasks[taskNum - 1].subTasks[stNum].display;
    tasks[taskNum - 1].subTasks[stNum].display =
      display === "none" ? "block" : "none";
    this.setState({ tasks });
  }

  toggleCheckbox(taskNum, stNum, sstNum) {
    if (sstNum !== null) {
      let tasks = this.state.tasks;
      const current =
        tasks[taskNum - 1].subTasks[stNum].subSubTasks[sstNum].checked;
      tasks[taskNum - 1].subTasks[stNum].subSubTasks[sstNum].checked = !current;
      this.setState({ tasks });
    } else {
      let tasks = this.state.tasks;
      const current = tasks[taskNum - 1].subTasks[stNum].checked;
      tasks[taskNum - 1].subTasks[stNum].checked = !current;
      this.setState({ tasks });
    }
  }

  render() {
    const funcs = {
      pointsEarned: this.pointsEarned,
      toggleSubtaskDisplay: this.toggleSubtaskDisplay,
      toggleCheckbox: this.toggleCheckbox
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
