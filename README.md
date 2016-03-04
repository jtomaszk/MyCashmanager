#MyCashmanager

[![Build Status](https://travis-ci.org/jtomaszk/MyCashmanager.svg?branch=master)](https://travis-ci.org/jtomaszk/MyCashmanager)
[![codecov.io](https://codecov.io/github/jtomaszk/MyCashmanager/coverage.svg?branch=master)](https://codecov.io/github/jtomaszk/MyCashmanager?branch=master)
[![Dependency Status](https://gemnasium.com/jtomaszk/MyCashmanager.svg)](https://gemnasium.com/jtomaszk/MyCashmanager)
[![Code Climate](https://codeclimate.com/github/jtomaszk/MyCashmanager/badges/gpa.svg)](https://codeclimate.com/github/jtomaszk/MyCashmanager)
[![Issue Count](https://codeclimate.com/github/jtomaszk/MyCashmanager/badges/issue_count.svg)](https://codeclimate.com/github/jtomaszk/MyCashmanager)

Personal accounting web application written in Python Flask & AngularJS.


##Configuration

Create in root of app file `secret.prop`

```ini
[GoogleOAuth] 
GOOGLE_ID=insert_id
GOOGLE_SECRET=insert_secret
[App]
TOKEN_SECRET=insert_random_string
```

##Run on Heroku
### Configuring heroku
set Config Variables:
```
DATABASE_URL postgres://...
ENV_MODE true
GOOGLE_ID
GOOGLE_SECRET
TOKEN_SECRET 
```

add buildpack for node and python
```
heroku buildpacks
=== demo-mycashmanager Buildpack URLs
1. heroku/nodejs
2. heroku/python
```

### Intialize database 
```
heroku run python app.py db upgrade
```
