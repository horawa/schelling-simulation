import unittest
from numpy import array
from ..get_neighborhood import get_neighborhood


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



	def check_get_neighborhood_expected_output(self, parameters, radius):
		for agent_index, expected_output in parameters:
			with self.subTest(name='get_neighborhood_r'+str(radius), index=agent_index):
				output = get_neighborhood(self.test_array, agent_index, radius)
				self.assertAlmostEqual(output, expected_output)


	def test_get_neighborhood_radius1(self):
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

		self.check_get_neighborhood_expected_output(parameters, 1)



	def test_get_neighborhood_radius2(self):
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
			((2,2), [[1, 2, 3, 4, 5], [4, 5, 6, 7, 8], [1, 2, 4, 5], [4, 5, 6, 7, 8], [1, 2, 3, 4, 5]]),
		]

		self.check_get_neighborhood_expected_output(parameters, 2)


if __name__ == '__main__':
	unittest.main()
