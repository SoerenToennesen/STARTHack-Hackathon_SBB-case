import React, { Component } from 'react';
import DirectionsCarIcon from '@material-ui/icons/DirectionsCar';

export default class EasyRequest extends Component {
    render() {
        const cars = this.props.cars.map((car) => {
                if (car < this.props.rating) {
                    return <DirectionsCarIcon id={car} style={{'color':'black'}}/>
                } else {
                    return <DirectionsCarIcon id={car} style={{'color':'grey'}}/>
                }
            }   
        )

        return (
            <div>
                { cars }    
            </div>
        );
    }
}