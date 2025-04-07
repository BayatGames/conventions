# Unity Scripting Guidelines

This document outlines best practices for Unity-specific scripting according to Bayat standards.

## Component Architecture

### Component Design

- **Single Responsibility**: Each component should have one specific purpose
- **Composition over Inheritance**: Prefer composing multiple components rather than creating deep inheritance hierarchies
- **Interface Implementation**: Use interfaces to define behavior contracts between components

  ```csharp
  // Define interface in appropriate namespace
  namespace Bayat.Games.Core
  {
      public interface IDamageable
      {
          void TakeDamage(float amount);
          bool IsInvulnerable { get; }
      }
  }
  
  // Implement interface in game-specific namespace
  namespace Bayat.Games.Twins
  {
      public class Player : MonoBehaviour, IDamageable
      {
          // Interface implementation
      }
  }
  ```

### Dependency Management

- Use **dependency injection** where appropriate:

  ```csharp
  // In appropriate Bayat namespace
  namespace Bayat.Games.Twins.Player
  {
      [RequireComponent(typeof(Rigidbody))]
      public class PlayerMovement : MonoBehaviour
      {
          private Rigidbody rb;
          
          private void Awake()
          {
              rb = GetComponent<Rigidbody>();
          }
      }
  }
  ```

- Use **[RequireComponent]** to explicitly define dependencies
- Consider using **ScriptableObjects** for shared data and configuration

## MonoBehaviour Usage

### Lifecycle Methods

Use the appropriate lifecycle methods for their intended purpose:

- **Awake()**: Component initialization, get references to other components
- **OnEnable()**: Register event listeners, reset state when object is activated
- **Start()**: Initialize values that depend on other components being initialized
- **Update()**: Frame-dependent logic (input handling, visual updates)
- **FixedUpdate()**: Physics-related code (movement, forces)
- **LateUpdate()**: Camera follow, final position adjustments
- **OnDisable()**: Unregister event listeners, cleanup when object is deactivated
- **OnDestroy()**: Final cleanup before object is destroyed

### Coroutines

- Use coroutines for:
  - Time-based operations
  - Procedural animations
  - Delayed actions
  - Operations that need to happen over multiple frames

```csharp
private IEnumerator DelayedAction(float delay)
{
    yield return new WaitForSeconds(delay);
    // Action after delay
}
```

- Prefer **WaitForSeconds** over manual time tracking
- Store coroutine references when you need to stop them:

  ```csharp
  private Coroutine fadeCoroutine;
  
  public void StartFade()
  {
      if (fadeCoroutine != null)
      {
          StopCoroutine(fadeCoroutine);
      }
      fadeCoroutine = StartCoroutine(FadeRoutine());
  }
  ```

## Performance Optimization

### General Optimizations

- **Object Pooling**: Reuse frequently created and destroyed objects:

  ```csharp
  public class ObjectPool : MonoBehaviour
  {
      public GameObject prefab;
      public int initialSize = 10;
      private Queue<GameObject> objects = new Queue<GameObject>();
      
      // Implementation of Get() and Return() methods
  }
  ```

- **Caching**: Cache references to components and frequently accessed values
- **Avoid string comparisons**: Use enums or constants instead
- **Avoid Empty Callbacks**: Don't implement empty OnEnable/OnDisable/Update methods

### Physics Optimizations

- Use **non-alloc** physics methods to reduce garbage collection:

  ```csharp
  private RaycastHit[] results = new RaycastHit[10];
  
  void Update()
  {
      int hitCount = Physics.RaycastNonAlloc(transform.position, transform.forward, results);
      for (int i = 0; i < hitCount; i++)
      {
          // Process results[i]
      }
  }
  ```

- Use **layer masks** to filter physics queries
- Set appropriate **collision matrix** in project settings
- Consider using **triggers** instead of collision detection when possible

### Memory Considerations

- Avoid instantiating and destroying objects frequently (use pooling)
- Be mindful of allocations in Update/FixedUpdate methods
- Use **struct** for small, frequently created objects to reduce GC pressure
- Avoid LINQ and anonymous functions in performance-critical code

## Event Systems

### Unity Events

- Use **UnityEvent** for events exposed in the Inspector. Allows designers to hook up callbacks without code.

### C# Events

- Use C# events (`event Action<T>`) for code-only communication between scripts. More performant than UnityEvents.

### Message System

- Consider a centralized message system (e.g., observer pattern) for complex projects to decouple components.
