# Authentication Best Practices

This document outlines Bayat's standards and best practices for implementing secure authentication across all projects and platforms.

## Table of Contents

- [General Principles](#general-principles)
- [Password Standards](#password-standards)
- [Multi-Factor Authentication](#multi-factor-authentication)
- [Session Management](#session-management)
- [Token-Based Authentication](#token-based-authentication)
- [OAuth and OpenID Connect](#oauth-and-openid-connect)
- [Single Sign-On (SSO)](#single-sign-on-sso)
- [API Authentication](#api-authentication)
- [Mobile Authentication](#mobile-authentication)
- [Account Recovery](#account-recovery)
- [Biometric Authentication](#biometric-authentication)
- [Implementation Guidelines by Platform](#implementation-guidelines-by-platform)
- [Testing and Validation](#testing-and-validation)
- [Compliance Considerations](#compliance-considerations)

## General Principles

- **Defense in Depth**: Never rely on a single authentication mechanism
- **Least Privilege**: Grant minimal access required for the user's role
- **Secure by Default**: All authentication systems must be secure in their default configuration
- **Usability vs. Security**: Balance security requirements with user experience
- **Fail Securely**: Authentication failures should not reveal sensitive information
- **Centralized Authentication**: Use centralized authentication services where possible

## Password Standards

### Minimum Requirements

- **Length**: Minimum 12 characters
- **Complexity**: No specific character type requirements, but encourage use of:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
- **Prohibit Common Passwords**: Block the top 10,000 most common passwords
- **Context-specific Banned Words**: Prevent use of application name, username, and other context-specific terms
- **Detailed Standards**: For comprehensive password requirements, policies, and implementation guidelines, refer to our [Password Policy and Conventions](password-policy.md) document

### Password Storage

- **Use Modern Hashing Algorithms**: bcrypt, Argon2id, or PBKDF2 with sufficient iterations
- **Never Store Plaintext Passwords**: Even temporarily
- **Salt All Passwords**: Use unique, random salts for each password
- **Implement Pepper**: Add a server-side secret to password hashing when possible
- **Implementation Details**: For detailed implementation guidance, see the [Password Policy and Conventions](password-policy.md) document

### Password Policies

- **No Mandatory Rotation**: Don't force regular password changes unless there's evidence of compromise
- **Password Change Verification**: Require current password to set a new one
- **Prevent Password Reuse**: Maintain history of password hashes to prevent reuse
- **Sensitive Account Lockout**: Implement progressive delays or temporary lockouts after multiple failed attempts
- **Advanced Policies**: For more detailed password lifecycle management, account recovery, and special account policies, refer to the [Password Policy and Conventions](password-policy.md) document

## Multi-Factor Authentication (MFA)

### Implementation Requirements

- **Mandatory for Privileged Access**: Require MFA for admin accounts, financial operations, and sensitive data access
- **Optional but Encouraged for Regular Users**: Incentivize MFA adoption for all users
- **Multiple Options**: Support at least two different second-factor methods

### Supported Methods

- **Time-based One-Time Passwords (TOTP)**: Preferred primary second factor
- **Security Keys**: Support for FIDO2/WebAuthn where possible
- **Push Notifications**: For mobile applications
- **SMS/Email as Fallback Only**: Not recommended as primary second factor

### Recovery Planning

- **Backup Codes**: Provide one-time use backup codes
- **Multiple Registered Devices**: Allow registration of multiple MFA devices
- **Emergency Procedures**: Document process for account recovery when MFA is not available

## Session Management

### Session Creation

- **Generate Strong Session IDs**: Use cryptographically secure random IDs with high entropy
- **New Session on Authentication**: Create a new session after login/privilege change
- **Session Context Validation**: Include device fingerprint and IP address in session validation

### Session Storage

- **Server-Side Session Storage**: Prefer over client-only storage
- **Encrypted Cookie Contents**: If using cookies, encrypt the contents
- **Secure Cookie Flags**: Always use Secure and HttpOnly flags for authentication cookies
- **SameSite Cookie Attribute**: Use "Strict" or "Lax" for session cookies

### Session Expiration and Renewal

- **Absolute Timeout**: Maximum session duration of 24 hours for high-security applications
- **Idle Timeout**: Expire after 30-120 minutes of inactivity, depending on sensitivity
- **Sliding Expiration**: Renew session timeout on activity
- **Remember Me Functionality**: Implement with separate, long-lived token with limited privileges

### Session Termination

- **Logout Function**: Clear session data on server and client
- **Single Sign-Out**: Propagate logout to all integrated services
- **Force Session Termination**: Ability to terminate all sessions for a user account

## Token-Based Authentication

### JWT Standards

- **Token Contents**: Include only necessary claims in payload
- **Signature Algorithm**: Use RS256 or ES256 for asymmetric signing
- **Token Expiration**: Short-lived access tokens (5-60 minutes)
- **Token Validation**: Validate all claims before granting access
- **Token Revocation**: Implement token blacklisting or leverage Redis/cache for active management

### Refresh Token Handling

- **Longer Validity**: Typically 1-14 days depending on sensitivity
- **Secure Storage**: Store in HttpOnly, Secure cookie or secure mobile storage
- **Single Use**: Exchange for new refresh token with each use (token rotation)
- **Bound to Device**: Include device identifier in token validation
- **Revocation**: Ability to revoke all refresh tokens for a user

## OAuth and OpenID Connect

### Implementation Standards

- **Approved Flows**:
  - Authorization Code Flow with PKCE for web applications
  - Authorization Code Flow for server-side applications
  - Device Flow for limited-input devices
  - **Avoid**: Implicit Flow and Resource Owner Password Credentials Flow

### Configuration Requirements

- **State Parameter**: Always use to prevent CSRF attacks
- **Scope Limitations**: Request minimal necessary scopes
- **Redirect URI Validation**: Strict validation of pre-registered URIs
- **Client Authentication**: Use client_secret for confidential clients
- **PKCE**: Required for all public clients

### Provider Guidelines

- **Approved Identity Providers**:
  - First-party identity provider based on certified OAuth implementation
  - Major providers: Google, Microsoft, Apple, etc.
  - Custom enterprise IdP only after security review

## Single Sign-On (SSO)

### Implementation Standards

- **Protocol Choice**: Prefer OpenID Connect, SAML 2.0 as fallback for enterprise
- **Identity Provider Selection**: Follow OAuth/OIDC provider guidelines above
- **User Provisioning**: Document SCIM or similar for user management
- **Account Linking**: Enable linking multiple authentication methods to a single user account

### Security Controls

- **Federation Restrictions**: Control which external domains can authenticate
- **Just-in-Time Provisioning**: Create accounts securely at first login
- **Role Mapping**: Document how external IdP roles/groups map to application permissions
- **Attribute Verification**: Validate claims and attributes from identity providers

## API Authentication

### Standards by API Type

- **Public APIs**:
  - API keys with rate limiting and minimal privileges
  - OAuth 2.0 for user-context operations

- **Partner APIs**:
  - OAuth 2.0 Client Credentials flow
  - Mutual TLS (mTLS) for highly sensitive integrations

- **Internal APIs**:
  - Service-to-service: JWT or mTLS
  - User-context: Forward user authentication token with additional context

### API Key Management

- **Issuance Process**: Document secure generation and delivery process
- **Rotation Policy**: Regular rotation schedule and on-demand rotation
- **Revocation Process**: Immediate revocation capability
- **Storage Requirements**: Store hashed, not plaintext API keys

## Mobile Authentication

### Implementation Requirements

- **Secure Local Storage**: Use platform secure storage (Keychain, Keystore) for credentials
- **Biometric Integration**: Follow biometric authentication guidelines below
- **Certificate Pinning**: Implement for API communications
- **Device Binding**: Link authentication tokens to device identifiers
- **Offline Authentication**: Document standards for offline usage if required

### App-Specific Considerations

- **Automatic Logout**: When app moves to background for sensitive applications
- **Screenshot Prevention**: Disable screenshots on authentication screens
- **Secure Keyboard**: Use secure keyboard for credential entry where available
- **Jailbreak/Root Detection**: Implement for high-security applications

## Account Recovery

### Password Reset Mechanisms

- **Secure Delivery Method**: Time-limited, single-use reset links
- **Secondary Verification**: Require additional verification for high-value accounts
- **Rate Limiting**: Implement limits on reset requests
- **Notification**: Alert user through secondary channel when password reset occurs

### Recovery Questions

- **If Used**: Require multiple questions with non-discoverable answers
- **Preference**: Prefer other verification methods over security questions
- **Storage**: Store answers with the same protection as passwords

### Verification Methods

- **Approved Channels**:
  - Email to registered address
  - SMS to verified phone number
  - Authenticator app push notification
  - Recovery codes provided during account setup

## Biometric Authentication

### Implementation Guidelines

- **Local Verification Only**: Biometric data should never leave the user's device
- **Fallback Mechanism**: Always provide alternate authentication method
- **Server Attestation**: Verify biometric verification happened on trusted hardware
- **Framework Use**: Use platform-provided APIs (FaceID, TouchID, Biometric API)

### User Experience Considerations

- **Transparent Operation**: Clear communication about biometric data usage
- **Opt-in Only**: Never mandate biometric authentication
- **Privacy Notices**: Include in application terms and privacy policy

## Implementation Guidelines by Platform

### Web Applications

- **HTTPS Requirement**: Enforce HTTPS for all authentication endpoints
- **Anti-Automation**: Implement CAPTCHA or similar for login attempts where needed
- **CSP Headers**: Set appropriate Content-Security-Policy headers
- **Login Forms**: Submit to same domain, never include in iframes

### Mobile Applications

- **Secure Auth Storage**: Use platform secure storage mechanisms
- **Certificate Validation**: Implement proper SSL validation with pinning
- **App-Specific Security**: Follow platform vendor security guidelines

### Desktop Applications

- **Credential Storage**: Use OS credential management (Keychain, Credential Manager)
- **Auto-Update**: Ensure authentication libraries can be updated
- **Local Encryption**: Encrypt any locally stored auth data

## Testing and Validation

### Required Testing

- **Penetration Testing**: Regular testing of authentication mechanisms
- **Credential Stuffing Resistance**: Test resistance to automated attacks
- **Brute Force Prevention**: Verify rate limiting and account lockout
- **Authentication Bypass Testing**: Verify no authentication bypass vulnerabilities

### Validation Methods

- **OWASP Testing Guide**: Follow OWASP Authentication Testing guidelines
- **Automated Scanning**: Regular automated scanning for common vulnerabilities
- **Manual Review**: Code review of authentication implementation by security team

## Compliance Considerations

### Regulatory Requirements

- **GDPR**: Compliance with user data protection requirements
- **PCI DSS**: Follow requirements for authentication in payment systems
- **SOC 2**: Align with SOC 2 authentication requirements
- **Industry-Specific**: Address vertical-specific requirements (HIPAA, etc.)

### Internal Requirements

- **Audit Logging**: Log all authentication events for audit purposes
- **Monitoring**: Implement monitoring for suspicious authentication activity
- **Risk Assessment**: Regular risk assessment of authentication systems
- **Documentation**: Maintain current documentation of authentication systems

## References

- [NIST SP 800-63B Digital Identity Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Session Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html)
- [JWT Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-jwt-bcp) 