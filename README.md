# Run Docker container on EC2 Spot instance

Read this first:
https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html

and this:
https://docs.aws.amazon.com/cdk/v2/guide/work-with.html#work-with-prerequisites

To Do:
- add user data to define what should happen on the instance
- give the instance read access to the internet so that it can collect Docker images
- add reading input data (from an S3 bucket?)
- add writing output data (to an S3 bucket?)