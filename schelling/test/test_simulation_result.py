import unittest
import os

from schelling.simulation_result import SimulationResult

class ResultTestCase(unittest.TestCase):
	def setUp(self):
		names=['entropy_average', 
			'switch_rate_average', 'clusters', 'mix_deviation_average']
		self.result = SimulationResult(names)
		
		# leave one empty
		for name in names[:-1]:
			self.result.save_measure(name, 4)
			self.result.save_measure(name, 5)
			self.result.save_measure(name, 6)
			self.result.save_measure(name, 7)


	def test_JSON(self):
		path = './out.json'

		initial_dict = dict(self.result._segregation_measures)

		self.result.save_JSON(path)
		self.result.parse_JSON(path)

		final_dict = dict(self.result._segregation_measures)

		os.remove(path)

		self.assertEqual(initial_dict, final_dict)


	def test_str(self):
		expected_output = ""
		items = self.result._segregation_measures.items()
		for item in items:
			expected_output += item[0] + ": " 
			if item[1]:
				expected_output += str(item[1][-1])
			expected_output += "\n"

		output = str(self.result)

		self.assertEqual(output, expected_output)
