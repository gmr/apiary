DATABASE=data/dev.sqlite3

cli:
	@python -c "from apiary.tools import cli; cli.main()"

setup:
	@-rm ${DATABASE}
	@python -c "from apiary.tools import setup; setup.main('${DATABASE}')"

teardown:
	rm ${DATABASE}
