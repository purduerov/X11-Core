import React, { Component } from 'react';
import styles from './CameraScreen.css';
// import PropTypes from 'prop-types';

export default class CameraScreen extends Component {
    constructor(props) {
        super(props);

        /* https://reactjs.org/docs/typechecking-with-proptypes.html
        this.propTypes = {
            next: PropTypes.number,
            prev: PropTypes.number,
        };
        */

        this.state = {
            name: '',
            sub: 'Name',
            pxybypass: false,
            pakconf: {},
            numcams: 2, // Hardcoded number of accessable cams. For future growth use pakfornt api
            camscreens: [
                0,
                1,
            ],
            camnames: [
                'Cam1',
                'Cam2',
                'Cam3',
                'Cam4',
                'Cam5',
            ],
            stream: {
                ip: '10.42.0.204',
                query: '/?action=stream',
                rovip: 'raspberrypi.local',
            },
            camnext: props.next,
            camprev: props.prev,
            prevcamnext: 0,
            prevcamprev: 0,
        };
        this.getconf();
    }

    getconf() {
        var res = null;
        var bypass = this.state.pxybypass;
        if (!bypass) {
            res = fetch('http://localhost:1905')
                .then(response => response.json())
                .then((results) => {
                    this.setState({
                        pakconf: results,
                    });
                });
        }

        return res;
    }

    handleClick(screennum, camnum) {
        const camscreens = this.state.camscreens.slice();
        camscreens[screennum] = camnum;
        this.setState({
            camscreens,
        });
    }

    camUpdate(screennum, newName) {
        const camnames = this.state.camnames.slice();
        camnames[this.state.camscreens[screennum]] = newName;
        this.setState({
            camnames,
        });
    }

    checkPrevPress() {
        if (this.state.camnext === 1 && this.state.prevcamnext === 0) {
            return true;
        }
        this.state.prevcamnext = this.state.camnext;
        return false;
    }

    checkNextPress() {
        if (this.state.camprev === 1 && this.state.prevcamprev === 0) {
            return true;
        }
        this.state.prevcamprev = this.state.camprev;
        return false;
    }

    renderCamSel(screennum) {
        return (
            <div>
                <input
                    type="text"
                    value={this.state.name}
                    onChange={e => this.setState({ name: e.target.value }) }
                />
                <input
                    type="submit"
                    value={this.state.sub}
                    onClick={() => this.camUpdate(screennum, this.state.name)}
                />
            </div>);
    }

    renderStream(strnum) {
        var camnum = this.state.camscreens[strnum];
        var IP;

        if (this.checkPrevPress()) {
            const camscreens = this.state.camscreens.slice();
            camscreens[strnum] -= 1;
            if (camscreens[strnum] === -1) {
                camscreens[strnum] = this.state.numcams;
            }
            this.setState({
                camscreens,
            });
        }
        if (this.checkNextPress()) {
            const camscreens = this.state.camscreens.slice();
            camscreens[strnum] = (camscreens[strnum] + 1) % this.state.numcams;
            this.setState({
                camscreens,
            });
        }

        if (camnum >= this.state.numcams) {
            camnum = 0;
        }
        let port;
        let query = '';
        if (typeof this.state.pakconf.socketio !== 'undefined') {
            switch (camnum) {
            case 0:
                port = this.state.pakconf.camnum0.stream;
                break;
            case 1:
                port = this.state.pakconf.camnum1.stream;
                break;
            case 2:
                port = this.state.pakconf.camnum2.stream;
                break;
            case 3:
                port = this.state.pakconf.camnum3.stream;
                break;
            case 4:
                port = this.state.pakconf.camnum4.stream;
                break;
            default:
                port = this.state.pakconf.camnum0.stream;
            }
        } else {
            port = 8000;
        }

        if (this.state.pxybypass) {
            port = 8080;
            query = this.state.stream.query + this.state.camscreens[strnum];
            IP = this.state.stream.rovip;
        } else {
            IP = this.state.stream.ip;
        }
        const url = `http://10.42.0.204:8080/?action=stream`// `http://${IP}:${port}${query}`;
        return <img src={url} width="100%" alt="Camera Stream Window wannabe" />;
    }

    renderSquare(screennum, camnum) {
        return (
            <button
                className={styles.butt}
                onClick={() => this.handleClick(screennum, camnum)}
                type="submit"
            >
                {this.state.camnames[camnum]}
            </button>
        );
    }

    render() {
        return (
            <div className={styles.container}>
                <header className={styles.header}>
                    <div className={styles.whiteText}>
                        Screen1:
                        {this.renderCamSel(0)}
                    </div>
                </header>
                <div className={styles.contentBox}>
                    <div className={styles.column2}>
                        {this.renderStream(0)}
                    </div>
                    <div className={styles.column1}>
                        {this.renderSquare(0, 0)}
                        {this.renderSquare(0, 1)}
                        {this.renderSquare(0, 2)}
                        {this.renderSquare(0, 3)}
                        {this.renderSquare(0, 4)}
                    </div>
                </div>
            </div>
        );
    }
}
