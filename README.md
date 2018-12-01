# iReporter [![Build Status](https://travis-ci.org/edkahara/iReporter.svg?branch=develop)](https://travis-ci.org/edkahara/iReporter) [![Coverage Status](https://coveralls.io/repos/github/edkahara/iReporter/badge.svg?branch=develop)](https://coveralls.io/github/edkahara/iReporter?branch=develop)
This is an iReporter web app.

Here are the API endpoints which you must add to the heroku app link (https://edkahara-ireporter.herokuapp.com/) when using POSTMAN:

GET all records: /api/v1/red-flags

GET a specific record: /api/v1/red-flags/&lt;id&gt;

POST (create) a new record: /api/v1/red-flags

PATCH (edit) a specific record's location: /api/v1/red-flags/&lt;id&gt;/location

PATCH (edit) a specific record's comment: /api/v1/red-flags/&lt;id&gt;/comment

DELETE a specific record: /api/v1/red-flags/&lt;id&gt;
