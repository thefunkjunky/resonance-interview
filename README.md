# resonance-interview
Take-home interview for Resonance

*NOTE:* I attempted the first challenge to try to broaden my current K8 experience, but it became clear that I wasn't going to complete it in time.  I requested extra time to switch to Challenge 2, since I already had boilerplate Terraform to draw from.  However, I was still strapped for time, so I had to make some concessions in the execution.

*Challenge 2 - Terraform/Cloud* 
Select one of the 3 major cloud providers (AWS, Azure, GCP) which you feel comfortable using in Terraform. Don't worry about applying these configurations, a plan will suffice.

Using Terraform create a 3-tiered system:

- a compute instance to hold a UI which is publicly available.
- a compute instance for an API which is not publicly available.
- a database instance which is not publicly available
Ensure the UI instance has access to the API instance. The API and database are both in the same subnet and have access to one another. You can assume IAM policies are already in place for the instances but security groups are not.

Key Concepts:

- Create a VPC
  - Ensure there is a public subnet
  - Ensure there is a private subnet
  - Security groups are in place
- Create a UI compute instance
  - Deploy in a public subnet
- Create an API compute instance
  - Deployed in a private subnet but has access to communicate with UI
  - Ensure the instance has access to the database
- Create a database
  - Deploy this is in a private subnet

## Installation / destruction
1. Install Terraform - https://www.terraform.io/downloads
1. Configure AWS in `~/.aws/config` and `~/.aws/credentials` - https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html
1. Configure parameters in `vars.tf`.
1. Initialize Terraform:
```bash
terraform init
```
1. Generate Terraform Plan:
```bash
terraform plan
```
1. Apply terraform:
```bash
terraform apply
```
1. To destroy:
```bash
terraform destroy
```

## General overview of resources
1. Creates a VPC with a public subnet in a single Availability zone, and 1 private subnet in a zone. The module used is located in the `modules` folder.  Because this creates only 1 instance of the UI, API, and RDS instances, I didn't need the other availability zones. More can be added by appending the appropriate hash maps in the variables. 
1. Creates the networking resources required for communication between resources in the VPC.  Also allows for outgoing communication in the private subnet, so that instances inside can communicate outward and receive responses, but will not allow incoming public requests except for instances on the VPC.
1. Creates a UI EC2 instance in the public subnet, with ports open on 443 and 80 to the public.
1. Creates an API EC2 instance in the private subnet, which allows incoming requests from the UI server on port 443.
1. Creates an RDS postgresql instance in the private subnet, which allows incoming requests from the API server.

## Configuration
Configure the resources by modifying the variables in `vars.tf`.  Normally I would list each one and describe what they are, and what data types they expect, but I'm already over time on this challenge.  Most of them should be fairly obvious by the name.

## Concessions
I am way over time due to switching challenges, so I had remove some features I normally would use.

- Normally I would set up a remote state backend in S3 with DynamoDB state locking to prevent corruption by multiple users. This creates a single source of truth safely stored on AWS, and allows for multiple users to collaborate.

An interesting solution to the chicken-and-egg problem of
setting up state backends in Terraform can be seen at
https://github.com/thefunkjunky/gcloud-takehome/tree/main/00-backend.
It is configured for Google Cloud, but the idea is similar.

- I don't like secrets stored in plaintext, so I usually only set a temporary RDS password in the variables, create an ACM key, encrypt a new password, and then update the terraform to store the hashed password in a new variable, and to decrypt it.

- Authentication for the EC2 instances has not been configured. As such, they do not accept SSH connections.  Furthermore, I did not configure a VPN or bastion host to be able to connect to the private instances.

- Although I think the security groups are set up correctly, I don't have a way to actually check them.  Some modifications may be required.

- It's not clear to me whether the private instances have the correct networking in place to allow connections from the public subnets.  I have my doubts, but it may already be ok as-is.

## Botched 1st challenge
My incomplete attempt at the first challenge can be seen on this branch:
https://github.com/thefunkjunky/resonance-interview/tree/dev

I'm sure with enough time I could have solved it, but I miscalculated how much I would need to complete it.  I wanted to challenge myself, which was a mistake given the circumstances.

I would have loved to solve challenge 3, which was the most interesting of the bunch.  However, I knew right away that would take too long to complete.

## Authors
- Garrett Anderson <garrett@devnull.rip>


