import unittest
import numpy as np
from schelling.array_utils import get_agent_indices, get_vacancy_indices

class ArrayUtilsTest(unittest.TestCase):
	def setUp(self):
		self.test_array = np.array([
				[0, 1, 1, 0],
				[1, 1, 0, 1],
				[0, 2, 2, 0],
				[0, 1, 2, 0]
			])
		self.agent_indices= np.array([
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
		self.vacancy_indices = np.array([
			(0,0),
			(0,3),
			(1,2),
			(2,0),
			(2,3),
			(3,0),
			(3,3),
		])


	def test_agent_indices(self):
		output = get_agent_indices(self.test_array)
		expected_output = self.agent_indices


		self.assertTrue(np.array_equal(output, expected_output))


	def test_vacancy_indices(self):
		output = get_vacancy_indices(self.test_array)
		expected_output = self.vacancy_indices

		self.assertTrue(np.array_equal(output, expected_output))

if __name__ == '__main__':
	unittest.main()