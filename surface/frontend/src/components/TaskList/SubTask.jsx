import React, { Component } from "react";
import PropTypes from "prop-types";
import styles from "./TaskList.css";

export default class SubTask extends Component {
  constructor(props) {
    super(props);
    this.togglePanel = this.togglePanel.bind(this);
  }

  // togglePanel() {
  //   const currentState = this.state.panelStyle.display;
  //   this.setState({
  //     panelStyle: {
  //       display: currentState === "none" ? "block" : "none"
  //     }
  //   });
  // }

  render() {
    return (
      <div>
        <div className={styles.subTask} onClick={this.props.togglePanel(this.props.subTask.idx)}>
          {this.props.subTask.name}
          <div className={styles.panel} style={this.props.subTask.panelStyle}>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce in
            convallis quam. Praesent venenatis augue at quam fringilla mollis.
            Donec facilisis sapien felis, at bibendum lectus malesuada vitae.
            Maecenas sed faucibus tellus, in pretium turpis. Ut mattis felis a
            purus congue fringilla.
          </div>
        </div>
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
    score: PropTypes.number,
    panelStyle: PropTypes.shape({
      display: PropTypes.string.isRequired,
      overflow: PropTypes.string.isRequired
    }).isRequired
  }).isRequired
};
