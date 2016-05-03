.. Stock Portfolio Risk Analyzer documentation master file, created by
   sphinx-quickstart on Mon May 02 17:06:30 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Stock Portfolio Risk Analyzer!
=========================================================

Analyzes and displays the riskiness of your stock portfolio. A project for CS428 at UIUC.

How to Use
===========

1. Install Python 2.7.x
2. Create a new virtualenv (``virtualenv venv``)
3. Activate the virtualenv (``source venv/bin/activate``)
4. Change directories (``cd venv``)
5. Clone this repo (``git clone git@github.com:Stock-Portfolio-Risk-Analyzer/spr-web.git stockportfolio``)
6. Change directories (``cd stockportfolio``)
7. Run ``pip install -r requirements.txt`` to install dependencies
8. Run ``python manage.py migrate`` to bring in the existing database models
9. Run ``python manage.py runserver 0.0.0.0:5000``
10. Connect to ``localhost:5000`` from your webbrowser to view the existing site

Local Database Setup
=============

Download and install PostgresSQL, including the development packages. 
For details on how to do this, consult the PostgresSQL documentation for your 
operating system or Linux distribution. 

Then you must create a database called `spra` along with a user/password called `spra`.
Alternatively, you can change these settings in `stockportfolio/settings/local.py`

Sort your Imports
=============

``isort -rc --atomic .``

Check for PEP-8 compatability
=============

``flake8 stockportfolio``

Setup for Portfolio Simulation
=============

Optionally, you can configure the site to simulate portfolios for you.

1. ``pip install -r simulation-requirements.txt``
    Note that there are several system requirements that must be met.
2. Set up the environment: ``export MATPLOTLIB_AVAILABLE=YES``

Generating Documentation
=============

To autodoc/generate templates:
``sphinx-apidoc -f -o docs/ stockportfolio/ stockportfolio/api/migrations stockportfolio/settings``

To build the html pages:
``cd docs; make html``

An example of how methods should be documented: 

Contributors
=============


- Rohan Kapoor
- Laurynas Tamulevicius
- Enrique Espaillat
- Alex Ashley
- Ronit Chakraborty
- Arpit Dev Mathur
- Shivam Gupta
- Thibaut Xiong


.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

