import unittest
import math
import numpy as np

from schelling.simulation import (_get_unsatisfied_agent_indices, update_array,
	_pick_agent_index_to_move, _get_better_vacancies, run_simulation,
	_pick_better_vacancy_index, _move, _random_picker, _first_picker, 
	_create_roulette_picker)
import schelling.utility_functions as ut
from schelling.array_utils import get_agent_indices, get_vacancy_indices
from schelling.utility_functions import (get_utility_for_array, 
	create_flat_utility)
from schelling.simulation_settings import SimulationSettings
from schelling.simulation_result import SimulationResult

# TODO Refactor this abomination

class SimulationTestCase(unittest.TestCase):
	def setUp(self):
		self.test_array = np.array([
				[0, 1, 1, 0],
				[1, 1, 0, 1],
				[0, 2, 2, 0],
				[0, 1, 2, 0]
			])


	def test_get_unsatisfied_agent_indices(self):

		parameters = [
			(ut.create_flat_utility(0.5), [5, 6, 7]),
			(ut.create_peaked_utility(0.5), [0, 1, 2, 3, 5, 6, 7, 8]),
			(ut.create_spiked_utility(0.5), [0, 1, 2, 3, 5, 6, 7, 8]),
		]

		self.check_get_unsatisfied_agent_indices_expected_output(parameters, 
			False)


	def test_get_unsatisfied_agent_indices_satisficers(self):

		parameters = [
			(ut.create_flat_utility(0.5), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
			(ut.create_peaked_utility(0.5), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
			(ut.create_spiked_utility(0.5), [0, 1, 2, 3, 4, 5, 6, 7, 8]),
		]

		self.check_get_unsatisfied_agent_indices_expected_output(parameters, 
			True)


	def check_get_unsatisfied_agent_indices_expected_output(self, parameters, 
			satisficers):
		agent_indices = get_agent_indices(self.test_array)

		for utility_function, expected_output in parameters:
			utility = ut.get_utility_for_array(utility_function, 
				self.test_array)

			output = _get_unsatisfied_agent_indices(utility, agent_indices, 
				satisficers=satisficers)
			expected_output = agent_indices[np.array(expected_output)]
			with self.subTest(ut=utility_function, out=output, 
					expected=expected_output):
				self.assertTrue(np.array_equal(output, expected_output))


	def test_pick_agent_index_to_move(self):
		agent_indices = get_agent_indices(self.test_array)
		unsatisfied_agent_index_indices = [0, 1, 2, 3, 5, 6, 7, 8]
		unsatisfied_agent_indices = \
			agent_indices[unsatisfied_agent_index_indices]

		expected_agent_index = _first_picker(unsatisfied_agent_indices)		

		agent_index = _pick_agent_index_to_move(unsatisfied_agent_indices, 
			_first_picker)

		with self.subTest(out=agent_index, expected=expected_agent_index):
			self.assertEqual(expected_agent_index, agent_index)


	def test_get_better_vacancies(self):
		parameters = [
			(5, np.array([4, 5, 6])),
			(6, np.array([4, 5, 6])),
			(7, np.array([0, 1, 2, 3, 5]))
		]

		self.check_better_vacancy_expected_output(parameters, False)


	def test_get_better_vacancies_satisficers(self):

		parameters = [
			(0, np.array([0, 1, 2, 3, 5])),
			(1, np.array([0, 1, 2, 3, 5])),
			(2, np.array([0, 1, 2, 3, 5])),
			(3, np.array([0, 1, 2, 3, 5])),
			(5, np.array([4, 5, 6])),
			(6, np.array([4, 5, 6])),
			(7, np.array([0, 1, 2, 3, 5])),
			(8, np.array([4, 5, 6])),
		]

		self.check_better_vacancy_expected_output(parameters, True)


	def check_better_vacancy_expected_output(self, parameters, satisficers):
		utility = get_utility_for_array(create_flat_utility(0.5), 
			self.test_array)

		agent_indices = get_agent_indices(self.test_array)
		vacancy_indices = get_vacancy_indices(self.test_array)

		for unsatisfied_agent_index, expected_output_indices in parameters:
			expected_output = vacancy_indices[expected_output_indices]
			i = agent_indices[unsatisfied_agent_index]

			output = _get_better_vacancies(self.test_array, i, utility, 
				vacancy_indices, satisficers=satisficers)

			with self.subTest(i= unsatisfied_agent_index, out=output, 
					expected=expected_output):
				self.assertTrue(np.array_equal(output, expected_output))


	def test_pick_better_vacancy_index(self):
		parameters = [
			(5, np.array([4, 5, 6])),
			(6, np.array([4, 5, 6])),
			(7, np.array([0, 1, 2, 3, 5]))
		]

		vacancies = get_vacancy_indices(self.test_array)

		for agent_index, better_vacancy_indices in parameters:
			for chosen_vacancy_index in range(len(better_vacancy_indices)):
				def picker(array, i=None):
					return array[chosen_vacancy_index]

				better_vacancies = vacancies[better_vacancy_indices]

				output = _pick_better_vacancy_index(better_vacancies, picker)
				expected_output = better_vacancies[chosen_vacancy_index]
				
				with self.subTest(chosen_index=chosen_vacancy_index, 
						agent=agent_index,
						out=output, expected=expected_output):
					self.assertTrue(np.array_equal(output, expected_output))

		# Empty vacancy list
		with self.subTest(name="Empty vacancy list should return none."):
			output = _pick_better_vacancy_index(np.array([]), _first_picker)
			self.assertTrue(output is None)


	def test_move(self):
		parameters = [
			((0, 1), (0, 0), np.array([
					[1, 0, 1, 0],
					[1, 1, 0, 1],
					[0, 2, 2, 0],
					[0, 1, 2, 0]
				])),
			((2, 1), (0, 3), np.array([
					[0, 1, 1, 2],
					[1, 1, 0, 1],
					[0, 0, 2, 0],
					[0, 1, 2, 0]
				])),
			((1, 3), (2, 3), np.array([
					[0, 1, 1, 0],
					[1, 1, 0, 0],
					[0, 2, 2, 1],
					[0, 1, 2, 0]
				])),
		]

		for agent_index, vacancy_index, expected_result in parameters:
			array = np.copy(self.test_array)
			_move(array, agent_index, vacancy_index)
			with self.subTest():
				self.assertTrue(np.array_equal(array, expected_result))


	def test_random_picker(self):
		data = [
			(1, 2,), 
			(3, 4,), 
			(2, 3,),
			(4, 5,),
			(4, 5,),
			(6, 7,),
		]


		array = np.array(data)
		for i in range(20):
			picked = _random_picker(array)
			with self.subTest(data=data, picked=picked):
				self.assertTrue(picked in data)


	def test_first_picker(self):
		parameters = [
			[
				(1, 2,), 
				(3, 4,), 
				(2, 3,),
			],
			[
				(4, 5,),
				(4, 5,),
				(6, 7,),
			],
		]

		for data in parameters:
			array = np.array(data)
			picked = _first_picker(array)
			with self.subTest(data=data, picked=picked):
				self.assertEqual(picked, data[0])


	def test_roulette_picker_weight0(self):
		agent_indices = [
			(1, 2),
			(7, 8),
			(4, 5),
			(8, 9),
		]

		agent_indices_sorted = [
			(8, 9),
			(7, 8),
			(4, 5),
			(1, 2),
		]

		agent_utilities = [
			0.75, 0.25, 0.5, 0.1,
		]

		def utility(agent_index, agent_type=None):
			i = agent_indices.index(tuple(agent_index))
			return agent_utilities[i]

		agent_cum_weights = [0.9, 1.65, 2.15, 2.4]

		picked_values = np.arange(0, 2.6, 0.2)

		for picked_value in picked_values:
			def uniform_dist(hibound):
				return picked_value

			roulette_picker = _create_roulette_picker(0.0, utility, 
				for_agents=True, uniform_dist=uniform_dist)

			index = -1
			for i in range(len(agent_cum_weights)):
				if picked_value <= agent_cum_weights[i]:
					index = i
					break
			
			expected_output = agent_indices_sorted[index]
			output = roulette_picker(np.array(agent_indices))
			with self.subTest(picked_value=picked_value):
				self.assertEqual(output, expected_output)

	def test_roulette_picker_weight01(self):
		agent_indices = [
			(1, 2),
			(7, 8),
			(4, 5),
			(8, 9),
			(3, 4),
		]

		agent_indices_sorted = [
			(8, 9),
			(7, 8),
			(4, 5),
			(1, 2),
			(3, 4),
		]

		agent_utilities = [
			0.75, 0.25, 0.5, 0.1, 1.0,
		]

		def utility(agent_index, agent_type=None):
			i = agent_indices.index(tuple(agent_index))
			return agent_utilities[i]
		
		agent_cum_weights = [1.0, 1.85, 2.45, 2.8, 2.9]

		picked_values = np.arange(0, 3.0, 0.1)

		for picked_value in picked_values:
			def uniform_dist(hibound):
				return picked_value

			roulette_picker = _create_roulette_picker(0.1, utility, 
				for_agents=True, uniform_dist=uniform_dist)

			index = -1
			for i in range(len(agent_cum_weights)):
				if picked_value < agent_cum_weights[i] or math.isclose(
						picked_value,agent_cum_weights[i]):
					index = i
					break
			
			expected_output = agent_indices_sorted[index]
			output = roulette_picker(np.array(agent_indices))
			with self.subTest(picked_value=picked_value):
				self.assertEqual(output, expected_output)


	def test_run_simulation(self):
		iteration_states = [
			np.array([
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[2, 2, 2, 2],
				[3, 3, 3, 3]
			]),
			np.array([
				[1, 0, 0, 0],
				[0, 1, 1, 1],
				[2, 2, 2, 2],
				[3, 3, 3, 3]
			]),
			np.array([
				[1, 1, 0, 0],
				[0, 0, 1, 1],
				[2, 2, 2, 2],
				[3, 3, 3, 3]
			]),
			np.array([
				[1, 1, 1, 0],
				[0, 0, 0, 1],
				[2, 2, 2, 2],
				[3, 3, 3, 3]
			]),
			np.array([
				[1, 1, 1, 1],
				[0, 0, 0, 0],
				[2, 2, 2, 2],
				[3, 3, 3, 3]
			]),
		] + ([np.array([
				[1, 1, 1, 1],
				[2, 0, 0, 0],
				[0, 2, 2, 2],
				[3, 3, 3, 3]
			]),							
			np.array([
				[1, 1, 1, 1],
				[0, 2, 0, 0],
				[0, 2, 2, 2],
				[3, 3, 3, 3]
			])] * 100) # here it starts oscillating forever
		

		def callback(array, result, iteration):
			expected_output = iteration_states[iteration]
			with self.subTest(i=iteration, out=array, expected=expected_output):	
				self.assertTrue(np.array_equal(array, expected_output))


		settings = SimulationSettings(		
			grid_size=4,
			vacancy_proportion=0.25,
			agent_proportions=(1/3, 1/3, 1/3),
			initial_random_allocation=False,
			utility_function=create_flat_utility(0.5),
			satisficers=False,
			agent_picking_regime='first',
			vacancy_picking_regime='first',
			radius=1,
			iterations=len(iteration_states)
		)

		result = run_simulation(settings, callback)

		clusters = [3, 4, 4, 4, 3] + ([4, 3] * 100)
		with self.subTest():
			self.assertEqual(result.clusters, clusters)


	def test_simulation_halted(self):
		all_satisfied_array = np.array([
				[0, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 1, 1],
			])
		
		callback_count = [0]
		expected_callback_count = 1

		def callback(array, result, iteration):
			expected_output = all_satisfied_array
			with self.subTest():	
				self.assertTrue(np.array_equal(array, expected_output))
			callback_count[0] += 1

		settings = SimulationSettings(		
			grid_size=4,
			vacancy_proportion=0.5,
			agent_proportions=(1.0,),
			initial_random_allocation=False,
			utility_function=create_flat_utility(0.5),
			satisficers=False,
			agent_picking_regime='first',
			vacancy_picking_regime='first',
			radius=1,
			iterations=100
		)

		result = run_simulation(settings, callback)

		clusters = [1]
		with self.subTest():
			self.assertEqual(result.clusters, clusters)

		with self.subTest():
			self.assertEqual(callback_count[0], expected_callback_count)


	def test_simulation_satisficers(self):
		iteration_states = [
			np.array([
				[0, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 1, 1],
			]),
		] + ([	
			np.array([
				[1, 0, 0, 0],
				[0, 0, 0, 0],
				[0, 1, 1, 1],
				[1, 1, 1, 1],
			]),
			np.array([
				[0, 1, 0, 0],
				[0, 0, 0, 0],
				[0, 1, 1, 1],
				[1, 1, 1, 1],
			]),
		] * 100) # oscillates forever

		def callback(array, result, iteration):
			expected_output = iteration_states[iteration]
			with self.subTest(i=iteration, out=array, expected=expected_output):	
				self.assertTrue(np.array_equal(array, expected_output))


		settings = SimulationSettings(		
			grid_size=4,
			vacancy_proportion=0.5,
			agent_proportions=(1.0,),
			initial_random_allocation=False,
			utility_function=create_flat_utility(0.5),
			satisficers=True,
			agent_picking_regime='first',
			vacancy_picking_regime='first',
			radius=1,
			iterations=len(iteration_states)
		)

		result = run_simulation(settings, callback)

		clusters = [1] + ([2, 2] * 100)
		with self.subTest():
			self.assertEqual(result.clusters, clusters)	


	def test_run_simulation_vacancies_counted(self):
		iteration_states = [
			np.array([
				[0, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[2, 2, 2, 2],
			]),
			np.array([
				[2, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[0, 2, 2, 2],
			]),
			np.array([
				[2, 2, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[0, 0, 2, 2],
			]),
			np.array([
				[2, 2, 2, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[0, 0, 0, 2],
			]),
			np.array([
				[2, 2, 2, 2],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[0, 0, 0, 0],
			]),
			None
		] # simulation halted, should not fail at none

		def callback(array, result, iteration):
			expected_output = iteration_states[iteration]
			with self.subTest(i=iteration, out=array, expected=expected_output):	
				self.assertTrue(np.array_equal(array, expected_output))


		settings = SimulationSettings(		
			grid_size=4,
			vacancy_proportion=0.5,
			agent_proportions=(0.5, 0.5),
			initial_random_allocation=False,
			utility_function=create_flat_utility(0.5),
			satisficers=False,
			agent_picking_regime='first',
			vacancy_picking_regime='first',
			count_vacancies=True,
			radius=1,
			iterations=len(iteration_states)
		)

		result = run_simulation(settings, callback)

		clusters = [2, 3, 3, 3, 2]
		with self.subTest():
			self.assertEqual(result.clusters, clusters)


	def test_simulation_random_agent_picker(self):
		# initial_array = [
		# 	np.array([
		# 		[0, 0, 0, 0],
		# 		[0, 0, 0, 0],
		# 		[1, 1, 1, 1],
		# 		[1, 1, 2, 2]
		# 	]),
		# ]

		possible_states = [
			np.array([
				[1, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 0, 1],
				[1, 1, 2, 2]
			]),
			np.array([
				[1, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 0],
				[1, 1, 2, 2]
			]),
			np.array([
				[2, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 0, 2]
			]),
			np.array([
				[2, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 2, 0]
			]),
		]

		possible_states_reached = set()
		
		def callback(array, result, iteration):
			if iteration == 1:
				with self.subTest(out=np.copy(array)):
					is_possible_state = False
					for i, state in enumerate(possible_states):
						if np.array_equal(array, state):
							is_possible_state = True
							possible_states_reached.add(i)
							break
					self.assertTrue(is_possible_state)


		settings = SimulationSettings(		
			grid_size=4,
			vacancy_proportion=0.5,
			agent_proportions=(0.75, 0.25),
			initial_random_allocation=False,
			utility_function=create_flat_utility(3/8),
			satisficers=False,
			agent_picking_regime='random',
			vacancy_picking_regime='first',
			radius=1,
			iterations=2
		)

		# Assume all states should be reached in 30 tries
		for i in range(30):
			run_simulation(settings, callback)

		with self.subTest():
			self.assertEqual(len(possible_states_reached), len(possible_states))
			

	def test_simulation_random_vacancy_picker(self):
		# array = [
		# 	np.array([
		# 		[0, 0, 0, 0],
		# 		[1, 1, 1, 1],
		# 		[1, 1, 1, 1],
		# 		[1, 1, 2, 2]
		# 	]),
		# ]

		possible_states = [
			np.array([
				[1, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 0, 1],
				[1, 1, 2, 2]
			]),
			np.array([
				[0, 1, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 0, 1],
				[1, 1, 2, 2]
			]),
			np.array([
				[0, 0, 1, 0],
				[1, 1, 1, 1],
				[1, 1, 0, 1],
				[1, 1, 2, 2]
			]),
			np.array([
				[0, 0, 0, 1],
				[1, 1, 1, 1],
				[1, 1, 0, 1],
				[1, 1, 2, 2]
			]),
		]

		possible_states_reached = set()
		
		def callback(array, result, iteration):
			if iteration == 1:
				with self.subTest(out=np.copy(array)):
					is_possible_state = False
					for i, state in enumerate(possible_states):
						if np.array_equal(array, state):
							is_possible_state = True
							possible_states_reached.add(i)
							break
					self.assertTrue(is_possible_state)


		settings = SimulationSettings(		
			grid_size=4,
			vacancy_proportion=0.25,
			agent_proportions=(10/12, 2/12),
			initial_random_allocation=False,
			utility_function=create_flat_utility(1/8),
			satisficers=False,
			agent_picking_regime='first',
			vacancy_picking_regime='random',
			radius=1,
			iterations=2
		)

		# Assume all states should be reached in 30 tries
		for i in range(30):
			run_simulation(settings, callback)

		with self.subTest():
			self.assertEqual(len(possible_states_reached), len(possible_states))


	def test_update_array_roulette_agent_picker0(self):
		array = np.array([
			[0, 0, 0, 0],
			[0, 0, 0, 0],
			[1, 1, 1, 1],
			[1, 1, 2, 2]
		])

		utility = get_utility_for_array(create_flat_utility(0.5), array, True)

		states_for_picked = [
			(
				0.0, 
				np.array([
					[2, 0, 0, 0],
					[0, 0, 0, 0],
					[1, 1, 1, 1],
					[1, 1, 0, 2]
				])
			),
			(
				0.5, 
				np.array([
					[2, 0, 0, 0],
					[0, 0, 0, 0],
					[1, 1, 1, 1],
					[1, 1, 0, 2]
				])
			),
			(
				1.0, 
				np.array([
					[2, 0, 0, 0],
					[0, 0, 0, 0],
					[1, 1, 1, 1],
					[1, 1, 0, 2]
				])
			),
			(
				1.00001, 
				np.array([
					[2, 0, 0, 0],
					[0, 0, 0, 0],
					[1, 1, 1, 1],
					[1, 1, 2, 0]
				])
			),
			(
				1.5, 
				np.array([
					[2, 0, 0, 0],
					[0, 0, 0, 0],
					[1, 1, 1, 1],
					[1, 1, 2, 0]
				])
			),
			(
				2.0, 
				np.array([
					[2, 0, 0, 0],
					[0, 0, 0, 0],
					[1, 1, 1, 1],
					[1, 1, 2, 0]
				])
			),			

		]

		result = SimulationResult()

		for picked_value, expected_state in states_for_picked:
			array = np.array([
				[0, 0, 0, 0],
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 2, 2]
			])
			agent_picker = _create_roulette_picker(0.0, utility, True,
				lambda *a: picked_value)
			update_array(array, utility, 1, result, agent_picker, _first_picker,
			 True, False)

			with self.subTest(v=picked_value, out=array, exp=expected_state):
				self.assertTrue(np.array_equal(array, expected_state))


	def test_update_array_roulette_agent_picker_01(self):
		array = np.array([
			[0, 0, 0],
			[0, 1, 1],
			[1, 2, 2]
		])

		utility = get_utility_for_array(create_flat_utility(0.5), array, True)

		states_for_picked = [
			(
				0.0,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 0, 2]
				])
			),
			(
				0.5,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 0, 2]
				])
			),
			(
				1.1,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 0, 2]
				])
			),		
			(
				1.5,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 2, 0]
				])
			),
			(
				2.2,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 2, 0]
				])
			),
			(
				2.3,
				np.array([
					[1, 0, 0],
					[0, 0, 1],
					[1, 2, 2]
				])
			),
			(
				2.4,
				np.array([
					[1, 0, 0],
					[0, 1, 0],
					[1, 2, 2]
				])
			),
			(
				2.5,
				np.array([
					[1, 0, 0],
					[0, 1, 1],
					[0, 2, 2]
				])
			),
		]

		result = SimulationResult()

		for picked_value, expected_state in states_for_picked:
			array = np.array([
				[0, 0, 0],
				[0, 1, 1],
				[1, 2, 2]
			])
			agent_picker = _create_roulette_picker(0.1, utility, True,
				lambda *a: picked_value)
			update_array(array, utility, 1, result, agent_picker, _first_picker,
			 True, True)

			with self.subTest(v=picked_value, out=array, exp=expected_state):
				self.assertTrue(np.array_equal(array, expected_state))


	def test_update_array_roulette_vacancy_picker_01(self):
		array = np.array([
			[0, 0, 0],
			[0, 1, 1],
			[1, 2, 2]
		])

		utility = get_utility_for_array(create_flat_utility(0.5), array, True)

		states_for_picked = [
			(
				0.1,
				np.array([
					[0, 0, 2],
					[0, 1, 1],
					[1, 0, 2]
				])
			),
			(
				0.2,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 0, 2]
				])
			),
			(
				1.2,
				np.array([
					[2, 0, 0],
					[0, 1, 1],
					[1, 0, 2]
				])
			),		
			(
				2.3,
				np.array([
					[0, 2, 0],
					[0, 1, 1],
					[1, 0, 2]
				])
			),
			(
				3.4,
				np.array([
					[0, 0, 0],
					[2, 1, 1],
					[1, 0, 2]
				])
			),
			(
				3.5,
				np.array([
					[0, 0, 0],
					[2, 1, 1],
					[1, 0, 2]
				])
			),
			
		]

		result = SimulationResult()

		for picked_value, expected_state in states_for_picked:
			array = np.array([
				[0, 0, 0],
				[0, 1, 1],
				[1, 2, 2]
			])
			vacancy_picker = _create_roulette_picker(0.1, utility, False,
				lambda *a: picked_value)
			agent_picker = _create_roulette_picker(0.0, utility, True, 
				lambda *a: 0.0)

			update_array(array, utility, 1, result, agent_picker, 
				vacancy_picker, True, True)

			with self.subTest(v=picked_value, out=array, exp=expected_state):
				self.assertTrue(np.array_equal(array, expected_state))


	def test_update_array_all_agents_satisfied_should_end_simulation(self):
		all_satisfied_array = np.array([
				[0, 0, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 1, 1],
				[0, 0, 0, 0]
			])
		result = SimulationResult()

		expected_output = True

		utility = get_utility_for_array(create_flat_utility(0.5), 
			all_satisfied_array)

		output = update_array(all_satisfied_array, utility, 
			1, result, _first_picker, _first_picker, False)

		self.assertEqual(output, expected_output)

	
	def test_update_array_no_better_vacancies_first_picker(self):
		no_better_vacancies_array = np.array([
				[0, 2, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 1, 1],
				[0, 2, 0, 2]
			])
		result = SimulationResult()

		expected_output = True

		utility = get_utility_for_array(create_flat_utility(0.5), 
			no_better_vacancies_array)

		output = update_array(no_better_vacancies_array, 
			utility, 1, result, _first_picker, _first_picker, False)

		self.assertEqual(output, expected_output)


	def test_update_array_no_better_vacancies_for_first_agent(self):
		no_better_vacancies_for_first_agent_array = np.array([
				[1, 1, 2, 0],
				[2, 2, 2, 1],
				[1, 1, 1, 1],
				[1, 2, 1, 2]
			])
		result = SimulationResult()

		expected_output = False

		utility = get_utility_for_array(create_flat_utility(0.5), 
			no_better_vacancies_for_first_agent_array)

		output = update_array(no_better_vacancies_for_first_agent_array, 
			utility, 1, result, _first_picker, 
			_first_picker, False)

		self.assertEqual(output, expected_output)


	def test_no_better_vacancies_not_first_picker(self):
		def custom_first_picker(array_1D):
			return _first_picker(array_1D)

		no_better_vacancies_array = np.array([
				[0, 2, 0, 0],
				[1, 1, 1, 1],
				[1, 1, 1, 1],
				[0, 2, 0, 2]
			])
		result = SimulationResult()

		expected_output = False

		utility = get_utility_for_array(create_flat_utility(0.5),  
			no_better_vacancies_array)

		output = update_array(no_better_vacancies_array, 
			utility, 1, result, custom_first_picker, 
			custom_first_picker, False)

		self.assertEqual(output, expected_output)


if __name__ == '__main__':
	unittest.main()