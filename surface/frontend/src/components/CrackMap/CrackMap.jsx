import React, { Component } from "react";
import * as d3 from "d3";

export default class CrackMap extends Component {
  constructor(props) {
    super(props);
  }
  componentDidMount() {
    function gridData() {
      var data = new Array();
      var xpos = 1;
      var ypos = 1;
      var width = 100;
      var height = 100;
      var click = 0;
      
      for (var row = 0; row < 3; row++) {
        data.push( new Array() );
        
        for (var column = 0; column < 4; column++) {
          data[row].push({
            x: xpos,
            y: ypos,
            width: width,
            height: height,
            click: click
          })
          xpos += width;
        }
        xpos = 1;
        ypos += height;	
      }
      return data;
    }
    
    var griddata = gridData();
    console.log(griddata);
    
    var grid = d3.select("#grid")
      .append("svg")
      .attr("width","510px")
      .attr("height","510px");
      
    var row = grid.selectAll(".row")
      .data(griddata)
      .enter().append("g")
      .attr("class", "row");
      
    var column = row.selectAll(".square")
      .data(function(d) { return d; })
      .enter().append("rect")
      .attr("class","square")
      .attr("x", function(d) { return d.x; })
      .attr("y", function(d) { return d.y; })
      .attr("width", function(d) { return d.width; })
      .attr("height", function(d) { return d.height; })
      .style("fill", "#fff")
      .style("stroke", "#222");
  }
  render() {
    return <div id="grid"></div>;
  }
}
