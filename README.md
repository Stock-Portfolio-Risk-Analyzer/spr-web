# Stock Portfolio Risk Analysis Django Project

![travis ci button](https://travis-ci.org/Stock-Portfolio-Risk-Analyzer/spr-web.svg)
[![Coverage Status](https://coveralls.io/repos/github/Stock-Portfolio-Risk-Analyzer/spr-web/badge.svg?branch=develop)](https://coveralls.io/github/Stock-Portfolio-Risk-Analyzer/spr-web?branch=develop)
[![Documentation Status](https://readthedocs.org/projects/spr-web/badge/?version=latest)](http://spr-web.readthedocs.io/en/latest/?badge=latest)


Analyzes and displays the riskiness of your stock portfolio. A project for CS428 at UIUC.

## How to Use

1. Install Python 2.7.x
2. Create a new virtualenv (`virtualenv venv`)
3. Activate the virtualenv (`source venv/bin/activate`)
4. Change directories (`cd venv`)
5. Clone this repo (`git clone git@github.com:Stock-Portfolio-Risk-Analyzer/spr-web.git stockportfolio`)
6. Change directories (`cd stockportfolio`)
7. Run `pip install -r requirements.txt` to install dependencies
8. Run `python manage.py migrate` to bring in the existing database models
9. Run `python manage.py runserver 0.0.0.0:5000`
10. Connect to `localhost:5000` from your webbrowser to view the existing site

## Local Database Setup

Download and install PostgresSQL, including the development packages.
For details on how to do this, consult the PostgresSQL documentation for your
operating system or Linux distribution.

Then you must create a database called `spra` along with a user/password called `spra`.
Alternatively, you can change these settings in `stockportfolio/settings/local.py`

## Sort your Imports
`isort -rc --atomic .`

## Check for PEP-8 compatability
`flake8 stockportfolio`

## Setup for Portfolio Simulation

Optionally, you can configure the site to simulate portfolios for you.

1. `pip install -r simulation-requirements.txt`
    Note that there are several system requirements that must be met.
2. Set up the environment: `export MATPLOTLIB_AVAILABLE=YES`

## Generating Documentation

To autodoc/generate templates:
`sphinx-apidoc -f -o docs/ stockportfolio/ stockportfolio/api/migrations stockportfolio/settings`

To build the html pages:
`cd docs; make html`

An example of how methods should be documented:

```python
def get_stock_data(symbol, start_date=None, end_date=None):
    """
    Get OHLC stock data from Yahoo Finance for a single stock

    :param symbol: (string)
    :param start_date: (DateTime)
    :param end_date: (DateTime)
    :return: (DataFrame) of stock data from start_date to end_date
    """
```


## Contributors

- Rohan Kapoor
- Laurynas Tamulevicius
- Enrique Espaillat
- Alex Ashley
- Ronit Chakraborty
- Arpit Dev Mathur
- Shivam Gupta
- Thibaut Xiong









