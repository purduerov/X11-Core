import React, { Component } from "react";
import PropTypes from 'prop-types';
import * as d3 from "d3";

const SQUARE_WIDTH_CM = 30; // 30 cm wide square


export default class CrackMap extends Component {
  constructor(props) {
    super(props);
    console.log(props);
    this.getSizes();
  }

  getSizes() {
    const { width, height, crackLX, crackLY, crackRX, crackSquare } = this.props;
    let squareSize;
    if (width / 4 > height / 3) {
      squareSize = height / 3;
      squareSize -= squareSize % 10;
    } else {
      squareSize = width / 4;
      squareSize -= squareSize % 10;
    }
    const offset = this.getOffset(crackSquare);
    const crackLXPixels = crackLX / SQUARE_WIDTH_CM * squareSize;
    const crackLYPixels = crackLY / SQUARE_WIDTH_CM * squareSize;
    const crackRXPixels = crackRX / SQUARE_WIDTH_CM * squareSize;
    const absCrackLX = offset.x + crackLXPixels;
    const absCrackLY= offset.y + crackLYPixels;
    const crackWidth = Math.abs(crackLXPixels - crackRXPixels);
    const crackHeight = 1.85 / SQUARE_WIDTH_CM * squareSize;

    this.state = {
      squareSize,
      crackX: absCrackLX,
      crackY: absCrackLY,
      crackWidth,
      crackHeight
    };
  }

  getOffset(crackSquare) {
    crackSquare = crackSquare.split('');

    const letterOffset = { A: 0, B: 1, C: 2, D: 3 }[crackSquare[0]];
    const numberOffset = crackSquare[1] - 1;

    return { x: letterOffset, y: numberOffset };
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
  componentDidMount() {
    const griddata = this.gridData();
    console.log(griddata);
    console.log(this.state);

    const grid = d3
      .select("#grid")
      .append("svg")
      .attr("width", this.props.width + 2)
      .attr("height", this.props.height + 2);

    const row = grid
      .selectAll(".row")
      .data(griddata)
      .enter()
      .append("g")
      .attr("class", "row");

    row
      .selectAll(".square")
      .data(d => d)
      .enter()
      .append("rect")
      .attr("class", "square")
      .attr("x", d => d.x)
      .attr("y", d => d.y)
      .attr("width", d => d.width)
      .attr("height", d => d.height)
      .style("fill", "#fff")
      .style("stroke", "#222");

    grid
      .append("rect")
      .attr("class", "crack")
      .attr("x", this.state.crackX)
      .attr("y", this.state.crackY)
      .attr("width", this.state.crackWidth)
      .attr("height", this.state.crackHeight)
      .style("fill", "green");
  }
  render() {
    return <div id="grid" />;
  }
}

CrackMap.propTypes = {
  width: PropTypes.number.isRequired,
  height: PropTypes.number.isRequired,
  crackSquare: PropTypes.string.isRequired,
  crackLX: PropTypes.number.isRequired,
  crackLY: PropTypes.number.isRequired,
  crackRX: PropTypes.number.isRequired,
  crackRY: PropTypes.number,
}
