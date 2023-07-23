# Saving Money With AWS Lambdas

![AWS Billing Dashboard](/static/aws-billing.png)

## I host this website and my Jenkins setup on AWS, and have detailed in the past how I [automate the setup of this](/2022-01-15_terraform-and-ansible). However, running an EC2 24/7 to handle occasional CI builds for personal projects didn't seem like the best idea, and I wanted to see if I could save money by thinking the process through a bit. This explains how I used AWS lambdas to automate the started of an EC2 through the AWS CLI, and how to set this up within GitHub and Jenkins to drop your single EC2 instance bill by around 90-95%.

I host this website and my Jenkins setup on AWS, and have detailed in the past how I [automate the setup of this](/2022-01-15_terraform-and-ansible). However, running an EC2 24/7 to handle occasional CI builds for personal projects didn't seem like the best idea, and I wanted to see if I could save money by thinking the process through a bit. This explains how I used AWS lambdas to automate the started of an EC2 through the AWS CLI, and how to set this up within GitHub and Jenkins to drop your single EC2 instance bill by around 90-95%.

### The Plan

To make sure this was going to cover everything I used the Jenkins instance for, along with saving some money, it had to have some relatively clear requirements:

1. It can be triggered by a user (me) or via a webhook on GitHub
2. It must shut itself down when not performing any activity, but should try to avoid shutting down mid-build (this would be fairly undesirable)
3. In the case of being started by some other means (e.g. manually through the console), it should still be able to shut itself down
4. It should be able to start itself periodically to run scheduled jobs once a day

There was going to be a few additions to my AWS account to make this happen, ultimately the plan was going to look like the following:

![Plan for AWS EC2 Instance Starting Automation, Including Lambdas](/static/aws-start-plan.png)

- **API Gateway** - Any requests would head through an API Gateway first, which would serve a separate DNS that could be used to handle API requests, and that I could use in the first instance to ensure the instance was online
- **On-demand Lambda** - Checks if the instance is online or scheduled to start, starts it and returns a holding page that refreshes automatically. If the instance is already online, it updates the scheduled stop time to keep it online for another 30 mins and transparently serves the request
- **Cloudwatch Event** - Triggers the Cron Lambda once per day at 5am
- **Cron Lambda** - Works the same as the On-demand Lambda but only triggers the start, does not handle API requests
- **Start/stop Storage** - Records when the instance was scheduled to start and stop, and when it has actually started and stopped
- **Jenkins Instance Crons** - When the instance first boots, it makes sure there is a scheduled stop time in the database and record a default one for 30 mins time if not. It then runs every 5 mins to check if the scheduled stop time has passed, and shuts the instance down if it has

The process for starting will be as follows:

1. A request comes from either me or a GitHub Webhook
2. The On-demand Lambda records that it's starting the instance (and the default scheduled stop time), triggers a start through the AWS API and returns a holding page
3. The Lambda is re-requested and checks the instance state, waiting until it is online to pass the request through
4. When ready, the Lambda passes through the request and either the user or GitHub receives their response
5. GitHub won't wait and resend the request, so to get around this problem, all the GitHub multi-branch pipelines are set to refresh when the Jenkins instance comes online - this means it picks up any new branches or PRs and the builds are triggered immediately
6. In the background, the Jenkins instance checks every 5 mins to see if it is time to shut down yet
7. If any further GitHub webhooks or user requests are made, the On-demand Lambda updates the scheduled stop time so the instance will stay online to complete the new build
8. Once the scheduled stop time has elapsed, the instance shuts itself down

Now that the plan is in place, let's walk through the On-demand Lambda code and how it runs.

### Lambda Code

