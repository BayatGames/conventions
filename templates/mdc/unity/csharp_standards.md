# C# Coding Standards for Unity

This document outlines the C# coding standards for Unity development according to Bayat standards.

## Naming Conventions

### General Rules

- Use **PascalCase** for:
  - Classes, interfaces, and structs (e.g., `PlayerController`, `IInteractable`)
  - Methods (e.g., `CalculateDamage()`)
  - Properties (e.g., `MaxHealth`)
  - Static fields (e.g., `DefaultSpawnPoint`)
  - Namespaces (e.g., `Bayat.Game.Core`)
  - Enums and enum values (e.g., `GameState`, `GameState.Playing`)

- Use **camelCase** for:
  - Local variables (e.g., `int playerHealth`)
  - Method parameters (e.g., `void TakeDamage(float damageAmount)`)
  - Private and protected fields (e.g., `private float currentHealth`)

- Prefix interfaces with "I" (e.g., `IInteractable`)

### Unity-Specific

- For **public fields** that appear in the Unity Inspector:
  - Use **PascalCase** for public fields (e.g., `public float MovementSpeed`)
  - Or use [SerializeField] with private camelCase fields (preferred)

    ```csharp
    [SerializeField] 
    private float movementSpeed;
    ```

- Add **Callback** suffix to delegates:

  ```csharp
  public delegate void PlayerDeathCallback(Player player);
  ```

- Add **On** prefix to events and actions:

  ```csharp
  public UnityAction OnDeath;
  public event Action<int> OnScoreChanged;
  ```

## Code Structure

### Class Organization

1. **Fields and properties**
   - Serialized fields first
   - Private fields next
   - Properties last

2. **Unity Lifecycle Methods** (in order of execution)
   - Awake()
   - OnEnable()
   - Start()
   - Update()
   - FixedUpdate()
   - LateUpdate()
   - OnDisable()
   - OnDestroy()

3. **Public Methods**

4. **Private Methods**

5. **Coroutines**

### Namespaces

Always wrap your code in namespaces to avoid conflicts. Bayat follows a strict hierarchical namespace convention:

```csharp
// For games
namespace Bayat.Games.GameName
{
    public class PlayerController : MonoBehaviour
    {
        // Class implementation
    }
}

// For libraries or packages
namespace Bayat.Games.UI
{
    public class Button : MonoBehaviour
    {
        // Class implementation
    }
}

// For core libraries
namespace Bayat.Core
{
    public class Logger
    {
        // Class implementation
    }
}
```

Namespace guidelines:
- Games must be under the `Bayat.Games` namespace
- Game-specific code should be under `Bayat.Games.{GameName}` (e.g., `Bayat.Games.Twins`)
- Libraries for games should be under `Bayat.Games.{Category}` (e.g., `Bayat.Games.UI`)
- Core libraries are under `Bayat.{Category}` (e.g., `Bayat.Core`)

Adding the "Game" suffix to game namespaces (e.g., `Bayat.Games.TwinsGame`) is optional based on project requirements.

### Package Identifiers

For Unity packages and games, follow these package identifier conventions:

- Unity packages: `io.bayat.unity.{category}` (e.g., `io.bayat.unity.ui`)
- Game bundles: `io.bayat.games.{gamename}` (e.g., `io.bayat.games.twins`)

## Code Documentation

- Use **XML documentation comments** (`///`) for public classes, methods, and properties
- Describe the purpose, parameters, and return values
- Keep documentation concise and up-to-date

```csharp
/// <summary>
/// Manages the player's health and damage state.
/// </summary>
public class PlayerHealth : MonoBehaviour
{
    /// <summary>
    /// Gets the current health of the player.
    /// </summary>
    public float CurrentHealth { get; private set; }

    /// <summary>
    /// Applies damage to the player.
    /// </summary>
    /// <param name="amount">The amount of damage to apply.</param>
    public void TakeDamage(float amount)
    {
        // ... implementation
    }
}
```

## Best Practices

### General

- Use **access level modifiers** explicitly (don't omit `private`)
- Prefer **properties** over public fields
- Use one declaration per line:

  ```csharp
  // Good
  private int health;
  private int maxHealth;
  
  // Bad
  private int health, maxHealth;
  ```

- Use **braces** for all control structures, even single-line ones:

  ```csharp
  // Good
  if (isGameOver) {
      RestartGame();
  }
  
  // Bad
  if (isGameOver) RestartGame();
  ```

### Unity-Specific

- **Cache component references** in Awake() rather than using GetComponent() repeatedly:

  ```csharp
  private Rigidbody rb;
  
  private void Awake()
  {
      rb = GetComponent<Rigidbody>();
  }
  ```

- **Avoid** using GameObject.Find() and similar methods (FindObjectOfType, etc.) - especially in Update()
- Use **[SerializeField]** for inspector-exposed variables instead of making them public
- Prefer **AddListener()** over direct function assignment for Unity Events:

  ```csharp
  // Good
  button.onClick.AddListener(HandleButtonClick);
  
  // Avoid
  button.onClick = HandleButtonClick;
  ```

- Avoid using strings for identifiers (animation names, input axes) - use constants instead:

  ```csharp
  private const string ANIM_PARAM_RUNNING = "IsRunning";
  ```

- **DO NOT** use SendMessage and Invoke - use events, callbacks or coroutines instead
