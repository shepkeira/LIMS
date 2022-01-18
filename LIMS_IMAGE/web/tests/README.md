# Testing guide

## Useful Resources

[Django Docs - Writing and Running Tests](https://docs.djangoproject.com/en/3.2/topics/testing/overview/)

[Model Bakery Docs](https://model-bakery.readthedocs.io/en/latest/)

## Tes File Structure

 - All test files must be in this directory

 - All tests must be named `test_*.py` (eg. `test_orders.py`)
    - For our repo, we will use the following naming scheme for test files: `test_<app name>_<models/views/other>`. See the existing files in this folder for examples.

 - Tests should import TestCase from django.test (not Python unittest; django.test extends Python unit test)

 - Each test file contains a class that takes TestCase as an argument. All test code is contained in this class.

## Fixture Setup

 - In the test case class, there may be a setUp function that creates the required objects to be used by all tests in this file. (More on the differences betweem Djangos setUp methods [here](https://stackoverflow.com/a/43594694/4780821))

 - Tests are divided into functions. Each function will typically test a different feature. There should be at least 1 assert per test function.

Tests can be executed with `sudo docker exec -it lims_web_server python manage.py test tests/`

## Coverage

 Coverage is extremely useful for showing where more tests are needed.
 
  1. To use the coverage library, access a bash terminal in the container and run `coverage run manage.py test tests/`.
  2. Export it to an html document by running `coverage html`.
  3. Copy the report output out to the host machine by running `docker cp lims_web_server:/src/htmlcov .`. This command needs to be run on the host machine.
  4. Navigate to `index.html` in `html_cov/` and open it in a browser.
