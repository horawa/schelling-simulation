import unittest
from ..simulation import _get_unsatisfied_agent_indices, _get_random_agent_index, _get_better_vacancies, _get_random_better_vacancy_index, _move
import numpy as np
import schelling.utility_functions as ut
from ..array_utils import get_agent_indices, get_vacancy_indices
from ..neighborhood import get_unlike_neighbor_fraction
from ..utility_functions import get_utility_for_array, create_flat_utility


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

		agent_indices = get_agent_indices(self.test_array)

		for utility_function, expected_output in parameters:
			utility = ut.get_utility_for_array(utility_function, self.test_array)

			output = _get_unsatisfied_agent_indices(utility, agent_indices)
			expected_output = np.array(expected_output)
			with self.subTest(ut=utility_function, out=output, expected=expected_output):
				self.assertTrue(np.array_equal(output, expected_output))


	def test_get_random_agent_index(self):
		agent_indices = get_agent_indices(self.test_array)
		unsatisfied_agent_indices = [0, 1, 2, 3, 5, 6, 7, 8]

		for unsatisfied_agent_index in unsatisfied_agent_indices:
			random_chooser = lambda *args: (unsatisfied_agent_index,)
			
			chosen_index = random_chooser()
			expected_agent_index = tuple(agent_indices[chosen_index])
			
			agent_index = _get_random_agent_index(agent_indices, unsatisfied_agent_indices, random_chooser)

			with self.subTest(out=agent_index, expected=expected_agent_index):
				self.assertEqual(expected_agent_index, agent_index)


	def test_get_better_vacancies(self):
		utility = get_utility_for_array(create_flat_utility(0.5), self.test_array)

		agent_indices = get_agent_indices(self.test_array)
		vacancy_indices = get_vacancy_indices(self.test_array)

		parameters = [
			(5, np.array([4, 5, 6])),
			(6, np.array([4, 5, 6])),
			(7, np.array([0, 1, 2, 3, 5]))
		]

		for unsatisfied_agent_index, expected_output in parameters:
			i = agent_indices[unsatisfied_agent_index]
			output = _get_better_vacancies(self.test_array, i, utility, vacancy_indices)

			with self.subTest(out=output, expected=expected_output):
				self.assertTrue(np.array_equal(output, expected_output))


	def test_get_random_better_vacancy(self):
		parameters = [
			(5, np.array([4, 5, 6])),
			(6, np.array([4, 5, 6])),
			(7, np.array([0, 1, 2, 3, 5]))
		]

		vacancies = get_vacancy_indices(self.test_array)

		for agent_index, better_vacancies in parameters:
			for chosen_vacancy_index in range(len(better_vacancies)):
				random_chooser = lambda *args: chosen_vacancy_index

				output = _get_random_better_vacancy_index(better_vacancies, vacancies, random_chooser)
				expected_output = vacancies[chosen_vacancy_index][0]
				
				with self.subTest(out=output, expected=expected_output):
					self.assertTrue(np.array_equal(output, expected_output))


		# Empty vacancy list
		with self.subTest(name="Empty vacancy list should return none."):
			output = _get_random_better_vacancy_index(np.array([]), np.array([[0, 0], [1, 1]]))
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


if __name__ == '__main__':
	unittest.main()