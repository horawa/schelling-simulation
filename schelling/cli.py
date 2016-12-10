from .simulation import run_simulation
from .simulation_settings import SimulationsSettings
import schelling.utility_functions as ut
from .arr_to_img import to_image, imsave

import click
import os
from math import log10

_utility_function_creators = {
		'flat': ut.create_flat_utility,
		'peaked': ut.create_peaked_utility,
		'peaked_cutoff': lambda peak: ut.create_peaked_utility(peak, cutoff=True),
		'spiked': ut.create_spiked_utility,
	}

@click.command()
@click.option('--grid-size', '-s', default=10,
	help='Simulation grid size (grid is square with specified side)')
@click.option('--vacancy-proportion', '-v', default=0.2,
	help='Proportion of vacant spots in grid')
@click.option('--agent-proportion', '-a', multiple=True, type=float,
	help='Proportion of agents. Specify multiple for up 8 agent types (must sum up to 1)')
@click.option('--initial-random-allocation/--initial-segregated-allocation', default=True,
	help='Random or segregated initial agent allocation')
@click.option('--utility-function', '-u', type=(click.Choice(_utility_function_creators.keys()), float), default=('flat', 5/8),
	help='Utility function name and parameter. E. g. *flat 0.5* for flat utility with threshold 0.5')
@click.option('--satisficers/--no-satisficers', default=False,
	help='Satisficer relocation regime. Agents move to vacancies of equal utility instead of only moving to vacancies of greater utility')
@click.option('--move-to-random/--move-to-first', default=True,
	help='Relocation regime - agents move to random better vacancy or to first better vacancy. Random by default.')
@click.option('--iterations', '-i', default=10000,
	help='Number of iterations. One agent moves during an iteration')
@click.option('--save-to', type=click.Path(dir_okay=True),
	help='Directory to save simulation output')
@click.option('--save-period', type=click.IntRange(0, None), default=100)
def simulation(grid_size, vacancy_proportion, agent_proportion, initial_random_allocation,
	utility_function, satisficers, move_to_random, iterations, save_to, save_period):
	
	print(locals())

	ut_name = utility_function[0]
	ut_arg = utility_function[1]

	create_utility = _utility_function_creators[ut_name]

	utility = create_utility(ut_arg)

	settings = SimulationsSettings(
			grid_size=grid_size,
			vacancy_proportion=vacancy_proportion,
			agent_proportions=agent_proportion,
			initial_random_allocation=initial_random_allocation,
			utility_function=utility,
			satisficers=satisficers,
			move_to_random=move_to_random,
			iterations=iterations
		)

	if save_to is not None:
		order_of_magnitude = int(log10(iterations))
		def save_state(array, iteration):
			if iteration % save_period == 0:
				file_name = str(iteration).zfill(order_of_magnitude) + '.png'
				imsave(arr_to_img(array), os.path.join(save_to, filename))
		callback = save_state
	else:
		callback = lambda array, iteration: None

	run_simulation(settings, callback)

if __name__ == '__main__':
	simulation()
