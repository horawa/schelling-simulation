import unittest
from ..simulation import _get_unsatisfied_agent_indices
import numpy as np
import schelling.utility_functions as ut
from ..array_utils import get_agent_indices
from ..get_neighborhood import get_unlike_neighbor_fraction


class SimulationTestCase(unittest.TestCase):
	def setUp(self):
		self.test_array = np.array([
				[0, 1, 1, 0],
				[1, 1, 0, 1],
				[0, 2, 2, 0],
				[0, 1, 2, 0]
			])




	def test_get_unsatisfied_agent_indices(self):
		# parameters =[
		# 	(0, 0), []
		# 	(0, 1),
		# 	(0, 2),
		# 	(0, 3),
		# 	(1, 0),
		# 	(1, 1),
		# 	(1, 2),
		# 	(1, 3),
		# 	(2, 0),
		# 	(2, 1),
		# 	(2, 2),
		# 	(2, 3),
		# 	(3, 0),
		# 	(3, 1),
		# 	(3, 2),
		# 	(3, 3),
		# ]

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





if __name__ == '__main__':
	unittest.main()