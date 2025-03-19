<!--
Document: Unreal Engine Development Conventions
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Unreal Engine Development Conventions

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Naming Conventions](#naming-conventions)
4. [Blueprints](#blueprints)
5. [C++ Coding Standards](#c-coding-standards)
6. [Asset Management](#asset-management)
7. [Level Design](#level-design)
8. [Performance Optimization](#performance-optimization)
9. [Multiplayer and Networking](#multiplayer-and-networking)
10. [UI/UX Design](#uiux-design)
11. [Animation](#animation)
12. [Audio](#audio)
13. [Version Control](#version-control)
14. [Testing and Quality Assurance](#testing-and-quality-assurance)
15. [Documentation](#documentation)
16. [Build and Deployment](#build-and-deployment)
17. [Cross-Platform Development](#cross-platform-development)
18. [Team Collaboration](#team-collaboration)

## Introduction

This document outlines the standard conventions and best practices for Unreal Engine development at Bayat. These guidelines aim to ensure consistency, maintainability, and scalability across all Unreal Engine projects.

## Project Structure

### Folder Organization

```
ProjectName/
├── Config/                 # Project configuration files
├── Content/                # All project assets
│   ├── Characters/         # Character assets
│   │   ├── Player/         # Player character assets
│   │   └── NPCs/           # Non-player character assets
│   ├── Environment/        # Environment assets
│   │   ├── Landscapes/     # Landscape assets
│   │   ├── Props/          # Prop assets
│   │   └── Materials/      # Environment materials
│   ├── Gameplay/           # Gameplay-related assets
│   │   ├── Abilities/      # Ability system assets
│   │   ├── Items/          # Item assets
│   │   └── Mechanics/      # Gameplay mechanics
│   ├── UI/                 # User interface assets
│   │   ├── HUD/            # Heads-up display assets
│   │   ├── Menus/          # Menu assets
│   │   └── Common/         # Common UI elements
│   ├── Audio/              # Audio assets
│   │   ├── Music/          # Music tracks
│   │   ├── SFX/            # Sound effects
│   │   └── Dialogue/       # Dialogue recordings
│   ├── VFX/                # Visual effects
│   ├── Maps/               # Level maps
│   │   ├── Levels/         # Gameplay levels
│   │   └── Sublevels/      # Streaming sublevels
│   ├── Core/               # Core systems
│   │   ├── GameModes/      # Game mode assets
│   │   ├── GameStates/     # Game state assets
│   │   └── PlayerStates/   # Player state assets
│   └── _Dev/               # Development-only assets
│       ├── Developers/     # Developer-specific folders
│       └── Testing/        # Testing assets
├── Source/                 # C++ source code
│   ├── ProjectName/        # Main project source
│   │   ├── Characters/     # Character classes
│   │   ├── Gameplay/       # Gameplay classes
│   │   ├── UI/             # UI classes
│   │   └── Core/           # Core system classes
│   └── ProjectNameEditor/  # Editor-specific code
├── Plugins/                # Project-specific plugins
└── Documentation/          # Project documentation
```

### Content Organization Principles

- Group assets by type and functionality
- Use consistent naming across folders
- Keep a clean separation between different asset categories
- Maintain a clear hierarchy for ease of navigation
- Use subfolders to avoid overcrowded directories

## Naming Conventions

### General Naming Rules

- Use PascalCase for all asset names
- Use descriptive names that clearly indicate the asset's purpose
- Avoid abbreviations unless they are widely understood
- Use prefixes to indicate asset types
- Be consistent with pluralization

### Asset Type Prefixes

| Asset Type | Prefix | Example |
|------------|--------|---------|
| Blueprint | BP_ | BP_PlayerCharacter |
| Material | M_ | M_Wood |
| Material Instance | MI_ | MI_WoodPainted |
| Texture | T_ | T_WoodDiffuse |
| Static Mesh | SM_ | SM_Chair |
| Skeletal Mesh | SK_ | SK_PlayerCharacter |
| Animation Blueprint | ABP_ | ABP_PlayerCharacter |
| Animation Sequence | A_ | A_PlayerIdle |
| Particle System | PS_ | PS_Fire |
| Widget Blueprint | WBP_ | WBP_MainMenu |
| Sound Cue | SC_ | SC_Explosion |
| Level | LVL_ | LVL_MainMenu |
| Data Asset | DA_ | DA_WeaponStats |
| Data Table | DT_ | DT_EnemySpawnRates |

### C++ Naming Conventions

- Classes: Use PascalCase with 'A' prefix for Actors, 'U' for UObjects
  - Example: `APlayerCharacter`, `UHealthComponent`
- Interfaces: Use PascalCase with 'I' prefix
  - Example: `IInteractable`, `IDamageable`
- Variables: Use camelCase with descriptive names
  - Example: `healthPoints`, `movementSpeed`
- Functions: Use PascalCase for public functions, camelCase for private
  - Example: `ApplyDamage()`, `calculateDamageMultiplier()`
- Enums: Use PascalCase with 'E' prefix
  - Example: `EWeaponType`, `EDamageType`
- Constants: Use ALL_CAPS with underscores
  - Example: `MAX_HEALTH`, `DEFAULT_SPEED`

## Blueprints

### Blueprint Organization

- Keep Blueprint graphs clean and organized
- Use functions and macros for reusable logic
- Group related nodes using comments
- Use event dispatchers for communication between Blueprints
- Implement interfaces for common functionality

### Blueprint Best Practices

- Prefer functions over macros when possible
- Use Blueprint interfaces for polymorphism
- Keep execution chains short and readable
- Break complex logic into smaller functions
- Use Blueprint Function Libraries for utility functions
- Implement proper error handling

### Blueprint Performance Considerations

- Minimize the use of "Tick" events
- Use timers instead of continuous checks
- Cache references to frequently accessed objects
- Avoid complex calculations in loops
- Use Blueprint nativization for performance-critical Blueprints

### Blueprint Communication

- Use direct references for parent-child communication
- Use interfaces for unrelated Blueprint communication
- Use event dispatchers for one-to-many communication
- Use Game Instance, Game State, or Player State for global data

## C++ Coding Standards

### Code Organization

- Follow the Unreal Engine coding standard
- Group related functionality into classes
- Use components for modular functionality
- Keep header files clean and minimal
- Use forward declarations to minimize dependencies

### C++ Best Practices

- Use UPROPERTY and UFUNCTION macros for engine integration
- Implement proper memory management
- Use smart pointers for non-UObject pointers
- Follow the Rule of Three/Five for custom resource management
- Use const correctness throughout the codebase

```cpp
// Good example
UCLASS()
class PROJECTNAME_API AWeapon : public AActor
{
    GENERATED_BODY()
    
public:
    AWeapon();
    
    UFUNCTION(BlueprintCallable, Category = "Weapon")
    virtual void Fire();
    
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Weapon")
    float Damage;
    
protected:
    UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category = "Components")
    USkeletalMeshComponent* WeaponMesh;
    
    UPROPERTY(EditDefaultsOnly, Category = "Effects")
    UParticleSystem* MuzzleFlash;
    
private:
    UPROPERTY()
    ACharacter* OwningCharacter;
    
    float LastFireTime;
};
```

### C++ and Blueprint Integration

- Use BlueprintCallable functions for Blueprint access
- Expose properties with appropriate specifiers
- Use BlueprintImplementableEvents for Blueprint overrides
- Create Blueprint function libraries for utility functions
- Use BlueprintNativeEvent for functions with default implementations

## Asset Management

### Texture Guidelines

- Use appropriate texture sizes (powers of 2)
- Set proper compression settings based on texture type
- Use texture atlases for related small textures
- Implement proper mip-mapping
- Use normal maps for detail on low-poly models

### Material Guidelines

- Create a material library with base materials
- Use material instances for variations
- Implement material functions for reusable operations
- Use material parameter collections for global parameters
- Optimize material complexity for target platforms

### Static Mesh Guidelines

- Use appropriate LODs (Levels of Detail)
- Optimize polygon count for target platforms
- Set up proper collision
- Use proper UV mapping
- Implement proper vertex normals and tangents

### Skeletal Mesh Guidelines

- Create clean, efficient rigs
- Use appropriate bone counts
- Set up proper physics assets
- Implement socket naming conventions
- Use proper LODs for skeletal meshes

## Level Design

### Level Organization

- Use persistent levels for common elements
- Implement streaming sublevels for large worlds
- Group related actors in folders
- Use level blueprints sparingly
- Implement proper level bounds

### Level Optimization

- Use occlusion culling
- Implement proper LOD transitions
- Use instanced static meshes for repeated elements
- Implement distance-based streaming
- Use light baking for static lighting

### World Composition

- Plan level streaming zones
- Use world composition for large open worlds
- Implement proper level transitions
- Use landscape streaming for large terrains
- Set up proper preloading volumes

## Performance Optimization

### CPU Optimization

- Minimize actors in the world
- Use efficient algorithms
- Implement proper threading
- Optimize AI and behavior trees
- Use timers instead of per-frame checks

### GPU Optimization

- Optimize material complexity
- Reduce overdraw
- Use appropriate texture resolutions
- Implement proper LODs
- Optimize lighting and shadows

### Memory Optimization

- Use asset streaming
- Implement proper garbage collection
- Optimize texture and mesh memory usage
- Use object pooling for frequently spawned objects
- Implement proper reference handling

### Profiling and Optimization Tools

- Use Unreal Insights for performance analysis
- Implement stat commands for specific metrics
- Use the GPU Visualizer
- Implement memory profiling
- Use automation testing for performance regression

## Multiplayer and Networking

### Network Architecture

- Design with client-server model in mind
- Implement proper authority checks
- Use replicated properties for synchronized state
- Implement RPC (Remote Procedure Calls) for events
- Design for network bandwidth optimization

### Replication

- Use replicated properties for state synchronization
- Implement proper replication conditions
- Use RepNotify for change notifications
- Optimize replication frequency
- Implement proper ownership and relevancy

```cpp
// Good replication example
UPROPERTY(Replicated)
float Health;

UPROPERTY(ReplicatedUsing = OnRep_IsReloading)
bool bIsReloading;

UFUNCTION()
void OnRep_IsReloading();

virtual void GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const override;

// In CPP file
void AWeapon::GetLifetimeReplicatedProps(TArray<FLifetimeProperty>& OutLifetimeProps) const
{
    Super::GetLifetimeReplicatedProps(OutLifetimeProps);
    
    DOREPLIFETIME(AWeapon, Health);
    DOREPLIFETIME_CONDITION(AWeapon, bIsReloading, COND_SkipOwner);
}
```

### Network Optimization

- Implement proper network relevancy
- Use network compression
- Optimize RPC frequency
- Implement client-side prediction
- Use network prioritization

## UI/UX Design

### UI Architecture

- Use widget blueprints for UI elements
- Implement proper widget hierarchy
- Use data binding when possible
- Create reusable UI components
- Implement proper focus navigation

### UI Best Practices

- Design for different screen resolutions
- Implement proper scaling
- Use consistent styling
- Create responsive layouts
- Implement proper input handling

### UMG Guidelines

- Use anchors and alignment for responsive design
- Implement proper widget navigation
- Use animation for transitions
- Create style guides for consistent UI
- Implement proper accessibility features

## Animation

### Animation Blueprint Organization

- Use state machines for character animations
- Implement blend spaces for smooth transitions
- Use animation notifies for events
- Create modular animation graphs
- Implement proper animation caching

### Animation Best Practices

- Use root motion when appropriate
- Implement proper animation blending
- Use additive animations for variations
- Create reusable animation assets
- Implement proper animation compression

### Animation Performance

- Use appropriate animation LODs
- Implement animation budgets
- Use animation caching
- Optimize animation blueprint complexity
- Implement proper culling for animations

## Audio

### Audio Organization

- Create a consistent audio hierarchy
- Use sound classes for grouping
- Implement sound mixes for audio control
- Use sound cues for complex audio
- Create reusable audio components

### Audio Implementation

- Use attenuation settings for spatial audio
- Implement proper audio prioritization
- Use concurrency settings to manage voice count
- Implement dynamic audio based on gameplay
- Use audio occlusion when appropriate

### Audio Optimization

- Implement proper audio compression
- Use streaming for long audio files
- Implement voice limiting
- Use appropriate sample rates
- Optimize audio memory usage

## Version Control

### Version Control Workflow

- Use Git or Perforce for version control
- Implement proper branching strategy
- Use meaningful commit messages
- Create stable release branches
- Implement proper merge procedures

### Unreal-Specific Version Control

- Use .uasset file locking
- Implement proper binary file handling
- Use the Unreal Editor source control integration
- Create proper .gitignore or P4ignore files
- Implement proper large file handling

## Testing and Quality Assurance

### Testing Methodology

- Implement unit tests for C++ code
- Use the Automation Testing framework
- Create functional tests for gameplay features
- Implement performance testing
- Use continuous integration for automated testing

### Quality Assurance Process

- Create test plans for features
- Implement bug tracking procedures
- Use proper QA environments
- Create regression test suites
- Implement proper versioning for testing

## Documentation

### Code Documentation

- Document all public APIs
- Use proper comment formatting
- Create class and function documentation
- Document complex algorithms
- Keep documentation up-to-date with code changes

### Project Documentation

- Create design documents
- Implement technical specifications
- Document asset creation workflows
- Create onboarding documentation
- Maintain up-to-date project guidelines

## Build and Deployment

### Build Configuration

- Create proper build configurations
- Implement automated build processes
- Use proper versioning
- Create distribution packages
- Implement proper DLC support

### Deployment Process

- Create release checklists
- Implement proper platform-specific deployment
- Use continuous deployment when appropriate
- Create proper update procedures
- Implement proper version tracking

## Cross-Platform Development

### Platform Considerations

- Design for multiple platforms from the start
- Implement proper platform abstractions
- Use platform-specific optimizations
- Create scalable content for different hardware
- Implement proper input handling for all platforms

### Platform-Specific Optimizations

- Create platform-specific asset LODs
- Implement proper shader complexity for each platform
- Use platform-specific rendering features
- Optimize memory usage for mobile platforms
- Implement proper loading screens for slower platforms

## Team Collaboration

### Collaboration Workflow

- Define clear roles and responsibilities
- Implement proper task tracking
- Use regular code reviews
- Create collaborative design processes
- Implement proper knowledge sharing

### Communication Guidelines

- Use clear and concise communication
- Document decisions and rationales
- Create proper handoff procedures
- Implement regular status updates
- Use proper issue reporting procedures 