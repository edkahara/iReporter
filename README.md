# iReporter [![Build Status](https://travis-ci.org/edkahara/iReporter.svg?branch=develop)](https://travis-ci.org/edkahara/iReporter) [![Coverage Status](https://coveralls.io/repos/github/edkahara/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/edkahara/iReporter?branch=develop)
This is an iReporter web app.

Here are the API endpoints which you must add to the heroku app link (https://edkahara-ireporter.herokuapp.com/):

GET all records: /api/v1/red-flags

GET specific record: /api/v1/red-flags/<id>

POST a record: /api/v1/red-flags

Edit a record's location: /api/v1/red-flags/<id>/location

Edit a record's comment: /api/v1/red-flags/<id>/comment

Delete a record: /api/v1/red-flags/<id>
