import React, { Component } from 'react';

import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Grid from '@material-ui/core/Grid';
import Button from '@material-ui/core/Button';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';
import Divider from '@material-ui/core/Divider';
import Chip from '@material-ui/core/Chip';
import ListItem from '@material-ui/core/ListItem';
import List from '@material-ui/core/List';

import Day from './Day';
import EasyRequest from './EasyRequest';

export default class Application extends Component {
    constructor(props) {
        super(props);

        this.handleChange = this.handleChange.bind(this);
        this.handleDelete = this.handleDelete.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleDateChange = this.handleDateChange.bind(this);
        this.handleTimeChange = this.handleTimeChange.bind(this);
        this.randomData = this.randomData.bind(this);

        this.state = {
            items: [],
            date: '',
            time: '', 
            timeInt: 0,
            selected: {station: '', date: ''},
            submitted: false,
            persent: '',
            data: []
        }
    }

    componentWillMount() {
        // Fetch names of stations.
        fetch('https://data.sbb.ch/api/records/1.0/search/?dataset=mobilitat&q=&facet=stationsbezeichnung')
        .then(res => res.json())
        .then(data => this.setState({ items: data.facet_groups[0].facets }))

        this.randomData()

        // Get current date and time.
        let currentDate = new Date();
        let month = currentDate.getMonth();
        if (month <= 9) {
            month = '0'+month
        }
        let hour = currentDate.getHours();
        if (hour <= 9) {
            hour = '0'+hour
        }
        let minutes = currentDate.getMinutes();
        if (minutes <= 9) {
            minutes = '0'+minutes
        }
        let day = currentDate.getDate();
        if (day <= 9) {
            day = '0'+day
        }

        this.setState({date: currentDate.getFullYear()+'-'+month+'-'+day, 
                       time: hour+':'+minutes})
    }

    handleSubmit() {
        if (this.state.selected.station !== '') {
            this.setState({submitted: true})
            this.randomData()
        }
    }

    handleChange(option) {
        this.setState({selected: {station: option.name}})
    }

    handleDelete() {
        this.setState({submitted: false})
    };

    handleDateChange(event) {
        this.setState({date: event.target.value})
        this.randomData()
    };

    handleTimeChange(event) {
        this.setState({'timeInt': parseInt(event.target.value.substr(0,2),10)})
        this.setState({time: event.target.value})
    };

    randomData() {
        let sampleData = []
        for (let i = 0; i < 24; i++) {
            if (i < 5) {
                sampleData.push({'time': '0'+i+':00', 'occupancy': random(0, 0.2)})
            } else if (i === 23) {
                sampleData.push({'time': ''+i+':00', 'occupancy': random(0, 0.2)})
            } else if (i > 4 && i < 7) {
                sampleData.push({'time': '0'+i+':00', 'occupancy': random(0.2, 0.4)})
            } else if (i > 6 && i < 10) {
                sampleData.push({'time': '0'+i+':00', 'occupancy': random(0.4, 0.7)})
            } else if (i > 9 && i < 16) {
                sampleData.push({'time': ''+i+':00', 'occupancy': random(0.5, 1)})
            } else if (i > 15 && i < 20) {
                sampleData.push({'time': ''+i+':00', 'occupancy': random(0.3, 0.6)})
            } else if (i > 19 && i < 23) {
                sampleData.push({'time': ''+i+':00', 'occupancy': random(0.1, 0.3)})
            }
        }
        this.setState({'data': sampleData})
    }

    render() {
        return (
            <Card style={{
                'maxWidth': '800px',
                'minWidth': '600px',
                'margin': '50px auto 10px'
            }}>
            <CardContent>
            <Typography variant="h5" component="h2">
                Parking Lot Forecast
            </Typography>
            <Typography variant="body2" component="p">
                Choose the station and the time to get a forecast of our parking spaces at the train station
            </Typography>
            <Grid container spacing={2}>
                <Grid item xs={12}>
                <Autocomplete
                    id="stations"
                    options={this.state.items}
                    getOptionLabel={(option) => option.name}
                    renderInput={(params) => <TextField {...params} label="Choose a Station" variant="outlined" />}
                    style={{'margin': '20px auto 10px'}}
                    onChange={(event,value) => this.handleChange(value)}
                />
                </Grid>
                <Grid item xs={2}></Grid>
                <Grid item xs={3}>
                <form noValidate style={{'marginLeft':'20px'}}>
                    <TextField
                      id="date"
                      label="Date"
                      type="date"
                      defaultValue={this.state.date}
                      onChange={(event) => this.handleDateChange(event)}
                      InputLabelProps={{
                        shrink: true,
                      }}
                    />
                </form>
                </Grid>
                <Grid item xs={3}>
                <form noValidate>
                    <TextField
                    id="time"
                    label="Time"
                    type="time"
                    defaultValue={this.state.time}
                    onChange={(event) => this.handleTimeChange(event)}
                    InputLabelProps={{
                      shrink: true,
                    }}
                    inputProps={{
                      step: 6000 
                    }}
                  />
                </form>
                </Grid>
                <Grid item xs={1}>
                    <Button variant="contained" color="secondary" onClick={this.handleSubmit}>
                        Submit
                    </Button>
                </Grid>
                <Grid item xs={1}></Grid>
            </Grid>
            {(this.state.submitted && this.state.selected.station !== '') && 
                <div>
                    <Divider style={{'margin': '30px 30px auto'}}/>
                    <Typography variant="h5" component="h3" style={{'margin': '30px 30px auto'}}>
                        Parking Situation at    
                        <Chip label={this.state.selected.station} onDelete={this.handleDelete} style={{'margin': '10px'}}/>
                    </Typography>
                    <List >
                      <ListItem style={{'margin': '0px 5px 0px 50px'}}>
                        <EasyRequest forecast={this.state.data[this.state.timeInt].occupancy}/>
                      </ListItem>
                      <Divider style={{'margin': '0px 50px 0px 50px'}}/>
                        <Typography variant="h6" component="h3" style={{'margin': '30px 30px auto'}}>
                            Expected car traffic in percent on {this.state.date}
                        </Typography>
                      <ListItem style={{'margin': '0px 5px 0px 50px'}}>
                        <Day data={this.state.data}/>
                      </ListItem>
                      <Divider style={{'margin': '0px 50px 0px 50px'}}/>
                     </List>
                </div>
            }
            </CardContent>
            </Card>
        );
    }
}

function random(min, max) {
    return min + Math.random() * (max - min);
  }