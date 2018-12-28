[![Build Status](https://travis-ci.org/edkahara/iReporter.svg?branch=develop-v2)](https://travis-ci.org/edkahara/iReporter) [![Coverage Status](https://coveralls.io/repos/github/edkahara/iReporter/badge.svg?branch=develop-v2)](https://coveralls.io/github/edkahara/iReporter?branch=develop-v2) <a href="https://codeclimate.com/github/edkahara/iReporter/maintainability"><img src="https://api.codeclimate.com/v1/badges/c0b772db50ebe1ed6889/maintainability" /></a>

# iReporter

This is an iReporter web app. iReporter allows a user to report on corruption incidents and request government intervention. In order to use it, you must have a user account.

## How it works.

* Users can create accounts and log in.

* Users can create, edit, or delete their reports.

* Users can create two types of reports:
  - red-flag report: This is a report in which a user reports an incidence of corruption. For instance, a user can report a bribery incident.

  - intervention report: This is a report in which a user reports an incident that requires government intervention. For instance, a user can report a flooding incident.

* In a report, a user can post and edit both the location of the incident and a comment on the incident.

* All stories are reviewed by administrators, who can either place them under investigation, resolve them or reject them.

## Installation and deployment.

### Create two postgresql databases

  Create two postgresql databases, one for the app and one for testing, which you will use during this deployment.

### Clone this repository

  `git clone https://github.com/edkahara/iReporter.git`

### Set up a virtual environment

  `python3 - m venv env`

## Create a .env file in the root directory and fill it with details using .env.example as a template. Then type:

  `source .env`

### Install dependencies needed

  `pip install -r requirements.txt`

### Run the application

  `flask run`

### Test the application

  `nosetests --with-coverage --cover-package=app`

## Endpoints to test

Here are the API endpoints which you can test using either the heroku app link (https://edkahara-ireporter-v2.herokuapp.com/) or your local server using POSTMAN:

|    METHOD   |   ENDPOINT                                                 | DESCRIPTION                             |    
|-------------|------------------------------------------------------------|-----------------------------------------|
|   POST      |    /api/v2/auth/signup                                     |   Sign a user up                        |
|   POST      |    /api/v2/auth/login                                      |   Log a user in                         |
|   DELETE    |    /api/v2/auth/logout                                     |   Log a user out                        |
|   POST      |    /api/v2/reports/                                        |   Create a new report                   |
|   GET       |    /api/v2/reports/                                        |   Fetch all reports                     |
|   GET       |    /api/v2/reports/red-flags                               |   Fetch all red-flag reports            |
|   GET       |    /api/v2/reports/interventions                           |   Fetch all intervention reports        |
|   GET       |    /api/v2/users/&lt;username&gt;/reports                  |   Fetch a user's reports                |
|   GET       |    /api/v2/users/&lt;username&gt;/reports/red-flags        |   Fetch a user's red-flag reports       |
|   GET       |    /api/v2/users/&lt;username&gt;/reports/interventions    |   Fetch a user's intervention reports   |
|   GET       |    /api/v2/reports/&lt;int:id&gt;                          |   Fetch a specific report by its id     |
|   PATCH     |    /api/v2/reports/&lt;int:id&gt;/location                 |   Edit a specific report's location     |
|   PATCH     |    /api/v2/reports/&lt;int:id&gt;/comment                  |   Edit a specific report's comment      |
|   PATCH     |    /api/v2/reports/&lt;int:id&gt;/status                   |   Edit a specific report's status       |
|   DELETE    |    /api/v2/reports/&lt;int:id&gt;                          |   Delete a specific report              |

## API Documentation

You can view the API documentation on https://ireporterv2.docs.apiary.io/

# Author

Edward Njoroge
