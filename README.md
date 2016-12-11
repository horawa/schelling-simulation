# schelling-simulation

## Description
A simulation of the Schelling Model of Segregation. 

In the model, agents of several types are allocated on a 2D square grid. The agents decide whether they are satisfied with their location based on the other agents in their neighbourhood. If they are not satisfied, they attempt to move to a vacancy of higher utility.

## Usage
### Setup
Install dependencies:

```
$ pip3 install -r requirements.txt
```

### Command Line Interface


```
Usage: python3 -m schelling.cli [OPTIONS]

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
                                  Satisficer relocation regime. Agents move to
                                  vacancies of equal utility instead of only
                                  moving to vacancies of greater utility. Off
                                  by default.
  --pick-random / --pick-first    Relocation regime - agent to relocate picked
                                  at random, or first on list. Random by
                                  default.
  --move-to-random / --move-to-first
                                  Relocation regime - agents move to random
                                  better vacancy, or to first better vacancy.
                                  Random by default.
  -r, --radius INTEGER            Radius of neighborhood that agents will
                                  consider. Default = 1 (only directly
                                  adjacent neighbors).
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

  def save(array, result, iteration):
    if iteration%save_period == 0:
      # print status to console
      print(iteration)
      print(result)

      # save output image (assuming ./image/ exists and is a directory)
      output_file = os.path.join('./image/', 
        str(iteration).zfill(4)+'.png')
      image_save(to_image(array), output_file)

  simulation_result = run_simulation(settings, callback=save)
  simulation_result.save_JSON('result.json')
  simulation_result.plot_measures()
```