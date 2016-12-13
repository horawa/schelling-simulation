import unittest
from math import isclose

from ..agent_distributions import (get_uniform_distribution, 
	get_exponential_distribution,
	get_normal_distribution,
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


	def test_get_exponential_distribution(self):
		"""
		wolfram:

		integrate exp(-x) on (0, 1);
		integrate exp(-x) on (1, 2);
		integrate exp(-x) on (2, 3);
		integrate exp(-x) on (3, 4);
		integrate exp(-x) on (4, 5);
		integrate exp(-x) on (5, 6);
		integrate exp(-x) on (6, infinity);

		etc. 
		"""

		parameters = [
			(1, (0.63212, 0.23254, 0.085548, 0.031471, 0.011578, 
				0.0042592, 0.0024788)),
			(2, (0.86466, 0.11702, 0.015837, 0.0021433, 0.00029006, 
				0.000039256, 6.1442e-6))
		]

		for lambda_, expected_output in parameters:
			output = get_exponential_distribution(lambda_)	
			for out_val, ex_val in zip(output, expected_output):
				with self.subTest(lambda_=lambda_, out=out_val, ex=ex_val):
					vals_close = isclose(out_val, ex_val, rel_tol=1e-04)
					self.assertTrue(vals_close)


	def test_get_normal_distribution(self):
		"""
		dev1
		0.00621, 0.06681, 0.30854, 0.69146, 0.93319, 0.93319, 1, 	
		(0.006209665, 0.060597536, 0.241730337, 0.241730337, 
			0.241730337, 0.060597536, 0.006209665)

		dev0.5
		0.00002, 0.00135, 0.15866, 0.84134, 0.99865, 0.99998, 1
		(2.866515719E-7, 0.001349611, 0.157305356, 0.682689492, 
			0.157305356, 0.001349611, 2.866515719E-7)
		"""

		parameters = [
			(1, (0.006209665, 0.060597536, 0.241730337, 0.382924923, 
				0.241730337, 0.060597536, 0.006209665)),
			(0.5, (2.866515719E-7, 0.001349611, 0.157305356, 0.682689492, 
				0.157305356, 0.001349611, 2.866515719E-7))
		]


		for sd, expected_output in parameters:
			output = get_normal_distribution(sd)
			for out_val, ex_val in zip(output, expected_output):
				with self.subTest(sd=sd, out=out_val, ex=ex_val):
					vals_close = isclose(out_val, ex_val, rel_tol=1e-04)
					self.assertTrue(vals_close)				



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

