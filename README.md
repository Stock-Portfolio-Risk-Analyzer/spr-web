# Stock Portfolio Risk Analysis Django Project

![travis ci button](https://travis-ci.org/Stock-Portfolio-Risk-Analyzer/spr-web.svg)

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

## Sort your Imports
`isort -rc --atomic .`

## Setup for Portfolio Simulation

Optionally, you can configure the site to simulate portfolios for you.

1. `pip install -r simulation-requirements.txt`
    Note that there are several system requirements that must be met.
2. Set up the environment: `export MATPLOTLIB_AVAILABLE=YES`

If you encounter a segfault when using the portfolio simulation feature, you may need to set matplotlib's backend directly. 

Find `matplotlibrc` and overwrite the current backend setting with `backend : agg`

