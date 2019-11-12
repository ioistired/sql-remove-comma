#!/usr/bin/env python3

import ast
import setuptools

with open('sql_remove_comma.py') as f:
	mod = ast.parse(f.read())
	for stmt in mod.body:
		if (
			isinstance(stmt, ast.Assign)
			and any(isinstance(target, ast.Name) and target.id == '__version__' for target in stmt.targets)
		):
			VERSION = stmt.value.s
			break
	else:
		raise RuntimeError('version is not defined')

setuptools.setup(
	name='sql-remove-comma',
	use_scm_version=True,
	author='Io Mintz',
	author_email='io@mintz.cc',
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	py_modules=['sql_remove_comma'],
	setup_requires=['setuptools_scm'],
	install_requires=['sqlparse>=0.3.0,<0.4.0'],
)
