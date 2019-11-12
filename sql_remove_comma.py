#!/usr/bin/env python3

import sqlparse

def enumerate_reversed(seq):
	return zip(reversed(range(len(seq))), reversed(seq))

def remove_trailing_comma(stmt):
	for outer_tok in stmt.tokens:
		if not isinstance(outer_tok, sqlparse.sql.IdentifierList):
			continue

		for i, tok in enumerate_reversed(outer_tok.tokens):
			if tok.ttype is sqlparse.tokens.Token.Punctuation and tok.value == ',':
				del outer_tok.tokens[i]
				return

def lines_to_statements(it):
	buf = []
	for line in it:
		buf.append(line)
		stmts = sqlparse.parse(''.join(buf))
		if len(stmts) > 1:
			yield stmts[0]
			last_line = buf[-1]
			buf.clear()
			buf.append(last_line)

def main():
	import sys
	for stmt in lines_to_statements(sys.stdin):
		remove_trailing_comma(stmt)
		print(stmt)

if __name__ == '__main__':
	main()
