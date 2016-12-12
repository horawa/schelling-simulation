import unittest
from math import isclose

from ..agent_distributions import (get_uniform_distribution, 
	get_distribution_including_vacancies)

from ..simulation_settings import SimulationSettings
	
class DistributionsTestCase(unittest.TestCase):
	def test_get_uniform_distribution(self):
		parameters = [
			((1,), (1.0,)),
			((2,), (0.5, 0.5)),
			((3,), (1/3, 1/3, 1/3)),
			((4,), (0.25, 0.25, 0.25, 0.25)),
			((5,), (0.2, 0.2, 0.2, 0.2, 0.2)),
			((6,), (1/6, 1/6, 1/6, 1/6, 1/6, 1/6)),
			((7,), (1/7, 1/7, 1/7, 1/7, 1/7, 1/7, 1/7)),
		]

		self.check_distribution_expected_output(get_uniform_distribution, 
			parameters)

		error_values = [-1000, -10, -1, 0, 8, 10, 100, 1000]

		for value in error_values:
			with self.subTest():
				with self.assertRaises(ValueError):
					get_uniform_distribution(value)

	def test_get_distribution_including_vacancies(self):
		parameters = [
			((0.5, (0.5, 0.5)), (0.5, 0.25, 0.25)),
			((0.25, (0.5, 0.5)), (0.25, 0.375, 0.375)),
			((1/3, (0.5, 0.5)), (1/3, 1/3, 1/3)),
			((1/3, (1/3, 1/3, 1/3)), (1/3, 2/9, 2/9, 2/9)),
		]

		self.check_distribution_expected_output(
			get_distribution_including_vacancies, parameters)

		def check_for_settings(vacancies, agent_distribution):
			settings = SimulationSettings(vacancy_proportion=vacancies, 
				agent_proportions=agent_distribution)
			return settings.get_agent_type_proportions()

		self.check_distribution_expected_output(check_for_settings, parameters)

	def check_distribution_expected_output(self, function, parameters):
		for args, expected_output in parameters:
			output = function(*args)
			with self.subTest(f=function):
				output_almost_equal = \
					all([isclose(*o) for o in zip(output, expected_output)])
				self.assertTrue(output_almost_equal)
			with self.subTest(f=function, name='sum to 1'):
				self.assertAlmostEqual(sum(output), 1.0)

