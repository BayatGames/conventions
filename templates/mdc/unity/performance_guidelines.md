# Unity Performance Guidelines

This document outlines best practices for optimizing performance in Unity projects according to Bayat standards.

## CPU Optimization

### Script Optimization

- **Avoid empty callback methods**: Don't have empty Update, FixedUpdate, or LateUpdate methods
- **Cache component references**:

  ```csharp
  // Good - cache in Awake
  private Transform targetTransform;
  private void Awake() {
      targetTransform = target.transform;
  }
  
  // Bad - don't do this in Update
  void Update() {
      target.GetComponent<Transform>().position += Vector3.up;
  }
  ```

- **Use appropriate Update methods**:
  - `Update`: Use for regular game logic, input handling
  - `FixedUpdate`: Use for physics calculations
  - `LateUpdate`: Use for camera follow, final position adjustments
- **Avoid Find operations** in performance-critical code:
  - `GameObject.Find()`
  - `FindObjectOfType<T>()`
  - `FindObjectsOfType<T>()`

### Physics Optimization

- **Use primitive colliders** when possible (sphere, box, capsule) instead of mesh colliders
- **Set appropriate Rigidbody interpolation** modes to avoid jittery movement
- **Use non-allocating physics APIs**:

  ```csharp
  // Good - pre-allocate array
  private RaycastHit[] results = new RaycastHit[10];
  private void Update() {
      int hitCount = Physics.RaycastNonAlloc(transform.position, transform.forward, results);
  }
  
  // Bad - creates garbage
  private void Update() {
      RaycastHit[] hits = Physics.RaycastAll(transform.position, transform.forward);
  }
  ```

- **Use appropriate collision layers** and collision matrix settings
- **Deactivate Rigidbodies** when not needed by setting `isKinematic = true`

### Memory Management

- **Object Pooling**: Reuse game objects instead of instantiating and destroying them:

  ```csharp
  public class ObjectPool : MonoBehaviour {
      public GameObject prefab;
      public int initialSize = 10;
      private Queue<GameObject> objects;
      
      private void Start() {
          objects = new Queue<GameObject>();
          for (int i = 0; i < initialSize; i++) {
              GameObject obj = Instantiate(prefab);
              obj.SetActive(false);
              objects.Enqueue(obj);
          }
      }
      
      public GameObject Get() {
          GameObject obj = objects.Count > 0 ? objects.Dequeue() : Instantiate(prefab);
          obj.SetActive(true);
          return obj;
      }
      
      public void Return(GameObject obj) {
          obj.SetActive(false);
          objects.Enqueue(obj);
      }
  }
  ```

- **Avoid boxing of value types**:
  - Be careful with generic collections of value types
  - Avoid unnecessary conversions to object
- **Minimize heap allocations** in performance-critical methods:
  - Avoid `new` in Update methods when possible
  - Reuse collections instead of recreating them
  - Avoid LINQ in performance-critical code
  - Be cautious with closures and anonymous methods

## Rendering Optimization

### Draw Call Optimization

- **Use static batching** for stationary objects
- **Enable dynamic batching** for small, moving objects with the same material
- **Implement GPU instancing** for repeated objects with the same mesh and material
- **Use texture atlases** to reduce material count

### Materials and Shaders

- **Share materials** between objects when possible
- **Use appropriate shader complexity** for target platforms
- **Consider using Shader Graph** for complex shader effects with built-in optimizations
- **Implement Level of Detail (LOD)** for complex materials

### Lighting and Shadows

- **Use mixed lighting** where appropriate
- **Bake lighting** for static scenes
- **Limit real-time light count**
- **Use light probes** for dynamic objects in baked lighting scenes
- **Optimize shadow distance** and resolution
- **Disable shadow casting** for small or distant objects

## Mobile-Specific Optimizations

### CPU/GPU Considerations

- **Target 30 FPS** for complex games, 60 FPS for simpler games
- **Reduce physics simulation frequency** when appropriate
- **Use simplified collision meshes**
- **Implement framerate throttling** for less critical sequences

### Memory Constraints

- **Compress textures** aggressively
- **Use texture mipmap streaming**
- **Set appropriate quality settings** per platform
- **Implement asset bundle streaming** for large games

### Battery Usage

- **Reduce Update frequency** for background processes
- **Implement application pause optimizations**
- **Reduce physics simulation** when application is not focused

## Profiling and Measurement

### Unity Profiler

- **Profile your game regularly** during development
- **Set baseline performance metrics** and test against them
- **Focus on CPU, GPU, memory, and rendering measurements**
- **Profile on target devices** (not just in the editor)

### Common Issues to Look For

- **CPU bottlenecks**:
  - Heavy Update methods
  - Physics calculations
  - Garbage collection spikes
- **GPU bottlenecks**:
  - Fill rate issues (too many transparent objects)
  - Draw call count too high
  - Shader complexity too high for target platform
- **Memory issues**:
  - Texture memory usage
  - Asset duplication
  - Memory leaks from unmanaged resources

## Tools and Techniques

- **Unity Profiler**: Built-in profiling for CPU, GPU, and memory
- **Frame Debugger**: Analyze draw calls and rendering order
- **Memory Profiler**: Find memory leaks and asset duplication
- **Code stripping**: Remove unused code in builds
- **Assembly definition files**: Speed up compilation and reduce dependencies
- **Addressable Assets**: Optimize asset loading and memory usage
