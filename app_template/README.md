# Deploy resume template as a static website on Amazon S3

**On AWS CLI, run the following commands:**

*Create an Amazon s3 bucket*

- `aws CLI command: aws s3api create-bucket --bucket resume.collinsunaichi.co.uk
 --region eu-west-2 --create-bucket-configuration LocationConstraint=eu-central-1`

*Copy files to the bucket*

- `aws s3 cp índex.html s3://Bucketname`

- `aws s3 cp style.css s3://Bucketname`

*Configure the S3 bucket for static website*

- `aws s3 website s3://my-bucket --index-document index.html`