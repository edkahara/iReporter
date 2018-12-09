[![Build Status](https://travis-ci.org/edkahara/iReporter.svg?branch=develop)](https://travis-ci.org/edkahara/iReporter) [![Coverage Status](https://coveralls.io/repos/github/edkahara/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/edkahara/iReporter?branch=develop) <a href="https://codeclimate.com/github/edkahara/iReporter/maintainability"><img src="https://api.codeclimate.com/v1/badges/c0b772db50ebe1ed6889/maintainability" /></a>

# iReporter

This is an iReporter web app. iReporter allows a user to report on corruption incidents and request government intervention. In order to use it, you must have a user account.

## How it works.

* Users can create accounts and log in.

* Users can view, create, edit and delete their reports.

* Users can create two types of reports:
  - red-flag report: This is a report in which a user reports an incidence of corruption. For instance, a user can report a bribery incident.

  - intervention report: This is a report in which a user reports an incident that requires government intervention. For instance, a user can report a flooding incident.

* In a report, a user can post and edit both the location of the incident and a comment on the incident.

* All stories are reviewed by administrators, who can either place them under investigation, resolve them or reject them.

## Installation and deployment.

### Clone this repository

  `git clone https://github.com/edkahara/iReporter.git`

### Set up a virtual environment and activate it

  `py -3 -m venv env`

### Create an env.bat file that using env.example as a template

### Activate the virtual environment

  `env.bat`

### Install dependencies needed

  `pip install -r requirements.txt`

### Run the application

  `flask run`

### Test the application

  `nosetests`

## Endpoints to test

Here are the API endpoints which you can test using either the heroku app link (https://edkahara-ireporter.herokuapp.com) or your local server using POSTMAN:

|    METHOD   |   ENDPOINT                                  | DESCRIPTION                           |    
|-------------|---------------------------------------------|---------------------------------------|
|   POST      |    /api/v1/auth/signup                      |   Sign a user up                      |
|   POST      |    /api/v1/auth/signup                      |   Log a user in                       |
|   POST      |    /api/v1/reports/                         |   Create a new report                 |
|   GET       |    /api/v1/reports/                         |   Fetch all existing reports          |
|   GET       |    /api/v1/reports/&lt;int:id&gt;           |   Fetch a specific report by its id   |
|   PATCH     |    /api/v1/reports/&lt;int:id&gt;/location  |   Edit a specific report's location   |
|   PATCH     |    /api/v1/reports/&lt;int:id&gt;/comment   |   Edit a specific report's comment    |
|   DELETE    |    /api/v1/reports/&lt;int:id&gt;           |   Delete a specific report            |

## API Docs

You can view the API documentation on https://documenter.getpostman.com/view/5360822/RzfiGTp4

# Author

Edward Njoroge
