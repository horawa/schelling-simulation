from ..create_array import create_array
from decimal import Decimal
import unittest
import numpy as np

class CreateArrayTest(unittest.TestCase):

	def test_array_properties(self):
		arr = create_array(50, (0.2, 0.4, 0.4))
		self.assertEqual(arr.ndim, 2)
		self.assertEqual(arr.shape, (50, 50))
		self.assertEqual(arr.size, 2500)
		self.assertEqual(arr.dtype, 'int64')


	def test_agent_type_counts(self):
		# arr_size (int), agent_proportions (tuple), has rounding error (bool)
		parameters_list = [
			(50, (0.2, 0.4, 0.4), False),
			(2, (0.1, 0.4, 0.5), True),
			(100, (1/3,1/3,1/3), True),
			(1000, (1/3,1/3,1/3), True),
			(100, (0.25, 0.25, 0.25, 0.25), False),
			(1000, tuple([Decimal(0.01)]*100), False),

		]

		for arr_size, agent_proportions, has_rounding_error in parameters_list:
			arr = create_array(arr_size, agent_proportions)

			for agent_index, agent_proportion in enumerate(agent_proportions):
				with self.subTest(arr_size=arr_size, agent_proportions=agent_proportions, agent_index=agent_index):			
					expected_count = int((arr_size**2) * agent_proportion)
					if agent_index == 0 and has_rounding_error: 
						expected_count += 1

					arr_where_agent = arr == agent_index
					count = arr_where_agent.sum()
					
					self.assertEqual(expected_count, count)				


	def test_agent_fractions_input_should_equal_one_error(self):
		parameters_list = [
			(50, (0.2, 0.2, 0.2)),
			(50, (0.2, 0.6, 0.6)),
			(50, ()),
			(50, (100, 100, 100)),
			(50, (0.33, 0.33, 0.33)),
		]

		for parameters in parameters_list:
			with self.subTest(parameters=parameters):
				with self.assertRaises(ValueError):
					create_array(*parameters)					


	def test_correct_array_sizes(self):
		for size in range(50):
			with self.subTest(name="array_size", size=size):
				arr = create_array(size, (0.2, 0.4, 0.4))
				self.assertEqual(arr.size, size*size)


	def test_segregated_allocation(self):
		parameters = [
			(5, (0.2, 0.4, 0.4), 
				np.array([
				[0]*5, 
				[1]*5,
				[1]*5,
				[2]*5,
				[2]*5,
				])),
			(6, (0.2, 0.4, 0.4), 
				np.array([
				[0]*6,
				[0, 0] + [1]*4,
				[1] * 6,
				([1] * 4) + ([2] * 2),
				[2] * 6,
				[2] * 6,
				])) # 8, 14, 14 
			]

		for arr_size, agent_fractions, expected_output in parameters:
			output = create_array(arr_size, agent_fractions, random_allocation=False)
			
			with self.subTest(out=output, expected=expected_output):
				self.assertTrue(np.array_equal(output, expected_output))

if __name__ == '__main__':
	unittest.main()