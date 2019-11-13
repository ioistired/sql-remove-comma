#!/usr/bin/env python3

import sqlparse
import sqlparse.sql

def enumerate_reversed(seq):
	return zip(reversed(range(len(seq))), reversed(seq))

def is_comma(tok):
	return tok.ttype is sqlparse.tokens.Token.Punctuation and tok.value == ','

def remove_trailing_commas(stmt: sqlparse.sql.Statement) -> sqlparse.sql.Statement:
	"""Remove trailing commas in place from the given statement.
	Return the statement for convenience in larger expressions.
	"""
	seen = set()
	fix_extraneous_identifierlist(stmt)
	for tok in stmt.flatten():
		if (
			tok.parent not in seen
			and isinstance(tok.parent, (sqlparse.sql.IdentifierList, sqlparse.sql.Parenthesis))
		):
			_remove_trailing_comma(tok.parent)
			seen.add(tok.parent)

	return stmt

def _remove_trailing_comma(tok):
	outer_tok = tok
	for i, tok in enumerate_reversed(outer_tok.tokens):
		if is_trailing_comma(i, tok):
			del outer_tok.tokens[i]
			return

def fix_extraneous_identifierlist(stmt):
	"""remove extraneous identifier lists from a create table statement (workaround for #521)"""
	createtable = find_createtable(stmt)
	if not createtable:
		return

	i, tok = createtable
	try:
		func = next(tok for tok in stmt.tokens[i+1:] if isinstance(tok, sqlparse.sql.Function))
	except StopIteration:
		return

	_, par = func.token_next(0, skip_cm=True)

	for i, tok in enumerate(par.tokens):
		if isinstance(tok, sqlparse.sql.IdentifierList):
			par.tokens[i:i+1] = tok.tokens

def find_createtable(stmt):
	if not isinstance(stmt, sqlparse.sql.Statement):
		return False

	tok = stmt.token_first(skip_cm=True)
	i, next = stmt.token_next(stmt.token_index(tok), skip_cm=True)
	return (
		isinstance(stmt, sqlparse.sql.Statement)
		and (tok.ttype, tok.value.upper()) == (sqlparse.tokens.Token.Keyword.DDL, 'CREATE')
		and (next.ttype, next.value.upper()) == (sqlparse.tokens.Token.Keyword, 'TABLE')
		and (i, next)
	)

def is_trailing_comma(i, tok):
	_, next_tok = tok.parent.token_next(i, skip_cm=True)
	if next_tok == tok.parent.tokens[-1] and not isinstance(next_tok, sqlparse.sql.Identifier) and is_comma(tok):
		print(repr(next_tok))
		print(tok.parent.tokens)
		print(next_tok == tok.parent.tokens[-1])
		print(type(next_tok))
		return True

def lines_to_statements(it):
	import io
	buf = io.StringIO()
	for line in it:
		buf.write(line)
		stmts = sqlparse.parse(buf.getvalue())
		if len(stmts) > 1 and str(stmts[1]).strip():
			yield stmts[0]
			buf.seek(0); buf.truncate()
			for trailing_stmt in sqlparse.split(line):
				buf.write(str(trailing_stmt))
				buf.write('\n')

	yield from sqlparse.parse(buf.getvalue())

def main():
	import sys
	for stmt in lines_to_statements(sys.stdin):
		remove_trailing_commas(stmt)
		print(stmt)

if __name__ == '__main__':
	main()
