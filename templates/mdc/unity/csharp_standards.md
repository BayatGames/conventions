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

Always wrap your code in namespaces to avoid conflicts:

```csharp
namespace Bayat.Game.Core
{
    public class PlayerController : MonoBehaviour
    {
        // Class implementation
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
