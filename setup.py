from setuptools import setup
from setuptools.command.install import install as InstallCommand
import pip


class Install(InstallCommand):
	"""Install requirements with pip, install_requires causes bugs
	with numpy/scipy"""

	def run(self, *args, **kwargs):
		pip.main(['install', '.'])
		InstallCommand.run(self, *args, **kwargs)


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
	scripts=['bin/run-simulation', 'bin/run-v-T', 
		'bin/verify_simulations_halted', 'bin/get_results'],
	entry_points={
		'console_scripts': ['schelling-cli=schelling.cli:simulation'],
	},
	cmdclass={
		'install': Install,
	}
)