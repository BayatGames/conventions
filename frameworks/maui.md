# .NET MAUI Development Guidelines

This document outlines the standards and best practices for developing cross-platform applications using .NET MAUI (Multi-platform App UI) at Bayat.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Development Environment](#development-environment)
4. [Architecture](#architecture)
5. [UI Development](#ui-development)
6. [Platform-Specific Considerations](#platform-specific-considerations)
7. [Performance](#performance)
8. [Security](#security)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Resources](#resources)

## Introduction

.NET MAUI is Microsoft's cross-platform UI framework for creating native mobile and desktop apps with C# and XAML. It allows developers to build applications for Android, iOS, macOS, and Windows from a single codebase.

### When to Use .NET MAUI

.NET MAUI is the preferred choice when:
- You need a cross-platform solution with strong Windows integration
- Your team has existing .NET/C# expertise
- You want to share code between mobile and desktop platforms
- You need access to native platform features
- You're building enterprise applications in the Microsoft ecosystem

### Key Benefits

- **Single Codebase**: Build for multiple platforms from one codebase
- **Native Performance**: Direct access to native APIs and controls
- **C# and .NET**: Modern language features and extensive libraries
- **XAML**: Declarative UI with strong design-time support
- **Microsoft Ecosystem**: Integration with Azure and other Microsoft services

## Project Structure

### Standard Project Layout

```
project-root/
├── .github/                    # GitHub workflows
├── src/                        # Source code
│   ├── ProjectName/            # Main project
│   │   ├── App.xaml            # Application definition
│   │   ├── AppShell.xaml       # Shell navigation
│   │   ├── MauiProgram.cs      # App initialization
│   │   ├── Models/             # Data models
│   │   ├── ViewModels/         # View models
│   │   ├── Views/              # UI pages and controls
│   │   ├── Services/           # Business logic and services
│   │   ├── Helpers/            # Utility classes
│   │   ├── Resources/          # App resources
│   │   │   ├── Fonts/          # Custom fonts
│   │   │   ├── Images/         # Image assets
│   │   │   ├── Raw/            # Raw asset files
│   │   │   └── Styles/         # Global styles
│   │   └── Platforms/          # Platform-specific code
│   │       ├── Android/        # Android-specific code
│   │       ├── iOS/            # iOS-specific code
│   │       ├── MacCatalyst/    # macOS-specific code
│   │       └── Windows/        # Windows-specific code
│   └── ProjectName.Core/       # Core library (optional)
│       ├── Models/             # Shared models
│       ├── Services/           # Shared services
│       └── Helpers/            # Shared utilities
├── tests/                      # Test projects
│   ├── ProjectName.Tests.Unit/ # Unit tests
│   └── ProjectName.Tests.UI/   # UI tests
├── .editorconfig               # Editor configuration
├── Directory.Build.props       # MSBuild properties
├── ProjectName.sln             # Solution file
└── README.md                   # Project documentation
```

### Key Files

- **MauiProgram.cs**: Application entry point and dependency injection setup
- **App.xaml**: Application resources and startup configuration
- **AppShell.xaml**: Shell-based navigation structure
- **MainPage.xaml**: Initial page shown to users

## Development Environment

### Required Tools

- Visual Studio 2022 (Windows) or Visual Studio for Mac
- .NET 7.0 SDK or newer
- Android SDK (for Android development)
- Xcode (for iOS/macOS development, Mac only)
- Windows App SDK (for Windows development)

### Development Setup

```bash
# Install .NET MAUI workload
dotnet workload install maui

# Create a new MAUI project
dotnet new maui -n MyMauiApp

# Build the project
dotnet build MyMauiApp

# Run on specific platform
dotnet build -t:Run -f net7.0-android
dotnet build -t:Run -f net7.0-ios
dotnet build -t:Run -f net7.0-maccatalyst
dotnet build -t:Run -f net7.0-windows10.0.19041.0
```

## Architecture

### MVVM Pattern

Use the Model-View-ViewModel (MVVM) pattern for all MAUI applications:

```csharp
// Model
public class TodoItem
{
    public string Id { get; set; }
    public string Title { get; set; }
    public bool IsCompleted { get; set; }
}

// ViewModel
public class TodoListViewModel : ObservableObject
{
    private readonly ITodoService _todoService;
    private ObservableCollection<TodoItem> _items;
    
    public ObservableCollection<TodoItem> Items
    {
        get => _items;
        set => SetProperty(ref _items, value);
    }
    
    [RelayCommand]
    private async Task LoadItemsAsync()
    {
        var items = await _todoService.GetItemsAsync();
        Items = new ObservableCollection<TodoItem>(items);
    }
    
    // Other commands and properties
}
```

```xml
<!-- View (XAML) -->
<ContentPage xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
             xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
             xmlns:viewmodels="clr-namespace:MyApp.ViewModels"
             x:Class="MyApp.Views.TodoListPage"
             x:DataType="viewmodels:TodoListViewModel">
    
    <CollectionView ItemsSource="{Binding Items}">
        <CollectionView.ItemTemplate>
            <DataTemplate x:DataType="models:TodoItem">
                <Grid>
                    <Label Text="{Binding Title}" />
                    <CheckBox IsChecked="{Binding IsCompleted}" />
                </Grid>
            </DataTemplate>
        </CollectionView.ItemTemplate>
    </CollectionView>
    
    <Button Text="Refresh" 
            Command="{Binding LoadItemsCommand}" />
</ContentPage>
```

### Dependency Injection

Use the built-in dependency injection container:

```csharp
// MauiProgram.cs
public static MauiApp CreateMauiApp()
{
    var builder = MauiApp.CreateBuilder();
    builder
        .UseMauiApp<App>()
        .ConfigureFonts(fonts =>
        {
            fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
            fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
        });
        
    // Register services
    builder.Services.AddSingleton<ITodoService, TodoService>();
    
    // Register pages and viewmodels
    builder.Services.AddTransient<TodoListViewModel>();
    builder.Services.AddTransient<TodoListPage>();
    
    return builder.Build();
}
```

### Navigation

Use Shell navigation for most applications:

```xml
<!-- AppShell.xaml -->
<Shell xmlns="http://schemas.microsoft.com/dotnet/2021/maui"
       xmlns:x="http://schemas.microsoft.com/winfx/2009/xaml"
       xmlns:views="clr-namespace:MyApp.Views"
       x:Class="MyApp.AppShell">
    
    <ShellContent Title="Home"
                  Icon="icon_home.png"
                  ContentTemplate="{DataTemplate views:HomePage}" />
    
    <ShellContent Title="Tasks"
                  Icon="icon_tasks.png"
                  ContentTemplate="{DataTemplate views:TodoListPage}" />
</Shell>
```

```csharp
// Navigation in code
await Shell.Current.GoToAsync("//tasks");

// Navigation with parameters
await Shell.Current.GoToAsync($"taskdetail?id={taskId}");
```

## UI Development

### XAML Best Practices

- Use XAML for all UI definitions
- Leverage XAML compilation for performance and compile-time checking
- Use styles and resources for consistent appearance
- Implement responsive layouts with Grid and FlexLayout

```xml
<!-- Styles example -->
<Style TargetType="Button" x:Key="PrimaryButton">
    <Setter Property="BackgroundColor" Value="{StaticResource PrimaryColor}" />
    <Setter Property="TextColor" Value="White" />
    <Setter Property="CornerRadius" Value="8" />
    <Setter Property="Padding" Value="16,8" />
</Style>

<!-- Resource dictionary -->
<ResourceDictionary>
    <Color x:Key="PrimaryColor">#512BD4</Color>
    <Color x:Key="SecondaryColor">#DFD8F7</Color>
</ResourceDictionary>
```

### Controls and Layouts

- Use CollectionView instead of ListView for better performance
- Use Grid for complex layouts
- Use FlexLayout for responsive designs
- Prefer built-in controls over custom renderers when possible

```xml
<!-- Responsive layout example -->
<FlexLayout Direction="Row" 
            Wrap="Wrap" 
            JustifyContent="SpaceBetween">
    <Frame FlexBasis="48%" Margin="4">
        <!-- Content -->
    </Frame>
    <Frame FlexBasis="48%" Margin="4">
        <!-- Content -->
    </Frame>
</FlexLayout>
```

### Handlers and Custom Controls

- Use Handlers for platform-specific UI customization
- Create reusable custom controls for common UI patterns

```csharp
// Custom handler mapping
public static class CustomHandlers
{
    public static void Initialize()
    {
        EntryHandler.Mapper.AppendToMapping("CustomEntry", (handler, view) =>
        {
            if (view is Entry entry)
            {
                #if ANDROID
                handler.PlatformView.SetBackgroundColor(Colors.Transparent.ToPlatform());
                #elif IOS
                handler.PlatformView.BorderStyle = UIKit.UITextBorderStyle.None;
                #endif
            }
        });
    }
}
```

## Platform-Specific Considerations

### Conditional Compilation

Use conditional compilation for platform-specific code:

```csharp
#if ANDROID
    // Android-specific code
#elif IOS
    // iOS-specific code
#elif WINDOWS
    // Windows-specific code
#elif MACCATALYST
    // macOS-specific code
#endif
```

### Platform-Specific Implementations

Use partial classes and the Platforms folder for platform-specific implementations:

```csharp
// Interface
public interface IPhotoPickerService
{
    Task<Stream> GetPhotoAsync();
}

// Implementation in Platforms/Android/PhotoPickerService.cs
public partial class PhotoPickerService : IPhotoPickerService
{
    public partial Task<Stream> GetPhotoAsync()
    {
        // Android-specific implementation
    }
}
```

### Device Idiom Adaptation

Adapt UI based on device idiom:

```xml
<StackLayout>
    <StackLayout.Padding>
        <OnIdiom x:TypeArguments="Thickness"
                 Phone="10,5"
                 Tablet="20,10"
                 Desktop="30,15" />
    </StackLayout.Padding>
</StackLayout>
```

## Performance

### Performance Best Practices

- Use CollectionView with virtualization for large lists
- Implement incremental loading for large data sets
- Optimize image loading and caching
- Minimize layout passes with proper layout choices
- Use startup tracing to improve app startup time

```csharp
// Efficient image loading
<Image Source="{Binding ImageUrl}"
       Aspect="AspectFill"
       LoadingPlaceholder="placeholder.png"
       CacheStrategy="Cache" />
```

### Memory Management

- Unsubscribe from events in IDisposable implementation
- Use weak event patterns for long-lived objects
- Implement proper cleanup in page lifecycle methods

```csharp
public partial class MyPage : ContentPage, IDisposable
{
    private bool _disposed = false;
    
    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }
    
    protected virtual void Dispose(bool disposing)
    {
        if (!_disposed)
        {
            if (disposing)
            {
                // Unsubscribe from events
                MessagingCenter.Unsubscribe<App>(this, "SomeEvent");
            }
            
            _disposed = true;
        }
    }
}
```

## Security

### Data Protection

- Use SecureStorage for sensitive data
- Implement proper authentication and authorization
- Use HTTPS for all network communications
- Validate all user inputs

```csharp
// Secure storage example
await SecureStorage.SetAsync("oauth_token", token);
var oauthToken = await SecureStorage.GetAsync("oauth_token");
```

### Authentication

- Use Microsoft Authentication Library (MSAL) for OAuth/OIDC
- Implement biometric authentication where appropriate
- Use secure storage for tokens and credentials

```csharp
// MSAL authentication
var authResult = await _publicClientApp.AcquireTokenInteractive(scopes)
    .WithParentActivityOrWindow(Platform.CurrentActivity)
    .ExecuteAsync();
```

## Testing

### Unit Testing

Use xUnit for unit testing:

```csharp
public class TodoViewModelTests
{
    [Fact]
    public async Task LoadItemsCommand_ShouldPopulateItems()
    {
        // Arrange
        var mockService = new Mock<ITodoService>();
        mockService.Setup(s => s.GetItemsAsync())
            .ReturnsAsync(new List<TodoItem> { new TodoItem { Title = "Test" } });
            
        var viewModel = new TodoListViewModel(mockService.Object);
        
        // Act
        await viewModel.LoadItemsCommand.ExecuteAsync(null);
        
        // Assert
        Assert.Single(viewModel.Items);
        Assert.Equal("Test", viewModel.Items[0].Title);
    }
}
```

### UI Testing

Use Appium or .NET MAUI UI Testing:

```csharp
[Test]
public void AddTodoItem_ShouldAppearInList()
{
    // UI test implementation
    app.Tap(c => c.Marked("AddButton"));
    app.EnterText(c => c.Marked("TitleEntry"), "New Todo");
    app.Tap(c => c.Marked("SaveButton"));
    
    var result = app.Query(c => c.Marked("TodoList").Descendant().Text("New Todo"));
    Assert.IsNotEmpty(result);
}
```

## Deployment

### App Signing

- Configure signing for all target platforms
- Use secure certificate management
- Implement CI/CD for automated builds and signing

### Store Submission

- Follow platform-specific store guidelines
- Implement proper versioning strategy
- Create compelling store listings with screenshots for all form factors

### Updates

- Implement app update checks
- Consider using App Center for distribution and analytics
- Implement proper versioning according to [Versioning Standards](../versioning/standards.md)

## Resources

- [.NET MAUI Documentation](https://learn.microsoft.com/en-us/dotnet/maui/)
- [.NET MAUI GitHub Repository](https://github.com/dotnet/maui)
- [Microsoft Learn MAUI Tutorials](https://learn.microsoft.com/en-us/training/paths/build-apps-with-dotnet-maui/)
- [MVVM Community Toolkit](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/mvvm/)
- [.NET MAUI Community Toolkit](https://learn.microsoft.com/en-us/dotnet/communitytoolkit/maui/) 