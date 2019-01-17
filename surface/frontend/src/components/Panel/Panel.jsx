import React from 'react';
import { MDBContainer, Row, Col, Navbar, NavbarBrand, Card, CardBody, CardImage, CardTitle, CardText, small } from 'mdbreact';

export default class Panel extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
      <Card className="my-2">
        <CardBody className="elegant-color white-text rounded-bottom">
          <h6>{this.props.title}</h6>
          {this.props.children}
        </CardBody>

      </Card>
    )
  }
}