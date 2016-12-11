from .simulation import run_simulation
from .simulation_settings import SimulationsSettings
import schelling.utility_functions as ut
from .arr_to_img import to_image, image_save

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
@click.option('--grid-size', '-s', default=30,
	help='Simulation grid size (grid is square with specified side). Default = 30.')
@click.option('--vacancy-proportion', '-v', default=0.2,
	help='Proportion of vacant spots in grid. Default = 0.2')
@click.option('--agent-proportion', '-a', multiple=True, type=float, default=(0.5, 0.5),
	help='Proportion of agents. Specify multiple for up 8 agent types (must sum up to 1) Default = 0.5 0.5')
@click.option('--initial-random-allocation/--initial-segregated-allocation', default=True,
	help='Random or segregated initial agent allocation. Default is random')
@click.option('--utility-function', '-u', type=(click.Choice(_utility_function_creators.keys()), float), default=('flat', 5/8),
	help='Utility function name and parameter. Functions are: "flat", "peaked", "peaked_cutoff", "spiked". E. g. *-u flat 0.5* for flat utility with threshold 0.5. Default = flat 0.625.')
@click.option('--satisficers/--no-satisficers', default=False,
	help='Satisficer relocation regime. Agents move to vacancies of equal utility instead of only moving to vacancies of greater utility. Off by default.')
@click.option('--move-to-random/--move-to-first', default=True,
	help='Relocation regime - agents move to random better vacancy or to first better vacancy. Random by default.')
@click.option('--radius', '-r', default=1,
	help='Radius of neighborhood that agents will consider. Default = 1 (only directly adjacent neighbors).')
@click.option('--iterations', '-i', default=10000,
	help='Number of iterations. One agent moves during an iteration. Default = 10000')
@click.option('--save-to', type=click.Path(dir_okay=True), default='./out',
	help='Directory to save simulation output. Default = ./out')
@click.option('--save-period', type=click.IntRange(0, None), default=100,
	help='Save output array image every given number of iterations. If -v, also print status to console. Default = 100')
@click.option('--verbose', '-v', is_flag=True, default=False,
	help='Periodically print iteration number and segregation measures to console. Off by default.')
def simulation(grid_size, vacancy_proportion, agent_proportion, initial_random_allocation,
	utility_function, satisficers, move_to_random, radius, iterations, save_to, save_period, verbose):

	ut_name = utility_function[0]
	ut_arg = utility_function[1]

	create_utility = _utility_function_creators[ut_name]

	utility = create_utility(ut_arg)

	settings = SimulationSettings(
			grid_size=grid_size,
			vacancy_proportion=vacancy_proportion,
			agent_proportions=agent_proportion,
			initial_random_allocation=initial_random_allocation,
			utility_function=utility,
			satisficers=satisficers,
			move_to_random=move_to_random,
			iterations=iterations
		)


	if os.path.exists(save_to):
		if not os.path.isdir(save_to):
			print("Not a directory: " + save_to)
			exit(1)
	else:
		os.mkdir(save_to)


	order_of_magnitude = int(log10(iterations))
	def save_state(array, result, iteration):
		if iteration % save_period == 0:
			file_name = str(iteration).zfill(order_of_magnitude) + '.png'
			image_save(to_image(array), os.path.join(save_to, file_name))
			if verbose:
				print(iteration)
				print(result)

	
	result = run_simulation(settings, save_state)

	result.save_JSON(os.path.join(save_to, 'result.json'))


if __name__ == '__main__':
	simulation()
