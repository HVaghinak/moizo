# Moizo
Moizo API
## Getting started
Clone the project, create new virtualenv (`virtualenv moizo` , `source /envs/moizo/bin/activate`) for the project, after go to project directory and run 
```
pip install -r requirements.txt
```

## Create Database
```
    $ sudo apt-get install postgresql-contrib
    $ sudo su - postgres
    $ createdb moizo
    $ psql
    $ CREATE USER moizo;
    $ ALTER USER moizo PASSWORD 'root';
    $ ALTER USER moizo CREATEDB;
```

## Start server

Run 
```
python manage.py migrate
python manage.py runserver
```

## API Documentation
127.0.0.1:8000/documentation
