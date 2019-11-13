import sqlparse

from . import remove_trailing_commas

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
		print(remove_trailing_commas(stmt))

if __name__ == '__main__':
	main()
