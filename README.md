# Adjust Home Task

A demo project where user can make dynamic queries and get results based on provided parameters.

## Getting Started

Kindly create virtual environment if you don't want to mess up libraries =)

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.7
- Django 3.2.1
- Django Rest Framework 3.12.4


### Installing

First clone the repo into your local directory.

```
git clone https://github.com/MirzaBaig715/Adjust-Home
```
Requirements installation
```
pip install -r requirements.txt
```
Create database
```
python manage.py makemigrations
python manage.py migrate
```

Migrate the dump data into database.
```
python manage.py dump_data
```

Thats it! Now you can go to [localhost](localhost:8000/metrics/api/). To test the apis please use [postman documentation](https://documenter.getpostman.com/view/5135674/TzRRDU4Y)
