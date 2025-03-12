# Unity Development Conventions

This document outlines the standards and best practices for Unity development at Bayat. These guidelines ensure consistency, quality, and maintainability across all Unity projects.

## Table of Contents

- [Project Setup](#project-setup)
- [Asset Organization](#asset-organization)
- [Scene Structure](#scene-structure)
- [Prefab Usage](#prefab-usage)
- [Scripting Conventions](#scripting-conventions)
- [Architectural Patterns](#architectural-patterns)
- [Performance Guidelines](#performance-guidelines)
- [Editor Extensions](#editor-extensions)
- [Build and Deployment](#build-and-deployment)
- [Version Control](#version-control)

## Project Setup

### Unity Version

- Use the specified Unity version for each project
- Document the exact version in the README.md
- Define a process for Unity version upgrades
- Use Unity Hub for version management

### Package Management

- Use the Unity Package Manager for dependencies
- Lock package versions in the manifest.json
- Document custom packages and their purpose
- Consider creating internal UPM packages for shared functionality

### Project Settings

- Configure project settings appropriately for the target platform
- Use consistent quality settings across development machines
- Configure physics settings based on project requirements
- Establish consistent color space (generally Linear)
- Set appropriate player settings for each platform

### Project Structure

Organize Unity projects according to our [repository structure conventions](../git/repos.md#game-projects).

## Asset Organization

### Folder Structure

The Assets folder should follow this structure:

```
Assets/
├── _Project/              # Project-specific assets
│   ├── Art/               # All art assets
│   │   ├── Models/
│   │   ├── Textures/
│   │   ├── Materials/
│   │   ├── Animations/
│   │   └── Effects/
│   ├── Audio/             # All audio assets
│   │   ├── Music/
│   │   ├── SFX/
│   │   └── Ambient/
│   ├── Prefabs/           # Prefabricated GameObjects
│   │   ├── UI/
│   │   ├── Environment/
│   │   ├── Characters/
│   │   └── Gameplay/
│   ├── Scenes/            # All Unity scenes
│   │   ├── Levels/
│   │   ├── UI/
│   │   └── Loading/
│   ├── Scripts/           # All C# scripts
│   │   ├── Core/
│   │   ├── Gameplay/
│   │   ├── UI/
│   │   └── Utils/
│   ├── Settings/          # Project configuration
│   ├── UI/                # UI assets
│   └── Resources/         # Dynamic loading resources
├── Plugins/               # Third-party assets and plugins
├── Editor/                # Editor scripts
└── StreamingAssets/       # Platform-specific assets
```

### Asset Naming Conventions

Use consistent naming patterns for all assets:

| Asset Type | Naming Convention | Example |
|------------|-------------------|---------|
| Scripts | PascalCase | `PlayerController.cs` |
| Prefabs | PrefixCategory_PascalCase | `Char_Player.prefab` |
| Models | PrefixCategory_PascalCase | `Prop_Chair.fbx` |
| Textures | PrefixType_AssetName_Suffix | `T_WoodFloor_D.png` (D for diffuse) |
| Materials | Mat_PascalCase | `Mat_WoodFloor.mat` |
| Animations | Anim_Action_State | `Anim_Player_Idle.anim` |
| Scenes | Scene_Purpose | `Scene_Level1.unity` |
| Audio | SFX_Category_Description | `SFX_Weapon_Gunshot.wav` |

Where common prefixes include:
- T_ for textures
- M_ for models
- Mat_ for materials
- Anim_ for animations
- SFX_ for sound effects
- UI_ for UI elements

### Asset Import Settings

- Configure appropriate import settings for each asset type
- Create presets for common asset types
- Document platform-specific import settings
- Set appropriate compression settings for textures
- Configure model import settings based on intended use

## Scene Structure

### Scene Hierarchy Organization

Organize scene hierarchies consistently:

```
- _SceneContext            # Root for scene-specific managers
  - SceneManager
  - LightingManager
  - AudioManager
- _DynamicObjects          # Root for runtime-spawned objects
- _Environment             # Root for environment objects
  - Terrain
  - Props
  - Lighting
- _Characters              # Root for NPCs and players
  - Player
  - NPCs
- _UI                      # Root for UI elements
  - Canvas
    - HUD
    - Menus
- _Cameras                 # Root for cameras
  - MainCamera
  - CutsceneCamera
```

### Multi-Scene Setup

For larger projects, use a multi-scene approach:

- Create specialized scenes (UI, environment, gameplay)
- Use scene loading additively
- Document dependencies between scenes
- Use ScriptableObjects for cross-scene communication

### Lighting

- Use appropriate lighting solutions (baked vs. real-time)
- Configure light probes and reflection probes properly
- Document lightmapping settings
- Use lighting presets for different environments

## Prefab Usage

### Prefab Structure

- Create modular prefabs with clear hierarchies
- Use nested prefabs for complex objects
- Establish prefab variants for object variations
- Document prefab interfaces and dependencies

### Prefab Best Practices

- Prefer prefabs over scene instances for reusable elements
- Use prefab overrides sparingly
- Document breaking changes to shared prefabs
- Use prefab variants rather than duplicating prefabs
- Create clear ownership boundaries for prefabs

## Scripting Conventions

Follow the [C# coding conventions](../languages/csharp.md) with these Unity-specific additions:

### MonoBehaviour Lifecycle

- Use appropriate lifecycle methods for different purposes:
  - `Awake`: Component initialization and reference setup
  - `Start`: Cross-component initialization
  - `OnEnable`: Setup that should happen each time the object is enabled
  - `Update`: Frame-dependent logic
  - `FixedUpdate`: Physics-related logic
  - `LateUpdate`: Camera follow and final adjustments
  - `OnDisable`: Cleanup when object is disabled
  - `OnDestroy`: Final cleanup

### Serialized Fields

- Use `[SerializeField]` for inspector-exposed private fields
- Use appropriate range attributes for numeric values
- Group related fields with headers
- Provide tooltips for non-obvious fields

Example:
```csharp
[Header("Movement Parameters")]
[SerializeField, Tooltip("Maximum movement speed in units per second")]
[Range(1f, 20f)]
private float _moveSpeed = 5f;

[SerializeField, Tooltip("How quickly the character reaches maximum speed")]
[Range(0.1f, 10f)]
private float _acceleration = 2f;
```

### Component References

- Cache component references in Awake
- Use GetComponentInChildren/GetComponentInParent sparingly
- Document required components with RequireComponent attribute

```csharp
[RequireComponent(typeof(Rigidbody))]
public class PlayerMovement : MonoBehaviour
{
    private Rigidbody _rigidbody;
    
    private void Awake()
    {
        _rigidbody = GetComponent<Rigidbody>();
    }
}
```

## Architectural Patterns

### Dependency Management

- Use dependency injection where appropriate
- Consider service locators for global systems
- Document component dependencies clearly
- Prefer Scene-based references for explicit relationships

### State Management

- Use state patterns for complex behavior
- Implement finite state machines for character behavior
- Use ScriptableObjects for shared state
- Document state transitions and conditions

### Event Systems

- Use event-based communication for decoupling
- Document event payloads and expected listeners
- Consider ScriptableObject-based events
- Unsubscribe from events when objects are destroyed

Example of ScriptableObject-based event:
```csharp
[CreateAssetMenu(fileName = "GameEvent", menuName = "Events/Game Event")]
public class GameEvent : ScriptableObject
{
    private readonly List<GameEventListener> _listeners = new List<GameEventListener>();

    public void Raise()
    {
        for (int i = _listeners.Count - 1; i >= 0; i--)
        {
            _listeners[i].OnEventRaised();
        }
    }

    public void RegisterListener(GameEventListener listener)
    {
        if (!_listeners.Contains(listener))
            _listeners.Add(listener);
    }

    public void UnregisterListener(GameEventListener listener)
    {
        if (_listeners.Contains(listener))
            _listeners.Remove(listener);
    }
}
```

### Object Pooling

- Use object pooling for frequently spawned objects
- Document pool sizes and initialization
- Handle pool expansion gracefully
- Return objects to pool rather than destroying them

## Performance Guidelines

### CPU Optimization

- Profile code regularly using Unity Profiler
- Optimize Update methods to minimize per-frame work
- Use coroutines for distributing work across frames
- Implement LOD (Level of Detail) systems
- Cache references and computation results

### Memory Management

- Avoid allocations in performance-critical code
- Use object pooling to reduce garbage collection
- Optimize asset loading and unloading
- Manage scene loading to control memory usage
- Set appropriate texture compression settings

### Rendering Optimization

- Use appropriate batching techniques (static/dynamic)
- Optimize draw calls through material sharing
- Implement occlusion culling for complex scenes
- Use atlasing for UI textures
- Optimize shader complexity for target hardware

### Mobile-Specific Optimization

- Target appropriate frame rates (30/60fps)
- Reduce overdraw with proper culling
- Optimize touch input handling
- Implement battery-saving measures
- Test on actual target devices

## Editor Extensions

### Custom Editors

- Create custom inspectors for complex components
- Use property drawers for custom types
- Document editor script functionality
- Store editor scripts in Editor folders

### Editor Tools

- Develop tools for repetitive tasks
- Create scene setup automation
- Document tool usage in README
- Use editor preprocessing for platform-specific code

## Build and Deployment

### Build Pipeline

- Document build steps and dependencies
- Automate build process with scripts
- Configure appropriate build settings for each platform
- Create build variants (development, QA, release)

### Optimization for Shipping

- Strip debug symbols from release builds
- Configure appropriate compression settings
- Remove development-only features
- Set up analytics and crash reporting

### Platform-Specific Considerations

- Document platform-specific features and limitations
- Create platform-specific code with preprocessing directives
- Test thoroughly on all target platforms
- Configure appropriate resolution and quality settings

## Version Control

Follow the [Bayat Git Flow](../git/flow.md) conventions with these Unity-specific additions:

### Unity-Specific .gitignore

Use appropriate .gitignore settings for Unity projects:
- Exclude Library, Temp, Logs, and UserSettings folders
- Exclude build outputs
- Include appropriate .meta files

### Git LFS Usage

- Configure Git LFS for binary assets
- Set up appropriate tracking patterns
- Document LFS usage in README
- Monitor LFS bandwidth usage

### Scene and Prefab Merging

- Use Unity's Smart Merge tool for scene and prefab merging
- Document merge conflict resolution process
- Consider using prefab variants to reduce merge conflicts
- Work in separate scenes when possible

### Unity Collaboration

When multiple team members are working in Unity:

- Communicate before large refactorings
- Create isolated test scenes for experimental features
- Use prefab workflows to minimize scene conflicts
- Document asset dependencies clearly

## Additional Resources

- [Unity's Official Best Practice Guide](https://unity.com/how-to/organizing-your-project)
- [Unity Learn Tutorials](https://learn.unity.com/)
- [Unity Manual](https://docs.unity3d.com/Manual/)

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | YYYY-MM-DD | Initial version | 