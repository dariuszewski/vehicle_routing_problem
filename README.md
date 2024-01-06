This repository implements metaheuristic solution to the 
vehicle routing problem using simmulated anneling and tabu search algorithm.

## Demo
https://github.com/dariuszewski/vehicle_routing_problem/blob/master/notebook.ipynb

## Input data 
Project defines cites that have to be visited by algorithm in the `/data` directory. `orders_with_depots.csv` file contains list of the cities in the given format: 
| city | order | latitude | longitude | isDepot |
|------|-------|----------|-----------|---------|
| Kraków  | 0   |    50.0619474   | 19.9368564 | True |

where `orders` cannot be larger than the maximal capacity.

## Usage
Example could be found in `notebook.ipynb`. In a nutshell:
1. Create a graph manager object using a file from `/data` directory. 
2. Create an instance of `SimulatedAnnealing` or `TabuSearch` class then 
3. Run `optimize()`
4. Optionally, turn the algorithm instance to a fleet with `Algorithm.to_fleet()` and generate a graphical depiction with `utils.generate_nx_graph()`

### Simulated Annealing parameters

- graph_manager - object which manages routes and solution
- initial_temp - initial temperature for annealing process
- epochs - number of epochs for annealing process
- attempts - number of batches in epoch
- cooling_rate - cooling rate for annealing proccess between 0 and 1

### Tabu Search parameters

- graph_manager - object which manages routes and solution
- max_iterations - iterations to run by the algorithm
- tabu_size - size of the tabu list

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
