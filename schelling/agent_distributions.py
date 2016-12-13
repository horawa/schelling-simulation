import scipy.integrate as integrate
import numpy as np
from math import exp, sqrt, pi

def get_uniform_distribution(agent_count):
	if agent_count < 1 or agent_count > 7:
		raise ValueError(
			"Only agent counts between 1 and 7 currently supported.")

	uniform_distribution = [1/agent_count] * agent_count
	return tuple(uniform_distribution)


def get_exponential_distribution(lambda_=1.0):
	if lambda_ <= 0:
		raise ValueError("lambda_ must be > 0")

	def exponential_dist_func(x):
		return lambda_*exp(-lambda_*x)

	max_agent_count = 7

	agent_fractions = []

	for agent in range(max_agent_count - 1):
		fraction = integrate.quad(exponential_dist_func, agent, agent + 1)[0]
		agent_fractions.append(fraction)

	agent = max_agent_count - 1
	last_fraction = integrate.quad(exponential_dist_func, agent, np.inf)[0]
	agent_fractions.append(last_fraction)

	return agent_fractions


def get_normal_distribution(std_dev):
	if std_dev <= 0:
		raise ValueError("std_dev must be > 0")

	mean = 4
	def normal_dist_func(x):
		n = (1/sqrt(2*pi*(std_dev**2))) * exp(-(((x-mean)**2)/(2*(std_dev**2))))
		return n

	# (1/sqrt(2*pi*(1^2))) * exp(-(((x-4)^2)/(2*(1^2))))

	max_agent_count = 7

	agent_fractions = []

	# -inf, 1.5
 	# 1.5, 2.5
	# 2.5, 3.5
	# 3.5, 4.5: mean +/- 0.5 
	# 4.5, 5.5
	# 5.5, 6.5
	# 6.5, inf

	agent = 0
	first_fraction = integrate.quad(normal_dist_func, -np.inf, 1.5)[0]
	agent_fractions.append(first_fraction)

	for agent in range(1, max_agent_count - 1):
		fraction = integrate.quad(normal_dist_func, agent + 0.5, agent + 1.5)[0]
		agent_fractions.append(fraction)

	agent = max_agent_count - 1
	last_fraction = integrate.quad(normal_dist_func, agent + 0.5, np.inf)[0]
	agent_fractions.append(last_fraction)

	return agent_fractions


def get_linear_distribution(agent_count):
	if agent_count < 1 or agent_count > 7:
		raise ValueError(
			"Only agent counts between 1 and 7 currently supported.")
		
	def linear_func(x):
		# 1 = agent_count * h / 2
		h = 2 / agent_count
		gradient = -h / agent_count
		return gradient * x + h

	agent_fractions = []
	for agent in range(agent_count):
		fraction = integrate.quad(linear_func, agent, agent + 1)[0]
		agent_fractions.append(fraction)

	return agent_fractions


def get_distribution_including_vacancies(vacancy_proportion, distribution):
	agent_proportion = 1.0 - vacancy_proportion
	agent_type_proporitons = \
		[p * agent_proportion for p in distribution]
	distribution_including_vacancies = \
		[vacancy_proportion] + agent_type_proporitons
	return tuple(distribution_including_vacancies)

