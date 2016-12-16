# schelling-simulation

## Description
A simulation of the Schelling Model of Segregation. 

In the model, agents of several types are allocated on a 2D square grid. The agents decide whether they are satisfied with their location based on the other agents in their neighbourhood. If they are not satisfied, they attempt to move to a vacancy of higher utility.

## Usage
### Setup
Install:

```
$ python setup.py install
```

### Command Line Interface


```
Usage: schelling-cli [OPTIONS]

  Command line interface for the Schelling simulation.

Options:
  -s, --grid-size INTEGER         Simulation grid size (grid is square with
                                  specified side). Default = 30.
  -v, --vacancy-proportion FLOAT  Proportion of vacant spots in grid. Default
                                  = 0.2
  -a, --agent-proportion FLOAT    Proportion of agents. Specify multiple for
                                  up 8 agent types (must sum up to 1). Default
                                  = 0.5 0.5
  --initial-random-allocation / --initial-segregated-allocation
                                  Random or segregated initial agent
                                  allocation. Default is random
  -u, --utility-function <CHOICE FLOAT>...
                                  Utility function name and parameter.
                                  Functions are: "flat", "peaked",
                                  "peaked_cutoff", "spiked". E. g. *-u flat
                                  0.5* for flat utility with threshold 0.5.
                                  Default = flat 0.625.
  --satisficers / --no-satisficers
                                  Satisficer relocation regime. Agents can
                                  move to vacancies of equal utility instead
                                  of only moving to vacancies of greater
                                  utility. Off by default.
  --agent-picking-regime [random|first|roulette]
                                  Agent picking regime. Agents to relocate are
                                  picked according to the specified
                                  regime.Available regimes are: "random" -
                                  agents picked randomly, "first" - first
                                  agent on list picked"roulette" - agents
                                  picked according to roulette algorithm, in
                                  which each agent is picked with a
                                  probability proportional to its weight The
                                  weight of each agent is given by: w = 1 -
                                  utility + base-weight; requires the
                                  --roulette-base-weight optionDefault is
                                  random
  --vacancy-picking-regime [random|first|roulette]
                                  Vacancy picking regime. Vacancies to
                                  relocate to are picked according to the
                                  specified regime.Available regimes are:
                                  "random" - vacancies picked randomly,
                                  "first" - first vacancy on list
                                  picked"roulette" - vacancies picked
                                  according to roulette algorithm, in which
                                  each vacancy is picked with a probability
                                  proportional to its weightThe weight of each
                                  vacancy is given by: w = 1 - utility + base-
                                  weight; requires the --roulette-base-weight
                                  option. Agents only pick from better or
                                  equal vacanciesDefault is random
  --agent-roulette-base-weight FLOAT
                                  The base weight used with roulette
                                  algorithm. The satisficers option must be
                                  set for values over 0 to have an
                                  effect.Default is 0.0
  --vacancy-roulette-base-weight FLOAT
                                  The base weight used with roulette
                                  algorithm. Default is 0.0
  -r, --radius INTEGER            Radius of neighborhood that agents will
                                  consider. Default = 1 (only directly
                                  adjacent neighbors).
  --count-vacancies               Specifies, if vacancies should be counted as
                                  neighbors, when calculating the fraction of
                                  unlike neighbors.
  -i, --iterations INTEGER        Number of iterations. One agent moves during
                                  an iteration. Default = 10000
  --save-to PATH                  Directory to save simulation output. Default
                                  = ../out
  --save-period INTEGER RANGE     Save output array image every given number
                                  of iterations. If -v, also print status to
                                  console. Default = 100
  -v, --verbose                   Periodically print iteration number and
                                  segregation measures to console. Off by
                                  default.
  --help                          Show this message and exit.
```


### Example Code

```python
"""
This will run the Schelling Model simulation for 10000 iterations.
Every 100 iterations the state will be printed to console  and the array 
will be saved as an image.
The simulation result, containing segregation measures for each iteration
will be saved as JSON and a plot will be shown.
"""
from schelling.simulation import run_simulation, get_save_state_callback
from schelling.utility_functions import create_flat_utility
from schelling.arr_to_img import image_save, to_image
from schelling.simulation_settings import SimulationSettings
import os

settings = SimulationSettings(
    grid_size=40,
    vacancy_proportion=0.2,
    agent_proportions=(0.5, 0.5),
    utility_function=create_flat_utility(5/8),
    iterations=10000
  )

save_period = 100

# assuming ./image/ directory exists
save_callback = get_save_state_callback('./image/', save_period, 
  settings.iterations, verbose=True)

simulation_result = run_simulation(settings, callback=save_callback)
simulation_result.save_JSON('result.json')
simulation_result.plot_measures()
```