import unittest
from schelling.utility_functions import (create_flat_utility, 
	create_peaked_utility, create_spiked_utility)
from numpy import linspace

class UtilityFunctionsTest(unittest.TestCase):

	def test_flat_utility(self):
		# step threshold, exepcted output for 0.0 - 1.0, step 0.1
		test_data = [
			(0.0 , [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
			(0.25, [1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
			(0.5 , [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]),
			(0.75, [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0]),
			(1.0 , [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]),	
		]


		for threshold, exepcted_output_list in test_data:
			flat_utility = create_flat_utility(threshold)
			self.check_expected_output_for_range_0_1('flat_'+str(threshold), 
				flat_utility, exepcted_output_list)



	def test_peaked_utility(self):
		# peak, exepcted output for 0.0 - 1.0, step 0.1
		test_data = [
			(0.00, [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]),
			(0.10, [0, 1, 0.888888889, 0.777777778, 0.666666667, 0.555555556, 
				0.444444444, 0.333333333, 0.222222222, 0.111111111, 0]),
			(0.20, [0, 0.5, 1, 0.875, 0.75, 0.625, 0.5, 0.375, 0.25, 0.125, 0]),
			(0.30, [0, 0.333333333, 0.666666667, 1, 0.857142857, 0.714285714, 
				0.571428571, 0.428571429, 0.285714286, 0.142857143, 0]),
			(0.40, [0, 0.25, 0.5, 0.75, 1, 0.833333333, 0.666666667, 0.5, 
				0.333333333, 0.166666667, 0]),
			(0.50, [0, 0.2, 0.4, 0.6, 0.8, 1, 0.8, 0.6, 0.4, 0.2, 0]),
			(0.60, [0, 0.166666667, 0.333333333, 0.5, 0.666666667, 0.833333333, 
				1, 0.75, 0.5, 0.25, 0]),
			(0.70, [0, 0.142857143, 0.285714286, 0.428571429, 0.571428571, 
				0.714285714, 0.857142857, 1, 0.666666667, 0.333333333, 0]),
			(0.80, [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 0.5, 0]),
			(0.90, [0, 0.111111111, 0.222222222, 0.333333333, 0.444444444, 
				0.555555556, 0.666666667, 0.777777778, 0.888888889, 1, 0]),
			(1.00, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
		]

		for peak, exepcted_output_list in test_data:
			peaked_utility = create_peaked_utility(peak)
			self.check_expected_output_for_range_0_1(
				'peaked_'+str(peak), peaked_utility, exepcted_output_list)



	def test_peaked_utility_cutoff(self):
		test_data = [
			(0.00, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
			(0.10, [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
			(0.20, [0, 0.5, 1, 0, 0, 0, 0, 0, 0, 0, 0]),
			(0.30, [0, 0.333333333, 0.666666667, 1, 0, 0, 0, 0, 0, 0, 0]),
			(0.40, [0, 0.25, 0.5, 0.75, 1, 0, 0, 0, 0, 0, 0]),
			(0.50, [0, 0.2, 0.4, 0.6, 0.8, 1, 0, 0, 0, 0, 0]),
			(0.60, [0, 0.166666667, 0.333333333, 0.5, 0.666666667, 0.833333333, 
				1, 0, 0, 0, 0]),
			(0.70, [0, 0.142857143, 0.285714286, 0.428571429, 0.571428571, 
				0.714285714, 0.857142857, 1, 0, 0, 0]),
			(0.80, [0, 0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875, 1, 0, 0]),
			(0.90, [0, 0.111111111, 0.222222222, 0.333333333, 0.444444444, 
				0.555555556, 0.666666667, 0.777777778, 0.888888889, 1, 0]),
			(1.00, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]),
		]

		for peak, exepcted_output_list in test_data:
			peaked_utility = create_peaked_utility(peak, True)
			self.check_expected_output_for_range_0_1(
				'peaked_cutoff_'+str(peak), 
				peaked_utility, exepcted_output_list)



	def test_spiked_utility(self):
		test_data = [
			(0.00, [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
			(0.50, [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]),
			(1.00, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),
		]

		for spike, exepcted_output_list in test_data:
			spiked_utility = create_spiked_utility(spike)
			self.check_expected_output_for_range_0_1(
				'spiked_cutoff_'+str(spike), spiked_utility, 
				exepcted_output_list)


		# test close values
		spiked_utility = create_spiked_utility(0.5)

		small_values = [9.99999e-8, 1e-10, 1e-11]

		for val in small_values:
			with self.subTest(name='spiked_cutoff_close +', val=val):
				output = spiked_utility(0.5 + val)
				self.assertAlmostEqual(output, 1.0)
			with self.subTest(name='spiked_cutoff_close -', val=val):
				output = spiked_utility(0.5 - val)
				self.assertAlmostEqual(output, 1.0)



	def check_expected_output_for_range_0_1(self, name, utility_function, 
			exepcted_output_list):
		for unlike_neighbors, exepcted_output in zip(linspace(0.0, 1.0, 11), 
				exepcted_output_list):
			with self.subTest(name=name, input=unlike_neighbors):
				output = utility_function(round(unlike_neighbors, 4))
				self.assertAlmostEqual(output, exepcted_output)


	def test_value_error_outside_0_1(self):
		functions = {
			'flat': create_flat_utility(0.5),
			'peaked': create_peaked_utility(0.5),
			'peaked_cutoff': create_peaked_utility(0.5, True),
			'spiked': create_spiked_utility(0.5),
			'create_flat': create_flat_utility,
			'create_peaked': create_peaked_utility,
			'create_spiked': create_spiked_utility,
		}

		error_inputs = [-10, -1, -0.1, -0.00001, 1.00001, 1.1, 2, 10]

		for name, function in functions.items():
			for error_input in error_inputs:
				with self.subTest(name=name, input=error_input):
					with self.assertRaises(ValueError):
						function(error_input)


if __name__ == '__main__':
	unittest.main()

