from functools import wraps
from math import isclose
from schelling.neighborhood import get_unlike_neighbor_fraction


def range_check_0_1(function):
	"""Raises value error, if range of first argument is not in [0, 1]"""

	@wraps(function)
	def checked_function(*args, **kwargs):

		value=args[0]
		if value < 0.0 or value > 1.0:
			raise ValueError("Argument must be between 0.0 and 1.0. Given: " + 
				str(value))

		return function(*args, **kwargs)

	return checked_function


@range_check_0_1
def create_flat_utility(threshold):
	"""Creates a flat utility function with the specified threshold of unlike 
		neighbors.
	Flat utility: u(t) = 1, if t <= threshold; 0, if t > threshold
	
	Args:
	    threshold (float): threshold - in range [0.0, 1.0]
	
	Returns:
	    function: utility function
	"""

	@range_check_0_1
	def flat_utility(unlike_neighbor_fraction):

		if unlike_neighbor_fraction <= threshold:
			return 1.0
		else:
			return 0.0
	
	return flat_utility


@range_check_0_1
def create_peaked_utility(peak, cutoff=False):
	"""Creates peaked utility function with 
	peak value at specified fraction of unlike neighbors and optional cutoff
	Peaked utility without cutoff:
		u(t) = (1 / peak) * t, if t < peak; 
				1 - (1/(1-peak))*(t - peak), if t >= peak

	Peaked utility with cutoff:
		u(t) = (1 / peak) * t, if t <= peak; 0, if t >= peak

	Args:
	    peak (float): Utility function peaks at this argument - in range [0, 1]
	    cutoff (bool, optional): Sets cutoff behavior
	
	Returns:
	    function: utility function
	"""

	try:
		left_gradient = 1 / peak
	except ZeroDivisionError:
		left_gradient = 1.0
	
	try:
		right_gradient = (-1 / (1 - peak))
	except ZeroDivisionError:
		right_gradient = 1.0

	@range_check_0_1
	def peaked_utility(unlike_neighbor_fraction):
		if unlike_neighbor_fraction < peak:
			return left_gradient * unlike_neighbor_fraction
		else:
			return (right_gradient * (unlike_neighbor_fraction - peak)) + 1

	@range_check_0_1
	def peaked_utility_cutoff(unlike_neighbor_fraction):
		if unlike_neighbor_fraction <= peak:
			return left_gradient * unlike_neighbor_fraction
		else:
			return 0.0

	if cutoff:
		return peaked_utility_cutoff
	else:
		return peaked_utility


@range_check_0_1
def create_spiked_utility(spike):
	"""Create spiked utility function with spike at specified fraction of 
		unlike neighbors
	u(t) = 1, if t = spike; 0, otherwise
	
	Args:
	    spike (float): Spike at this argument - in range [0, 1]
	
	Returns:
	    function: utility function
	"""
	@range_check_0_1
	def spiked_utility(unlike_neighbor_fraction):
		if isclose(unlike_neighbor_fraction, spike, abs_tol=1e-7):
			return 1.0
		else:
			return 0.0

	return spiked_utility


def get_utility_for_array(utility_function, array, count_vacancies=False, radius=1):
	"""A wrapper for utility functions.
	The returned function gets unlike neighbor fraction for specified index
	in array and optionally agent type and returns the value to the utility 
		function.
	
	Args:
	    utility_function (callable): function to wrap - (0, 1) -> (0, 1)
	    array (ndarray): array
	
	Returns:
	    function: wrapped utility function
	"""
	def utility(index, agent_type=None):
		return utility_function(get_unlike_neighbor_fraction(array, index, 
			radius=radius, agent_type=agent_type, 
			count_vacancies=count_vacancies))
	
	return utility


