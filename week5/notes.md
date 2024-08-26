# Testing
## Assert 
Assert allows you to checking the values. If assert statement is false then it generates exception error.
## unittest
Create a class called Test and add functions to that class which are the tests you want to run.,
## Django Unittests
You can unittest django in tests.py. Django creates entirely new database just for testing purposes.
To run your tests python manage.py tests
### web tests
You can also test webpages whetever they are working the way you want to be. 
## Browser testing
Using selenium you can simulate web browser. Simulating user interaction.
# CI/CD
## CI -> Continous integration.
* Frequent merges to main branch,
* Automated unit testing. 
## CD -> Continous Delivery
* Short release schedules
### Github Actions
It is a tool that helps you create workflow. Where you can apply certain steps everytime
someone push code to main branch. You can run some test on that code.
It uses YAML. Configuration Language. (similiar to dictionary)
key1: value1
key2: value2
key3:
    - item1
    - item2
    - item3