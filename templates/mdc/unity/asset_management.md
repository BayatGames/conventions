# Unity Asset Management Guidelines

This document outlines best practices for organizing and managing assets in Unity projects according to Bayat standards.

## Project Structure

### Root-Level Folders

Organize your project with the following root-level folders:

```plaintext
Assets/
├── _Project/           # Project-specific assets
├── Plugins/            # Third-party plugins and libraries
├── Resources/          # Assets loaded via Resources.Load()
├── ScriptableObjects/  # Scriptable Object assets
├── Settings/           # Project settings assets
└── StreamingAssets/    # Assets accessed via file path at runtime
```

### _Project Structure

The `_Project` folder should have the following structure:

```plaintext
_Project/
├── Art/                # All visual assets
├── Audio/              # All audio assets
├── Prefabs/            # Reusable GameObject templates
├── Scenes/             # Game scenes
├── Scripts/            # C# code
└── UI/                 # UI-specific assets
```

### Further Breakdown

Each major folder should be organized by feature or module:

```plaintext
Scripts/
├── Core/               # Core systems and managers
├── Player/             # Player-related scripts
├── Enemies/            # Enemy-related scripts
├── UI/                 # UI-related scripts
└── Utils/              # Utility scripts
```

## Naming Conventions

### General Rules

- Use **PascalCase** for all assets and folders
- Be descriptive but concise
- Group related assets with prefixes
- Use suffixes to identify asset types

### Package Identifier Conventions

For Unity packages and assets published by Bayat, follow these conventions:

- Unity packages: `io.bayat.unity.{category}` (e.g., `io.bayat.unity.ui`, `io.bayat.unity.tools`)
- Game packages: `io.bayat.games.{gamename}` (e.g., `io.bayat.games.twins`)
- Asset store packages: `Bayat.{Category}` (e.g., `Bayat.UI`, `Bayat.Core`)

Project settings should reflect these naming conventions in:
- Package manifest (package.json)
- Assembly definition files (.asmdef)
- Product name and bundle identifier in Player Settings

### Asset Type Suffixes

- **Animations**: `_Anim` or `_Animation`
- **Materials**: `_Mat` or `_Material`
- **Textures**: `_Tex` or `_Texture`
- **Sprites**: `_Sprite`
- **Prefabs**: `_Prefab`
- **Scriptable Objects**: `_SO` or `_Data`
- **Audio Clips**: `_SFX` or `_Music`

### Examples

- `PlayerCharacter_Prefab`
- `WoodFloor_Mat`
- `MonsterAttack_Anim`
- `WeaponStats_SO`
- `Explosion_SFX`

## Asset Management Practices

### Texture Guidelines

- Set appropriate **compression settings** based on the texture's use
- Define **max texture sizes** (e.g., UI: 1024, Characters: 2048, Environment: 4096)
- Use **texture atlases** for related small textures
- Use appropriate **texture formats**:
  - Standard color textures: PNG or JPEG
  - Normal maps: TGA or PNG (with normal map import settings)
  - Height/Mask maps: RAW, EXR, or TGA

### Model Guidelines

- Clean up models before importing (remove unnecessary meshes)
- Set up **proper scale** (e.g., 1 unit = 1 meter)
- Configure **appropriate LODs** (Levels of Detail)
- Use **model prefabs** for complex model setups

### Prefab Workflow

- Create **prefab variants** for objects that share common elements but have variations
- Use **nested prefabs** to create complex hierarchies
- Break complex objects into **modular prefabs**
- Create **prefab templates** for commonly used object types

## Resource Loading Strategies

### Loading Methods

- **Direct references**: for assets known at design time
- **Resources.Load()**: for assets that need dynamic loading (use sparingly)
- **Addressables**: for larger projects with many assets (preferred method for dynamic loading)
- **Asset Bundles**: for downloadable content and platform-specific assets

### Best Practices

- Minimize Resources folder usage (impacts build size and loading times)
- Group logically related assets together in Addressable groups
- Consider load time vs. memory usage tradeoffs
- Implement asset preloading for critical paths

## Version Control Considerations

- Use appropriate **.gitignore** for Unity projects
- Consider using **Git LFS** for large binary files
- Keep **meta files** under version control
- Organize commits by feature or asset type
- Use meaningful commit messages referencing features/tasks

## Performance Optimization

- **Texture atlasing** for UI and small repeating textures
- **Asset compression** appropriate for target platforms
- **Mipmap** settings for textures based on their use
- **Mesh optimization** (vertex count, draw calls)
- **Material instancing** vs. unique materials consideration
- **Asset dependency** management to reduce duplicate assets
