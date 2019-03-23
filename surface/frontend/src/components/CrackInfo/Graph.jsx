import React, { Component } from "react";
import PropTypes from "prop-types";

import styles from "./CrackInfo.css";

const NUM_ROWS = 3;
const NUM_COLS = 4;

export default class Graph extends Component {
  constructor(props) {
    super(props);
    this.getSizes();
  }

  getSizes() {
    let { width, height, length, crackSquare } = this.props;
    width -= 2;
    height -= 2;
    let squareSize;
    if (width / NUM_COLS > height / NUM_ROWS) {
      squareSize = height / NUM_ROWS;
      squareSize -= squareSize % 10;
    } else {
      squareSize = width / NUM_COLS;
      squareSize -= squareSize % 10;
    }

    height = squareSize * 3 + 2;
    width = squareSize * 4 + 2;

    this.state = {
      squareSize,
      crackSquare,
      length,
      height,
      width
    };
  }

  gridData() {
    const { squareSize } = this.state;
    const data = [];
    let xpos = 1;
    let ypos = 1;

    for (let row = 0; row < 3; row++) {
      data.push([]);

      for (let column = 0; column < 4; column++) {
        data[row].push({
          id: `${String.fromCharCode(97 + column).toUpperCase()}${row + 1}`,
          x: xpos,
          y: ypos,
          width: squareSize,
          height: squareSize
        });
        xpos += squareSize;
      }
      xpos = 1;
      ypos += squareSize;
    }
    return data;
  }

  rows(row, index) {
    return (
      <g className="row" key={index}>
        {row.map(this.columns, this)}
      </g>
    );
  }

  columns({ id, x, y, width, height }, index) {
    return (
      <g key={index}>
        <rect
          key={id}
          x={x}
          y={y}
          width={width}
          height={height}
          fill="#FFFFFF"
          stroke="#222222"
        />
        {id === this.state.crackSquare ? (
          <Text squareSize={this.state.squareSize} length={this.state.length} x={x} y={y} />
        ) : (
          ""
        )}
      </g>
    );
  }

  render() {
    return (
      <div>
        <svg className={styles.grid} height={this.state.height} width={this.state.width}>
          {this.gridData().map(this.rows, this)}
        </svg>
      </div>
    );
  }
}

function Text({ squareSize, length, x, y }) {
  const fontSize = squareSize / 5.5;

  return (
    <text
      x={x + squareSize / 10}
      y={y + (squareSize - fontSize) / 1.5}
      fontSize={`${fontSize}px`}
      fill="blue"
    >
      {length} cm
    </text>
  );
}

Graph.propTypes = {
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
  crackSquare: PropTypes.string.isRequired,
  length: PropTypes.number.isRequired
};
