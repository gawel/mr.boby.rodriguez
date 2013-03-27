from setuptools import setup
from setuptools import find_packages

version = '0.1.dev0'

setup(name='mr.boby.rodriguez',
      version=version,
      description="mr.boby.rodriguez package",
      long_description=open('README.rst').read(),
      classifiers=[
          'Intended Audience :: Developers',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.3',
          'License :: OSI Approved :: MIT License',
      ],
      keywords='',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='https://github.com/gawel/mr.boby.rodriguez/',
      license='MIT',
      packages=find_packages(exclude=['docs', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      extras_require={
        'test': ['nose'],
      },
      entry_points="""
      [console_scripts]
      #mrbobyrodriguez = mrbobyrodriguez.scripts:main
      """,
      )
