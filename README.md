# PythonPackageTemplate

[![docs (development version)](https://img.shields.io/badge/docs-dev-blue.svg)](https://github.com/robert-lieck/PythonPackageTemplate/)

![build](https://github.com/robert-lieck/PythonPackageTemplate/workflows/build/badge.svg)
[![PyPI version](https://badge.fury.io/py/PythonPackageTemplate.svg)](https://badge.fury.io/py/PythonPackageTemplate)

[![test_main](https://github.com/robert-lieck/PythonPackageTemplate/actions/workflows/test_main.yml/badge.svg)](https://github.com/robert-lieck/PythonPackageTemplate/actions/workflows/test_main.yml)
[![codecov](https://codecov.io/gh/robert-lieck/PythonPackageTemplate/branch/master/graph/badge.svg)](https://codecov.io/gh/robert-lieck/PythonPackageTemplate)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


A template repo for Python packages featuring:
- main/dev branch workflow
- unittests
- publishing on pypi
- building docu
- generating code coverage reports

## How To

To create a new Python package from this template, start by cloning this repo (or use it as a template when creating a new repo on GitHub) and then follow the procedure outlined below.

### Badges README

The `README.md` is obviously specific to your project, but you might want to reuse the badges at the top... TODO

### Package Name

The example package provided by this repo is named `PythonPackageTemplate` and this name appears in many locations. Therefore, the first step is to replace all occurrences by the name of your package. In particular, you have to rename the folder `PythonPackageTemplate` accordingly and replace all occurrences in the following files (this is described in more detail in the respective sections below):
- `setup.py`
- `tests/test_template.py`
- `.github/workflows/tests_main.yml`
- `.github/workflows/test_dev.yml`
- `docs/conf.py`
- `docs/index.rst`
- `docs/api_summary.rst`

### Folder Structure

* Your source code goes into the `PythonPackageTemplate` directory (after renaming it to your package name).
* Your unittests go into the `test` directory.
* Your documentation goes into the `docs` directory.
* The `.github` folder contains workflows for GitHub actions.

### Adapt `requirements.txt` and `setup.py`

List all required Python packages in `requirements.txt`.

In `setup.py` replace the following:
- `PythonPackageTemplate`: replace with the name of your package
- `version="..."`: the version of your package
- `author="..."`: your name
- `author_email="..."`: your email
- `description="..."`: a short description of the package
- `url="..."`: the URL of the repo
- `python_requires="..."`: the Python version requirement for your package

Moreover, in the `classifiers` argument, you may want to adapt the following to your liking:
- `Programming Language :: Python :: 3`
- `License :: OSI Approved :: GNU General Public License v3 (GPLv3)`
- `Operating System :: OS Independent`

If you change the license information, you probably also want to adapt the `LICENSE` file and the badge at the top of the `README.md`.

### GitHub Actions

GitHub actions are defined in the `*.yml` files in the `.github/workflows` directory. There are predefined actions to
- run tests on the `main` and `dev` branch
- publish the package on [pypi.org](https://pypi.org/)
- build the documentation

#### Tests

Adapt the `test_main.yml` and `test_dev.yml` by replacing the following:
- `python-version: [...]`: Python versions to run the tests for (e.g. `["3.6", "3.7", "3.8", "3.9"]`)
- `PythonPackageTemplate`: the name of your package chosen above
- `bash <(curl -s https://codecov.io/bash -t <codecov_token>)`: your [codecov.io](https://about.codecov.io/) token (comment out if you do not want to use codecov.io)

Of course, you would want to replace the `test_template.py` file with some real tests for you package (at least, you have to replace `PythonPackageTemplate` with your package name).

The GitHub actions for running tests on the `main` and `dev` branch are almost identical. The only differences are:
- their name (used to display in the web interface)
- the branch name (adapt if you use different names)
- the `workflow_dispatch` statement (only for `dev`) that allows to manually trigger execution
- the line for publishing the code coverage results (only for `main`)

The tests run on `push` and `pull_request` events of the respective branch, for `dev` they can additionally be triggered manually.

#### PyPi

You do not need to adapt the `publish.yml` file, the action is triggered when a new `release` is created (or manually). However, the two lines
- `TWINE_USERNAME: __token__`
- `TWINE_PASSWORD: ${{ secrets.PYPI_PASSWORD }}`

require you to setup... TODO

#### Documentation

The `docs` folder contains a skeleton documentation using the [Read the Docs Sphinx Theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/) that you can adapt to your needs. You should replace the following:
- in `conf.py`, `index.rst`, `api_summary.rst`
  - replace `PythonPackageTemplate` with your package name
- in `conf.py` adapt the following:
  - `project = 'PythonPackageTemplate'`
  - `copyright = '...'`
  - `author = '...'`


For local builds, you can run `make` commands in the `docs` directory (you will have to install in packages specified in `docs/requirements.txt`), in particular
- `make html`: builds the documentation
- `make doctest`: runs all code examples in the documentation and checks if the actual output matches the one shown in the documentation
- `make clean`: remove all built files (except `_autosummary`, see below)
- `make help`: get information about available make commands.

To automatically generate a detailed API, the Sphinx extension `autosummary` is used, which may cause some trouble:
- You may get `WARNING: duplicate object description ...` warnings.
- The generated files are stored inside `_autosummary`, which is not cleaned up by `make clean`, so you have to manually remove those files.