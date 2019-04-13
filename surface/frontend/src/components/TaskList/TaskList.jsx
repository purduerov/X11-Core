import React, { Component } from "react";
import Task from "./Task.jsx";
import styles from "./TaskList.css";
import Nav from "./Nav.jsx";
import * as TaskManifest from "./TaskManifest.json";

export default class TaskList extends Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTab: 1
    };

    this.switchTab = this.switchTab.bind(this);
  }

  getTask(activeTab) {
    return TaskManifest.find(({ taskNum }) => taskNum === activeTab);
  }

  switchTab(tabNum) {
    return () => this.setState({ activeTab: tabNum });
  }
  render() {
    return (
      <div>
        <Nav active={this.state.activeTab} switchTab={this.switchTab} />
        <div className={styles.body}>
          <Task task={this.getTask(this.state.activeTab)}/>
        </div>
      </div>
    );
  }
}
