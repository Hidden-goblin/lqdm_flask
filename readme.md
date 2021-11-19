# lqdm flask

## Purpose

Created to demonstrate how I automate test. It stays uncompleted :( 

I leave it so that one can see the automation process .

## Dockerized api

Before creating the stack, please add a `.env`  file in the API folder.

This file must contains  the `JWT_SECRET_KEY`  key such as

```
JWT_SECRET_KEY='mysecretKey'
```



Once this file is created then run in a shell command line

```
 docker-compose -f .\docker-compose.yml up
```

It should start a bunch of containers (lqdmMongoDb & lqdmApi are the most significant).

## Access

You should access the api swagger at `[Flasgger](http://localhost:5000/apidocs)`



## Users

| email                 | password  | role   |
| --------------------- | --------- | ------ |
| bobadmin@test.com     | bob!123   | Admin  |
| elsawriter@pencil.edu | elsa!123  | Writer |
| robinplayer@test.com  | robin!123 | Player |

## Tests

All the test automation is in either the `JMETERS` folder or `test` folder.

The Jmeter tests were to demonstrate that you can create automated test quickly but with a low readability (for PO or Customer).

The test tests were to demonstrate that you can create automated test with a better readability.



### JMeter run

Please use apache Jmeter software (google it)

### `test` run

You need python to be installed on your pc with the pipenv package

See [Pipenv: Python Dev Workflow for Humans &#8212; pipenv 2021.11.15 documentation](https://pipenv.pypa.io/en/latest/) for installation process.



Running test is first iniate the virutal env and then run a command in this environment.

```powershell
pipenv install
pipenv run python run.py
```


