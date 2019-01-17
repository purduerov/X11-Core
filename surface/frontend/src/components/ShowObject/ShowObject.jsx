import React, { Component } from 'react';
import styles from './ShowObject.css';



let that;

/*
    <SliderControl min='0' max='100' key={'thrust0'} indx={0} val={this.state.scales[0]} inv={this.state.inv[0]} rend={this.rendData.bind(this)} name={"Thruster 0"} />
*/

export default class ShowObject extends Component {
    constructor(props) {
        super(props);

        this.state = { obj: props.obj };

        this.rendObj = this.rendObj.bind(this);

        that = this;
    }

    rendChild(obj, parent_key) {
        return Object.keys(obj).map((val, index) => (
            <span key={`${parent_key}_${val}`} className={styles.center}>
                {index != 0 && <hr className={styles.squashed} />}
                <span className={styles.halfLeft}>
                    {val}
:
                </span>
                <span className={styles.halfRight}>{obj[val]}</span>
            </span>
        ));
    }

    rendObj() {
        return Object.keys(this.props.obj).map((val, index) => {
            if (typeof this.props.obj[val] === 'object') {
                return (
                    <div key={val} className={styles[val]}>
                        <div key={val} className={styles.openCenter}>
                            <center>{val}</center>
                            <hr className={styles.squashed} />
                            <div>
                                {this.rendChild(this.props.obj[val], val)}
                            </div>
                        </div>
                        <hr />
                    </div>
                );
            }
            var obj = {};
            obj[val] = this.props.obj[val];
            return (
                <div key={val} className={styles[val]}>
                    <div className={styles.openCenter}>
                        <ul>
                            {this.rendChild(obj, val)}
                        </ul>
                    </div>
                    <hr />
                </div>
            );
        });
    }

    render() {
        // console.log(this.props.obj)
        return (
            <div className={styles.container}>
                <div>
                    {this.rendObj()}
                </div>
            </div>
        );
    }
}
