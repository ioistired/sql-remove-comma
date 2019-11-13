# sql-remove-comma

[![Tests Status](https://img.shields.io/travis/iomintz/sql-remove-comma/master.svg?label=tests)](https://travis-ci.org/iomintz/sql-remove-comma)
[![Coverage Status](https://coveralls.io/repos/github/iomintz/sql-remove-comma/badge.svg?branch=master)](https://coveralls.io/github/iomintz/sql-remove-comma?branch=master)

Dumb command line script that removes illegal trailing commas from your SQL code.

Intended as a preprocessor for SQL that allows you to use trailing commas like you should be able to.
This makes diffs easier.

## Usage

```
$ sql-remove-comma
$ cat queries.sql
SELECT
	x,
	y,
	z,
FROM tab;

	SELECT
		0 AS sort_order,
		x,
		y,
		z,
	FROM tab1
UNION ALL
	SELECT
		1 AS sort_order,
		a,
		b,
		c,
	FROM tab2
$ sql-remove-comma < queries.sql
SELECT 
	x,
	y,	
	z
FROM tab;
SELECT
		0 AS sort_order,
		x,
		y,
		z
	FROM tab1
UNION ALL
	SELECT
		1 AS sort_order,
		a,	
		b,
		c
	FROM tab2 
```

## License

BSD 2-clause + Patent. See the LICENSE file in this repository for details.
