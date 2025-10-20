# meeting_archive


## Run commands

1. make .env

```
cp .env.example .env
vi .env
```

2. install virtualenv

```
pip install virtualenv
```

3. make virtual environment

```
virtualenv venv
python -m virtualenv venv
```

4. install dependencies

```
source venv/bin/activate
pip install -r requirements.txt
```

5. Database migration

```
python manage.py migrate
```

6. run
```
python manage.py runserver
python manage.py runserver 0.0.0.0:8000
```
