import unittest
from math import isclose

from ..agent_distributions import (get_uniform_distribution, 
	get_exponential_distribution,
	get_normal_distribution, get_linear_distribution,
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
			((1,), (0.63212, 0.23254, 0.085548, 0.031471, 0.011578, 
				0.0042592, 0.0024788)),
			((2,), (0.86466, 0.11702, 0.015837, 0.0021433, 0.00029006, 
				0.000039256, 6.1442e-6))
		]

		self.check_distribution_expected_output(get_exponential_distribution, 
			parameters)


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
			((1,), (0.006209665, 0.060597536, 0.241730337, 0.382924923, 
				0.241730337, 0.060597536, 0.006209665)),
			((0.5,), (2.866515719E-7, 0.001349611, 0.157305356, 0.682689492, 
				0.157305356, 0.001349611, 2.866515719E-7))
		]

		self.check_distribution_expected_output(get_normal_distribution, 
			parameters)		


	def test_get_linear_distribution(self):
		parameters = [
			((1,), [1,]),
			((2,), [0.75, 0.25]),
			((3,), [5/9, 1/3, 1/9]),
			((4,), [0.4375, 0.3125, 0.1875, 0.0625]),
			((5,), [0.36, 0.28, 0.2, 0.12, 0.04]),
			((6,), [0.305555556, 0.25, 0.194444444, 0.138888889, 0.083333333, 
				0.027777778]),
			((7,), [0.265306122, 0.224489796, 0.183673469, 0.142857143, 
				0.102040816, 0.06122449, 0.020408163]),
		]

		self.check_distribution_expected_output(get_linear_distribution,
			parameters)


	def test_validation(self):
		parameters = [
			(get_uniform_distribution, [(0,), (-10,), (8,), (100,)]),
			(get_linear_distribution, [(0,), (-10,), (8,), (100,)]),
			(get_normal_distribution, [(0,), (-10,), (-50,), (-100,)]),
			(get_exponential_distribution, [(0,), (-10,), (-50,), (-100,)]),
		]

		for function, params_list in parameters:
			for params in params_list:
				with self.subTest(f=function, p=params):
					with self.assertRaises(ValueError):
						function(*params)


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

			for out_val, ex_val in zip(output, expected_output):
				with self.subTest(f=function, p=args, out=out_val, ex=ex_val):
					vals_close = isclose(out_val, ex_val, rel_tol=1e-04)
					self.assertTrue(vals_close)	
			with self.subTest(f=function, name='sum to 1'):
				self.assertAlmostEqual(sum(output), 1.0)

