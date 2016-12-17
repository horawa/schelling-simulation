import unittest
import os

from schelling.simulation_result import SimulationResult

class ResultTestCase(unittest.TestCase):
	def setUp(self):
		self.result = SimulationResult()
		self.result.switch_rate_average = [4, 5]
		self.result.entropy_average = [4, 5]
		self.result.ghetto_rate = [4, 5]
		self.result.clusters = [4, 5]
		self.result.distance_average = [4, 5]
		self.result.mix_deviation_average = []

	def test_JSON(self):
		path = './out.json'

		initial_dict = dict(self.result.__dict__)

		self.result.save_JSON(path)
		self.result.parse_JSON(path)

		final_dict = dict(self.result.__dict__)

		os.remove(path)

		self.assertEqual(initial_dict, final_dict)


	def test_str(self):
		expected_output = ""
		items = self.result.__dict__.items()
		for item in items:
			expected_output += item[0] + ": " 
			if item[1]:
				expected_output += str(item[1][-1])
			expected_output += "\n"

		output = str(self.result)

		self.assertEqual(output, expected_output)
