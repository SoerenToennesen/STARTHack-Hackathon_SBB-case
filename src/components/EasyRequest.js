import React, { Component } from 'react';

import DirectionsCarIcon from '@material-ui/icons/DirectionsCar';
import Typography from '@material-ui/core/Typography';
import HelpOutlineRoundedIcon from '@material-ui/icons/HelpOutlineRounded';
import Dialog from '@material-ui/core/Dialog';
import DialogContent from '@material-ui/core/DialogContent';
import DialogContentText from '@material-ui/core/DialogContentText';
import DialogTitle from '@material-ui/core/DialogTitle';
import DialogActions from '@material-ui/core/DialogActions';
import Button from '@material-ui/core/Button';

export default class EasyRequest extends Component {
    constructor(props) {
        super(props);

        this.handleClose = this.handleClose.bind(this);
        this.handleInfo = this.handleInfo.bind(this);

        this.state = {
            rating: [],
            info: false
        }
    }

    componentDidMount() {
        var arr = [];
        for(let i = 0; i < 5; i++) {
            if (i < this.props.forecast) {
                arr.push(true)
            } else {
                arr.push(false)
            }
        }
        this.setState({rating: arr})
    }

    handleInfo() {
        this.setState({info: true})
    }

    handleClose() {
        this.setState({info: false})
    }

    render() {
        const cars = this.state.rating.map((bool) => {
                if (bool) {
                    return <DirectionsCarIcon style={{'color':'black'}}/>
                } else {
                    return <DirectionsCarIcon style={{'color':'grey'}}/>
                }
            }
        );

        return (
            <div>
                <Typography variant="h6" component="h3">
                    Current Status <Button onClick={this.handleInfo}><HelpOutlineRoundedIcon/> </Button>
                </Typography>
                { cars }
                {this.state.info &&
                    <Dialog onClose={this.handleClose} open={this.state.info}> 
                         <DialogTitle>Information</DialogTitle>
                    <DialogContent>
                      <DialogContentText>
                      Current status shows how full your selected parking area is.
                      </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Close
                        </Button>
                    </DialogActions>
                    </Dialog>
                }
            </div>
        );
    }
}