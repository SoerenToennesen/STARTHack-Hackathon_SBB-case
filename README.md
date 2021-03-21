# STARTHack SBB case - Part-Time Hackers

As team Part-Time Hackers for the STARTHack hackathon, we've been assigned the case to work on the Swiss Federal Station, with regards to predicting parking occupancy for a given location and date(+time of day).

The GitHub for the case is provided here:
https://github.com/START-Global/SBB-STARTHACK21

The hackathon is provided here:
https://www.starthack.eu/

## How to run the code

Make sure both node.js, pip, python, npm is installed on your system.

In the project directory, you can run:

### `npm install`
For all the python modules used, run pip install (...), which are present in the algorithm.py file.
### `pip install (...)`


## What does the code entail

The code includes a frontend application developed with reactjs, which communicates with a backend developed in python. The communication uses flask. The frontend lets the user specify a location and time the user wishes to get information regarding parking avaliability, sends it to the backend, which retrieves data from appropriate SBB databases to parse historical data and algorithmically forecast future occupancy of a specified train station parking lot.

The backend entirely runs on algorithm.py.

An alternative solution and approach for saving data and using this formatted data is shown in start.py, which uses test.csv as the data format required.

## More info. and pitch
A video of our pitch can be found at:

https://www.youtube.com/watch?v=l4dAfJDMBnc&feature=emb_logo&ab_channel=MichelleLee

The finalized hand-in is found at:

https://app.hackjunction.com/projects/start-hack/view/6055b89a4aa8b7004355cab6

## Contributors

The authors and developers of this project are:

Michelle S. Lee

lions-code

Fuego

Søren Tønnesen

A special thanks to SBB for the case and STARTHack for the hackathon opportunity!