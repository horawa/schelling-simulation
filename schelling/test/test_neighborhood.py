import unittest
from numpy import array, array_equal
from schelling.neighborhood import (get_neighborhood, 
	get_neighborhood_exclusive, get_unlike_neighbor_fraction, has_neighbors)


class GetNeighborhoodTest(unittest.TestCase):
	def setUp(self):
		self.test_array = array([
				[1, 2, 3, 4, 5, 6],
				[4, 5, 6, 7, 8, 9],
				[1, 2, 3, 4, 5, 6],
				[4, 5, 6, 7, 8, 9],
				[1, 2, 3, 4, 5, 6],
				[4, 5, 6, 7, 8, 9],
			])

		self.frac_test_array = array([
				[0, 1, 1, 0],
				[1, 1, 0, 1],
				[0, 2, 2, 0],
				[0, 1, 2, 0]
			])
		

	def check_get_neighborhood_expected_output(self, parameters, radius, 
			exclusive=False):
		for agent_index, expected_output in parameters:
			with self.subTest(name='get_neighborhood_r'+str(radius), 
					index=agent_index):
				if exclusive:
					output = get_neighborhood_exclusive(self.test_array, 
						agent_index, radius)
					self.assertEqual(output, expected_output)
				else:
					output = get_neighborhood(self.test_array, agent_index, 
						radius)
					self.assertTrue(array_equal(output, expected_output))



	def test_get_neighborhood_exclusive_radius1(self):
		parameters = [
			((0,0), [[2], [4, 5]]),
			((1,0), [[1, 2], [5], [1, 2]]),
			((5,0), [[1, 2], [5]]),
			((5,2), [[2, 3, 4], [5, 7]]),
			((5,5), [[5, 6], [8]]),
			((4,5), [[8, 9], [5], [8, 9]]),
			((0,5), [[5], [8, 9]]),
			((0,4), [[4, 6], [7, 8, 9]]),
			((1,1), [[1, 2, 3], [4, 6], [1, 2, 3]]),
		]

		self.check_get_neighborhood_expected_output(parameters, 1, True)



	def test_get_neighborhood_exclusive_radius2(self):
		parameters = [
			((0,0), [[2, 3], [4, 5, 6], [1, 2, 3]]),
			((1,0), [[1, 2, 3], [5, 6], [1, 2, 3], [4, 5, 6]]),
			((5,0), [[4, 5, 6], [1, 2, 3], [5, 6]]),
			((5,2), [[4, 5, 6, 7, 8], [1, 2, 3, 4, 5], [4, 5, 7, 8]]),
			((5,5), [[7, 8 , 9], [4, 5, 6], [7, 8]]),
			((4,5), [[4, 5, 6], [7, 8, 9], [4, 5], [7, 8, 9]]),
			((0,5), [[4, 5], [7, 8, 9], [4, 5, 6]]),
			((0,4), [[3, 4, 6], [6, 7, 8, 9], [3, 4, 5, 6]]),
			((1,1), [[1, 2, 3, 4], [4, 6, 7], [1, 2, 3, 4], [4, 5, 6, 7]]),
			((2,2), [[1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [1, 2, 4, 5], 
				[4, 5, 6, 7, 8], [1, 2, 3, 4, 5]]),
		]

		self.check_get_neighborhood_expected_output(parameters, 2, True)


	def test_get_neighborhood_radius1(self):
		parameters = [
			((0,0), array([[1, 2], [4, 5]])),
			((1,0), array([[1, 2], [4, 5], [1, 2]])),
			((5,0), array([[1, 2], [4, 5]])),
			((5,2), array([[2, 3, 4], [5, 6, 7]])),
			((5,5), array([[5, 6], [8, 9]])),
			((4,5), array([[8, 9], [5, 6], [8, 9]])),
			((0,5), array([[5, 6], [8, 9]])),
			((0,4), array([[4, 5, 6], [7, 8, 9]])),
			((1,1), array([[1, 2, 3], [4, 5, 6], [1, 2, 3]])),
		]

		self.check_get_neighborhood_expected_output(parameters, 1)


	def test_get_neighborhood_radius2(self):
		parameters = [
			((0,0), array([[1, 2, 3], [4, 5, 6], [1, 2, 3]])),
			((1,0), array([[1, 2, 3], [4, 5, 6], [1, 2, 3], [4, 5, 6]])),
			((5,0), array([[4, 5, 6], [1, 2, 3], [4, 5, 6]])),
			((5,2), array([[4, 5, 6, 7, 8], [1, 2, 3, 4, 5], 
				[4, 5, 6, 7, 8]])),
			((5,5), array([[7, 8 , 9], [4, 5, 6], [7, 8, 9]])),
			((4,5), array([[4, 5, 6], [7, 8, 9], [4, 5, 6], [7, 8, 9]])),
			((0,5), array([[4, 5, 6], [7, 8, 9], [4, 5, 6]])),
			((0,4), array([[3, 4, 5, 6], [6, 7, 8, 9], [3, 4, 5, 6]])),
			((1,1), array([[1, 2, 3, 4], [4, 5, 6, 7], [1, 2, 3, 4], 
				[4, 5, 6, 7]])),
			((2,2), array([[1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5], 
				[4, 5, 6, 7, 8], [1, 2, 3, 4, 5]])),
		]

		self.check_get_neighborhood_expected_output(parameters, 2)


	def test_get_unlike_agent_fraction(self):
		agent_fractions = [
			((0,1), 0),
			((0,2), 0),
			((1,0), 1/3),
			((1,1), 2/5),
			((1,3), 1/2),
			((2,1), 3/5),
			((2,2), 3/5),
			((3,1), 3/3),
			((3,2), 1/3),
		]

		for agent_index, expected_output in agent_fractions:
			with self.subTest(name='unlike_fraction', index=agent_index):
				output = get_unlike_neighbor_fraction(self.frac_test_array, 
					agent_index)
				self.assertAlmostEqual(output, expected_output)


	def test_get_unlike_agent_fraction_count_vacancies(self):
		agent_fractions = [
			((0,1), 0),
			((0,2), 0),
			((1,0), 1/5),
			((1,1), 2/8),
			((1,3), 1/5),
			((2,1), 3/8),
			((2,2), 3/8),
			((3,1), 3/5),
			((3,2), 1/5),
		]

		for agent_index, expected_output in agent_fractions:
			with self.subTest(name='unlike_fraction', index=agent_index):
				output = get_unlike_neighbor_fraction(self.frac_test_array, 
					agent_index, count_vacancies=True)
				self.assertAlmostEqual(output, expected_output)


	def test_has_neighbors(self):
		test_array = array([
				[1, 0, 1, 0],
				[0, 0, 0, 2],
				[0, 0, 0, 0],
				[0, 2, 0, 0]
			])

		expected_outputs = [
			((0,0), False),
			((0,2), True),
			((1,3), True),
			((3,1), False)
		]

		for agent_index, expected_output in expected_outputs:
			with self.subTest(name='has_neigbors', index=agent_index):
				output = has_neighbors(test_array, agent_index)
				self.assertEqual(output, expected_output)


if __name__ == '__main__':
	unittest.main()
