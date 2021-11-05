# Testing guide

See the [Django Docs page for Writing and Running Tests](https://docs.djangoproject.com/en/3.2/topics/testing/overview/)

All test files must be in this directory

For test discovery, all tests must be named following `test_*.py` (eg. `test_orders.py`)

Tests should import TestCase from django.test

Every test file has a class that takes TestCase as an input

The test case class should have a useful docstring

In the test case class, there may be a setUp function that creates the required objects to be used by all tests in this file

Tests are further divided into functions. Each function will typically test a different feature. There should be at least 1 assert per test function.

Tests can be executed with `sudo docker exec -it lims_web_server python manage.py test tests/`