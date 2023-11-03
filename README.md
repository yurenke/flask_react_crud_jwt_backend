# Flask backend with PostgreSQL
The following instructions are for the MacOS environment, they might be slightly different on Windows/Linux.
## 1. Database Setup
### 1.1 pull postgres docker image and run
```
$ docker pull postgres
$ docker run -d \
        --name my-postgres \
        -p 5432:5432 \
        -e POSTGRES_PASSWORD=postgres \
        -v [host_src_path]:/var/lib/postgresql/data \
        postgres
```
### 1.2 run container bash, then run psql command as user _postgres_
```
$ docker exec -it my-postgres bash
# psql -U postgres
```
> you will be presented with a psql terminal like this
```
psql (16.0 (Debian 16.0-1.pgdg120+1))
Type "help" for help.

postgres=# 
```
### 1.3 create database
```
postgres=# CREATE DATABASE testdb;
```
### 1.4 create role
```
postgres=# CREATE ROLE test WITH LOGIN PASSWORD ‘test’;
```
### 1.5 grant privileges to the role above
```
postgres=# \c testdb;
You are now connected to database "testdb" as user "postgres".
testdb=# grant all on schema public to test;
GRANT
testdb=# grant all privileges on database testdb to test;
GRANT
testdb=# \q
```

## 2. Flask Setup
### 2.1 Install python3 (don't install Python 3.12.x, psycopg2 isnt working in python 3.12.0 recently, not sure if it has been fixed or not)
```
$ python3 --version
Python 3.11.6
```
### 2.2 Create Python venv and activate it
```
$ cd [the project root folder]
$ python3 -m venv .venv
$ source ./.venv/bin/activate
```
### 2.3 Install python packages
```
### under the project folder ###
(.venv) $ pip install -r ./requirements.txt
```
### 2.4 create .env file and set environment variables
```
(.venv) $ nano flaskreact/.env
```
> set the corresponding settings
```
DATABASE_URI='postgresql+psycopg2://test:test@localhost:5432/testdb'
DEVELOPMENT_SECRET_KEY='flask app secret key'              <- modify this
DEVELOPMENT_JWT_SECRET='flask-jwt-extended jwt secret key' <- modify this
```
### 2.5 run Flask-Migrate commands to create tables (a folder called migrations will be created)
```
### under the project root folder ###
(.venv) $ flask db init
(.venv) $ flask db migrate
(.venv) $ flask db upgrade
```

## 3. Run the Flask development server
```
### unser the project root folder ###
(.venv) $ flask run
```
> you should see this after flask run
```
* Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
