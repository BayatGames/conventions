<!--
Document: Software Licensing Guide
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Software Licensing Guide

## Introduction

This guide provides standards and best practices for handling software licenses in Bayat projects. It covers licensing selection, compliance, management, and related processes to ensure legal compliance and protect intellectual property.

## License Selection

### Internal Projects

#### Proprietary Projects

- Use a standard company-specific proprietary license
- Include clear terms for internal use and distribution
- Specify confidentiality requirements
- Document any third-party components and their licenses
- Include appropriate copyright notices

#### Inner Source Projects

- Use a modified proprietary license allowing internal contributions
- Define contribution terms for employees and contractors
- Establish clear ownership and IP assignment
- Document usage rights across business units
- Include guidelines for forking and modification

### Open Source Projects

#### Permissive Licenses

Recommended for developer tools, libraries, and frameworks:

- **MIT License**: Simple, permissive license allowing commercial use
- **Apache License 2.0**: Includes patent protections and contributor terms
- **BSD 3-Clause**: Balanced permissive license with attribution requirements

#### Copyleft Licenses

Consider for foundational technologies or to prevent proprietary forks:

- **GNU GPL v3**: Strong copyleft requiring derivative works to be open-sourced
- **GNU LGPL v3**: Library-focused copyleft allowing proprietary linking
- **Mozilla Public License 2.0**: File-level copyleft with business-friendly terms

#### License Selection Matrix

| Project Type | Recommended Licenses | Considerations |
|-------------|---------------------|----------------|
| Client libraries | MIT, Apache 2.0 | Maximize adoption |
| Developer tools | MIT, BSD | Simplicity, wide acceptance |
| Web services | Apache 2.0 | Patent protections |
| Core technologies | GPL, AGPL | Prevent proprietary forks |
| Plugins/extensions | MPL 2.0, LGPL | Balance openness with integration |

### Dual Licensing

- Considerations for offering both commercial and open source licenses
- Revenue models for dual-licensed software
- License compatibility requirements
- Contributor agreements for dual-licensed projects
- Examples of successful dual licensing models

## License Compliance

### License Inventorying

- Maintain a comprehensive inventory of all licenses used
- Document license details for all dependencies
- Map licenses to specific components and features
- Regularly update and verify license inventory
- Assign responsibility for license tracking

### Dependency Analysis

- Automated scanning of dependencies for license information
- Process for analyzing transitive dependencies
- License compatibility checking
- Risk assessment for problematic licenses
- Documentation of dependency license decisions

### Compliance Checks

- Pre-commit and pre-release license compliance verification
- Automated verification in CI/CD pipelines
- License compatibility matrices for common license combinations
- Processes for resolving compliance issues
- Regular compliance audits

### Attribution Requirements

- Standard format for attribution notices
- Centralized attribution document templates
- Process for collecting and maintaining attributions
- Distribution of attribution information with software
- Verification of complete attribution

## License Management

### License Headers

- Standard license header templates for different languages
- Automated tools for header verification and insertion
- Required elements in license headers
- Header format for generated code
- Header requirements for different license types

### NOTICE and LICENSE Files

- Standard structure for LICENSE files
- NOTICE file requirements and format
- Placement of license information in repositories
- Version control for license files
- Handling license changes

### Software Bill of Materials (SBOM)

- SBOM generation as part of the build process
- Required components in the SBOM
- SBOM format standards (SPDX, CycloneDX)
- SBOM verification and validation
- SBOM distribution and storage

### License Change Management

- Process for changing licenses in existing projects
- Compatibility considerations when upgrading licenses
- Communication to users and contributors about license changes
- Handling of contributions under previous licenses
- Version control and documentation of license history

## Special Cases

### Multi-licensed Code

- Handling components with multiple license options
- Documentation of license selection decisions
- Implementation of license compatibility checks
- Management of multi-license dependencies
- License selection documentation

### Modified Open Source Components

- Tracking modifications to open source components
- Documentation of changes to licensed code
- Compliance with modification disclosure requirements
- Contribution back to upstream projects
- Maintaining separate forks with license compliance

### Generated Code

- License considerations for AI-generated code
- Proper attribution for code generation tools
- Compliance verification for generated code
- Documentation of generation processes
- Review process for generated code licensing

### Containers and Dependencies

- License compliance in containerized applications
- Runtime vs. build-time dependency considerations
- Handling of dynamically linked dependencies
- Container image license documentation
- License scanning for container images

## License Policies

### Approved Licenses

- List of approved licenses for project dependencies
- Process for approving new license types
- License approval criteria
- License categories (approved, restricted, prohibited)
- Documentation of license approval decisions

### License Compatibility

- Compatibility matrix for common license combinations
- Guidelines for integrating components with different licenses
- License boundary management
- Technical measures to ensure license separation
- Documentation of compatibility decisions

### Contribution Licensing

- Contributor License Agreements (CLAs)
- Developer Certificate of Origin (DCO) implementation
- Process for accepting external contributions
- Handling contributions with incompatible licenses
- Verification of contribution license compliance

### Enforcement Policies

- Process for handling compliance violations
- Escalation procedures for license issues
- Remediation requirements and timelines
- Legal response to external enforcement actions
- Prevention of future compliance issues

## Training and Resources

### Developer Training

- License awareness training for developers
- License selection decision trees
- Regular updates on licensing changes and trends
- Practical examples of licensing scenarios
- License compliance tooling training

### Legal Resources

- Contact information for legal assistance
- License interpretation guidelines
- Process for legal review of license questions
- Documentation of previous license determinations
- Legal escalation procedures

### External Resources

- Links to license text repositories
- Industry standards and guidelines
- License compatibility tools
- Open source compliance organizations
- Software composition analysis resources

## Appendix

### License Comparison Table

Detailed comparison of key license attributes for common open source licenses:

| License | Permissive/Copyleft | Patent Grant | Sublicense Rights | Modification Disclosure | Attribution Required |
|---------|-------------------|-------------|------------------|------------------------|---------------------|
| MIT | Permissive | No | Yes | No | Yes |
| Apache 2.0 | Permissive | Yes | Yes | No | Yes |
| BSD 3-Clause | Permissive | No | Yes | No | Yes |
| GPL v3 | Strong Copyleft | Yes | No | Yes | Yes |
| LGPL v3 | Weak Copyleft | Yes | No | Yes (library only) | Yes |
| MPL 2.0 | Weak Copyleft | Yes | No | Yes (file level) | Yes |
| AGPL v3 | Strong Copyleft | Yes | No | Yes + network use | Yes |

### Glossary of Licensing Terms

- **Permissive License**: Minimal restrictions on software reuse
- **Copyleft**: Requires derivative works to be under the same license
- **Patent Grant**: Explicit permission to use patent rights
- **Sublicense**: Right to grant licenses to others
- **Derivative Work**: New work based on original licensed software
- **Distribution**: Providing software to another party
- **Attribution**: Acknowledging original authors
- **License Compatibility**: Ability to combine software under different licenses
- **Copyright**: Legal protection for creative works
- **Intellectual Property (IP)**: Legal rights resulting from intellectual activity
