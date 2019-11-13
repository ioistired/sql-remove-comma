#!/usr/bin/env python3

import setuptools

setuptools.setup(
	name='sql-remove-comma',
	description='remove illegal trailing commas from your SQL code',
	use_scm_version=True,
	author='Io Mintz',
	author_email='io@mintz.cc',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	license='BSD-2-Clause-Patent',
	packages=['sql_remove_comma'],
	setup_requires=['setuptools_scm'],
	install_requires=['sqlparse>=0.3.0,<0.4.0'],
	extras_require={
		'test': [
			'pytest',
			'pytest-cov',
		],
	},
	entry_points={
		'console_scripts': [
			'sql-remove-comma = sql_remove_comma.__main__:main',
		],
	},
	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Programming Language :: Python :: 3.9',
		'Topic :: Database',
		'Topic :: Software Development :: Pre-processors',
		'Topic :: Utilities',
	],
)
