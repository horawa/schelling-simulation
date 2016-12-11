import unittest
from ..simulation import (_get_unsatisfied_agent_indices, 
	_pick_agent_index_to_move, _get_better_vacancies, run_simulation,
	_pick_better_vacancy_index, _move, _random_picker, _first_picker)
import numpy as np
import schelling.utility_functions as ut
from ..array_utils import get_agent_indices, get_vacancy_indices
from ..neighborhood import get_unlike_neighbor_fraction
from ..utility_functions import get_utility_for_array, create_flat_utility
from ..simulation_settings import SimulationSettings


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
			expected_output = np.array(expected_output)
			with self.subTest(ut=utility_function, out=output, 
					expected=expected_output):
				self.assertTrue(np.array_equal(output, expected_output))


	def test_pick_agent_index_to_move(self):
		agent_indices = get_agent_indices(self.test_array)
		unsatisfied_agent_indices = [0, 1, 2, 3, 5, 6, 7, 8]

		for unsatisfied_agent_index in unsatisfied_agent_indices:
			
			chosen_index = _first_picker(unsatisfied_agent_indices)
			expected_agent_index = tuple(agent_indices[chosen_index])
			
			agent_index = _pick_agent_index_to_move(agent_indices, 
				unsatisfied_agent_indices, _first_picker)

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

		for unsatisfied_agent_index, expected_output in parameters:
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

		for agent_index, better_vacancies in parameters:
			for chosen_vacancy_index in range(len(better_vacancies)):
				def picker(array_1D):
					return array_1D[chosen_vacancy_index]

				output = _pick_better_vacancy_index(better_vacancies, 
					vacancies, picker)
				vacancy_index_index = better_vacancies[chosen_vacancy_index]
				expected_output = vacancies[vacancy_index_index]
				
				with self.subTest(chosen_index=chosen_vacancy_index,
						out=output, expected=expected_output):
					self.assertTrue(np.array_equal(output, expected_output))

		# Empty vacancy list
		with self.subTest(name="Empty vacancy list should return none."):
			output = _pick_better_vacancy_index(np.array([]), 
				np.array([[0, 0], [1, 1]]), _first_picker)
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
		data = [1, 2, 3, 4, 5]

		array = np.array(data)
		for i in range(20):
			picked = _random_picker(array)
			with self.subTest(data=data, picked=picked):
				self.assertTrue(picked in data)


	def test_first_picker(self):
		parameters = [
			[1, 2, 3, 4, 5],
			[2, 3, 4, 5, 6],
			[4, 5, 6, 7, 8],
		]

		for data in parameters:
			array = np.array(data)
			picked = _first_picker(array)
			with self.subTest(data=data, picked=picked):
				self.assertEqual(picked, data[0])


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
			pick_random=False,
			move_to_random=False,
			radius=1,
			iterations=len(iteration_states)
		)

		result = run_simulation(settings, callback)

		clusters = [3, 4, 4, 4, 3] + ([4, 3] * 100)
		with self.subTest():
			self.assertEqual(result.clusters, clusters)


if __name__ == '__main__':
	unittest.main()