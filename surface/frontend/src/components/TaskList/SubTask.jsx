import React, { Component } from "react";
import PropTypes from "prop-types";
import styles from './TaskList.css';

export default class SubTask extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    return (
      <div>
        <div className={styles.subTask}>{this.props.subTask.name}</div>
      </div>
    );
  }
}

SubTask.propTypes = {
  subTask: PropTypes.shape({
    name: PropTypes.string.isRequired,
    subSubTasks: PropTypes.arrayOf(PropTypes.object),
    criteria: PropTypes.oneOfType([
      PropTypes.oneOf(["EACH_MAX_2", "EACH_MAX_4"]),
      PropTypes.object // could be null
    ]),
    score: PropTypes.number
  }).isRequired
};
