import unittest
from ..segregation_measures import (entropy, switch_rate, 
	entropy_average, switch_rate_average)
from ..neighborhood import get_neighborhood
from numpy import array, mean
from math import log

class SegregationMeasureTest(unittest.TestCase):

	def setUp(self):
		self.test_array = array([
				[0, 1, 1, 0],
				[1, 1, 0, 1],
				[0, 2, 2, 0],
				[0, 1, 2, 0]
			])



	def check_entropy_expected_output(self, parameters, radius):
		for agent_index, expected_output in parameters:
			with self.subTest(name='entropy_r'+str(radius), index=agent_index):
				output = entropy(self.test_array, agent_index, radius)
				self.assertAlmostEqual(output, -expected_output)


	def check_average_expected_output(self, measure, measure_average):
		agent_indices= array([
			(0,1),
			(0,2),
			(1,0),
			(1,1),
			(1,3),
			(2,1),
			(2,2),
			(3,1),
			(3,2),
		])

		agent_values = map(lambda a_i: measure(self.test_array, tuple(a_i)), 
			agent_indices)
		expected_output = sum(agent_values) / len(agent_indices)

		output = measure_average(self.test_array, agent_indices)

		self.assertEqual(expected_output, output)



	def test_entropy_average(self):
		self.check_average_expected_output(entropy, entropy_average)


	def test_switch_rate_average(self):
		self.check_average_expected_output(switch_rate, switch_rate_average)




	def test_entropy_radius1(self):
		parameters = [
			((0, 0), 0),
			((1, 1), (3/8)*log(3/8, 2) + (2/8)*log(2/8, 2)),
			((2, 2), (3/8)*log(3/8, 2) + (2/8)*log(2/8, 2)),
			((2, 1), (3/8)*log(3/8, 2) + (2/8)*log(2/8, 2)),
			((1, 2), (4/8)*log(4/8, 2) + (2/8)*log(2/8, 2)),
			((3, 0), (1/3)*log(1/3, 2) + (1/3)*log(1/3, 2)),
			((1, 0), (2/5)*log(2/5, 2) + (1/5)*log(1/5, 2)),
			((3, 1), (3/5)*log(3/5, 2)),
		]

		self.check_entropy_expected_output(parameters, 1)


	def test_entropy_radius2(self):
		parameters = [
			((1, 1), (5/15)*log(5/15, 2) + (3/15)*log(3/15, 2)),
			((2, 2), (6/15)*log(6/15, 2) + (2/15)*log(2/15, 2)),
			((2, 1), (6/15)*log(6/15, 2) + (2/15)*log(2/15, 2)),
			((1, 2), (6/15)*log(6/15, 2) + (3/15)*log(3/15, 2)),
			((0, 0), (4/8)*log(4/8, 2) + (2/8)*log(2/8, 2)),
			((3, 3), (3/8)*log(3/8, 2) + (3/8)*log(3/8, 2)),
			((0, 1), (4/11)*log(4/11, 2) + (2/11)*log(2/11, 2)),
			
		]

		self.check_entropy_expected_output(parameters, 2)


	def test_switch_rate(self):
		parameters = [
			((0, 0), 0),
			((1, 1), 6),
			((2, 2), 7),
			((2, 1), 5),
			((1, 2), 5),
			((3, 0), 3),
			((1, 0), 3),
			((3, 1), 2),
		]

		for agent_index, expected_output in parameters:
			with self.subTest(name='switch rate', index=agent_index):
				output = switch_rate(self.test_array, agent_index)
				self.assertEqual(output, expected_output)



if __name__ == '__main__':
	unittest.main()