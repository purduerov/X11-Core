import React, { Component } from 'react';
import styles from './SliderControl.css';


export default class SliderControl extends Component {
    constructor(props) {
        super(props);
        this.state = { val: props.power, inv: props.invert };

        this.onChangeCheck = this.onChangeCheck.bind(this);
        this.onChangeVal = this.onChangeVal.bind(this);
    }

    onChangeCheck(e) {
        const valcpy = this.state.val;
        this.setState({ inv: (e.target.checked - 0.5) * -2, val: valcpy }, function () {
            this.props.rend(this.state.val, this.state.inv, this.props.indx);
            // console.log(this.state.inv);
        });
    }

    onChangeVal(e) {
        const invcpy = this.state.inv;
        this.setState({ inv: invcpy, val: Number(e.target.value) }, function () {
            this.props.rend(Number(this.state.val), Number(this.state.inv), this.props.indx);
            // console.log(this.state.val);
        });
    }

    render() {
        return (
            <div className={styles.container}>
                <div className={styles.killPad}>
                    <p className={styles.fill}>
                        {this.props.name}
:
                    </p>
                    {this.state.val != undefined
                && (
                    <p className={styles.left}>
                        {this.props.power}
%
                    </p>
                )}
                    {this.state.inv != undefined
                && (
                    <p className={styles.right}>
                        <input type="checkbox" defaultChecked={this.props.invert === -1} onClick={this.onChangeCheck} />
                        <label>Invert</label>
                    </p>
                )}
                </div>
                {this.state.val != undefined
            && <input className="hugtop" type="range" min={this.props.min} max={this.props.max} value={this.state.val} onChange={this.onChangeVal} />}
            </div>
        );
    }
}
