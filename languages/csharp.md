# C# Coding Conventions

This document outlines the C# coding conventions and standards for all Bayat projects. Following these guidelines ensures code consistency, readability, and maintainability across all projects.

## Table of Contents

- [Naming Conventions](#naming-conventions)
- [Code Organization](#code-organization)
- [Coding Practices](#coding-practices)
- [Documentation](#documentation)
- [Performance Considerations](#performance-considerations)
- [Game-Specific Guidelines](#game-specific-guidelines)
- [Testing](#testing)
- [Tools and Enforcement](#tools-and-enforcement)

## Naming Conventions

### General Principles

- Names should be descriptive and reveal intention
- Choose clarity over brevity
- Avoid abbreviations unless universally understood
- Use consistent terminology throughout the codebase

### Specific Naming Patterns

| Element | Case | Example |
|---------|------|---------|
| Classes/Types | PascalCase | `PlayerController` |
| Interfaces | PascalCase with 'I' prefix | `IInteractable` |
| Methods | PascalCase | `CalculateDamage` |
| Properties | PascalCase | `PlayerHealth` |
| Fields (private) | camelCase with underscore prefix | `_playerHealth` |
| Fields (public) | PascalCase | `MaxHealth` |
| Parameters | camelCase | `damageAmount` |
| Local Variables | camelCase | `tempHealth` |
| Constants | UPPER_SNAKE_CASE | `MAX_PLAYER_COUNT` |
| Enums | PascalCase | `PlayerState` |
| Enum Values | PascalCase | `PlayerState.Running` |
| Events | PascalCase | `OnPlayerDeath` |
| Namespaces | PascalCase | `Bayat.Core.Utils` |

### File Naming

- One class per file (with exceptions for small related classes)
- Filename should match the primary class name: `PlayerController.cs`
- Test files should be named `[Tested Class]Tests.cs`: `PlayerControllerTests.cs`

## Code Organization

### Namespaces

Organize namespaces following this pattern:

```csharp
namespace Bayat.[ProductName].[Module].[Submodule]
```

Example:
```csharp
namespace Bayat.Game.Character.Movement
```

### File Structure

Organize class members in the following order:

1. Nested classes
2. Constants and static readonly fields
3. Static fields
4. Instance fields
5. Constructors and finalizers
6. Properties
7. Methods
8. Events

Use `#region` directives to group related members:

```csharp
#region Properties

public float Health { get; private set; }
public bool IsAlive => Health > 0;

#endregion

#region Public Methods

public void TakeDamage(float amount) 
{
    // Method implementation
}

#endregion
```

### Using Directives

- Place using directives at the top of the file, outside the namespace
- Group and sort using directives in the following order:
  1. System namespaces
  2. Third-party namespaces
  3. Bayat namespaces
- Remove unnecessary using directives

Example:
```csharp
using System;
using System.Collections.Generic;
using System.Linq;

using UnityEngine;
using TMPro;

using Bayat.Core.Utils;
using Bayat.Game.Character;
```

## Coding Practices

### Accessibility

- Make classes and members as restrictive as possible
- Use explicit access modifiers (don't rely on default internal/private)
- Consider using `internal` for classes not meant for external use

### Classes and Interfaces

- Keep classes focused on a single responsibility
- Prefer composition over inheritance
- Use interfaces to define contracts
- Limit class inheritance depth to 3 levels when possible

### Methods

- Keep methods short (aim for under 30 lines)
- Methods should do one thing and do it well
- Limit parameters to 4 or fewer; use parameter objects for more
- Return early to avoid deep nesting

Example:
```csharp
public bool TryGetPlayer(int id, out Player player)
{
    player = null;
    
    if (id <= 0)
        return false;
        
    if (!_players.ContainsKey(id))
        return false;
        
    player = _players[id];
    return true;
}
```

### Properties

- Use auto-implemented properties when no additional logic is needed
- Use expression-bodied members for simple properties

```csharp
// Auto-implemented property
public string Name { get; private set; }

// Expression-bodied property
public bool IsValid => !string.IsNullOrEmpty(Name) && Health > 0;
```

### Error Handling

- Use exceptions for exceptional conditions, not for control flow
- Catch specific exceptions rather than Exception
- Include meaningful exception messages
- Use nullable types and `TryGetX` patterns rather than exceptions for expected failure cases

### Async Code

- Suffix async methods with "Async"
- Always use `await` with async calls, or explicitly note when not doing so
- Use `Task.ConfigureAwait(false)` in library code
- Use cancellation tokens for cancellable operations

```csharp
public async Task<PlayerData> LoadPlayerDataAsync(int playerId, CancellationToken cancellationToken = default)
{
    try 
    {
        var result = await _repository.GetPlayerAsync(playerId, cancellationToken);
        return result;
    }
    catch (RepositoryException ex)
    {
        _logger.LogError($"Failed to load player {playerId}: {ex.Message}");
        throw new PlayerLoadException($"Could not load player {playerId}", ex);
    }
}
```

### LINQ

- Use LINQ for readability but be mindful of performance
- Prefer method syntax over query syntax for consistency
- Use meaningful variable names in lambda expressions
- Break long LINQ chains into multiple statements with intermediate variables

```csharp
// Good: Clear and readable
var activeAdults = people
    .Where(person => person.Age >= 18)
    .Where(person => person.IsActive)
    .OrderBy(person => person.LastName)
    .ToList();

// Avoid: Hard to understand at a glance
var result = people.Where(p => p.Age >= 18 && p.IsActive).OrderBy(p => p.LastName).ToList();
```

## Documentation

### Comments

- Write comments for "why", not "what" (the code should be self-explanatory)
- Use XML documentation for public APIs
- Update comments when code changes
- Use TODO comments with ticket numbers for unfinished work

### XML Documentation

Document all public types and members with XML documentation:

```csharp
/// <summary>
/// Represents a player in the game.
/// </summary>
public class Player
{
    /// <summary>
    /// Applies damage to the player.
    /// </summary>
    /// <param name="amount">The amount of damage to apply.</param>
    /// <param name="damageType">The type of damage being applied.</param>
    /// <returns>True if the player survived the damage, false if the player died.</returns>
    public bool TakeDamage(float amount, DamageType damageType)
    {
        // Implementation
    }
}
```

## Performance Considerations

### General Guidelines

- Prefer value types for small, simple data structures
- Use `StringBuilder` for string concatenation in loops
- Cache results of expensive operations
- Minimize allocations in performance-critical code
- Use appropriate data structures for the operation
- Be mindful of boxing/unboxing costs

### Unity-Specific Performance

- Cache component references rather than using GetComponent repeatedly
- Use object pooling for frequently created and destroyed objects
- Minimize operations in Update methods
- Use coroutines or Invoke for delayed operations
- Be mindful of garbage collection in game loops

```csharp
// Cache component reference
private Rigidbody _rigidbody;

private void Awake()
{
    _rigidbody = GetComponent<Rigidbody>();
}

private void ApplyForce(Vector3 direction)
{
    // Use cached reference
    _rigidbody.AddForce(direction);
}
```

## Game-Specific Guidelines

### MonoBehaviour Usage

- Initialize components in Awake, not in constructors
- Set up references between objects in Start
- Use appropriate message functions (Update, FixedUpdate, LateUpdate)
- Keep Update methods lightweight
- Use [SerializeField] for inspector-exposed private fields

```csharp
public class PlayerController : MonoBehaviour
{
    [SerializeField] private float _moveSpeed = 5f;
    [SerializeField] private Transform _cameraTransform;
    
    private Rigidbody _rigidbody;
    private PlayerInput _input;
    
    private void Awake()
    {
        _rigidbody = GetComponent<Rigidbody>();
        _input = new PlayerInput();
    }
    
    private void Start()
    {
        if (_cameraTransform == null)
        {
            _cameraTransform = Camera.main.transform;
        }
    }
    
    private void Update()
    {
        ProcessInput();
    }
    
    private void FixedUpdate()
    {
        MovePlayer();
    }
}
```

### Serialization

- Use [SerializeField] for fields that need to be serialized but remain private
- Implement ISerializationCallbackReceiver for complex serialization needs
- Be mindful of serialization limitations (no interfaces, etc.)
- Use ScriptableObjects for shared configuration data

### Component Design

- Follow the Single Responsibility Principle for components
- Use composition over inheritance
- Prefer interfaces for communication between components
- Consider using ScriptableObject-based events for decoupling

## Testing

### Unit Testing

- Write unit tests for all non-trivial logic
- Use NUnit for test frameworks
- Follow Arrange-Act-Assert pattern
- Mock dependencies for isolation
- Name tests using the pattern `[Method]_[Scenario]_[ExpectedResult]`

```csharp
[Test]
public void CalculateDamage_WithCriticalHit_ReturnsDoubleDamage()
{
    // Arrange
    var damageCalculator = new DamageCalculator();
    var baseAmount = 10f;
    var isCritical = true;
    
    // Act
    var result = damageCalculator.CalculateDamage(baseAmount, isCritical);
    
    // Assert
    Assert.AreEqual(20f, result);
}
```

### Integration and Play Testing

- Use Unity's Test Runner for integration tests
- Create test scenes for play-mode tests
- Automate UI testing where possible
- Test on all target platforms

## Tools and Enforcement

- Use ReSharper or Rider's built-in code analysis
- Configure StyleCop for style enforcement
- Use .editorconfig for consistent formatting
- Set up CI/CD to validate code style and run tests

## Additional Resources

- [Microsoft C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [Unity C# Style Guide](https://github.com/raywenderlich/c-sharp-style-guide)

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | YYYY-MM-DD | Initial version | 