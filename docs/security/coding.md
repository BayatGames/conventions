# Secure Coding Standards

This document outlines the secure coding standards and best practices for all Bayat projects. Following these guidelines helps prevent security vulnerabilities and ensures the development of secure, robust applications.

## Table of Contents

- [General Principles](#general-principles)
- [Input Validation](#input-validation)
- [Output Encoding](#output-encoding)
- [Authentication and Authorization](#authentication-and-authorization)
- [Session Management](#session-management)
- [Data Protection](#data-protection)
- [Database Security](#database-security)
- [File Operations](#file-operations)
- [Memory Management](#memory-management)
- [Error Handling and Logging](#error-handling-and-logging)
- [Communications Security](#communications-security)
- [Third-Party Components](#third-party-components)
- [Security Testing](#security-testing)
- [Language-Specific Guidelines](#language-specific-guidelines)
- [Code Review Process](#code-review-process)

## General Principles

These core principles should guide all security-related decisions in code:

1. **Defense in Depth**: Implement multiple layers of security controls
2. **Least Privilege**: Use the minimal permissions necessary
3. **Secure by Default**: Security should be the default state
4. **Fail Securely**: Errors should not compromise security
5. **Open Design**: Security should not depend on obscurity
6. **Keep It Simple**: Complexity is the enemy of security
7. **Fix Security Issues Correctly**: Address root causes, not symptoms
8. **Security as a Requirement**: Security is not optional

## Input Validation

### Validation Approach

Implement thorough input validation:

- Validate all input data, regardless of source
- Use a "whitelist" approach (accept known good)
- Validate for type, length, format, and range
- Implement both client-side and server-side validation
- Normalize input before validation
- Centralize validation logic
- Document validation requirements

### Validation Techniques

Use these validation techniques:

- **Types**: Enforce correct data types (integers, dates, etc.)
- **Format**: Validate patterns using regular expressions
- **Range**: Ensure numeric data is within acceptable bounds
- **Length**: Limit string length to prevent overflows
- **Whitelisting**: Allow only specific approved values

### Input Sources

Apply validation to all input sources:

- URL parameters
- Form fields
- JSON/XML data
- HTTP headers
- Cookies
- File uploads
- API responses
- Database results
- Configuration files

### Examples

#### JavaScript/TypeScript Input Validation Example

```javascript
// Using validation library (e.g., Joi, Yup, Zod)
import { z } from 'zod';

// Define validation schema
const userSchema = z.object({
  id: z.string().uuid(),
  username: z.string().min(3).max(50).regex(/^[a-zA-Z0-9_]+$/),
  email: z.string().email(),
  age: z.number().int().min(13).max(120).optional(),
  role: z.enum(['user', 'admin', 'moderator']),
});

// Validate input
function processUserData(userData) {
  try {
    // Throws error if validation fails
    const validatedData = userSchema.parse(userData);
    
    // Proceed with valid data
    saveUser(validatedData);
  } catch (error) {
    // Handle validation error
    logError('Invalid user data', error);
    throw new ValidationError('User data failed validation');
  }
}
```

#### Java Input Validation Example

```java
import javax.validation.constraints.*;

public class UserRegistrationRequest {
    @NotNull
    @Pattern(regexp = "^[a-zA-Z0-9_]{3,50}$", message = "Username must be alphanumeric, 3-50 characters")
    private String username;
    
    @NotNull
    @Email(message = "Email must be valid")
    private String email;
    
    @NotNull
    @Size(min = 8, max = 100, message = "Password must be 8-100 characters")
    private String password;
    
    @Min(value = 13, message = "Age must be at least 13")
    @Max(value = 120, message = "Age must be realistic")
    private Integer age;
    
    // Getters and setters...
}

// In controller/service:
public void registerUser(UserRegistrationRequest request) {
    Set<ConstraintViolation<UserRegistrationRequest>> violations = validator.validate(request);
    if (!violations.isEmpty()) {
        throw new ValidationException("Invalid user registration data");
    }
    
    // Proceed with valid data...
}
```

## Output Encoding

### Encoding Context

Use context-appropriate encoding:

- **HTML Context**: HTML encode to prevent XSS
- **JavaScript Context**: JavaScript encode strings
- **CSS Context**: CSS encode
- **URL Context**: URL encode parameters
- **XML Context**: XML encode data

### Encoding Libraries

Use established encoding libraries:

- OWASP ESAPI or similar library
- Purpose-built encoders for each context
- Framework-provided encoding utilities
- Avoid custom encoding solutions

### Safe Output Techniques

Implement safe output practices:

- Use template systems with automatic encoding
- Apply encoding immediately before output
- Never mix data and code
- Use Content Security Policy (CSP) headers
- Validate and sanitize rich text content

### Examples

#### HTML Context Encoding (JavaScript)

```javascript
import { encodeForHTML } from 'your-security-library';

function displayUserProfile(user) {
  // Unsafe - XSS vulnerability
  // document.getElementById('username').innerHTML = user.name;
  
  // Safe - Apply HTML encoding
  const encodedName = encodeForHTML(user.name);
  document.getElementById('username').innerHTML = encodedName;
}
```

#### Template Engine with Automatic Encoding (Node.js/Express/EJS)

```javascript
// In Express app setup
app.set('view engine', 'ejs');

// In route handler
app.get('/profile/:id', (req, res) => {
  const user = getUserById(req.params.id);
  
  // EJS automatically HTML-encodes variables by default
  res.render('profile', { user });
});
```

```html
<!-- In EJS template file -->
<div class="profile">
  <h1><%= user.name %></h1> <!-- Automatically HTML encoded -->
  <p><%= user.bio %></p>
  
  <!-- For intentionally unencoded content (CAREFUL!) -->
  <div class="formatted-content"><%- user.formattedContent %></div>
</div>
```

## Authentication and Authorization

### Authentication Fundamentals

Implement robust authentication:

- Use strong, adaptive password hashing (bcrypt, Argon2)
- Enforce multi-factor authentication for sensitive operations
- Implement secure password recovery
- Use secure session management
- Apply rate limiting and account lockout mechanisms
- Log authentication events
- Maintain a secure credential storage system

### Password Requirements

Enforce these password requirements:

- Minimum length of 12 characters
- No common/breached passwords
- Password strength meters for user feedback
- Support for password managers (long passwords, no composition rules)
- Secure transmission of credentials (HTTPS)
- Regular password rotation for privileged accounts only

### Authorization Controls

Implement effective authorization:

- Use Role-Based Access Control (RBAC)
- Apply the principle of least privilege
- Implement fine-grained permissions
- Centralize authorization logic
- Verify authorization on every request
- Revalidate authorization on sensitive operations
- Log authorization decisions

### Examples

#### Password Hashing (Node.js)

```javascript
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

async function hashPassword(plaintext) {
  try {
    const hash = await bcrypt.hash(plaintext, SALT_ROUNDS);
    return hash;
  } catch (error) {
    throw new Error('Password hashing failed');
  }
}

async function verifyPassword(plaintext, hash) {
  try {
    const match = await bcrypt.compare(plaintext, hash);
    return match;
  } catch (error) {
    throw new Error('Password verification failed');
  }
}
```

#### Authorization Middleware (Express.js)

```javascript
// Role-based authorization middleware
function requireRole(role) {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ error: 'Unauthorized' });
    }
    
    if (!req.user.roles.includes(role)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    
    next();
  };
}

// Use in routes
app.get('/admin/users', requireRole('admin'), (req, res) => {
  // Only admins can access this route
  const users = getAllUsers();
  res.json(users);
});
```

## Session Management

### Session Security

Implement secure session handling:

- Generate strong session identifiers
- Transmit session IDs securely (HTTPS, secure cookies)
- Regenerate session IDs after authentication
- Implement idle and absolute session timeouts
- Provide secure session termination
- Enable "remember me" safely
- Store minimal data in sessions

### Cookie Security

Configure cookies securely:

- Use the `Secure` flag (HTTPS only)
- Use the `HttpOnly` flag (no JavaScript access)
- Use the `SameSite` attribute (prevent CSRF)
- Set appropriate `Domain` and `Path` attributes
- Use cookie prefixes for additional security
- Set reasonable expiration times

### Examples

#### Secure Session Configuration (Express.js)

```javascript
const express = require('express');
const session = require('express-session');

const app = express();

app.use(session({
  secret: process.env.SESSION_SECRET,
  name: '__Host-session', // Cookie prefix for added security
  cookie: {
    secure: true,         // HTTPS only
    httpOnly: true,       // Not accessible via JavaScript
    sameSite: 'strict',   // Prevent CSRF
    maxAge: 3600000,      // 1 hour expiration
    path: '/'
  },
  resave: false,
  saveUninitialized: false,
  // Use a secure session store in production
  store: getSessionStore()
}));

// Regenerate session after login
app.post('/login', async (req, res) => {
  const { username, password } = req.body;
  
  const user = await authenticateUser(username, password);
  if (user) {
    // Regenerate session to prevent session fixation
    req.session.regenerate((err) => {
      if (err) {
        return res.status(500).json({ error: 'Session error' });
      }
      
      // Store user info in session
      req.session.user = {
        id: user.id,
        username: user.username,
        roles: user.roles
      };
      
      res.json({ success: true });
    });
  } else {
    res.status(401).json({ error: 'Invalid credentials' });
  }
});

// Secure logout
app.post('/logout', (req, res) => {
  req.session.destroy((err) => {
    res.clearCookie('__Host-session', { path: '/' });
    res.json({ success: true });
  });
});
```

## Data Protection

### Sensitive Data Handling

Handle sensitive data carefully:

- Classify data by sensitivity level
- Minimize collection of sensitive data
- Limit sensitive data exposure
- Implement strong access controls
- Apply data retention limits
- Securely delete data when no longer needed
- Mask or redact sensitive data in logs and displays

### Encryption Requirements

Use strong encryption:

- Use current, strong algorithms (AES-256, RSA-2048+)
- Implement proper key management
- Use different keys for different purposes
- Rotate encryption keys regularly
- Encrypt data in transit (TLS 1.3+)
- Encrypt sensitive data at rest
- Never implement custom cryptography

### Key Management

Implement robust key management:

- Store keys securely, separate from data
- Use key management services when available (AWS KMS, HashiCorp Vault)
- Implement key rotation procedures
- Backup keys securely
- Limit access to keys
- Monitor and log key usage

### Examples

#### Data Encryption (Java)

```java
import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import java.util.Base64;

public class DataEncryptor {
    private static final int GCM_IV_LENGTH = 12;
    private static final int GCM_TAG_LENGTH = 16;
    
    // Encrypt data using AES-GCM
    public String encrypt(byte[] plaintext, SecretKey key) throws Exception {
        // Generate a random IV
        byte[] iv = new byte[GCM_IV_LENGTH];
        secureRandom.nextBytes(iv);
        
        // Create the cipher with AES/GCM/NoPadding
        final Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec parameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH * 8, iv);
        cipher.init(Cipher.ENCRYPT_MODE, key, parameterSpec);
        
        // Perform encryption
        byte[] ciphertext = cipher.doFinal(plaintext);
        
        // Combine IV and ciphertext and return as Base64
        byte[] combined = new byte[iv.length + ciphertext.length];
        System.arraycopy(iv, 0, combined, 0, iv.length);
        System.arraycopy(ciphertext, 0, combined, iv.length, ciphertext.length);
        
        return Base64.getEncoder().encodeToString(combined);
    }
    
    // Decrypt data using AES-GCM
    public byte[] decrypt(String encryptedData, SecretKey key) throws Exception {
        byte[] combined = Base64.getDecoder().decode(encryptedData);
        
        // Extract IV
        byte[] iv = new byte[GCM_IV_LENGTH];
        System.arraycopy(combined, 0, iv, 0, iv.length);
        
        // Extract ciphertext
        byte[] ciphertext = new byte[combined.length - GCM_IV_LENGTH];
        System.arraycopy(combined, GCM_IV_LENGTH, ciphertext, 0, ciphertext.length);
        
        // Decrypt
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        GCMParameterSpec parameterSpec = new GCMParameterSpec(GCM_TAG_LENGTH * 8, iv);
        cipher.init(Cipher.DECRYPT_MODE, key, parameterSpec);
        
        return cipher.doFinal(ciphertext);
    }
}
```

## Database Security

### Query Safety

Prevent SQL injection:

- Use parameterized queries/prepared statements
- Use ORM frameworks correctly
- Avoid dynamic SQL when possible
- Apply input validation before database operations
- Use stored procedures with parameterization
- Implement proper error handling
- Escape outputs if dynamic SQL is unavoidable

### Database Access Controls

Implement database access control:

- Use separate database accounts for different applications
- Apply the principle of least privilege
- Use database roles to organize permissions
- Set appropriate connection limits
- Implement row-level security for multi-tenant systems
- Rotate database credentials regularly
- Use environment-specific credentials

### Examples

#### Parameterized Queries (Python/SQLAlchemy)

```python
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

def get_user_by_username(session, username):
    try:
        # Safe - Parameterized query
        stmt = text("SELECT * FROM users WHERE username = :username")
        result = session.execute(stmt, {"username": username})
        return result.fetchone()
    except SQLAlchemyError as e:
        # Log the error properly
        logger.error(f"Database error: {str(e)}")
        raise DatabaseError("Error retrieving user data")
```

#### ORM Usage (JavaScript/TypeORM)

```javascript
import { getRepository } from "typeorm";
import { User } from "../entity/User";

async function getUserOrders(userId) {
  try {
    const userRepository = getRepository(User);
    
    // Safe - Using ORM methods
    const user = await userRepository.findOne({
      where: { id: userId },
      relations: ["orders"]
    });
    
    if (!user) {
      throw new NotFoundError("User not found");
    }
    
    return user.orders;
  } catch (error) {
    // Proper error handling
    logger.error(`Error fetching user orders: ${error.message}`);
    throw new DatabaseError("Could not retrieve orders");
  }
}
```

## File Operations

### File Upload Security

Secure file uploads:

- Validate file type, size, and content
- Scan uploads for malware
- Store uploads outside web root
- Use a CDN or separate domain for serving user uploads
- Generate random filenames, preserving extensions
- Set proper file permissions
- Implement upload rate limiting

### File Path Security

Prevent path traversal:

- Canonicalize and validate file paths
- Use secure API alternatives to direct file operations
- Avoid including user input in file paths
- Use allowlists for permitted operations
- Never pass unsanitized input to file functions
- Restrict file operations to specific directories

### Examples

#### Secure File Upload (Node.js)

```javascript
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const { promisify } = require('util');
const fileType = require('file-type');

const writeFileAsync = promisify(fs.writeFile);
const UPLOAD_DIR = path.resolve(__dirname, '../uploads');
const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'application/pdf'];

async function saveUploadedFile(fileBuffer, originalFilename) {
  // Check file size
  if (fileBuffer.length > MAX_FILE_SIZE) {
    throw new Error('File exceeds maximum size limit');
  }
  
  // Verify file type using content analysis, not extension
  const type = await fileType.fromBuffer(fileBuffer);
  if (!type || !ALLOWED_MIME_TYPES.includes(type.mime)) {
    throw new Error('Invalid file type');
  }
  
  // Get the original extension
  const extension = path.extname(originalFilename).toLowerCase();
  
  // Generate random filename with original extension
  const randomFilename = crypto.randomBytes(16).toString('hex') + extension;
  
  // Ensure upload directory exists
  if (!fs.existsSync(UPLOAD_DIR)) {
    fs.mkdirSync(UPLOAD_DIR, { recursive: true });
  }
  
  // Save the file
  const filePath = path.join(UPLOAD_DIR, randomFilename);
  await writeFileAsync(filePath, fileBuffer);
  
  // Set secure permissions
  fs.chmodSync(filePath, 0o644);
  
  return {
    filename: randomFilename,
    path: filePath,
    size: fileBuffer.length,
    mimeType: type.mime
  };
}
```

## Memory Management

### Buffer Security

Prevent memory vulnerabilities:

- Use memory-safe languages when possible
- Apply bounds checking on all buffers
- Use safe alternatives to unsafe functions
- Validate buffer sizes before operations
- Initialize memory before use
- Release memory properly
- Avoid user-controlled allocation sizes

### C/C++ Specific Guidance

For C/C++ code:

- Use secure C/C++ functions (e.g., `strncpy` instead of `strcpy`)
- Use static analysis tools
- Avoid dangerous functions (`gets`, `sprintf`, etc.)
- Use smart pointers and RAII in C++
- Implement safe integer arithmetic
- Validate all array indices
- Check for integer overflows

### Examples

#### Buffer Operations in C

```c
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

// Unsafe function
void unsafe_copy(char *input) {
    char buffer[10];
    // BAD: Buffer overflow if input > 9 characters
    strcpy(buffer, input);
}

// Safe function
void safe_copy(const char *input) {
    if (input == NULL) {
        return;
    }
    
    char buffer[10];
    // Better: Uses bounded copy
    strncpy(buffer, input, sizeof(buffer) - 1);
    // Ensure null-termination
    buffer[sizeof(buffer) - 1] = '\0';
}

// Even safer function
void safer_copy(const char *input) {
    if (input == NULL) {
        return;
    }
    
    // Allocate exactly the right amount of memory
    size_t input_len = strlen(input);
    char *buffer = malloc(input_len + 1);
    
    if (buffer == NULL) {
        // Handle allocation failure
        fprintf(stderr, "Memory allocation failed\n");
        return;
    }
    
    // Safe copy with bounds checking
    strncpy(buffer, input, input_len);
    buffer[input_len] = '\0';
    
    // Use the buffer...
    
    // Don't forget to free memory
    free(buffer);
}
```

## Error Handling and Logging

### Secure Error Handling

Implement secure error handling:

- Use structured exception handling
- Never expose stack traces to users
- Use generic error messages in production
- Log detailed errors for debugging
- Validate and sanitize error message contents
- Handle all error conditions
- Maintain proper error state

### Secure Logging

Follow secure logging practices:

- Don't log sensitive data (credentials, tokens, PII)
- Protect log integrity
- Use consistent log formats
- Include security-relevant details in logs
- Set appropriate log levels
- Implement centralized log management
- Establish log retention policies

### Examples

#### Secure Error Handling (Java)

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class PaymentProcessor {
    private static final Logger logger = LoggerFactory.getLogger(PaymentProcessor.class);
    
    public PaymentResult processPayment(PaymentRequest request) {
        try {
            validateRequest(request);
            PaymentResult result = paymentGateway.submitPayment(request);
            logger.info("Payment processed successfully, id: {}", result.getTransactionId());
            return result;
        } catch (ValidationException e) {
            // Client error, can show specific message
            logger.warn("Payment validation failed: {}", e.getMessage());
            throw new PaymentException("The payment information is invalid", e);
        } catch (PaymentGatewayException e) {
            // Log detailed error
            logger.error("Payment gateway error: {}", e.getMessage(), e);
            // Return generic message to user
            throw new PaymentException("Payment processing failed, please try again later");
        } catch (Exception e) {
            // Unexpected error, log fully but return generic message
            logger.error("Unexpected error processing payment", e);
            throw new PaymentException("An unexpected error occurred");
        }
    }
}
```

#### Secure Logging (C#)

```csharp
using Microsoft.Extensions.Logging;
using System;

public class UserService
{
    private readonly ILogger<UserService> _logger;
    
    public UserService(ILogger<UserService> logger)
    {
        _logger = logger;
    }
    
    public User AuthenticateUser(string username, string password)
    {
        try
        {
            _logger.LogInformation("Authentication attempt for user: {Username}", username);
            
            // NEVER log passwords
            // BAD: _logger.LogDebug("Auth attempt with password: {Password}", password);
            
            var user = _userRepository.FindByUsername(username);
            if (user == null)
            {
                _logger.LogWarning("Authentication failed - user not found: {Username}", username);
                return null;
            }
            
            bool isValid = _passwordHasher.VerifyPassword(password, user.PasswordHash);
            if (!isValid)
            {
                _logger.LogWarning("Authentication failed - invalid password for user: {Username}", username);
                return null;
            }
            
            // Log success but don't include sensitive user details
            _logger.LogInformation("User authenticated successfully: {Username}, UserId: {UserId}", 
                username, user.Id);
                
            return user;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error during authentication for user: {Username}", username);
            throw new AuthenticationException("Authentication failed", ex);
        }
    }
}
```

## Communications Security

### TLS Configuration

Implement secure TLS:

- Require TLS 1.2+ for all communications
- Use strong cipher suites
- Implement proper certificate validation
- Use certificate pinning for mobile apps
- Configure HSTS headers
- Disable insecure protocols and ciphers
- Test TLS configuration regularly

### API Security

Secure API communications:

- Use secure authentication methods (OAuth 2.0, JWT)
- Implement rate limiting
- Validate all API requests
- Use CORS appropriately
- Consider API gateway solutions
- Document security requirements
- Monitor API usage

### Examples

#### HTTPS Configuration (Node.js)

```javascript
const https = require('https');
const fs = require('fs');
const express = require('express');

const app = express();

// Your app setup...

// TLS configuration (production-ready)
const tlsOptions = {
  key: fs.readFileSync('/path/to/private.key'),
  cert: fs.readFileSync('/path/to/certificate.crt'),
  ca: fs.readFileSync('/path/to/ca.crt'),
  ciphers: [
    'TLS_AES_256_GCM_SHA384',
    'TLS_AES_128_GCM_SHA256',
    'TLS_CHACHA20_POLY1305_SHA256',
    'ECDHE-RSA-AES256-GCM-SHA384',
    'ECDHE-RSA-AES128-GCM-SHA256'
  ].join(':'),
  honorCipherOrder: true,
  minVersion: 'TLS1.2'
};

// Create HTTPS server
const server = https.createServer(tlsOptions, app);

// Set up HSTS middleware
app.use((req, res, next) => {
  res.setHeader('Strict-Transport-Security', 'max-age=63072000; includeSubDomains; preload');
  next();
});

server.listen(443, () => {
  console.log('HTTPS server running on port 443');
});

// Redirect HTTP to HTTPS
const httpRedirect = express();
httpRedirect.all('*', (req, res) => {
  return res.redirect(301, `https://${req.headers.host}${req.url}`);
});

httpRedirect.listen(80, () => {
  console.log('HTTP redirect server running on port 80');
});
```

## Third-Party Components

### Dependency Management

Follow the [Dependency Management standards](docs/dependencies/management.md) for general guidelines on managing third-party dependencies.

Specific security considerations include:

- Use package managers with lockfiles
- Pin dependency versions where practical
- Regularly update dependencies to patch vulnerabilities
- Scan dependencies for known vulnerabilities (see below)
- Maintain an inventory of dependencies and their licenses
- Use trusted sources and verify package integrity
- Evaluate security posture of dependencies before adoption

### Dependency Scanning

Use dependency scanning tools to identify vulnerabilities in third-party libraries:

- **OWASP Dependency Check**: Scan for known vulnerabilities in dependencies
- **Snyk**: Monitor for new vulnerabilities in dependencies
- **WhiteSource**: Provide detailed dependency analysis

### Examples

#### OWASP Dependency Check Configuration (Maven)

```xml
<!-- pom.xml -->
<project>
  <build>
    <plugins>
      <plugin>
        <groupId>org.owasp</groupId>
        <artifactId>dependency-check-maven</artifactId>
        <version>9.2.0</version> <!-- Use the latest version -->
        <executions>
          <execution>
            <goals>
              <goal>check</goal>
            </goals>
          </execution>
        </executions>
        <configuration>
          <!-- Optional: Configure suppression file -->
          <!-- <suppressionFiles>
            <suppressionFile>dependency-check-suppressions.xml</suppressionFile>
          </suppressionFiles> -->
          <!-- Optional: Fail build on CVSS score -->
          <!-- <failBuildOnCVSS>8</failBuildOnCVSS> -->
        </configuration>
      </plugin>
    </plugins>
  </build>

  <!-- ... other project configurations ... -->

</project>
```

#### Secure Dependency Management (Node.js/npm)

```json
// package.json
{
  "name": "my-secure-app",
  "version": "1.0.0",
  "engines": {
    "node": ">=16.0.0"
  },
  "scripts": {
    "audit": "npm audit --production",
    "start": "node app.js",
    "preinstall": "npx npm-force-resolutions"
  },
  "dependencies": {
    "express": "4.18.2",
    "helmet": "6.0.1",
    "jsonwebtoken": "9.0.0"
  },
  "devDependencies": {
    "jest": "29.3.1"
  },
  "resolutions": {
    "minimist": "1.2.6"
  }
}
```

CI/CD Security Checks:

```yaml
# Example GitHub Actions workflow for security
name: Security Checks

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # Weekly check

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '16'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Run npm audit
        run: npm audit --production
        
      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Security Testing

### Testing Approach

Implement security testing:

- Include security tests in CI/CD pipeline
- Perform SAST (Static Application Security Testing)
- Conduct DAST (Dynamic Application Security Testing)
- Implement SCA (Software Composition Analysis)
- Schedule regular penetration testing
- Use security regression testing
- Test business logic for security flaws

### Security Testing Tools

Use these testing tools:

- SAST: SonarQube, ESLint Security Plugin, CodeQL
- DAST: OWASP ZAP, Burp Suite
- SCA: OWASP Dependency Check, Snyk, WhiteSource
- Container scanning: Trivy, Clair
- Infrastructure scanning: Terraform security scanners

### Examples

#### ESLint Security Configuration

```javascript
// .eslintrc.js
module.exports = {
  extends: [
    'eslint:recommended',
    'plugin:security/recommended'
  ],
  plugins: [
    'security'
  ],
  rules: {
    'security/detect-buffer-noassert': 'error',
    'security/detect-child-process': 'error',
    'security/detect-disable-mustache-escape': 'error',
    'security/detect-eval-with-expression': 'error',
    'security/detect-no-csrf-before-method-override': 'error',
    'security/detect-non-literal-fs-filename': 'error',
    'security/detect-non-literal-regexp': 'error',
    'security/detect-non-literal-require': 'error',
    'security/detect-object-injection': 'error',
    'security/detect-possible-timing-attacks': 'error',
    'security/detect-pseudoRandomBytes': 'error',
    'security/detect-unsafe-regex': 'error'
  }
};
```

## Language-Specific Guidelines

### JavaScript/TypeScript

- Use strict mode (`'use strict';`)
- Apply Content Security Policy
- Avoid `eval()` and similar dynamic execution
- Use typed interfaces in TypeScript
- Validate JSON before parsing
- Use secure functions for parsing data
- Apply automatic dependency scanning

### Python

- Use input validation libraries
- Apply CSRF protection in web frameworks
- Avoid `pickle` for untrusted data
- Use `secrets` module for cryptographic operations
- Be cautious with dynamic imports
- Validate YAML, XML inputs
- Use parameterized SQL queries

### Java

- Use security manager appropriately
- Apply static analysis tools for Java
- Validate XML inputs against XXE
- Use prepared statements for SQL
- Apply secure deserialization practices
- Avoid reflection with untrusted data
- Implement proper error handling

### C/C++

- Use modern C++ features for safety
- Apply static analysis tools
- Avoid unsafe string functions
- Validate array bounds
- Check integer operations for overflow
- Properly manage memory allocation
- Test for format string vulnerabilities

## Code Review Process

### Security Review Checklist

Include these in security reviews:

- Input validation implementation
- Output encoding practices
- Authentication and authorization controls
- Secure communications
- Proper error handling
- Sensitive data protection
- SQL injection prevention
- File operation safety
- Third-party component security
- Business logic security

### Security Review Tools

Use automated tools in reviews:

- Code quality scanners
- Security-focused linters
- Dependency scanners
- Commit hooks for pre-commit checks
- IDE security plugins
- Customized security rules

### Review Culture

Foster a security-aware culture:

- Train developers on security concepts
- Recognize and reward secure coding practices
- Use blameless postmortems for security issues
- Share security lessons learned
- Continuously improve security review process
- Build security champions within teams

## Secure Coding

Refer to the [Secure Coding Standards](docs/security/coding.md) for detailed guidelines on writing secure code across different languages and platforms.

Key principles include:

- Input validation and sanitization
- Output encoding
- Secure authentication and authorization
- Proper error handling and logging
- Protection against common vulnerabilities (OWASP Top 10)
- Dependency security management

Integrating security practices early and throughout the development process is crucial. See also: [DevSecOps Practices](docs/security/devsecops.md) and [Data Protection Standards](docs/security/data-protection.md).

## Testing

Refer to the [Testing Standards](docs/quality/testing.md) and [Frontend Testing Standards](docs/quality/frontend-testing.md) for comprehensive testing guidelines.

Security-specific testing includes:

- **Static Application Security Testing (SAST)**: Analyze source code for vulnerabilities.
- **Dynamic Application Security Testing (DAST)**: Test running applications for vulnerabilities.
- **Software Composition Analysis (SCA)**: Identify vulnerabilities in dependencies.
- **Penetration Testing**: Simulate attacks to find weaknesses.
- **Fuzz Testing**: Provide invalid or unexpected data to find crashes or vulnerabilities.

## Incident Response

Establish clear incident response procedures:

- **Detection**: Monitor for security incidents.
- **Containment**: Limit the impact of an incident.
- **Eradication**: Remove the cause of the incident.
- **Recovery**: Restore affected systems.
- **Post-mortem**: Analyze the incident and improve defenses.

## Compliance and Governance

Ensure adherence to relevant security standards and regulations:

- **GDPR**, **CCPA** for privacy compliance.
- **PCI DSS** for payment processing.
- **SOC 2**, **ISO 27001** for general security posture.
- Internal security policies and standards.

## Security Culture

Foster a strong security culture:

- **Training**: Regular security awareness and secure coding training.
- **Security Champions**: Designate security experts within teams.
- **Communication**: Share security updates and best practices.
- **Responsibility**: Security is everyone's responsibility.

## References

- [OWASP Top 10](https://owasp.org/Top10/)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)
- [NIST Secure Software Development Framework](https://csrc.nist.gov/Projects/ssdf)
- [SANS Institute](https://www.sans.org/)
- [CERT Secure Coding Standards](https://wiki.sei.cmu.edu/confluence/display/seccode/SEI+CERT+Coding+Standards)

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2025-03-20 | Initial version |
