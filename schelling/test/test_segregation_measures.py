import unittest
from schelling.segregation_measures import (entropy, switch_rate, 
	distance_average, entropy_average, switch_rate_average, ghetto_rate, 
	clusters, distance, mix_deviation, mix_deviation_average, share, 
	share_average, unlike_neighbor_fraction_average_ncv)
from numpy import array
from math import log

class SegregationMeasureTest(unittest.TestCase):

	def setUp(self):
		self.test_array = array([
				[0, 1, 1, 0],
				[1, 1, 0, 1],
				[0, 2, 2, 0],
				[0, 1, 2, 0]
			])


	def check_entropy_expected_output(self, parameters, radius, 
			count_vacancies=False):
		for agent_index, expected_output in parameters:
			with self.subTest(name='entropy_r'+str(radius)+str(count_vacancies),
					index=agent_index):
				output = entropy(self.test_array, agent_index, radius, 
					count_vacancies)
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


	def test_distance_average(self):
		self.check_average_expected_output(distance, distance_average)


	def test_mix_deviation_averate(self):
		self.check_average_expected_output(
			mix_deviation, mix_deviation_average)

	def test_share_average(self):
		self.check_average_expected_output(share, share_average)


	def test_entropy_radius1(self):
		parameters = [
			((0, 0), 0),
			((1, 1), (3/5)*log(3/5, 2) + (2/5)*log(2/5, 2)),
			((2, 2), (3/5)*log(3/5, 2) + (2/5)*log(2/5, 2)),
			((2, 1), (3/5)*log(3/5, 2) + (2/5)*log(2/5, 2)),
			((1, 2), (4/6)*log(4/6, 2) + (2/6)*log(2/6, 2)),
			((3, 0), (1/2)*log(1/2, 2) + (1/2)*log(1/2, 2)),
			((1, 0), (2/3)*log(2/3, 2) + (1/3)*log(1/3, 2)),
			((3, 1), (3/3)*log(3/3, 2)),
		]

		self.check_entropy_expected_output(parameters, 1)


	def test_entropy_radius2(self):
		parameters = [
			((1, 1), (5/8)*log(5/8, 2) + (3/8)*log(3/8, 2)),
			((2, 2), (6/8)*log(6/8, 2) + (2/8)*log(2/8, 2)),
			((2, 1), (6/8)*log(6/8, 2) + (2/8)*log(2/8, 2)),
			((1, 2), (6/9)*log(6/9, 2) + (3/9)*log(3/9, 2)),
			((0, 0), (4/6)*log(4/6, 2) + (2/6)*log(2/6, 2)),
			((3, 3), (3/6)*log(3/6, 2) + (3/6)*log(3/6, 2)),
			((0, 1), (4/6)*log(4/6, 2) + (2/6)*log(2/6, 2)),
		]

		self.check_entropy_expected_output(parameters, 2)


	def test_entropy_count_vacancies(self):
		parameters = [
			((0, 0), 0),
			((1, 1), (3/8)*log(3/8, 2) + (2/8)*log(2/8, 2) + (3/8)*log(3/8, 2)),
			((2, 2), (3/8)*log(3/8, 2) + (2/8)*log(2/8, 2) + (3/8)*log(3/8, 2)),
			((2, 1), (3/8)*log(3/8, 2) + (2/8)*log(2/8, 2) + (3/8)*log(3/8, 2)),
			((1, 2), (4/8)*log(4/8, 2) + (2/8)*log(2/8, 2) + (2/8)*log(2/8, 2)),
			((3, 0), (1/3)*log(1/3, 2) + (1/3)*log(1/3, 2) + (1/3)*log(1/3, 2)),
			((1, 0), (2/5)*log(2/5, 2) + (1/5)*log(1/5, 2) + (2/5)*log(2/5, 2)),
			((3, 1), (3/5)*log(3/5, 2) + (2/5)*log(2/5, 2)),
		]

		self.check_entropy_expected_output(parameters, 1, True)


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


	def test_ghetto_rate(self):
		parameters = [ 
			(array([
				[1, 1, 1, 1],
				[1, 1, 1, 1],
				[2, 2, 2, 2],
				[2, 2, 2, 2],
			]), 0.5),
			(array([
				[1, 1, 1, 1],
				[1, 1, 0, 1],
				[2, 2, 2, 2],
				[2, 2, 0, 2],
			]), 7/16),			
		]

		agent_indices = array(
			[[row, col] for row in range(4) for col in range(4)])

		for test_array, expected_output in parameters:
			output = ghetto_rate(test_array, agent_indices)
			with self.subTest(array=test_array):
				self.assertAlmostEqual(output, expected_output)


	def test_clusters(self):
		parameters = [ 
			(array([
				[1, 1, 1, 1],
				[0, 0, 0, 0],
				[2, 2, 2, 2],
				[2, 2, 2, 2],
			]), 2),
			(array([
				[1, 1, 0, 1],
				[1, 1, 0, 1],
				[2, 2, 0, 2],
				[2, 2, 0, 2],
			]), 4),		
			(array([
				[1, 0, 1, 0],
				[0, 1, 0, 1],
				[2, 2, 0, 2],
				[2, 2, 0, 2],
			]), 6),
			(array([
				[1, 1, 1, 1],
				[2, 1, 2, 1],
				[2, 1, 1, 1],
				[2, 2, 0, 2],
			]), 4),		
			(array([
				[1, 1, 0, 1],
				[0, 1, 0, 1],
				[2, 1, 0, 1],
				[2, 1, 1, 1],
			]), 2),
		]
		
		for test_array, expected_output in parameters:
			output = clusters(test_array)
			with self.subTest(array=test_array):
				self.assertEqual(output, expected_output)


	def test_distance(self):
		def check_output(test_array, parameters):
			for agent_index, expected_output in parameters:
				output = distance(test_array, agent_index)
				with self.subTest(array=test_array, index=agent_index):
					self.assertEqual(output, expected_output)

		parameters = [
			((0, 1), 2),
			((0, 2), 2),
			((1, 0), 1),
			((1, 1), 1),
			((1, 3), 1),
			((2, 1), 1),
			((2, 2), 1),
			((3, 1), 1),
			((3, 2), 1),
		]

		check_output(self.test_array, parameters)

		test_array1 = array([
				[1, 1, 1, 1],
				[1, 1, 1, 1],
				[0, 0, 0, 0],
				[0, 0, 0, 2]
			])

		parameters1 = [
			((0, 0), 3),
			((0, 1), 3),
			((0, 2), 3),
			((0, 3), 3),
			((1, 0), 3),
			((1, 1), 2),
			((1, 2), 2),
			((1, 3), 2),
			((3, 3), 2),
		]

		check_output(test_array1, parameters1)


	def test_mix_deviation(self):
		parameters = [
			((0, 1), 0.5),
			((0, 2), 0.5),
			((1, 0), 1/6),
			((1, 1), 0.1),
			((1, 3), 0.0),
			((2, 1), 0.1),
			((2, 2), 0.1),
			((3, 1), 0.5),
			((3, 2), 1/6),
		]

		for agent_index, expected_output in parameters:
			output = mix_deviation(self.test_array, agent_index)
			with self.subTest(i=agent_index):
				self.assertAlmostEqual(output, expected_output)


	def test_share(self):
		parameters = [
			((0, 1), 1.0),
			((0, 2), 1.0),
			((1, 0), 2/3),
			((1, 1), 3/5),
			((1, 3), 1/2),
			((2, 1), 2/5),
			((2, 2), 2/5),
			((3, 1), 0.0),
			((3, 2), 2/3),
		]

		for agent_index, expected_output in parameters:
			output = share(self.test_array, agent_index)
			with self.subTest(i=agent_index):
				self.assertAlmostEqual(output, expected_output)

	def test_unlike_neighbor_fraction_average_ncv(self):
		# parameters = [
		# 	((0, 1), 0),
		# 	((0, 2), 0),
		# 	((1, 0), 1/3),
		# 	((1, 1), 2/5),
		# 	((1, 3), 1/2),
		# 	((2, 1), 3/5),
		# 	((2, 2), 3/5),
		# 	((3, 1), 1),
		# 	((3, 2), 1/3),
		# ]

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

		expected_output = ((1/3) + (2/5) + (1/2) + (3/5) + (3/5) + 1 + (1/3)
			) / 9
		output = unlike_neighbor_fraction_average_ncv(
			self.test_array, agent_indices)
		self.assertAlmostEqual(output, expected_output)


if __name__ == '__main__':
	unittest.main()