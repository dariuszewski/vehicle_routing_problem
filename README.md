This repository implements metaheuristic solution to the 
vehicle routing problem using simmulated anneling algorithm.

## Input data 
Project defines cites that have to be visited by algorithm in the `/data` directory. `orders_with_depots.csv` file contains list of the cities in the given format: 
| city | order | latitude | longitude | isDepot |
|------|-------|----------|-----------|---------|
| Kraków  | 0   |    50.0619474   | 19.9368564 | True |

where `orders` is the integer value between 0 (should be set for the depot) and 500.

## Usage
Example could be found in `notebook.ipynb`. In a nutshell:
1. Create city list using `CityList.from_csv("./data/<desired_file>.csv")`
2. Create fleet using `Fleet` object.
3. Create instance of `SimulatedAnnealing` class then run `optimzie()`

### Algorithm parameters

- fleet - fleet of vehicles to be used for this problem
- initial_temp - initial temperature for annealing process
- epochs - number of epochs for annealing process
- attempts - number of batches in epoch
- cooling_rate - cooling rate for annealing proccess between 0 and 1
- annealing_method - function for finding next city one of `random`, `nearest_neighbor` or `city_swap`


## Development
Setup virtual environment for the project
```
$ pip install virtualenv
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirments.txt
```
Run unit tests with: `pytest tests/`  
Run code formatter with: `black .`
