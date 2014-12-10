from setuptools import setup, find_packages

version = '0.1.0'

setup(name='rcon_mc',
      version=version,
      description="Python wrapper for rcon connection to minecraft",
      long_description=open("README.md", "r").read(),
      classifiers=[
          "Topic :: Utilities",
          ],
      keywords='minecraft rcon python',
      author='MrPaws',
      author_email='paws@delimitize.com',
      url='http://github.com/mrpaws/python-rcon-mc',
      license='GNU',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      )
