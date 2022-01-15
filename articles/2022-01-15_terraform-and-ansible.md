# Using Terraform and Ansible

![Mr. Motivator](/static/mr-motivator.jpg)

## A guide to coupling a few using infrastructure as code and configuaration tools together to provide an effective, repeatable pattern for building instances both locally and remotely.

A while back now, I decided that I wanted to eschew one of the tenets I employ in my day job - everything is automated, 
everything is repeatable. My personal infrastructure setup was a little haphazard at the time, with a couple of EC2 
instances that were set up a while ago as pets and that I manually kept on top of - something I was becoming more and 
more aware was a bad idea. I decided to tear it all down and start again.

That left me with the task of deciding how to do it.

### Tooling

Terraform for most engineers has been the de facto standard for some time. Released and supported by Hashicorp, it 
links into multiple cloud providers and has the flexibility and extendability to work well in a variety of different 
circumstances. Terraform was a natural choice for building out my AWS-level infrastructure, and for acting as the 
orchestrator for all of my other integrations.

Second was how I configure the servers once they're in place. I thought a bit longer about this, as Packer is an 
excellent tool for compiling a set of images to spin up, but my use case with Jenkins meant I wanted to be able to 
continually configure the instances once they were running. This led me in the direction of Ansible for a few reasons. 
I usually gravitate towards Ansible by default due to its Python and YAML choices, preferring this over the likes of 
Puppet and Chef which use their own complexities. Ansible would allow me to create a set of roles and tasks relatively 
quickly, and to iterate on my instances once they were in place.

Now I had to think about how I link the two of them together - what I didn't want to do was feed Terraform outputs into 
a static file and drive Ansible separately, needing to hold some external state. I wanted Terraform's state and 
knowledge of the EC2 instance details to be automatically fed into Ansible on each run, such that building and 
updating the infrastructure would be driven from a `terraform apply` command.

### Getting Started

To follow along, you'll need the following installed on your local setup:

* Docker

That's it! Part of the goal was to create a repeatable process, and compiling the tooling into a Docker image meant 
that I wouldn't run into any problems on different devices with different setups and version incompatibilities, I 
could happily run this locally, from within Jenkins, or from within a remote EC2.

You'll also need an AWS account and your local setup configured with appropriate environment variables for full access:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`

Plus an SSH key pair installed at `~/.ssh/id_rsa` and `~/.ssh/id_rsa.pub` that will be used to configure the EC2 
instances in AWS.

