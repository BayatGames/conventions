<!--
Document: Password Policy and Conventions
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Password Policy and Conventions

This document outlines Bayat's comprehensive password policy and conventions for all systems, applications, and services across the organization.

## Table of Contents

- [Password Strength Requirements](#password-strength-requirements)
- [Password Creation Guidelines](#password-creation-guidelines)
- [Password Storage and Management](#password-storage-and-management)
- [Password Lifecycle Management](#password-lifecycle-management)
- [Special Account Types](#special-account-types)
- [Implementation Guidelines](#implementation-guidelines)
- [User Education](#user-education)
- [Compliance and Auditing](#compliance-and-auditing)
- [Technical Implementation](#technical-implementation)
- [References and Tools](#references-and-tools)

## Password Strength Requirements

### Minimum Requirements

- **Length**:
  - Standard user accounts: Minimum 12 characters
  - Privileged accounts: Minimum 16 characters
  - Service accounts: Minimum 20 characters

- **Complexity**:
  - Use a "complexity through length" approach rather than strict character type requirements
  - Encourage passphrases or long passwords over complex but short passwords
  - If character type requirements are necessary for compliance, require at least 3 of these 4 types:
    - Uppercase letters (A-Z)
    - Lowercase letters (a-z)
    - Numbers (0-9)
    - Special characters (!@#$%^&*()_+{}[]|\:;"'<>,.?/)

- **Entropy**:
  - At least 70 bits of entropy for standard accounts
  - At least 90 bits of entropy for privileged accounts

### Prohibited Passwords

- **Common Password Lists**:
  - Block the top 100,000 most common passwords
  - Use resources like the Have I Been Pwned API to check for compromised passwords

- **Context-specific Words**:
  - Block passwords containing:
    - The username or parts of it (with 4+ characters)
    - The company name, product names, or project names
    - Common keyboard patterns (qwerty, 12345, etc.)
    - Simple substitutions of the above (e.g., "B4y4t" for "Bayat")

- **Personal Information**:
  - Discourage use of personal information such as:
    - Names of family members, pets, or close associates
    - Birth dates, anniversary dates
    - Addresses, phone numbers, or ID numbers
    - Public information associated with the user

## Password Creation Guidelines

### Effective Password Strategies

- **Passphrases**:
  - Encourage the use of passphrases: multiple random words combined
  - Example (do not use): "correct-horse-battery-staple"
  - Aim for 4+ random words

- **Mnemonic Techniques**:
  - Create passwords from first letters of a memorable sentence
  - Example: "I love to eat pizza with extra cheese on Fridays!" → "Il2epw3coF!"

- **Random Password Generation**:
  - Provide a secure random password generator
  - Ensure generated passwords are easily inputted on all device types

### Password Feedback and Validation

- **Real-time Strength Meters**:
  - Implement visual password strength meters
  - Use algorithms like zxcvbn for meaningful password strength evaluation
  - Provide actionable feedback on how to improve password strength

- **Acceptance Criteria**:
  - Clearly communicate when a password meets requirements
  - Allow visibility toggles to verify correct typing

## Password Storage and Management

### Password Manager Usage

- **Enterprise Password Management**:
  - Provide and require use of enterprise password management solutions
  - Ensure cross-platform support (desktop, mobile, browser)
  - Configure automatic locking after periods of inactivity

- **Password Manager Security Requirements**:
  - Strong master password (minimum 16 characters)
  - Multi-factor authentication for password manager access
  - Regular backups of the password database
  - End-to-end encryption for all stored data

### Secure Storage Practices

- **Storage Requirements**:
  - Only store passwords using modern, secure hashing algorithms:
    - Argon2id (preferred)
    - bcrypt (minimum cost factor of 10, ideally 12+)
    - PBKDF2 (minimum 310,000 iterations with SHA-256)
  - Use unique, random salts (minimum 16 bytes) for each password
  - Implement a pepper (server-side secret key) for additional security

- **Monitoring and Auditing**:
  - Implement logging for password hash verification attempts
  - Monitor for mass password verification attempts
  - Regular automated audit of hashing implementations

## Password Lifecycle Management

### Password Expiration and Renewal

- **Expiration Policy**:
  - Don't require regular password changes without reason
  - Force password changes only under specific circumstances:
    - Evidence of compromise
    - User role change requiring higher privileges
    - Leaving a shared account
    - After password reset by administrator

- **Change Process**:
  - Require current password verification before allowing changes
  - Verify new password meets all requirements
  - Alert user on all registered communication channels when password is changed

### Account Lockout and Recovery

- **Failed Attempt Handling**:
  - Implement progressive delays between login attempts
  - Temporary account lockout after 5-10 failed attempts
  - Alert user of failed login attempts through secondary channels

- **Recovery Mechanisms**:
  - Implement secure account recovery that doesn't expose or email passwords
  - Use time-limited, single-use recovery tokens
  - Require identity verification through secondary confirmed channels
  - For high-security systems, require admin or help desk intervention

## Special Account Types

### Privileged Accounts

- **Administrator Accounts**:
  - Require stronger passwords (16+ characters)
  - Enforce multi-factor authentication
  - More frequent credential rotation (90 days)
  - Separate admin accounts from regular user accounts

- **Service Accounts**:
  - Use automatically generated, high-entropy passwords (20+ characters)
  - Store in secure vault systems with controlled access
  - Rotate credentials when personnel with access changes
  - Use certificate-based authentication when possible instead of passwords

### Shared Accounts

- **Shared Account Policies**:
  - Discourage shared accounts when possible
  - When necessary, implement through password management with individual accountability
  - Log all access and usage of shared credentials
  - Rotate passwords when team composition changes

## Implementation Guidelines

### Technical Controls

- **Secure Input Methods**:
  - Protect password fields from browser auto-complete when appropriate
  - Prevent cut/copy/paste in sensitive environments if required
  - Mask passwords by default with option to temporarily view

- **API and Service Authentication**:
  - Use API keys, tokens, or certificates instead of passwords when possible
  - Implement expiring access tokens with refresh capability
  - Apply same or higher entropy requirements to API keys as passwords

### Application-Specific Implementations

- **Web Applications**:
  - Implement HTTPS for all authentication traffic
  - Enforce Content Security Policy (CSP) to prevent XSS attacks on login forms
  - Use secure cookie attributes (HttpOnly, Secure, SameSite)

- **Mobile Applications**:
  - Support biometric authentication tied to device cryptography
  - Allow password manager integration
  - Prevent capturing or screenshotting of password input screens

- **Desktop Applications**:
  - Support OS-level credential storage
  - Enable password manager integration
  - Secure memory handling to prevent password extraction

## User Education

### Training and Awareness

- **Initial Training**:
  - Educate users on creating strong, memorable passwords
  - Train on recognizing phishing and social engineering attacks
  - Provide clear guidelines for password management

- **Ongoing Awareness**:
  - Regular security reminders and updates
  - Phishing simulation exercises
  - Clear reporting procedures for suspected compromises

### Documentation and Support

- **Self-Service Resources**:
  - Provide FAQ and knowledge base articles on password security
  - Offer guided password reset processes
  - Include examples of strong passwords and passphrases

- **Help Desk Procedures**:
  - Standardize identity verification for password resets
  - Train help desk staff on secure password practices
  - Document all password reset requests and actions

## Compliance and Auditing

### Regulatory Compliance

- **Standard Alignment**:
  - Ensure password policies align with relevant standards:
    - NIST SP 800-63B
    - ISO/IEC 27001
    - PCI DSS (for payment systems)
    - HIPAA (for health information)
    - GDPR (for EU personal data)

- **Documentation Requirements**:
  - Maintain up-to-date documentation of password policy
  - Record exceptions with business justification
  - Document risk assessments for policy decisions

### Audit and Verification

- **Regular Testing**:
  - Perform password cracking tests on password database dumps
  - Analyze password reset patterns for suspicious activity
  - Review password policy effectiveness annually

- **Compliance Checking**:
  - Automate detection of non-compliant passwords
  - Ensure password hashing implementations remain strong
  - Verify system configurations enforce policy requirements

## Technical Implementation

### Password Validation Code

When implementing password validation logic, use proven libraries rather than custom implementations. Here are examples in various languages:

**JavaScript/TypeScript**:

```javascript
// Using zxcvbn library for password strength
import zxcvbn from 'zxcvbn';

function validatePassword(password, username) {
  // Check minimum length
  if (password.length < 12) {
    return {
      valid: false,
      message: 'Password must be at least 12 characters long'
    };
  }
  
  // Check for username inclusion
  if (username && password.toLowerCase().includes(username.toLowerCase())) {
    return {
      valid: false,
      message: 'Password cannot contain your username'
    };
  }
  
  // Use zxcvbn for comprehensive strength check
  const result = zxcvbn(password);
  
  // Score less than 3 is too weak (scores are 0-4)
  if (result.score < 3) {
    return {
      valid: false,
      message: `Password is too weak: ${result.feedback.warning}. ${result.feedback.suggestions.join(' ')}`
    };
  }
  
  return { valid: true };
}
```

**Python**:

```python
import re
from argon2 import PasswordHasher

def validate_password(password, username=None, context_words=None):
    """
    Validate password strength based on organization policy.
    
    Args:
        password: The password to validate
        username: User's username to check against
        context_words: List of context-specific words to check against
        
    Returns:
        (bool, str): (is_valid, message)
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters long"
        
    # Check for username in password
    if username and username.lower() in password.lower():
        return False, "Password cannot contain your username"
    
    # Check for context-specific words
    if context_words:
        for word in context_words:
            if len(word) > 3 and word.lower() in password.lower():
                return False, f"Password cannot contain '{word}'"
    
    # Check for common patterns
    common_patterns = ['123456', 'qwerty', 'password']
    for pattern in common_patterns:
        if pattern in password.lower():
            return False, "Password contains a common pattern"
            
    return True, "Password meets requirements"
    
def hash_password(password):
    """Hash a password using Argon2id."""
    ph = PasswordHasher(time_cost=3, memory_cost=65536, parallelism=4)
    return ph.hash(password)
    
def verify_password(password_hash, password):
    """Verify a password against its hash."""
    ph = PasswordHasher()
    try:
        ph.verify(password_hash, password)
        return True
    except:
        return False
```

### Password Storage Implementation

**Hashing Example (Node.js)**:

```javascript
const crypto = require('crypto');
const argon2 = require('argon2');

// Generate a random salt
function generateSalt(size = 16) {
  return crypto.randomBytes(size);
}

// Server-side secret (pepper)
const PEPPER = process.env.PASSWORD_PEPPER;

// Hash a password with Argon2id
async function hashPassword(password) {
  // Combine password with pepper
  const passwordWithPepper = `${password}${PEPPER}`;
  
  // Hash with Argon2id
  return await argon2.hash(passwordWithPepper, {
    type: argon2.argon2id,
    memoryCost: 65536, // 64 MB
    timeCost: 3,       // 3 iterations
    parallelism: 4     // 4 parallel threads
  });
}

// Verify a password against a hash
async function verifyPassword(hash, password) {
  const passwordWithPepper = `${password}${PEPPER}`;
  
  try {
    return await argon2.verify(hash, passwordWithPepper);
  } catch (err) {
    console.error('Error verifying password:', err);
    return false;
  }
}
```

## References and Tools

### Password Security Resources

- [NIST Special Publication 800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [Have I Been Pwned](https://haveibeenpwned.com/) - Check if passwords have been exposed in data breaches

### Recommended Tools

- **Password Strength Evaluation**:
  - [zxcvbn](https://github.com/dropbox/zxcvbn) - Realistic password strength estimator
  - [nbvcxz](https://github.com/GoSimpleLLC/nbvcxz) - Java implementation of zxcvbn

- **Password Hashing Libraries**:
  - [Argon2](https://github.com/P-H-C/phc-winner-argon2) - Password hashing library
  - [bcrypt.js](https://github.com/dcodeIO/bcrypt.js) - JavaScript implementation of bcrypt
  - [Passlib](https://passlib.readthedocs.io/) - Python password hashing library

- **Password Managers**:
  - [Bitwarden](https://bitwarden.com/) - Open source password manager
  - [1Password](https://1password.com/) - Enterprise password management
  - [LastPass](https://www.lastpass.com/) - Cloud-based password manager
  - [KeePass](https://keepass.info/) - Local password manager
