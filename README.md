# sr-dispersal

### Steps to run the website locally

1.	Clone the github repository

```git clone git@github.com:vbuens/sr-dispersal.git```

2.	Create a virtual environment

``` python3 -m venv venv-SR```

3.	Activate venv

```source venv-SR/bin/activate```

4.	Install requirements

```pip install -r sr-dispersal/requirements.txt```

5. Configure the database

```
python manage.py makemigrations
python manage.py migrate
```

6. Set environment variables, e.g.

```
export SECRET_KEY=secret
export ALLOWED_HOSTS=".example.com 203.0.113.5"
```


7.	Run server

```python manage.py runserver```

8.	Open website locally

Open a browser and go to: http://127.0.0.1:8000/dispersal/

