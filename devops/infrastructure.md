# Infrastructure as Code Standards

This document outlines the standards and best practices for Infrastructure as Code (IaC) across all Bayat projects. Following these guidelines ensures consistent, reliable, and maintainable infrastructure management.

## Table of Contents

- [General Principles](#general-principles)
- [Tool Selection](#tool-selection)
- [Project Structure](#project-structure)
- [Code Organization](#code-organization)
- [Naming Conventions](#naming-conventions)
- [Configuration Management](#configuration-management)
- [Secrets Management](#secrets-management)
- [Version Control](#version-control)
- [Testing and Validation](#testing-and-validation)
- [Documentation](#documentation)
- [Deployment Workflows](#deployment-workflows)
- [Security Standards](#security-standards)
- [Resource Tagging and Metadata](#resource-tagging-and-metadata)
- [Monitoring and Observability](#monitoring-and-observability)
- [Compliance and Governance](#compliance-and-governance)

## General Principles

All infrastructure as code at Bayat should adhere to these core principles:

1. **Automation First**: Automate everything that can be automated
2. **Idempotence**: Running the same code multiple times produces the same result
3. **Reproducibility**: Infrastructure can be recreated reliably from code
4. **Immutability**: Infrastructure components are replaced rather than modified
5. **Modularity**: Use reusable components and abstraction layers
6. **Version Control**: All infrastructure code is versioned
7. **Documentation**: Infrastructure is well-documented and self-documenting
8. **Testing**: Infrastructure code is tested at multiple levels
9. **Security**: Security is built into the infrastructure from the start
10. **Cost Optimization**: Infrastructure is designed with cost efficiency in mind

## Tool Selection

### Approved Infrastructure as Code Tools

| Tool | Primary Use Case | Supported Cloud Platforms |
|------|-----------------|--------------------------|
| Terraform | Cloud infrastructure provisioning | AWS, Azure, GCP, Multi-cloud |
| AWS CloudFormation | AWS-specific infrastructure | AWS |
| Azure Resource Manager | Azure-specific infrastructure | Azure |
| Pulumi | Programmatic infrastructure | AWS, Azure, GCP, Multi-cloud |
| Kubernetes manifests | Container orchestration | Any Kubernetes cluster |
| Helm | Kubernetes application packaging | Any Kubernetes cluster |
| Ansible | Configuration management | Any platform |
| Packer | Machine image creation | Multiple platforms |

### Tool Selection Criteria

Choose the appropriate tool based on:

1. **Cloud Platform**: Match the tool to the target environment
2. **Team Expertise**: Consider existing team knowledge
3. **Integration Requirements**: Ensure compatibility with CI/CD and other systems
4. **Complexity**: Match the tool to the complexity of the infrastructure
5. **Lifecycle Management**: Consider the full lifecycle of infrastructure
6. **Ecosystem**: Evaluate the available modules and extensions

### Standard Tool Versions

Specify and standardize on specific tool versions:

- Keep tool versions consistent across all environments
- Use version pinning in CI/CD pipelines
- Document the standardized versions in the project README
- Establish a regular review cycle for version updates

## Project Structure

### Directory Structure

Adopt a consistent directory structure for infrastructure code:

```
infrastructure/
├── environments/              # Environment-specific configurations
│   ├── dev/
│   ├── staging/
│   └── prod/
├── modules/                   # Reusable infrastructure modules
│   ├── networking/
│   ├── compute/
│   ├── database/
│   └── security/
├── templates/                 # Template files
├── scripts/                   # Utility scripts
├── tests/                     # Infrastructure tests
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
└── versions.tf                # Terraform version constraints
```

### Environment Separation

Maintain clear separation between environments:

- Use separate directories or state files for each environment
- Implement naming conventions that include the environment
- Use consistent patterns for environment-specific configurations
- Limit cross-environment dependencies

### Module Structure

For reusable modules, follow this structure:

```
modules/example-module/
├── main.tf           # Main module resources
├── variables.tf      # Input variables
├── outputs.tf        # Output values
├── versions.tf       # Version constraints
├── README.md         # Module documentation
└── examples/         # Example implementations
    └── basic/
        ├── main.tf
        └── README.md
```

## Code Organization

### Resource Grouping

Group resources logically:

- Group by functionality or service
- Keep related resources in the same file or module
- Use consistent organizational patterns across projects
- Maintain separation of concerns

### Dependency Management

Manage dependencies explicitly:

- Clearly define the order of resource creation
- Use explicit dependencies where necessary
- Avoid circular dependencies
- Document complex dependency chains

### Terraform-Specific Standards

For Terraform projects:

- Use a single `providers.tf` file for provider configurations
- Use `variables.tf` and `outputs.tf` for inputs and outputs
- Use `locals.tf` for local variables and computations
- Use `main.tf` for primary resources
- Use separate files for complex resource groups

Example Terraform file:

```hcl
# main.tf - Primary infrastructure resources

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-vpc"
    }
  )
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.main.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index]
  
  tags = merge(
    var.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-public-subnet-${count.index + 1}"
      Type = "Public"
    }
  )
}

# Additional resources...
```

## Naming Conventions

### Resource Naming

Use consistent naming patterns for all resources:

- Include project or application name
- Include environment name (dev, staging, prod)
- Include resource type or purpose
- Use consistent separators (hyphens for user-visible names, underscores for variables)
- Keep names reasonably short but descriptive

Examples:

```
# AWS Resources
bayat-payment-prod-vpc
bayat-payment-prod-subnet-public-1
bayat-payment-prod-sg-web

# Azure Resources
bayat-inventory-dev-vnet
bayat-inventory-dev-vm-app01

# Kubernetes Resources
bayat-auth-staging-deploy
bayat-auth-staging-svc
```

### Variable Naming

For variables and parameters:

- Use snake_case for variable names
- Use descriptive names that indicate purpose
- Group related variables with common prefixes
- Document each variable with a description

Example:

```hcl
# variables.tf

variable "project_name" {
  description = "The name of the project"
  type        = string
}

variable "environment" {
  description = "The deployment environment (dev, staging, prod)"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "vpc_cidr" {
  description = "The CIDR block for the VPC"
  type        = string
  default     = "10.0.0.0/16"
}

variable "public_subnet_cidrs" {
  description = "List of CIDR blocks for public subnets"
  type        = list(string)
  default     = ["10.0.1.0/24", "10.0.2.0/24"]
}
```

## Configuration Management

### Parameter Hierarchy

Use a clear hierarchy for configuration parameters:

1. **Defaults**: Sensible default values in the code
2. **Variable Files**: Environment-specific variable files
3. **Parameter Store**: Externalized configuration in AWS Parameter Store, Azure Key Vault, etc.
4. **Command Line**: Override parameters at deployment time

### Configuration Files

Standardize configuration files:

- Use `.tfvars` files for Terraform variables
- Use YAML for Kubernetes configurations
- Use JSON for CloudFormation parameters
- Store configuration files in version control (except secrets)

Example Terraform variable file:

```hcl
# environments/prod/terraform.tfvars

project_name       = "payment-service"
environment        = "prod"
vpc_cidr           = "10.0.0.0/16"
public_subnet_cidrs = [
  "10.0.1.0/24",
  "10.0.2.0/24",
  "10.0.3.0/24"
]
private_subnet_cidrs = [
  "10.0.11.0/24",
  "10.0.12.0/24",
  "10.0.13.0/24"
]
instance_type     = "m5.large"
rds_instance_type = "db.r5.large"
```

### Environment Configuration

Implement graduated environment configurations:

- Use smaller, simpler resources in development environments
- Scale up resource sizes and redundancy in production
- Document the differences between environments
- Automate the propagation of configuration changes across environments

## Secrets Management

### Secrets Handling

Never store secrets in code:

- Use dedicated secrets management tools (HashiCorp Vault, AWS Secrets Manager, etc.)
- Integrate with CI/CD for secure deployment
- Rotate secrets regularly
- Audit secret access

### Secrets Integration

Integrate secrets securely:

- Use IAM roles and managed identities where possible
- Reference secrets by identifier, not value
- Inject secrets at runtime rather than build time
- Implement least privilege access to secrets

Example Terraform code with AWS Secrets Manager:

```hcl
data "aws_secretsmanager_secret" "db_credentials" {
  name = "/${var.project_name}/${var.environment}/db-credentials"
}

data "aws_secretsmanager_secret_version" "db_credentials" {
  secret_id = data.aws_secretsmanager_secret.db_credentials.id
}

locals {
  db_creds = jsondecode(data.aws_secretsmanager_secret_version.db_credentials.secret_string)
}

resource "aws_db_instance" "main" {
  # ... other configuration ...
  
  username = local.db_creds.username
  password = local.db_creds.password
}
```

## Version Control

### Repository Structure

Organize infrastructure code in repositories:

- Use dedicated repositories for core infrastructure
- Include application-specific infrastructure with application code
- Use monorepos for closely related infrastructure components
- Document repository structure and organization

### Branching Strategy

Implement a clear branching strategy:

- Use feature branches for development
- Use environment branches or tags for deployment
- Protect production branches with code reviews and approvals
- Automate testing on branch merge

### Commit Guidelines

Follow consistent commit practices:

- Write clear, descriptive commit messages
- Reference issue/ticket numbers in commits
- Make focused commits with related changes
- Verify code before committing

## Testing and Validation

### Testing Levels

Implement multiple levels of testing:

1. **Syntax Validation**: Verify code is syntactically correct
2. **Static Analysis**: Check for common issues and enforce standards
3. **Unit Testing**: Test individual modules or resources
4. **Integration Testing**: Test interactions between components
5. **Deployment Testing**: Verify successful deployment
6. **Acceptance Testing**: Validate against business requirements

### Testing Tools

Use these tools for infrastructure testing:

- Terraform: `terraform validate`, `terraform plan`, and `terraform-compliance`
- CloudFormation: AWS CloudFormation Linter (`cfn-lint`)
- Kubernetes: `kubeval` and `conftest`
- General: `checkov`, `tfsec`, and `terrascan` for security checks

### Test Automation

Automate testing in CI/CD pipelines:

- Run syntax validation and static analysis on every commit
- Run integration tests on pull requests
- Require manual approval for production deployments
- Generate and review change plans before applying

Example GitHub Actions workflow:

```yaml
name: Terraform Validation

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Setup Terraform
      uses: hashicorp/setup-terraform@v1
      with:
        terraform_version: 1.0.0
    
    - name: Terraform Format
      run: terraform fmt -check -recursive
      
    - name: Terraform Init
      run: terraform init -backend=false
      
    - name: Terraform Validate
      run: terraform validate
      
    - name: Setup TFLint
      uses: terraform-linters/setup-tflint@v1
      with:
        tflint_version: v0.29.0
        
    - name: Run TFLint
      run: tflint --format=compact
      
    - name: Run Checkov
      uses: bridgecrewio/checkov-action@master
      with:
        directory: .
        framework: terraform
```

## Documentation

### Code Documentation

Document infrastructure code thoroughly:

- Add clear comments for complex logic
- Document the purpose of each resource
- Explain non-obvious configuration choices
- Use consistent documentation patterns

Example documentation in Terraform:

```hcl
# This VPC is designed to support a multi-tier application with
# both public-facing and private components. It spans three availability zones
# for high availability and includes separate subnets for web, application, and
# database tiers.

resource "aws_vpc" "main" {
  # ... configuration ...
}

# NAT Gateways to allow private subnets to access the internet
# One gateway per AZ for high availability
resource "aws_nat_gateway" "main" {
  # ... configuration ...
}
```

### Module Documentation

Document reusable modules with:

- Purpose and functionality
- Input variables and their meaning
- Output values and their usage
- Dependencies and requirements
- Example usage

Example module README:

```markdown
# Networking Module

This module creates a complete networking stack including VPC, subnets,
route tables, Internet Gateway, and NAT Gateways.

## Features

- Multi-AZ deployment for high availability
- Public and private subnets
- NAT Gateways for outbound internet access from private subnets
- Network ACLs for additional security

## Usage

```hcl
module "networking" {
  source = "./modules/networking"
  
  project_name    = "payment-service"
  environment     = "prod"
  vpc_cidr        = "10.0.0.0/16"
  azs             = ["us-west-2a", "us-west-2b", "us-west-2c"]
  public_subnets  = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  private_subnets = ["10.0.11.0/24", "10.0.12.0/24", "10.0.13.0/24"]
}
```

## Inputs

| Name | Description | Type | Default | Required |
|------|-------------|------|---------|----------|
| project_name | The name of the project | `string` | n/a | yes |
| environment | The deployment environment | `string` | n/a | yes |
| vpc_cidr | The CIDR block for the VPC | `string` | `"10.0.0.0/16"` | no |
| azs | List of availability zones | `list(string)` | n/a | yes |
| public_subnets | List of public subnet CIDR blocks | `list(string)` | n/a | yes |
| private_subnets | List of private subnet CIDR blocks | `list(string)` | n/a | yes |

## Outputs

| Name | Description |
|------|-------------|
| vpc_id | ID of the VPC |
| public_subnet_ids | List of public subnet IDs |
| private_subnet_ids | List of private subnet IDs |
```

### Architecture Documentation

Create high-level architecture documentation:

- Diagram infrastructure components and relationships
- Document design decisions and rationales
- Explain infrastructure patterns and standards
- Include networking diagrams and security controls

## Deployment Workflows

### CI/CD Integration

Integrate infrastructure deployment with CI/CD:

- Automate infrastructure deployment through pipelines
- Use the same tools and workflows across projects
- Enforce approval gates for production changes
- Generate and store deployment artifacts

Example GitLab CI/CD pipeline:

```yaml
stages:
  - validate
  - plan
  - apply

variables:
  TF_IN_AUTOMATION: "true"

validate:
  stage: validate
  script:
    - terraform init -backend=false
    - terraform validate
    - terraform fmt -check -recursive
    - tflint --format=compact
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'

plan:
  stage: plan
  script:
    - terraform init
    - terraform plan -out=tfplan
  artifacts:
    paths:
      - tfplan
  rules:
    - if: '$CI_COMMIT_BRANCH == "main" || $CI_PIPELINE_SOURCE == "merge_request_event"'

apply:
  stage: apply
  script:
    - terraform init
    - terraform apply -auto-approve tfplan
  dependencies:
    - plan
  rules:
    - if: '$CI_COMMIT_BRANCH == "main"'
      when: manual
```

### Deployment Strategies

Implement safe deployment strategies:

- Use incremental deployments where possible
- Create change plans and review before applying
- Implement rollback procedures
- Use blue/green or canary deployments for critical infrastructure

### State Management

Manage infrastructure state securely:

- Use remote state backends (S3, Azure Storage, etc.)
- Secure access to state files
- Implement state locking to prevent conflicts
- Backup state before significant changes

Example Terraform backend configuration:

```hcl
terraform {
  backend "s3" {
    bucket         = "bayat-terraform-states"
    key            = "payment/prod/terraform.tfstate"
    region         = "us-west-2"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

## Security Standards

### Network Security

Implement secure network design:

- Use private subnets for sensitive workloads
- Implement network segmentation with security groups/NSGs
- Use VPC endpoints or private links for service access
- Implement proper ingress and egress filtering
- Document network flows and security boundaries

### IAM and Access Control

Implement least privilege access:

- Use IAM roles with minimal permissions
- Avoid long-lived credentials
- Implement proper service accounts
- Audit permission assignments regularly
- Use consistent naming for IAM resources

Example Terraform IAM policy:

```hcl
resource "aws_iam_role" "app_role" {
  name = "${var.project_name}-${var.environment}-app-role"
  
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
  })
  
  tags = var.common_tags
}

resource "aws_iam_policy" "app_policy" {
  name        = "${var.project_name}-${var.environment}-app-policy"
  description = "Policy for ${var.project_name} application in ${var.environment}"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Effect   = "Allow"
        Resource = [
          "arn:aws:s3:::${var.app_bucket}",
          "arn:aws:s3:::${var.app_bucket}/*"
        ]
      },
      {
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Effect   = "Allow"
        Resource = "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/${var.dynamodb_table}"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "app_attachment" {
  role       = aws_iam_role.app_role.name
  policy_arn = aws_iam_policy.app_policy.arn
}
```

### Encryption

Implement encryption standards:

- Encrypt data at rest and in transit
- Use customer-managed keys for sensitive data
- Implement key rotation policies
- Document encryption requirements and implementations

### Security Scanning

Integrate security scanning into workflows:

- Use infrastructure security scanners (tfsec, checkov, etc.)
- Implement automated compliance checks
- Fix identified vulnerabilities promptly
- Track security issues in the same system as other work

## Resource Tagging and Metadata

### Tagging Standards

Implement consistent resource tagging:

- Tag all resources with project, environment, owner, etc.
- Use consistent tag names and formats
- Automate tag application in IaC
- Use tags for cost allocation and monitoring

Example tagging in Terraform:

```hcl
# Common tags for all resources
locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = var.team_email
    CostCenter  = var.cost_center
    CreatedDate = formatdate("YYYY-MM-DD", timestamp())
  }
}

resource "aws_vpc" "main" {
  # ... other configuration ...
  
  tags = merge(
    local.common_tags,
    {
      Name = "${var.project_name}-${var.environment}-vpc"
    }
  )
}
```

### Resource Metadata

Include metadata in infrastructure:

- Add descriptions to resources where supported
- Include purpose and ownership information
- Document dependencies and relationships
- Use standardized naming for implicit relationships

## Monitoring and Observability

### Monitoring Integration

Build monitoring into infrastructure:

- Create monitoring resources alongside primary resources
- Configure default alarms and dashboards
- Implement logging infrastructure
- Set up centralized monitoring

Example Terraform CloudWatch alarms:

```hcl
resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  alarm_name          = "${var.project_name}-${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 2
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 300
  statistic           = "Average"
  threshold           = 80
  alarm_description   = "This metric monitors EC2 CPU utilization"
  
  dimensions = {
    AutoScalingGroupName = aws_autoscaling_group.app.name
  }
  
  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]
  
  tags = local.common_tags
}
```

### Observability Standards

Standardize observability practices:

- Implement consistent logging formats
- Configure log retention periods
- Set up distributed tracing
- Document observability implementation

## Compliance and Governance

### Policy as Code

Implement policy as code:

- Use tools like OPA/Conftest, HashiCorp Sentinel, or AWS Config Rules
- Codify compliance requirements
- Automate compliance checks
- Document compliance standards and verification

Example Sentinel policy:

```hcl
# Ensure all S3 buckets have encryption enabled
import "tfplan/v2" as tfplan

s3_buckets = filter tfplan.resource_changes as _, rc {
    rc.type is "aws_s3_bucket" and
    (rc.change.actions contains "create" or rc.change.actions contains "update")
}

violations = filter s3_buckets as _, bucket {
    bucket.change.after.server_side_encryption_configuration is null
}

main = rule {
    length(violations) is 0
}
```

### Infrastructure Governance

Establish governance processes:

- Define approval workflows for infrastructure changes
- Document infrastructure standards and patterns
- Implement regular infrastructure reviews
- Track and manage technical debt
- Establish clear ownership for infrastructure components 