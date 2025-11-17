# uHoo for Home Assistant

[![HACS Custom Repository][hacs-shield]][hacs]
[![GitHub Release][releases-shield]][releases]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE.md)

[![pre-commit.ci][pre-commit-ci-shield]][pre-commit-ci]
[![Build Status][build-shield]][build]

## About

Integrates support for the [uHoo](https://getuhoo.com/) air quality monitor into Home Assistant.

This integration is for uHoo home accounts.

![uHoo device view](dashboard.png)

## Installation

### HACS

Add `https://github.com/getuhoo/uhooair-homeassistant` as a custom integration repository and install the uHoo integration.

### Manual

Clone or download this repository, and copy the `custom_components/uhooair` directory into the `config/custom_components` directory of your Home Assistant instance. Restart Home Assistant.

## Configuration

Once installed, the uHoo integration is configured via the Home Assistant UI:

**Configuration** -> **Integrations** -> **Add** -> **uHoo (HACS)**

When prompted, enter your uHoo generated (API_KEY)

![uHoo Configuration](config.png)

## Setting up development environment

You need at least:

- Python 3.14+

First pull the repository and go inside the directory and create your own python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

To install all packages, including development dependencies:

```bash
pip install -r requirements.test.txt
```

This repository uses the [pre-commit][pre-commit] framework and all changes are formatted and linted prior to each commit. To run the checks manually:

```bash
pre-commit run --all-files
```

To run all project tests:

```bash
pytest
```
<!-- https://github.com/getuhoo/uhooair-homeassistant -->

[build-shield]: https://github.com/getuhoo/uhooair-homeassistant/actions/workflows/pythonpackage.yaml/badge.svg
[build]: https://github.com/getuhoo/uhooair-homeassistant/actions/workflows/pythonpackage.yaml
[hacs-shield]: https://img.shields.io/badge/HACS-Custom-orange.svg
[hacs]: https://hacs.xyz/
[license-shield]: https://img.shields.io/github/license/getuhoo/uhooair-homeassistant.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025
[pre-commit-ci-shield]: https://results.pre-commit.ci/badge/github/getuhoo/uhooair-homeassistant/main.svg
[pre-commit-ci]: https://results.pre-commit.ci/latest/github/getuhoo/uhooair-homeassistant/main
[pre-commit]: https://pre-commit.com/
[releases-shield]: https://img.shields.io/github/v/release/getuhoo/uhooair-homeassistant
[releases]: https://github.com/getuhoo/uhooair-homeassistant/releases
