# cloud-resume


2. step: deploying resume as a static website on Amazon S3 

- create a Amazon s3 bucket
aws CLI command: aws s3api create-bucket --bucket bucketname --region eu-west-2 --create-bucket-configuration LocationConstraint=eu-west-2
copy files to the bucket :
aws s3 cp style.css s3://Bucketname


Enabling website hosting
- configure the S3 bucket for static website
aws s3 website s3://my-bucket/ \
    --index-document index.html 
    <!-- --error-document error.html -->



https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html#getting-started-cloudfront-request-certificate
{
   "Version":"2012-10-17",
   "Statement":[{
      "Sid":"AddPerm",
      "Effect":"Allow",
      "Principal":"*",
      "Action":[
         "s3:GetObject"
      ],
      "Resource":[
         "arn:aws:s3:::your-domain-name/*"
      ]
    }]
}"


# API Gateway resource
https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html#services-apigateway-tutorial-role

# Follow lambda best practice
https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html

# Run test using 
"pytest -v test_lambda_fucntion.py "
https://github.com/aws-samples/serverless-test-samples/blob/main/python-test-samples/lambda-mock/README.md
https://aws.amazon.com/blogs/devops/unit-testing-aws-lambda-with-python-and-mock-aws-services/

https://github.com/awsdocs/aws-lambda-developer-guide/blob/main/sample-apps/blank-python/0-run-tests.sh


# sam commands
sam local invoke -e event.json