Code examples are included inline all the way through, but you can also head to 
[https://github.com/jamiefdhurst/terraform-ansible-example](https://github.com/jamiefdhurst/terraform-ansible-example) 
for the full reference example.

For this simple example, this will create an EC2 and install nginx on it, no more. You can expand from there as your 
needs require.

A simple Dockerfile could work as follows:

```
FROM hashicorp/terraform:0.14.11
WORKDIR /data
RUN apk update && apk add ansible aws-cli py3-boto3 py3-botocore
ADD id_rsa /.ssh-key
RUN chmod 600 /.ssh-key
ENTRYPOINT ["terraform"]
CMD ["-help"]
```

This is based on a Terraform image and installs Ansible on top of it, along with copying in the SSH key that is going 
to be needed to access the instances. It then calls Terraform by default, but that's it, nothing more.

Now building and starting this Docker image through the CLI can get a bit onerous, so I decided to wrap some of the 
repeated commands inside of a Makefile:

```
PWD := $(shell echo `pwd`)
SSH_PRIVATE_KEY := $(shell readlink ~/.ssh/id_rsa)
SSH_PUBLIC_KEY := $(shell readlink ~/.ssh/id_rsa.pub)
DOCKER_MAIN := docker run -v $(PWD):/data -e TF_VAR_SSH_PUBLIC_KEY="$(SSH_PUBLIC_KEY)" -e AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) -e AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY)
DOCKER_SH_ENTRYPOINT := --entrypoint /bin/sh
DOCKER_BASE := $(DOCKER_MAIN) -it infrastructure
DOCKER_BASE_CUSTOM := $(DOCKER_MAIN) $(DOCKER_SH_ENTRYPOINT) -it infrastructure -c

## build: build the container image to be used in all commands
build:
	@cp ~/.ssh/id_rsa id_rsa
	@docker build -t infrastructure .
	@rm id_rsa

## init: initialise terraform - must be run before any subsequent commands
init:
	@$(DOCKER_BASE) init

## plan: show output of state to be changed
plan:
	@$(DOCKER_BASE) plan

## apply: apply changes to remote files
apply:
	@$(DOCKER_BASE) apply

## debug: enter a shell with access to terraform and ansible
debug:
	@$(DOCKER_MAIN) $(DOCKER_SH_ENTRYPOINT) -it infrastructure

## create-state: create remote state in AWS environment
create-state:
	@$(DOCKER_BASE_CUSTOM) "cd state && terraform init && terraform apply"

.PHONY: help
all: help
help: Makefile
	@echo
	@echo " Choose a command to run:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo
```

This allows me to run the following commands:

* `make build` - Build the Docker image and ensure the SSH key is copied in
* `make init` - Initialise Terraform on the Docker container
* `make plan` - Run a TF plan
* `make apply` - Run a TF apply
* `make create-state` - Create the TF state and store it remotely in S3 and DynamoDB

It also passes in environment variables such as my AWS credentials, and the SSH key into a format I need to configure 
via Terraform.

To get started, create a file in your setup `state/main.tf` and add the following:

```
terraform {
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
  required_version = ">= 0.13"
}

provider "aws" {
  region = "eu-west-2"
}

resource "aws_s3_bucket" "terraform-state" {
  bucket = "terraform-ansible-example-state"
  
  versioning {
    enabled = true
  }
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_dynamodb_table" "terraform-locks" {
  name         = "terraform-ansible-example-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"
  attribute {
    name = "LockID"
    type = "S"
  }
}
```

Now you can run the following commands to initialise your remote state:

```
make build
make create-state
```

You'll be prompted to apply your changes, go ahead.

If you check your AWS account, you should see the services in place:

![tf-ansible-s3.png](Example showing S3 bucket)
![tf-ansible-dynamodb.png](Example showing DynamoDB table)

Now you're ready to build your first instance.

### Building an Instance

I'm going to be skipping any of the usual security restrictions and VPC separations that would be in place here to 
simplify the example. Create a `main.tf` file in your setup and add the following:

```
variable "SSH_PUBLIC_KEY" {
  type = string
  description = "Public key to use when deploying all AWS resources"
}

# Use the state we created earlier
terraform {
  required_version = ">= 0.14"
  backend "s3" {
    bucket          = "terraform-ansible-example-state"
    key             = "terraform.tfstate"
    region          = "eu-west-2"
    dynamodb_table  = "terraform-ansible-example-locks"
    encrypt         = true
  }
}

provider "null" {}
provider aws {
  region = "eu-west-2"
}

# Set up our key pair in KMS
resource "aws_key_pair" "root" {
  key_name   = "my-key-pair"
  public_key = var.SSH_PUBLIC_KEY
}

# Configure our VPC
resource "aws_default_vpc" "default" {
  tags = {
    name = "Default VPC"
  }
}

# Create a base security group
resource "aws_security_group" "default" {
  name        = "my-base"
  description = "Base security to allow SSH, and all private traffic"

  egress {
    description = "Allow all"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow from private"
    from_port   = 0
    to_port     = 0
    protocol    = -1
    cidr_blocks = [aws_default_vpc.default.cidr_block]
  }

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create an HTTP-specific security group
resource "aws_security_group" "http" {
  name        = "my-http"
  description = "Security group for HTTP/HTTPS"

  ingress {
    description = "Allow HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "Allow HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Get the latest Ubuntu AMI
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"]
}

# Create the instance
resource "aws_instance" "ec2" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  key_name                    = aws_key_pair.root.key_name
  vpc_security_group_ids      = [aws_security_group.default.id, aws_security_group.http.id]
  associate_public_ip_address = true
  availability_zone           = "eu-west-2a"

  root_block_device {
    volume_type = "gp2"
    volume_size = 10
  }

  lifecycle {
    ignore_changes = [ami]
  }
  
  tags = {
    Name = "my-instance"
  }
}

# Output the host once complete
output "hostname" {
  value = aws_instance.ec2.public_dns
}

```

This TF script is going to create a VPC, a set of security groups and an associated EC2 instance. To set things up a 
little more securely, you may want to adjust the script above to only allow SSH from your own IP.

If you run the following now, you'll get your instance configured and set up:

```
make init
make apply
```

![tf-ansible-ec2.png](Example showing created AWS EC2 instance)

### Configuring Ansible

Now your instance is ready, it's time to install something on it. For simplicity, let's get nginx installed and ready, 
giving you a foundation to set up more roles and responsibilities over time.

Create your Ansible config file first of all, in `ansible.cfg`, this will match up the SSH key on the Docker image and 
turn off those cows:

```
[defaults]
nocows=1
host_key_checking=False
private_key_file=/.ssh-key
retry_files_enabled=False
```

Next, configure your instance-level playbook in `ansible/my-instance.yml`:

```
- hosts: all
  become: true
  user: ubuntu
  roles:
    - nginx
```

And finally, define a role by creating `ansible/roles/nginx/tasks/main.yml`:

```
---
- name: Nginx | Install nginx
  apt:
    name: nginx
```

It's very simple, but it'll do the job. Now, in order to run the Ansible on your EC2 instance, it needs to be linked 
into Terraform.

### Triggering from Terraform

Some adjustments will need to be made to your EC2 creation to ensure your instance has what it needs to support running 
an Ansible playbook. In your `main.tf` file, add some userdata into your EC2 instance resource creation as follows:

```
  user_data = <<EOF
    #!/bin/bash
    sudo apt-get update
    sudo apt-get -y install python3 python3-docker python3-jenkins python3-boto3 awscli
	EOF
```

Next, we need to create a new resource to trigger the Ansible command. This will run on each `terraform apply` and will 
wait for your instance to be healthy before it triggers via the AWS CLI. Add it before the output in your `main.tf` file
as follows:

```
resource "null_resource" "ansible" {
  depends_on = [aws_instance.ec2]

  provisioner "local-exec" {
    command = "aws --region eu-west-2 ec2 wait instance-status-ok --instance-ids ${aws_instance.ec2.id} && ansible-playbook -e public_ip=${aws_instance.ec2.public_ip} -e private_ip=${aws_instance.ec2.private_ip} -e ansible_python_interpreter=/usr/bin/python3 -i ${aws_instance.ec2.public_ip}, ./ansible/my-instance.yml"
  }

  triggers = {
    always_run = timestamp()
  }
}
```

Now run `make apply` one more time, and your ansible should trigger and install ngix.

![tf-ansible-terminal.png](Example showing completed execution in the terminal)

### The Result

Now if you grab the result from your output, e.g.:

```
Outputs:

hostname = "ec2-18-130-17-56.eu-west-2.compute.amazonaws.com"
```

You can head to, for example, [http://ec2-18-130-17-56.eu-west-2.compute.amazonaws.com](http://ec2-18-130-17-56.eu-west-2.compute.amazonaws.com) 
in your browser and see the resulting install working:

![tf-ansible-terminal.png](Example showing completed execution in the terminal)

Now think about how you can expand this to do what you need!
