[![Build Status](https://travis-ci.org/andela-landia/bucket-list-application-api.svg?branch=develop)](https://travis-ci.org/andela-landia/bucket-list-application-api)
[![Coverage Status](https://coveralls.io/repos/github/andela-landia/bucket-list-application-api/badge.svg?branch=develop)](https://coveralls.io/github/andela-landia/bucket-list-application-api?branch=develop)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/251f29933e7d47dca535a64221b3f1f7)](https://www.codacy.com/app/loice-andia/bucket-list-application-api_2?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=andela-landia/bucket-list-application-api&amp;utm_campaign=Badge_Grade)
[![Code Health](https://landscape.io/github/andela-landia/bucket-list-application-api/develop/landscape.svg?style=flat)](https://landscape.io/github/andela-landia/bucket-list-application-api/develop)
[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)
# Bucket List API
Flask API for a bucket list service.

## Installation and setup

Clone this repo:

` https://github.com/andela-landia/bucket-list-application-api.git ` 

Navigate to the `bucket-list-application-api` directory:

` cd bucket-list-application-api ` 

Create a virtual environment and activate it.

` mkvirtualenv Bucketlist`
` workon Bucketlist `

Install dependencies:

` pip install -r requirements.txt `

Initialize, migrate and update the database:

` python run.py db init `
` python run.py db migrate `
` python run.py db upgrade `

Test the application by running:

` tox ` 

## Usage

To start the app:

` python run.py runserver `

Access the endpoints using your preferred client e.g Postman

### Endpoints

| Resource URL | Methods | Description | Requires Token |
| -------- | ------------- | --------- |--------------- |
| `/api/v1/auth/register` | POST  | User registration | FALSE |
| `/api/v1/auth/login` | POST | User login | FALSE |
| `/api/v1//bucketlists` | GET, POST | A user's bucket lists | TRUE |
| `/api/v1/bucketlists/<bucketlist_id>` | GET, PUT, DELETE | A single bucket list | TRUE |
| `/api/v1/bucketlists/<bucketlist_id>/items` | GET, POST | Items in a bucket list | TRUE |
| `/api/v1/bucketlists/<bucketlist_id>/items/<item_id>` | GET, PUT, DELETE | A single bucket list item | TRUE |

### Options

| Key | Description|
|-----| -----------|
| ?q | Enter a search parameter |
| ?limit | Number of items per page(default is 20) |

| Method | Description |
|------- | ----------- |
| GET | Retrieves a resource(s) |
| POST | Creates a new resource |
| PUT | Updates an existing resource |
| DELETE | Deletes an existing resource |