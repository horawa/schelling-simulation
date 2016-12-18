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
	install_requires=[
		"numpy>=1.12.0b1,<2.0.0",
		"scipy>=0.18.1,<1.0.0",
		"matplotlib>=1.5.3,<2.0.0",
		"scikit-image>=0.12.3,<1.0.0",
		"click>=6.6,<7.0",
	],
	include_package_data=True,
	zip_safe=False,
    scripts=['bin/run-simulation'],
	entry_points = {
		'console_scripts': ['schelling-cli=schelling.cli:simulation'],
	}
)