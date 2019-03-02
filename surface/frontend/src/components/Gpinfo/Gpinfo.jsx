import React, { Component } from 'react';
import styles from './Gpinfo.css';

export default class Gpinfo extends Component {
    constructor(props) {
        super(props);

        this.renderReady = this.renderReady.bind(this);
    }

    renderReady() {
        if (this.props.gp.ready === true) {
            return (
                <div>
                    <div>
                        <ul className={styles.ButtonNames}>
                            <li>
a:
                                {this.props.gp.buttons.a.curVal}
                            </li>
                            <li>
b:
                                {this.props.gp.buttons.b.curVal}
                            </li>
                            <li>
x:
                                {this.props.gp.buttons.x.curVal}
                            </li>
                            <li>
y:
                                {this.props.gp.buttons.y.curVal}
                            </li>
                            <li>
lb:
                                {this.props.gp.buttons.lb.curVal}
                            </li>
                            <li>
rb:
                                {this.props.gp.buttons.rb.curVal}
                            </li>
                            <li>
select:
                                {this.props.gp.buttons.select.curVal}
                            </li>
                            <li>
start:
                                {this.props.gp.buttons.start.curVal}
                            </li>
                            <li>
lpress:
                                {this.props.gp.buttons.lpress.curVal}
                            </li>
                            <li>
rpress:
                                {this.props.gp.buttons.rpress.curVal}
                            </li>
                            <li>
up:
                                {this.props.gp.buttons.up.curVal}
                            </li>
                            <li>
down:
                                {this.props.gp.buttons.down.curVal}
                            </li>
                            <li>
left:
                                {this.props.gp.buttons.left.curVal}
                            </li>
                            <li>
right:
                                {this.props.gp.buttons.right.curVal}
                            </li>
                        </ul>
                    </div>
                    <div>
                        <ul className={styles.AxisNames}>
                            <li>
LstickXaxis:
                                {this.props.gp.axes.LstickXaxis.curVal}
                            </li>
                            <li>
LstickYaxis:
                                {this.props.gp.axes.LstickYaxis.curVal}
                            </li>
                            <li>
RstickXaxis:
                                {this.props.gp.axes.RstickXaxis.curVal}
                            </li>
                            <li>
RstickYaxis:
                                {this.props.gp.axes.RstickYaxis.curVal}
                            </li>
                            <li>
Ltrigger:
                                {this.props.gp.axes.Ltrigger.curVal}
                            </li>
                            <li>
Rtrigger:
                                {this.props.gp.axes.Rtrigger.curVal}
                            </li>
                        </ul>
                    </div>
                    <div>
                        <ul>
                            <li>
upchk:
                                {this.props.gp.up}
                            </li>
                            <li>
dwnchk:
                                {this.props.gp.down}
                            </li>
                        </ul>
                    </div>
                </div>
            );
        }
        return (
            <div className={styles.NOTREADY}>"GP is not mapped"</div>
        );
    }

    render() {
        return (
            <div container={styles.container}>
                <h1>Gamepad</h1>
                <hr />
                <div className={styles.Gamepad}>
                    {this.renderReady()}
                </div>
            </div>
        );
    }
}
