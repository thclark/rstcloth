![cd](https://github.com/thclark/rstcloth/actions/workflows/cd.yml/badge.svg)
[![codecov](https://codecov.io/gh/thclark/rstcloth/branch/main/graph/badge.svg)](https://codecov.io/gh/thclark/rstcloth)
[![PyPI version](https://badge.fury.io/py/rstcloth.svg)](https://badge.fury.io/py/rstcloth)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
[![Documentation Status](https://readthedocs.org/projects/rstcloth/badge/?version=latest)](https://rstcloth.readthedocs.io/en/latest/?badge=latest)

# RstCloth

reStructuredText is a powerful human-centric markup language that is
well defined, flexible, with powerful tools that make writing and
maintaining text easy and pleasurable. Humans can edit
reStructuredText without the aide of complex editing tools, and the
resulting source is easy to manipulate and process.

As an alternative and a supplement, RstCloth is a Python API for
writing well formed reStructuredText programatically.

Find the [project documentation here](https://rstcloth.readthedocs.io)

## Developer notes

Repo is based on [thclark/python-library-template](https://github.com/thclark/python-library-template):

- vscode `.devcontainer`
- black style
- sphinx docs with some examples and automatic build
- pre-commit hooks
- tox tests
- github actions ci + cd
- code coverage

### Using VSCode

Check out the repo and use the remote `.devcontainer` to start developing, with everything installed out of the box.

### In other IDEs

Use `poetry --extras docs` to install the project and get started. You also You need to install pre-commit to get the hooks working. Do:

```
pip install pre-commit
pre-commit install && pre-commit install -t commit-msg
```

Once that's done, each time you make a commit, a wide range of checks are made and the project file formats are applied.

Upon failure, the commit will halt. **Re-running the commit will automatically fix most issues** except:

- The flake8 checks... hopefully over time Black (which fixes most things automatically already) will negate need for it.
- You'll have to fix documentation yourself prior to a successful commit (there's no auto fix for that!!).

You can run pre-commit hooks without making a commit, too, like:

```
pre-commit run black --all-files
```

or

```
# -v gives verbose output, useful for figuring out why docs won't build
pre-commit run build-docs -v
```

### Contributing

- Please raise an issue on the board (or add your \$0.02 to an existing issue) so the maintainers know
  what's happening and can advise / steer you.

- Create a fork of rstcloth, undertake your changes on a new branch, (see `.pre-commit-config.yaml` for branch naming conventions).

- To make life easy for us, use our conventional commits pattern (if you've got pre-commit installed correctly, it'll guide you on your first commit) to make your commits (if not, we'll try to preserve your history, but might have to squashmerge which would lose your contribution history)

- Adopt a Test Driven Development approach to implementing new features or fixing bugs.

- Ask the `rstcloth` maintainers _where_ to make your pull request. We'll create a version branch, according to the
  roadmap, into which you can make your PR. We'll help review the changes and improve the PR.

- Once checks have passed, test coverage of the new code is >=95%, documentation is updated and the Review is passed, we'll merge into the version branch.

### Release process

Releases are automated using conventional-commits and GitHub Actions.

## Documents

### Building documents automatically

In the VSCode `.devcontainer`, the RestructuredText extension should build the docs live for you (right click the `.rst` file and hit "Open Preview").

On each commit, the documentation will build automatically in a pre-configured environment. The way pre-commit works, you won't be allowed to make the commit unless the documentation builds,
this way we avoid getting broken documentation pushed to the main repository on any commit sha, so we can rely on
builds working.

### Building documents manually

**If you did need to build the documentation**

Install `doxgen`. On a mac, that's `brew install doxygen`; other systems may differ.

Install sphinx and other requirements for building the docs:

```
poetry install --extras docs
```

Run the build process:

```
sphinx-build -b html docs/source docs/build
```
