# Using SAM template to build, test and deploy REST API with Lambda proxy intergation

**After setting up SAM CLI run the following commands:**

- `SAM build`

- `SAM Deploy --guided`

*Test SAM template locally by running*
 
- `sam local invoke -e event.json`

## Test Lambda function locally with pytest

**You can also test the Lambda function and REST API, using python Moto package to mock AWS resource locally**

- `pytest -v ../test/test_lambda_fucntion.py`

## Resource
- [Getting started with SAM](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-getting-started.html)
- [Testing with Moto](https://aws.amazon.com/blogs/devops/unit-testing-aws-lambda-with-python-and-mock-aws-services/)
