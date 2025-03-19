# SAST/DAST Implementation Guidelines

This document defines Bayat's standards for implementing Static Application Security Testing (SAST) and Dynamic Application Security Testing (DAST) as part of the secure development lifecycle.

## Table of Contents

- [Introduction](#introduction)
- [SAST Implementation](#sast-implementation)
  - [Tool Selection](#sast-tool-selection)
  - [Configuration](#sast-configuration)
  - [Integration](#sast-integration)
  - [Issue Management](#sast-issue-management)
- [DAST Implementation](#dast-implementation)
  - [Tool Selection](#dast-tool-selection)
  - [Configuration](#dast-configuration)
  - [Integration](#dast-integration)
  - [Issue Management](#dast-issue-management)
- [DevSecOps Pipeline Integration](#devsecops-pipeline-integration)
- [Roles and Responsibilities](#roles-and-responsibilities)
- [Metrics and Reporting](#metrics-and-reporting)
- [Training and Awareness](#training-and-awareness)

## Introduction

SAST and DAST are complementary security testing methodologies that help identify vulnerabilities at different stages of development:

- **SAST (Static Application Security Testing)**: Analyzes source code for security vulnerabilities without executing the application
- **DAST (Dynamic Application Security Testing)**: Tests running applications to identify security issues from an external perspective

This document provides guidelines for effectively implementing both SAST and DAST in the development lifecycle.

## SAST Implementation

### SAST Tool Selection

Select SAST tools based on the following criteria:

1. **Language/Framework Support**: Must support all primary languages and frameworks used in the project
2. **Integration Capabilities**: Must integrate with existing CI/CD pipeline and code repositories
3. **Accuracy**: Low false positive rate and high true positive rate
4. **Rule Customization**: Ability to tailor rules to project-specific requirements
5. **Compliance Coverage**: Support for relevant security standards (OWASP Top 10, CWE, etc.)

Recommended SAST tools by language:

| Language     | Primary Tool                | Secondary Tool      |
|--------------|----------------------------|---------------------|
| Java         | SonarQube                  | SpotBugs            |
| JavaScript   | ESLint + security plugins  | SonarQube           |
| TypeScript   | ESLint + security plugins  | SonarQube           |
| Python       | Bandit                     | SonarQube           |
| C#           | SonarQube                  | Security Code Scan  |
| C/C++        | Coverity                   | Clang Static Analyzer |
| Go           | gosec                      | SonarQube           |
| Ruby         | Brakeman                   | SonarQube           |
| PHP          | PHPCS Security Rules       | SonarQube           |
| Swift        | SwiftLint                  | SonarQube           |

### SAST Configuration

1. **Baseline Configuration**:
   - Configure tools with a baseline set of rules aligned with OWASP Top 10 and CWE Top 25
   - Enable language-specific secure coding rules
   - Set appropriate severity levels for different vulnerability types

2. **Custom Rules**:
   - Develop custom rules for organization-specific security requirements
   - Create rules for proprietary frameworks and libraries

3. **Exclusions**:
   - Document any rule exclusions with justification
   - Review exclusions quarterly
   - Require approval for security rule exclusions

Example SonarQube quality gate configuration:

```json
{
  "name": "Bayat Security Gate",
  "conditions": [
    {
      "metric": "new_security_rating",
      "op": "GREATER_THAN",
      "value": "1"
    },
    {
      "metric": "new_reliability_rating",
      "op": "GREATER_THAN",
      "value": "1"
    },
    {
      "metric": "new_vulnerabilities",
      "op": "GREATER_THAN",
      "value": "0"
    }
  ]
}
```

### SAST Integration

1. **Development Integration**:
   - Configure IDE plugins for real-time SAST feedback
   - Provide developers with local scan capabilities

2. **CI/CD Integration**:
   - Run incremental SAST on pull requests
   - Run full SAST scans nightly
   - Block merges for critical or high security issues
   - Generate security reports as build artifacts

Example GitHub Actions workflow for SAST:

```yaml
name: SAST Analysis

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  sast-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
        with:
          fetch-depth: 0
      
      - name: SonarQube Scan
        uses: SonarSource/sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
          SONAR_HOST_URL: ${{ secrets.SONAR_HOST_URL }}
      
      - name: SonarQube Quality Gate Check
        uses: SonarSource/sonarqube-quality-gate-action@master
        timeout-minutes: 5
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### SAST Issue Management

1. **Categorization**:
   - Categorize findings by severity (Critical, High, Medium, Low)
   - Map findings to OWASP Top 10 or CWE categories

2. **Prioritization**:
   - Address all Critical and High findings before release
   - Create a remediation plan for Medium findings
   - Track Low findings for future sprints

3. **Remediation Workflow**:
   - Assign security findings to responsible developers
   - Track remediation in existing issue management system
   - Require security team review for critical vulnerability fixes

4. **False Positive Management**:
   - Document process for marking false positives
   - Require security team approval for false positive designations
   - Regularly review and update false positive list

## DAST Implementation

### DAST Tool Selection

Select DAST tools based on:

1. **Application Type Support**: Support for web, mobile, API, and other relevant application types
2. **Authentication Support**: Ability to test authenticated portions of applications
3. **Scan Depth**: Configurability of scan depth and coverage
4. **API Support**: Capabilities for testing REST, GraphQL, and other API types
5. **Automation Capability**: Support for automated scanning in CI/CD pipelines

Recommended DAST tools by application type:

| Application Type | Primary Tool               | Secondary Tool          |
|------------------|----------------------------|-------------------------|
| Web Applications | OWASP ZAP                  | Burp Suite Professional |
| APIs             | OWASP ZAP API Scan         | Postman + Newman        |
| Mobile Apps      | Mobile Security Framework  | OWASP ZAP Proxy         |
| Microservices    | OWASP ZAP                  | API Security Testing tools |

### DAST Configuration

1. **Scan Profiles**:
   - Create standard scan profiles for different application types
   - Define authentication sequences for authenticated testing
   - Configure crawling depth and exclusions

2. **Test Cases**:
   - Enable tests for OWASP Top 10 vulnerabilities
   - Configure specific tests based on application technology
   - Define custom test cases for business logic vulnerabilities

3. **Environment Configuration**:
   - Set up dedicated testing environments for DAST
   - Configure test data that doesn't impact production
   - Implement safeguards for destructive tests

Example ZAP configuration:

```yaml
# ZAP scanning configuration
scan:
  application:
    url: https://staging.example.com
    name: ExampleApp
  authentication:
    method: form
    loginUrl: https://staging.example.com/login
    usernameField: email
    passwordField: password
    loginIndicator: "Dashboard"
  alerts:
    maxHighRisk: 0
    maxMediumRisk: 3
  spider:
    maxDuration: 60
    blacklist:
      - "logout"
      - "delete"
  active_scan:
    strength: high
    threshold: medium
```

### DAST Integration

1. **Pipeline Integration**:
   - Run DAST in staging/pre-production environments
   - Integrate scheduled DAST scans post-deployment
   - Configure appropriate scan triggers (nightly, on-demand, post-deployment)

2. **API Testing**:
   - Generate OpenAPI/Swagger specifications for automated API testing
   - Implement API security testing in CI/CD pipeline

3. **Continuous Monitoring**:
   - Configure passive scanning for production environments
   - Implement traffic monitoring for security anomalies

Example GitHub Actions workflow for DAST:

```yaml
name: DAST Analysis

on:
  workflow_dispatch:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight
  deployment:
    environments: [staging]

jobs:
  zap-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: ZAP Baseline Scan
        uses: zaproxy/action-baseline@v0.7.0
        with:
          target: 'https://staging.example.com'
          rules_file_name: '.zap/rules.tsv'
          cmd_options: '-a -j'
          
      - name: Upload ZAP Report
        uses: actions/upload-artifact@v2
        with:
          name: zap-report
          path: reports/
```

### DAST Issue Management

1. **Verification**:
   - Validate DAST findings to eliminate false positives
   - Reproduce vulnerabilities in controlled environments
   - Document reproduction steps for developers

2. **Prioritization**:
   - Prioritize externally exposed vulnerabilities
   - Evaluate risk based on exploitability and impact
   - Create security advisories for authenticated vulnerabilities

3. **Remediation Tracking**:
   - Track DAST findings in security issue tracker
   - Set remediation SLAs based on severity
   - Verify fixes with targeted DAST rescans

## DevSecOps Pipeline Integration

1. **Security Gates**:
   - Define security quality gates for each pipeline stage
   - Automatically enforce security requirements for releases

2. **Integrated Workflow**:

   ```plaintext
   Development → Commit → SAST → Build → Deploy to Test → DAST → Security Review → Deploy to Prod
   ```

3. **Continuous Security Testing**:
   - Schedule recurring security scans
   - Implement continuous monitoring
   - Automate regression testing for security fixes

Pipeline configuration example:

```yaml
# Security stages in GitLab CI pipeline
stages:
  - build
  - sast
  - test
  - dast
  - deploy

sast:
  stage: sast
  script:
    - run-sast-tool
  artifacts:
    reports:
      sast: sast-report.json
  rules:
    - if: $CI_COMMIT_BRANCH == "main" || $CI_PIPELINE_SOURCE == "merge_request_event"

dast:
  stage: dast
  script:
    - deploy-to-test-env
    - run-dast-tool
  artifacts:
    reports:
      dast: dast-report.json
  rules:
    - if: $CI_COMMIT_BRANCH == "main" || $CI_PIPELINE_SOURCE == "merge_request_event"

security-gate:
  stage: deploy
  script:
    - evaluate-security-gates
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
```

## Roles and Responsibilities

1. **Developers**:
   - Run local SAST tools before commits
   - Fix identified security issues
   - Write security unit tests

2. **Security Champions**:
   - Review SAST/DAST configurations
   - Assist with remediation
   - Provide security guidance to teams

3. **Security Team**:
   - Configure and maintain SAST/DAST tools
   - Review and validate findings
   - Perform manual penetration testing
   - Provide security training

4. **DevOps Team**:
   - Integrate security tools into CI/CD
   - Maintain security testing environments
   - Monitor security testing performance

## Metrics and Reporting

1. **Key Security Metrics**:
   - Mean time to remediate security issues
   - Security debt (unresolved issues over time)
   - Security test coverage
   - False positive rate
   - Number of vulnerabilities by severity

2. **Reporting Requirements**:
   - Weekly security testing status report
   - Pre-release security assessment
   - Quarterly security posture review
   - Executive dashboard for security metrics

3. **Dashboard Example**:

   ```plaintext
   Security Dashboard
   -----------------
   Total Vulnerabilities: 42
   Critical: 0, High: 3, Medium: 15, Low: 24
   
   Fixed Last 7 Days: 12
   New Last 7 Days: 5
   
   Mean Time to Remediate: 4.2 days
   Security Coverage: 89%
   ```

## Training and Awareness

1. **Developer Training**:
   - Security tool usage training
   - Secure coding workshops
   - Remediation techniques

2. **Security Champions Program**:
   - Advanced security testing training
   - Tool configuration training
   - Vulnerability assessment skills

3. **Continuous Learning**:
   - Monthly security tool updates
   - Lessons learned from security incidents
   - New vulnerability awareness
