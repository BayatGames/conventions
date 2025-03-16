# Go Development Standards

This document outlines the standards and best practices for Go development at Bayat.

## Code Style and Formatting

### General Guidelines
- Follow the Go standard style using `gofmt` or `goimports`
- Maximum line length should be 100 characters, but there is flexibility for readability
- Indent with tabs, not spaces
- Files should be encoded in UTF-8
- Files should end with a newline
- Run `go fmt` before committing code

### Naming Conventions
1. **Package Names**:
   - Use short, concise, lowercase names
   - No underscores or mixed caps (e.g., `transport`, `auth`, `payment`)
   - Avoid generic names like `utils` or `common`
   - Package name should match directory name

2. **Interface Names**:
   - Use mixed caps (e.g., `Reader`, `Writer`, `Logger`)
   - One-method interfaces should end with -er (e.g., `Reader`, `Writer`)
   - Don't use "I" prefix for interfaces

3. **Variable and Function Names**:
   - Use camelCase for variable names
   - Use verbs for function names when appropriate
   - Keep names concise but descriptive
   - Acronyms in mixed case should be consistently capitalized (e.g., `HTTPClient`, `URL`)

4. **Constants**:
   - Use camelCase or MixedCaps, not SCREAMING_CASE
   - Group related constants in a const block

5. **Files**:
   - Use snake_case for filenames (e.g., `user_service.go`, `http_client.go`)
   - Meaningful names that reflect their content
   - Test files should be named `*_test.go`

### Code Organization
1. **Directory Structure**:
   - Use the standard Go project layout for consistency
   - Organize by functionality, not by type
   - Place main packages in `cmd/` directory
   - Place library code in `pkg/` directory
   - Place internal code in `internal/` directory

2. **Package Structure**:
   - Keep packages focused on a single responsibility
   - Avoid cyclic dependencies between packages
   - Keep package APIs minimal and well-defined
   - Use internal packages to hide implementation details

3. **File Organization**:
   - Group related functionality in the same file
   - Split large files into smaller, focused files
   - Keep files under 500 lines where possible

## Language Features and Idioms

### Error Handling
1. **Error Creation**:
   - Use `errors.New()` for simple errors
   - Use `fmt.Errorf()` for formatted errors
   - Add context to errors when wrapping them with `%w`
   - Consider using `github.com/pkg/errors` for stack traces

2. **Error Checking**:
   - Always check errors
   - Handle each error at the appropriate level
   - Avoid nested error handling when possible
   - Return errors to callers when appropriate

3. **Error Types**:
   - Define custom error types for specific error cases
   - Implement the `Error()` method to satisfy the error interface
   - Use error sentinel values for expected error conditions
   - Use error wrapping for adding context

### Concurrency
1. **Goroutines**:
   - Be aware of goroutine lifetimes and potential leaks
   - Ensure goroutines can exit normally
   - Use waitgroups to manage goroutine lifecycle
   - Consider goroutine pools for high-frequency operations

2. **Channels**:
   - Document channel ownership (who creates, writes, reads, closes)
   - Prefer buffered channels with known capacity
   - Use select statements for channel multiplexing
   - Follow the "don't close from receiver" rule

3. **Synchronization**:
   - Use mutexes to protect shared state
   - Keep critical sections small
   - Favor composition over inheritance for thread-safe types
   - Use atomic operations for simple counters and flags

### Resource Management
1. **Defer**:
   - Use `defer` for cleanup operations
   - Place `defer` statements near the resource acquisition
   - Be aware of arguments to deferred function calls
   - Remember deferred calls execute in LIFO order

2. **Context**:
   - Use `context.Context` for cancellation and timeouts
   - Pass contexts as the first parameter to functions
   - Don't store contexts in structs
   - Set appropriate timeouts for operations

3. **File and Network Handling**:
   - Always close resources after use
   - Use `defer` to ensure resources are released
   - Check and handle errors from Close() methods
   - Use buffered I/O for better performance

## Data Structures and Algorithms

### Standard Library
1. **Collections**:
   - Use appropriate collection types (slice, map, array)
   - Pre-allocate slices and maps when size is known
   - Be aware of map and slice internals for performance
   - Use sort package for sorting collections

2. **Strings**:
   - Use string builder for frequent concatenation
   - Be mindful of UTF-8 encoding
   - Use appropriate string manipulation functions
   - Consider runes for character-by-character processing

### Custom Types
1. **Structs**:
   - Group related fields together
   - Order fields to minimize padding
   - Use field tags for serialization
   - Document the purpose of each field

2. **Methods**:
   - Choose receiver type (value or pointer) appropriately
   - Be consistent with receiver types
   - Use pointer receivers for mutable methods
   - Use value receivers for immutable methods

## Testing

