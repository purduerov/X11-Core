import React, { Component } from "react";
import PropTypes from "prop-types";
import styles from "./TaskList.css";

export default class SubTask extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <div>
        <div
          className={styles.subTask}
          onClick={this.props.funcs.toggleSubtaskDisplay(this.props.sTNum)}
        >
          {this.props.subTask.name}
          <div
            className={styles.panel}
            style={{ display: this.props.subTask.display }}
          >
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
