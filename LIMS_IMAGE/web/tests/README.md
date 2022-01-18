# Testing guide

## Useful Resources

[Django Docs - Writing and Running Tests](https://docs.djangoproject.com/en/3.2/topics/testing/overview/)

[Model Bakery Docs](https://model-bakery.readthedocs.io/en/latest/)

## Tes File Structure

 - All test files must be in this directory
   - Django automatically puts test files in a new app's directory. For our project, we will move all test files to this directory.

 - For test discovery, all tests must be named `test_*.py` (eg. `test_orders.py`)
    - We will use the following naming scheme for test files: `test_<app name>_<models/views/other>`. See the existing files in this folder for examples.

 - Tests should import TestCase from django.test (not Python unittest; django.test extends Python unittest)

 - Each test file contains a class that takes TestCase as an argument. All test code is contained in this class.

## Fixture Setup

 - In the test case class, there may be a setUp function that creates the required objects before the tests are run. (More on the differences betweem Djangos setUp methods [here](https://stackoverflow.com/a/43594694/4780821))

 - The test case class will contain several methods. Each method will typically test a different feature. There should be at least 1 assert per test function (although using more asserts is always encouraged).

 ### Model Bakery
  
  - When runnning tests, Django creates a test database that is separate from the development database. That means we need to populate it with test data before we can run most our tests. The Model Bakery library makes this easy for us. To familiarize yourself with the basics of this library, it is highly encouraged to read through the [basic usage section of the docs](https://model-bakery.readthedocs.io/en/latest/basic_usage.html).

  - [Recipes](https://model-bakery.readthedocs.io/en/latest/recipes.html) are an extremely useful feature of this library that allow us to predefine how to intialize a model instance. In our project, these are extremely useful for models that have complex foreign-key relationships.
      
      - According to the model bakery docs, the standard practice is to put model recipe files in the corresponding app's directory. This will allow recipes to be automatically imported to our test file with the app. Recipes can also be defined in the testing file, but to remove clutter it is encouraged to put standard recipes in the `baker_recipe.py` file in the app directory.

      - A key feature of recipes are that you can pass specific paramaters when initializing from a recipe. A common use-case for this in our project is to create a user, then create a client or lab employee object with that user, then create additional data using that user. See the `test__example.py` file for an example of this. This file can also be copied as a template for your tests.

## Running Tests

Tests can be executed with `docker exec -it lims_web_server python manage.py test tests/`.

Tests are automatically run on our repository on pull requests with `development` or `main`. All tests must pass before a pull request can be accepted.

## Coverage

 Coverage is extremely useful for showing where more tests are needed.
 
  1. To use the coverage library, access a bash terminal in the container and run `coverage run manage.py test tests/`.
  2. Export the results to an html document by running `coverage html`.
  3. Copy the report output out to the host machine by running `docker cp lims_web_server:/src/htmlcov .`. This command needs to be run on the host machine.
  4. Navigate to `index.html` in `html_cov/` and open it in a browser.