### Unit Testing
1. **Test Organization**:
   - Place tests in the same package as the code being tested
   - Use `_test.go` suffix for test files
   - Group related tests together
   - Follow the "Arrange, Act, Assert" pattern

2. **Test Functions**:
   - Name tests as `TestXxx` where Xxx describes what's being tested
   - Use table-driven tests for testing multiple cases
   - Use subtests for organizing test cases
   - Keep tests independent and deterministic

3. **Assertions**:
   - Use the standard library's testing package
   - Consider using `testify` for more expressive assertions
   - Provide helpful failure messages
   - Test both positive and negative cases

### Integration Testing
- Use a separate package for integration tests
- Mock external dependencies when appropriate
- Use interfaces for dependency injection
- Consider docker-compose for testing with dependencies

### Benchmarking
- Write benchmarks for performance-critical code
- Use realistic input data for benchmarks
- Run benchmarks consistently on the same hardware
- Compare benchmarks against previous runs

## Documentation

### Code Comments
1. **Package Documentation**:
   - Use a package comment at the top of one file in the package
   - Describe the package's purpose and contents
   - Include usage examples when appropriate
   - Document any package-level variables or constants

2. **Function and Method Documentation**:
   - Document all exported functions and methods
   - Start comments with the function name
   - Describe parameters and return values
   - Document any error conditions

3. **Examples**:
   - Provide runnable examples in documentation
   - Test examples with `go test`
   - Show typical usage patterns
   - Include examples for complex interfaces

### Godoc
- Write documentation with godoc in mind
- Use proper formatting in documentation comments
- Link to related types and functions
- Include examples that illustrate usage

## Dependency Management

### Module Management
1. **Go Modules**:
   - Use Go modules for dependency management
   - Pin versions in go.mod file
   - Vendor dependencies when appropriate
   - Run `go mod tidy` to clean up dependencies

2. **Dependency Selection**:
   - Prefer standard library over third-party packages
   - Evaluate dependencies for security and maintenance
   - Consider license implications
   - Avoid deep dependency trees

3. **Versioning**:
   - Follow semantic versioning principles
   - Document breaking changes between versions
   - Use Go modules' version handling
   - Consider using vanity import paths

## Performance Optimization

### Profiling
1. **Tools**:
   - Use `pprof` for CPU and memory profiling
   - Use benchmarks to measure performance
   - Use trace tool for concurrency analysis
   - Profile in production with minimal overhead

2. **Common Optimizations**:
   - Reduce allocations
   - Use sync.Pool for frequently allocated objects
   - Optimize hot paths based on profiling results
   - Consider mechanical sympathy (CPU caches, etc.)

### Best Practices
- Write clear code first, then optimize
- Benchmark before and after optimizations
- Document performance characteristics
- Use appropriate algorithms and data structures

## Build and Deployment

### Build Process
1. **Build Tags**:
   - Use build tags for conditional compilation
   - Document build tags in package documentation
   - Test with different build tag combinations
   - Keep build constraints in dedicated files

2. **Cross-Compilation**:
   - Set GOOS and GOARCH for target platforms
   - Test on all target platforms
   - Be aware of platform-specific behavior
   - Use build constraints for platform-specific code

3. **Tooling**:
   - Use Makefiles or similar for build automation
   - Define standard build targets
   - Integrate with CI/CD pipelines
   - Include static analysis in the build process

### Deployment
- Build static binaries when possible
- Include version information in binaries
- Consider Docker for containerized deployment
- Follow the "Twelve-Factor App" methodology

## Code Quality

### Static Analysis
1. **Linting**:
   - Use `golint` or `golangci-lint` for code analysis
   - Run linters in CI/CD pipelines
   - Fix all linter warnings
   - Configure linter rules appropriately

2. **Other Tools**:
   - `go vet` for detecting suspicious code
   - `staticcheck` for additional static analysis
   - `errcheck` for ensuring errors are handled
   - `gosec` for security checks

### Code Review
- Review for correctness, maintainability, and performance
- Ensure code follows project standards
- Look for edge cases and error handling
- Check for security issues

## Security

### Input Validation
- Validate all user input
- Use safe parsing for structured data
- Be aware of injection vulnerabilities
- Don't trust external data sources

### Authentication and Authorization
- Use established authentication libraries
- Store credentials securely
- Implement proper access control
- Use HTTPS for all communications

### Common Vulnerabilities
- Be aware of OWASP Top 10
- Avoid common Go security pitfalls
- Use secure coding practices
- Keep dependencies updated

## References
- [Effective Go](https://golang.org/doc/effective_go.html)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Standard Go Project Layout](https://github.com/golang-standards/project-layout)
- [The Twelve-Factor App](https://12factor.net/)
- [Go Security Checklist](https://github.com/Checkmarx/Go-SCP) 