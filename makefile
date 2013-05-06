push-git:setup-git
	git push cyborg
	git push github
	git push github-tychoish

.git/standard-config:.git/config

setup-git:.git/standard-config
	git remote add cyborg gitosis@git.cyborginstitute.net:rstcloth.git
	git remote add github git@github.com:cyborginstitute/rstcloth.git
	git remote add github-tychoish git@github.com:tychoish/rstcloth.git

tags:
	@find . -name "*.py" | grep -v "\.\#" | etags --output TAGS -
	@echo [dev]: regenerated tags

release:push-git
	python setup.py sdist upload
