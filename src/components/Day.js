import React, { Component } from 'react';
import { AreaChart, Area,  XAxis, YAxis } from 'recharts';

export default class Day extends Component {
    render() {
        return (
            <div style={{'margin':'20px 0px 0px'}}>
                <AreaChart width={580} height={200} data={this.props.data}>
                  <Area type="monotone" dataKey="value" stroke="#555555" fill="#ececec" />
                  <XAxis dataKey="name" />
                  <YAxis />
                </AreaChart>
            </div>
        );
    }
}