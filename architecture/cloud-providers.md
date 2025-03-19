# Cloud Provider-Specific Guidelines

This document provides best practices and standards for working with major cloud providers at Bayat. While our Infrastructure as Code standards provide general guidance, these guidelines address specific considerations for each cloud platform.

## Table of Contents

- [Introduction](#introduction)
- [Cloud Provider Selection](#cloud-provider-selection)
- [Amazon Web Services (AWS)](#amazon-web-services-aws)
- [Microsoft Azure](#microsoft-azure)
- [Google Cloud Platform (GCP)](#google-cloud-platform-gcp)
- [Multi-Cloud Strategy](#multi-cloud-strategy)
- [Cost Optimization](#cost-optimization)
- [Security and Compliance](#security-and-compliance)
- [Monitoring and Observability](#monitoring-and-observability)
- [Disaster Recovery](#disaster-recovery)
- [Tools and Resources](#tools-and-resources)

## Introduction

Cloud services provide scalable, flexible infrastructure for Bayat's applications and services. These guidelines help teams make informed decisions about cloud provider selection, architecture patterns, and implementation best practices specific to each major cloud platform.

### Purpose

- Establish consistent practices across teams using cloud services
- Provide provider-specific guidance to complement general cloud standards
- Ensure compliance with security, cost, and performance requirements
- Accelerate development by building on proven patterns

## Cloud Provider Selection

When selecting a cloud provider for a new project, consider these factors:

### Technical Considerations

- **Service Requirements**: Which provider offers the best services for your specific needs
- **Integration**: Compatibility with existing systems and third-party tools
- **Technical Fit**: Alignment with team expertise and technology stack
- **Latency Requirements**: Geographic availability of regions and edge locations
- **Specialized Services**: Need for AI/ML, IoT, or other specialized offerings

### Business Considerations

- **Strategic Relationships**: Existing enterprise agreements and partnerships
- **Compliance Requirements**: Certifications and regulatory compliance
- **Cost Structure**: Pricing models aligned with usage patterns
- **Support Options**: Required level of support and service-level agreements
- **Risk Mitigation**: Vendor lock-in considerations

### Primary Providers

For most Bayat projects, select one of these primary providers:

- **AWS**: Default choice for most new projects
- **Azure**: Preferred for projects with significant Microsoft ecosystem integration
- **GCP**: Consider for projects leveraging Google's data analytics or ML capabilities

## Amazon Web Services (AWS)

### Account Structure

- **Organization**: Use AWS Organizations with consolidated billing
- **Accounts**: Separate accounts for production, staging, development, and sandbox
- **Guard Rails**: Use Service Control Policies (SCPs) to enforce security boundaries
- **IAM**: Follow least privilege principle with role-based access

### Core Services

#### Compute

- **EC2**:
  - Use Graviton instances for cost optimization where compatible
  - Leverage Auto Scaling Groups for all production workloads
  - Prefer spot instances for non-critical, fault-tolerant workloads
  - Use EC2 Instance Savings Plans for predictable workloads

- **Containers**:
  - Use ECS Fargate for simplified container management
  - Use EKS for Kubernetes-based workloads
  - Implement cluster auto-scaling for all container platforms

- **Serverless**:
  - Use Lambda for event-driven and short-running processes
  - Package dependencies using Lambda Layers
  - Implement proper timeout and memory allocation
  - Use provisioned concurrency for latency-sensitive functions

#### Storage

- **S3**:
  - Implement proper bucket policies and access controls
  - Use lifecycle policies to transition between storage classes
  - Enable versioning for critical data
  - Use S3 Transfer Acceleration for large uploads

- **EBS**:
  - Use gp3 volumes as the default general-purpose option
  - Enable encryption by default
  - Schedule regular snapshots for backup

- **RDS/Aurora**:
  - Use Multi-AZ deployments for production databases
  - Enable automated backups with appropriate retention
  - Use parameter groups for consistent configuration

#### Networking

- **VPC**:
  - Use separate VPCs for production and non-production environments
  - Implement proper subnet design (public, private, isolated)
  - Use VPC endpoints for AWS service access
  - Implement Transit Gateway for multi-VPC connectivity

- **CloudFront**:
  - Use for all public-facing static content
  - Implement proper cache policies
  - Configure with AWS WAF for security

### AWS-Specific Best Practices

- **Infrastructure as Code**: Use CloudFormation or Terraform with consistent naming conventions
- **Cost Monitoring**: Implement AWS Cost Explorer and Budgets
- **Security**: Enable AWS Config and Security Hub
- **Observability**: Use CloudWatch with proper metric filters and alarms
- **Compliance**: Leverage AWS Audit Manager for compliance frameworks

### AWS Architectural Patterns

- **Web Applications**: ALB + ECS/EKS + RDS + ElastiCache
- **Serverless API**: API Gateway + Lambda + DynamoDB
- **Data Processing**: S3 + Lambda/EMR + Athena/Redshift
- **Machine Learning**: SageMaker + S3 + Lambda

## Microsoft Azure

### Account Structure

- **Management Structure**: Use Management Groups for organizational hierarchy
- **Subscriptions**: Separate subscriptions for production and non-production
- **Resource Groups**: Organize by application and environment
- **RBAC**: Implement role-based access control with built-in and custom roles

### Core Services

#### Compute

- **Virtual Machines**:
  - Use Azure VM Scale Sets for auto-scaling
  - Leverage Spot VMs for non-critical workloads
  - Implement Azure Reserved VM Instances for cost savings
  - Standardize on VM images and sizes

- **Containers**:
  - Use AKS for Kubernetes workloads
  - Implement Azure Container Registry for image storage
  - Use Azure Container Instances for isolated containers

- **Serverless**:
  - Use Azure Functions with proper hosting plans
  - Leverage Durable Functions for long-running workflows
  - Use Event Grid for event-driven architectures

#### Storage

- **Blob Storage**:
  - Configure proper access tiers and lifecycle management
  - Use SAS tokens with minimal permissions
  - Implement soft delete and versioning

- **Azure SQL**:
  - Use elastic pools for multiple small databases
  - Configure geo-replication for critical databases
  - Implement proper backup retention policies

- **CosmosDB**:
  - Choose appropriate consistency levels
  - Implement proper partitioning strategies
  - Use autoscale for variable workloads

#### Networking

- **Virtual Network**:
  - Implement hub-spoke topology for large environments
  - Use Network Security Groups with specific rules
  - Leverage Azure Firewall for centralized protection
  - Implement Azure Private Link for service access

- **Front Door/CDN**:
  - Use for global load balancing and content delivery
  - Configure caching policies appropriately
  - Use with WAF for protection

### Azure-Specific Best Practices

- **Infrastructure as Code**: Use Azure Resource Manager templates or Terraform
- **Cost Management**: Implement Azure Cost Management + Billing
- **Security**: Enable Azure Security Center and configure Azure Sentinel
- **Observability**: Use Azure Monitor with Application Insights
- **Compliance**: Leverage Azure Policy for governance

### Azure Architectural Patterns

- **Web Applications**: Front Door + App Service/AKS + Azure SQL + Redis Cache
- **Serverless API**: API Management + Functions + CosmosDB
- **Data Processing**: Blob Storage + Data Factory + Synapse Analytics
- **Machine Learning**: Azure ML + Blob Storage + Data Factory

## Google Cloud Platform (GCP)

### Account Structure

- **Organization**: Implement GCP Organization with folders
- **Projects**: Separate projects for production, staging, and development
- **IAM**: Use custom roles with least privilege principles
- **VPC Service Controls**: Implement for sensitive data environments

### Core Services

#### Compute

- **Compute Engine**:
  - Use managed instance groups for auto-scaling
  - Leverage preemptible VMs for batch workloads
  - Implement committed use discounts for stable workloads
  - Use custom machine types for optimal sizing

- **Containers**:
  - Use GKE with autopilot for simplified management
  - Implement GKE Enterprise for multi-cluster management
  - Use Cloud Run for containerized microservices

- **Serverless**:
  - Use Cloud Functions for event-driven processing
  - Implement Cloud Run for container-based services
  - Use App Engine for simple web applications

#### Storage

- **Cloud Storage**:
  - Implement proper bucket policies and lifecycle rules
  - Use appropriate storage classes
  - Configure object versioning for critical data

- **Cloud SQL**:
  - Enable high availability configuration
  - Configure automated backups
  - Use private IP for secure access

- **Firestore/Datastore**:
  - Design proper entity structure and keys
  - Implement composite indexes for complex queries
  - Use transactions for data integrity

#### Networking

- **VPC**:
  - Implement shared VPC for multi-project environments
  - Use service networking for private service access
  - Configure Cloud NAT for outbound internet access

- **Cloud CDN/Load Balancing**:
  - Use global load balancing for public-facing services
  - Configure Cloud CDN for static content
  - Implement Cloud Armor for security

### GCP-Specific Best Practices

- **Infrastructure as Code**: Use Deployment Manager or Terraform
- **Cost Management**: Implement budgets and export billing to BigQuery
- **Security**: Enable Security Command Center
- **Observability**: Use Cloud Monitoring and Cloud Logging
- **Compliance**: Leverage Policy Intelligence tools

### GCP Architectural Patterns

- **Web Applications**: Cloud Load Balancing + GKE/Cloud Run + Cloud SQL + Memorystore
- **Serverless API**: API Gateway + Cloud Functions + Firestore
- **Data Processing**: Cloud Storage + Dataflow + BigQuery
- **Machine Learning**: Vertex AI + Cloud Storage + BigQuery

## Multi-Cloud Strategy

When implementing multi-cloud architectures:

### Architecture Considerations

- **Service Abstraction**: Build abstraction layers for cross-cloud services
- **Data Consistency**: Implement mechanisms for cross-cloud data synchronization
- **Identity Management**: Use centralized identity provider (Azure AD, Okta, etc.)
- **Network Connectivity**: Establish direct connectivity between clouds
- **Edge Locations**: Consider edge computing for latency-sensitive applications

### Management Approach

- **Governance**: Standardize policies across cloud platforms
- **Operations**: Use cloud-agnostic monitoring and management tools
- **Security**: Implement consistent security controls across clouds
- **Cost Management**: Use multi-cloud cost optimization platforms
- **Automation**: Standardize on cross-cloud IaC tools (Terraform preferred)

### Common Multi-Cloud Patterns

- **Disaster Recovery**: Primary in one cloud, DR in another
- **Workload Distribution**: Different workloads on different clouds
- **Data Residency**: Deploy in specific clouds for regulatory compliance
- **Vendor Leverage**: Use multiple vendors for negotiation advantage
- **Best-of-Breed Services**: Use optimal services from each provider

## Cost Optimization

### Cross-Provider Practices

- **Right-sizing**: Regularly review and adjust resource allocations
- **Automated Scaling**: Implement auto-scaling for all elastic workloads
- **Reserved Instances**: Use commitment-based discounts for stable workloads
- **Resource Scheduling**: Shut down non-production resources outside business hours
- **Orphaned Resource Cleanup**: Regularly identify and remove unused resources

### Provider-Specific Strategies

- **AWS**:
  - Leverage Savings Plans for compute commitment flexibility
  - Use S3 Intelligent-Tiering for automatic storage optimization
  - Implement Compute Optimizer recommendations
  - Use Graviton processors for compatible workloads

- **Azure**:
  - Use Azure Hybrid Benefit for Windows Server and SQL Server
  - Implement Azure Reservations for VMs, SQL, and other services
  - Leverage Azure Spot VMs for interruptible workloads
  - Use Azure Cost Management recommendations

- **GCP**:
  - Implement committed use discounts for predictable workloads
  - Use custom machine types for precise sizing
  - Leverage sustained use discounts for long-running VMs
  - Use preemptible VMs for fault-tolerant workloads

### FinOps Implementation

- **Team Responsibility**: Assign cost accountability to product teams
- **Tagging Strategy**: Implement consistent resource tagging across clouds
- **Reporting**: Generate regular cost allocation reports
- **Budgeting**: Set and enforce cloud spending budgets
- **Optimization Cycle**: Establish regular cost review and optimization process

## Security and Compliance

### Cross-Provider Security

- **Identity Management**: Use centralized identity provider with SSO
- **Secrets Management**: Implement dedicated secrets management solution
- **Network Security**: Consistent network segmentation and security groups
- **Data Encryption**: Encrypt data at rest and in transit across all providers
- **Security Monitoring**: Centralized SIEM for cross-cloud visibility

### Provider-Specific Security

- **AWS**:
  - Enable GuardDuty for threat detection
  - Implement AWS Security Hub for security posture
  - Use AWS Inspector for vulnerability assessment
  - Configure AWS Shield and WAF for DDoS protection

- **Azure**:
  - Enable Microsoft Defender for Cloud
  - Implement Azure Sentinel for SIEM
  - Use Azure Policy for security compliance
  - Configure Azure Firewall and WAF for protection

- **GCP**:
  - Enable Security Command Center
  - Implement Cloud Armor for WAF and DDoS protection
  - Use Cloud KMS for key management
  - Configure VPC Service Controls for data security

### Compliance Frameworks

- **General Guidelines**:
  - Document provider-specific controls for compliance frameworks
  - Leverage cloud provider compliance programs
  - Implement continuous compliance monitoring
  - Maintain evidence collection and audit trails

- **Provider-Specific Tools**:
  - AWS: AWS Audit Manager, AWS Config
  - Azure: Azure Policy, Compliance Manager
  - GCP: Assured Workloads, Security Command Center

## Monitoring and Observability

### Cross-Provider Monitoring

- **Centralized Approach**: Aggregate metrics and logs in a single platform
- **Service Level Objectives**: Define consistent SLOs across cloud providers
- **Alerting**: Implement standardized alerting thresholds and procedures
- **Dashboards**: Create unified dashboards for cross-cloud visibility
- **Tracing**: Implement distributed tracing across multi-cloud services

### Provider-Specific Monitoring

- **AWS**:
  - Use CloudWatch for metrics, logs, and alarms
  - Implement X-Ray for distributed tracing
  - Configure CloudTrail for API audit logs
  - Use CloudWatch Synthetics for canary testing

- **Azure**:
  - Use Azure Monitor for metrics and logs
  - Implement Application Insights for application monitoring
  - Configure Azure Log Analytics for log aggregation
  - Use Azure Monitor Workbooks for custom dashboards

- **GCP**:
  - Use Cloud Monitoring for metrics and alerting
  - Implement Cloud Logging for log management
  - Configure Cloud Trace for distributed tracing
  - Use Cloud Profiler for performance analysis

### Recommended Tools

- **Native**: Use cloud-native tools for detailed provider-specific insights
- **Cross-Platform**: Consider Prometheus, Grafana, ELK Stack, Datadog, New Relic for multi-cloud

## Disaster Recovery

### Cross-Provider DR Strategies

- **Documentation**: Maintain detailed DR documentation for each provider
- **Testing**: Regularly test DR procedures across providers
- **Automation**: Automate DR processes where possible
- **Data Synchronization**: Implement consistent data replication strategies
- **Recovery Objectives**: Define consistent RPO/RTO across providers

### Provider-Specific DR Solutions

- **AWS**:
  - Use Route 53 for DNS failover
  - Implement S3 Cross-Region Replication
  - Configure DynamoDB Global Tables
  - Use RDS Cross-Region Read Replicas

- **Azure**:
  - Use Traffic Manager for global load balancing
  - Implement Azure Site Recovery
  - Configure geo-redundant storage
  - Use Azure SQL geo-replication

- **GCP**:
  - Use Cloud DNS for global routing
  - Implement Cloud Storage replication
  - Configure Cloud SQL cross-region replicas
  - Use Regional Spanner for high availability

### Multi-Cloud DR Patterns

- **Active-Passive**: Primary in one cloud, standby in another
- **Pilot Light**: Core infrastructure ready in secondary cloud
- **Warm Standby**: Scaled-down but functional copy in secondary cloud
- **Active-Active**: Distributed workload across multiple clouds
- **Data Backup**: Cloud-to-cloud backup strategies

## Tools and Resources

### Infrastructure as Code

- **Cross-Cloud**: Terraform, Pulumi
- **AWS-Specific**: CloudFormation
- **Azure-Specific**: ARM Templates, Bicep
- **GCP-Specific**: Deployment Manager

### Management Tools

- **Cost Management**: CloudHealth, Cloudability, Kubecost
- **Security**: Prisma Cloud, Wiz, Orca
- **Compliance**: Compliance Sheriff, Vanta, Drata
- **Operations**: HashiCorp Suite, Crossplane, Rancher

### Learning Resources

- **AWS**: AWS Well-Architected Framework, AWS Solutions Library
- **Azure**: Azure Architecture Center, Microsoft Learn
- **GCP**: Google Cloud Architecture Framework, Cloud Adoption Framework
- **Multi-Cloud**: CNCF Landscape, The New Stack

### Internal Resources

- **Reference Architectures**: Provider-specific architecture templates
- **Landing Zones**: Pre-configured cloud environments with security controls
- **Policy Repositories**: Centralized cloud policies and governance
- **Best Practices Wiki**: Internal knowledge base for cloud implementation
