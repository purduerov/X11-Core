import React from "react";
import propTypes from "prop-types";
import styles from "./TaskList.css";

export default function Nav(props) {
  return (
    <div>
      <ul className="nav nav-tabs">
        <li className={"nav-item " + styles.navLi} onClick={props.switchTab(1)}>
          <a
            className={
              (props.active === 1 ? "nav-link active " : "nav-link ") +
              styles.textPrimary
            }
            href="#"
          >
            Task 1
          </a>
        </li>
        <li className={"nav-item " + styles.navLi} onClick={props.switchTab(2)}>
          <a
            className={
              (props.active === 2 ? "nav-link active " : "nav-link ") +
              styles.textPrimary
            }
            href="#"
          >
            Task 2
          </a>
        </li>
        <li className={"nav-item " + styles.navLi} onClick={props.switchTab(3)}>
          <a
            className={
              (props.active === 3 ? "nav-link active " : "nav-link ") +
              styles.textPrimary
            }
            href="#"
          >
            Task 3
          </a>
        </li>
      </ul>
    </div>
  );
}

Nav.propTypes = {
  switchTab: propTypes.func.isRequired,
  active: propTypes.number.isRequired
};
