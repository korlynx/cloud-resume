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