The Lambda code itself is a Python file with deliberately few dependencies. It depends on the data provided by the API Gateway during the initial request. A point of reference is the [Amazon documentation for Lambdas and API Gateways](https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html#apigateway-proxy), as this shows how the event is presented to the Lambda function. 

```python
import boto3
import datetime
import time
import urllib.parse
import urllib3

HOST_OUTPUT = 'some-example.myjenkins.com'
EC2_INSTANCE_NAME = 'myjenkins'
DYNAMO_TABLE = 'myjenkins-ec2-status'

def lambda_handler(event, context):    
    
    # Collect query string and event parameters
    queryString = '' if not event['queryStringParameters'] else '?' + urllib.parse.urlencode(event['queryStringParameters'])
    print(f"Received request: {event['httpMethod']} https://{event['headers']['Host']}{event['path']}{queryString}")
    instance_id = None
    instance_state = None
    
    # Check if instance is started and running
    print('Loading boto client libraries')
    ec2 = boto3.resource('ec2', region_name='eu-west-1')
    ec2_client = boto3.client('ec2', region_name='eu-west-1')
    dynamodb = boto3.resource('dynamodb')
    
    # Get current status from DynamoDB
    print('Loading DynamoDB table and entry')
    table = dynamodb.Table(DYNAMO_TABLE)
    existing = table.get_item(
        Key={
            'InstanceName': EC2_INSTANCE_NAME
        }
    )
    
    print('Loading instance details')
    instances = ec2.instances.filter(
        Filters=[{'Name': 'tag:Name', 'Values': [EC2_INSTANCE_NAME]}]
    )
    
    # Only one instance will be returned, so this loop will only occur once but is required for the iterable instances object
    for instance in instances:
        instance_id = instance.id
        instance_state = instance.state['Code']

    # If instance is not started, start it
    print(f'Instance ID: {instance_id}, state: {instance_state}')
    if instance_state > 16:
        print('Instance needs to be started')
        start = datetime.datetime.now()
        stop = start + datetime.timedelta(minutes=30)

        # Update or create the DynamoDB table entry
        if existing != None and 'Item' in existing:
            print('Updating DynamoDB entry')
            table.update_item(
                Key={
                    'InstanceName': EC2_INSTANCE_NAME
                },
                UpdateExpression='SET StartRequestedAt=:start, StartCompletedAt=:empty, StopRequestedAt=:stop, StopCompletedAt=:empty',
                ExpressionAttributeValues={
                    ':start': start.strftime('%Y-%m-%d %H:%M:%S'),
                    ':stop': stop.strftime('%Y-%m-%d %H:%M:%S'),
                    ':empty': ''
                }
            )
        else:
            print('Creating DynamoDB entry')
            table.put_item(
                Item={
                    'InstanceName': EC2_INSTANCE_NAME,
                    'StartRequestedAt': start,
                    'StartCompletedAt': '',
                    'StopRequestedAt': stop,
                    'StopCompletedAt': ''
                }
            )
        print('Starting instance')
        instance.start()
    else:

        # Instance is already online, but this is a new request so the stop time must be updated
        print('Updating stop time based on new request')
        print('Updating DynamoDB entry')
        start = datetime.datetime.now()
        stop = start + datetime.timedelta(minutes=30)
        table.update_item(
            Key={
                'InstanceName': EC2_INSTANCE_NAME
            },
            UpdateExpression='SET StopRequestedAt=:stop, StopCompletedAt=:empty',
            ExpressionAttributeValues={
                ':stop': stop.strftime('%Y-%m-%d %H:%M:%S'),
                ':empty': ''
            }
        )
    
    # Describe the instance to check its deeper status
    response = None if instance_state != 16 else ec2_client.describe_instance_status(InstanceIds=[instance_id])
    if response is None or len(response['InstanceStatuses']) < 1 or response['InstanceStatuses'][0]['InstanceStatus']['Status'] != 'ok':
        print('Instance is not ready, received this state data:')

        # Depending on request type, either return a refresh or simply wait for the instance to be available
        if event['httpMethod'] == 'GET':
            print('Returning GET HTML response')
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'text/html'
                },
                'body': '<html><head><meta http-equiv="refresh" content="30"><title>Instance Start/Stop</title></head><body><h1>Instance is starting, please wait...</h1><h2>This page will refresh every 30 seconds...</h2></body></html>'
            }
        else:
            # Wait for instance to become available
            print('Waiting for instance to be OK')
            while response is None or len(response['InstanceStatuses']) < 1 or response['InstanceStatuses'][0]['InstanceStatus']['Status'] != 'ok':
                time.sleep(5)
                response = ec2_client.describe_instance_status(InstanceIds=[instance_id])

    print('Instance is running, returning response')
    
    # Forward the request either as a GET, or proxy the POST response back (for GitHUb Webhooks)
    if event['httpMethod'] == 'GET':
        print(f'Returning redirect response to {HOST_OUTPUT}')
        return {
            'statusCode': 302,
            'headers': {
                'Location': 'https://' + HOST_OUTPUT + event['path'] + queryString
            }
        }
    
    print(f'POSTing to end state and returning response to {HOST_OUTPUT}')
    http = urllib3.PoolManager()
    response = http.request('POST', 'https://' + HOST_OUTPUT + event['path'] + queryString, headers=event['headers'], body=event['body'])
    return {
        'statusCode': response.status,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': response.data
    }
```

### Deploying with Terraform

Once your code is ready you can deploy it using a Terraform setup similar to the following (this isn't a complete TF file). This presumes you already have a Route53 entry available for your API Gateway and the EC2 instance itself. The EC2 instance will also need permissions to read/write to the DynamoDB table and to be able to shut itself down.

```hcl
resource "aws_dynamodb_table" "start_stop" {
  name          = "myjenkins-ec2-status"
  hash_key      = "InstanceName"
  billing_mode  = "PAY_PER_REQUEST"

  attribute {
    name = "InstanceName"
    type = "S"
  }
}

resource "aws_iam_role" "lambda_start_stop" {
  name = "iam-role-lambda-start-stop"

  assume_role_policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow"
    }
  ]
}
POLICY
}

resource "aws_iam_policy" "lambda_start_stop" {
  name = "iam-policy-lambda-start-stop"
  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:StartInstances",
        "ec2:StopInstances",
        "dynamodb:PutItem",
        "dynamodb:DescribeTable",
        "dynamodb:GetItem",
        "dynamodb:UpdateItem"
      ],
      "Resource": [
        "arn:aws:ec2:eu-west-1:890879110541:instance/*",
        "${aws_dynamodb_table.start_stop.arn}"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "ec2:DescribeInstances",
        "ec2:DescribeInstanceStatus"
      ],
      "Resource": "*"
    }
  ]
}
POLICY
}

resource "aws_iam_role_policy_attachment" "lambda_start_stop" {
  role       = aws_iam_role.lambda_start_stop.name
  policy_arn = aws_iam_policy.lambda_start_stop.arn
}

data "archive_file" "lambda_ci_start_on_request" {
  type        = "zip"
  source_file = "lambda/ci-start-on-request/lambda_function.py"
  output_path = "lambda_ci_start_on_request.zip"
}

resource "aws_lambda_function" "lambda_ci_start_on_request" {
  filename      = "lambda_ci_start_on_request.zip"
  function_name = "instance-ci-start-on-request-handler"
  role          = aws_iam_role.lambda_start_stop.arn
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 300

  source_code_hash = data.archive_file.lambda_ci_start_on_request.output_base64sha256
}

resource "aws_lambda_permission" "lambda_apigw_permission" {
  statement_id  = "AllowExecutionFromApiGW"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_ci_start_on_request.function_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_acm_certificate" "ci_gateway" {
  domain_name       = "some-example-gw.myjenkins.com"
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_apigatewayv2_domain_name" "ci_gateway" {
  domain_name = "some-example-gw.myjenkins.com"

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.ci_gateway.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }
}

resource "aws_apigatewayv2_api" "ci_gateway" {
  name          = "ci-gateway"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_integration" "ci_gateway" {
  api_id           = aws_apigatewayv2_api.ci_gateway.id
  integration_type = "AWS_PROXY"

  integration_method  = "POST"
  integration_uri     = aws_lambda_function.lambda_ci_start_on_request.invoke_arn
}

resource "aws_apigatewayv2_route" "ci_gateway" {
  api_id    = aws_apigatewayv2_api.ci_gateway.id
  route_key = "$default"
  target    = "integrations/${aws_apigatewayv2_integration.ci_gateway.id}"
}

resource "aws_apigatewayv2_deployment" "ci_gateway" {
  api_id      = aws_apigatewayv2_api.ci_gateway.id
  description = "$default"

  lifecycle {
    create_before_destroy = true
  }

  triggers = {
    redeployment = sha1(join(",", tolist([
      jsonencode(aws_apigatewayv2_integration.ci_gateway),
      jsonencode(aws_apigatewayv2_route.ci_gateway),
    ])))
  }

  depends_on = [aws_apigatewayv2_route.ci_gateway]
}

resource "aws_apigatewayv2_stage" "ci_gateway" {
  api_id        = aws_apigatewayv2_api.ci_gateway.id
  name          = "$default"
  auto_deploy   = true
}

resource "aws_apigatewayv2_api_mapping" "example" {
  api_id      = aws_apigatewayv2_api.ci_gateway.id
  domain_name = aws_apigatewayv2_domain_name.ci_gateway.id
  stage       = aws_apigatewayv2_stage.ci_gateway.id
}
```

### Configuring Jenkins and GitHub

The final pieces are to ensure that Jenkins and GitHub are able to work effectively with the new setup.

To configure Jenkins, it's best to ensure any multi-branch pipelines connected to GitHub are using a frequent scan of the remote repository, so it can easily detect new branches and PRs when the Jenkins instance comes online:

![Jenkins Configuration for Multi-branch Pipeline Showing Scan Triggers](/static/jenkins-scan-triggers.png)

For GitHub, ensure your webhook for the repository is using the new DNS that connects to the API Gateway:

![GitHub Webhook Configuration](/static/github-webhook.png)

And that's it! This should be enough top give you an idea of how this could be adapted to your setup.

### Potential Improvements

While the solution I have has been saving me a fair bit of money on my Jenkins setup so far, there are some improvements I'm going to find some time to add when I have a bit more free time:

- **Single DNS**: using a single DNS by efficiently passing through the Lambda when the instance is online would be a better user experience overall
- **Faster Startups**: the current startup detection is not fast, as it waits for the EC2 instance status to be reported through the AWS API, checking the API directly might be better
- **Faster Shutdowns**: tying the shutdowns more directly to the Jenkins builds would allow the system to shut down more promptly when finished to save even more pennies

If you have any comments or want to know more about any of this, please feel free to ping me on [Mastodon](https://howdee.social/@jamiefdhurst), which tends to be the best way to get in contact with me these days. I don't have any plans to add comments onto the blog anytime soon.