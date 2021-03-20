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

        this.state = {
            items: [],
            date: '',
            time: '', 
            selected: {station: '', date: ''},
            submitted: false,
            sampleData: [
                {
                    station: 'Burgdorf',
                    name: '05:00',
                    value: "0"
                },
                {
                    station: 'Burgdorf',
                    name: '06:00',
                    value: "1"
                },
                {
                    station: 'Burgdorf',
                    name: '07:00',
                    value: "2"
                },
                {
                    station: 'Burgdorf',
                    name: '08:00',
                    value: "4"
                },
                {
                    station: 'Burgdorf',
                    name: '09:00',
                    value: "4"
                },
                {
                    station: 'Burgdorf',
                    name: '10:00',
                    value: "4"
                },
                {
                    station: 'Burgdorf',
                    name: '11:00',
                    value: "3"
                },
                {
                    station: 'Burgdorf',
                    name: '12:00',
                    value: "2"
                },
                {
                    station: 'Burgdorf',
                    name: '13:00',
                    value: "3"
                },
                {
                    station: 'Burgdorf',
                    name: '14:00',
                    value: "3"
                }
            ]
        }
    }

    componentWillMount() {
        // Fetch names of stations.
        fetch('https://data.sbb.ch/api/records/1.0/search/?dataset=mobilitat&q=&facet=stationsbezeichnung')
        .then(res => res.json())
        .then(data => this.setState({ items: data.facet_groups[0].facets }))

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
        }
    }

    handleChange(option) {
        this.setState({selected: {station: option.name}})
    }

    handleDelete() {
        this.setState({submitted: false})
    };

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
                    onChange={(event, value) => this.handleChange(value)}
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
                        <EasyRequest forecast='3'/>
                      </ListItem>
                      <Divider style={{'margin': '0px 50px 0px 50px'}}/>
                      <ListItem style={{'margin': '0px 5px 0px 50px'}}>
                        <Day data={this.state.sampleData}/>
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