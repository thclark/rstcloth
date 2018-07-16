.PHONY: dev tags test

dev: tags test

tags:
	@find . -name "*.py" | grep -v "\.\#" | etags --output TAGS -
	@echo [dev]: regenerated tags

nosetests:
	@echo "[testing] running nosetests"
	nosetests
ifeq ($(shell test -f /etc/arch-release && echo arch || echo Linux),arch)
	nosetests2
endif


pyflakes:
	@echo "[testing] running pyflakes:"
	pyflakes rstcloth

pycodestyle:
	@echo "[testing] running pycodestyle: "
	pycodestyle --max-line-length=100 rstcloth


test: nosetests pyflakes pycodestyle

pep8: pycodestyle

push-git:
	git push cyborg
	git push github
	git push github-tychoish

setup-git:
	git remote add cyborg gitosis@git.cyborginstitute.net:rstcloth.git
	git remote add github git@github.com:cyborginstitute/rstcloth.git
	git remote add github-tychoish git@github.com:tychoish/rstcloth.git

release:push-git
	python setup.py sdist upload
