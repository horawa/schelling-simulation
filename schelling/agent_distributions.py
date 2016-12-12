def get_uniform_distribution(agent_count):
	if agent_count < 1 or agent_count > 7:
		raise ValueError(
			"Only agent counts between 1 and 7 currently supported.")

	uniform_distribution = [1/agent_count] * agent_count
	return tuple(uniform_distribution)


def get_distribution_including_vacancies(vacancy_proportion, distribution):
	agent_proportion = 1.0 - vacancy_proportion
	agent_type_proporitons = \
		[p * agent_proportion for p in distribution]
	distribution_including_vacancies = \
		[vacancy_proportion] + agent_type_proporitons
	return tuple(distribution_including_vacancies)
