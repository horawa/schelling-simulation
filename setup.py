from setuptools import setup

def readme():
	with open('README.md') as readme:
		return readme.read()


setup(
	name='Schelling Simulation',
	version='0.1',
	description='Simulation of the Schelling model of segregation',
	long_description=readme(),
	url='https://github.com/horawa/schelling-simulation',
	author='Stas Horawa',
	author_email='stashorawa@gmail.com',
	packages=['schelling'],
	include_package_data=True,
	zip_safe=False,
    scripts=['bin/run-simulation'],
	entry_points = {
		'console_scripts': ['schelling-cli=schelling.cli:simulation'],
	}
)