
from setuptools import setup
from pypandoc import convert_file

#: Converts the Markdown README in the RST format that PyPi expects.
long_description = convert_file('../README.md', 'rst')

setup(name='crispum',
      description='Declarative JSON data parsing pipeline',
      long_description=long_description,
      version='0.2.0',
      url='https://github.com/chrisinajar/crispum',
      author='Chris Vickery',
      author_email='chrisinajar@gmail.com',
      license='MIT',
      # classifiers=[
      #     'Development Status :: 4 - Beta',
      #     'Intended Audience :: System Administrators',
      #     'License :: OSI Approved :: Apache Software License',
      #     'Programming Language :: Python :: 3'
      # ],
      packages=['crispum'],
      install_requires=[
          'six>=1.10',
          'obstruction>=0.1.1',
          'dot-prop>=0.2.0',
      ]
    )
