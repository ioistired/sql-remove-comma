#!/usr/bin/env python3

import textwrap

import pytest
import sqlparse

from sql_remove_comma import remove_trailing_commas

def test_select():
	stmt = sqlparse.parse('select x, y, z, from tab')[0]
	assert str(remove_trailing_commas(stmt)) == 'select x, y, z from tab'

@pytest.mark.parametrize('s', (
	'select x, y, z from tab',
	'-- hi',
	'create table',  # invalid syntax, but sqlparse doesn't care so we need to make sure this is handled
	'with foo as (select 1), bar as (select 2) select 3',
	'with foo as (select 1),',
))
def test_only_illegal_commas_removed(s):
	stmt = sqlparse.parse(s)[0]
	assert str(remove_trailing_commas(stmt)) == s

def test_create_table():
	stmt = sqlparse.parse('create table foo (x integer not null, y text, primary key (x, y),)')[0]
	assert str(remove_trailing_commas(stmt)) == 'create table foo (x integer not null, y text, primary key (x, y))'

def test_multiple_select():
	stmt = sqlparse.parse('SELECT 0 AS a, b, c, FROM tab1 UNION ALL SELECT 1 AS a, b, c, FROM tab2')[0]
	assert str(remove_trailing_commas(stmt)) == \
		'SELECT 0 AS a, b, c FROM tab1 UNION ALL SELECT 1 AS a, b, c FROM tab2'

def test_cte():
	s = 'WITH x AS (SELECT foo FROM bar), y AS (SELECT baz FROM quux), SELECT garply FROM waldo'
	stmt = sqlparse.parse(s)[0]
	assert str(remove_trailing_commas(stmt)) == replace_right(s, ',', '', 1)

def replace_right(s, old, new, count=-1):
	return s[::-1].replace(old[::-1], new[::-1], count)[::-1]

def test_nested_func():
	stmt = sqlparse.parse('SELECT foo(bar(x, y, z,),)')[0]
	assert str(remove_trailing_commas(stmt)) == 'SELECT foo(bar(x, y, z))'
