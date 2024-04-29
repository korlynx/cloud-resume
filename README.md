# Hosting Static Website with dynamic page visit counter API on Amazon S3

The aim of this project is to deploy a serverless HTML resume website using Amazon S3 bucket, the webpage displays a dynamic visitor counter, using a REST API and a Lambda function back by a DynamoDB table. The S3 bucket endpoint, and REST API endpoint are served using Amazon CloudFront.

## Services use in this project
- Amazon S3 Bucket
- AWS Indentiy and Access Management
- DynamoDB
- AWS Lambda
- AWS API Gateway
- CloudFront
- AWS Route53
- AWS Severless Application Management (SAM)

## Some usefull links

- [Getting started with Cloudfront](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/getting-started-cloudfront-overview.html#getting-started-cloudfront-request-certificate)

- [API Gateway tutorial](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway-tutorial.html#services-apigateway-tutorial-role)

- [Lambda best practices](https://docs.aws.amazon.com/lambda/latest/dg/best-practices.html)

