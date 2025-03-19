<!--
Document: Qt Framework Development Guidelines
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Qt Framework Development Guidelines

This document outlines the standards and best practices for developing desktop and mobile applications using the Qt framework at Bayat.

## Table of Contents

1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Development Environment](#development-environment)
4. [Architecture](#architecture)
5. [C++ Conventions](#c-conventions)
6. [QML Best Practices](#qml-best-practices)
7. [Performance Optimization](#performance-optimization)
8. [Internationalization](#internationalization)
9. [Testing](#testing)
10. [Deployment](#deployment)
11. [Resources](#resources)

## Introduction

Qt is a powerful cross-platform framework for developing applications that can run on desktop (Windows, macOS, Linux), mobile (Android, iOS), embedded systems, and more. This guide focuses on desktop application development with Qt.

### When to Use Qt

Qt is the preferred choice when:
- You need high-performance native applications
- Deep system integration is required
- Cross-platform deployment is necessary
- You need custom UI controls or visualizations
- Real-time data processing or hardware integration is needed

### Key Components

- **Qt Widgets**: Traditional desktop UI framework
- **Qt Quick/QML**: Modern declarative UI framework with JavaScript integration
- **Qt Core**: Non-UI functionality (file I/O, networking, threading)
- **Qt Network**: Network programming capabilities
- **Qt SQL**: Database integration
- **Qt Test**: Unit testing framework

## Project Structure

### Standard Project Layout

```
project-root/
├── .github/                    # GitHub workflows
├── .vscode/                    # VS Code configuration (optional)
├── assets/                     # Application assets
│   ├── icons/                  # Application icons
│   ├── images/                 # Image resources
│   └── fonts/                  # Custom fonts
├── docs/                       # Documentation
├── src/                        # Source code
│   ├── core/                   # Core business logic
│   │   ├── models/             # Data models
│   │   ├── services/           # Business services
│   │   └── utils/              # Utility functions
│   ├── ui/                     # UI code
│   │   ├── views/              # QML or Widget UI components
│   │   ├── delegates/          # QML delegates
│   │   └── styles/             # Style definitions
│   ├── main.cpp                # Application entry point
│   └── application.h/cpp       # Main application class
├── resources/                  # Resource files (.qrc)
│   ├── qml.qrc                 # QML resources
│   └── assets.qrc              # Asset resources
├── tests/                      # Test files
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── auto/                   # Automated UI tests
├── translations/               # Translation files (.ts)
├── CMakeLists.txt              # CMake build configuration
├── .gitignore                  # Git ignore file
└── README.md                   # Project documentation
```

### Key Files

- **main.cpp**: Application entry point
- **CMakeLists.txt**: Build configuration
- **qml.qrc**: QML resource file
- **application.h/cpp**: Main application class

### Resource Management

- Use Qt Resource System (.qrc files) for embedding assets
- Structure resource files logically:

```xml
<RCC>
    <qresource prefix="/images">
        <file>assets/images/logo.png</file>
    </qresource>
    <qresource prefix="/fonts">
        <file>assets/fonts/CustomFont.ttf</file>
    </qresource>
    <qresource prefix="/views">
        <file>src/ui/views/MainView.qml</file>
    </qresource>
</RCC>
```

## Development Environment

### Recommended Setup

- **IDE**: Qt Creator or Visual Studio with Qt extension
- **Build System**: CMake (preferred) or qmake
- **Compiler**:
  - Windows: MSVC or MinGW
  - macOS: Clang
  - Linux: GCC or Clang
- **Qt Version**: Latest LTS release (currently Qt 6.5 LTS)

### Development Environment Setup

```bash
# Install Qt
# Download and run the Qt Online Installer from https://www.qt.io/download

# Create a new project
mkdir MyQtProject
cd MyQtProject
cmake -S . -B build -G "Ninja" -DCMAKE_PREFIX_PATH=/path/to/Qt/6.5.0/gcc_64

# Build the project
cmake --build build
```

## Architecture

### UI Technology Choice

Choose the appropriate UI technology based on project requirements:

1. **Qt Quick (QML)**: Recommended for modern applications
   - Fluid animations and modern UIs
   - Rapid development
   - Touch-friendly interfaces
   - Dynamic UI with JavaScript logic

2. **Qt Widgets**: Better for traditional desktop applications
   - Complex forms and data entry
   - Windows/macOS/Linux native look and feel
   - Legacy application maintenance
   - Accessibility requirements

### Architectural Patterns

#### Model-View-Controller (MVC)

For Qt Widgets applications:

```cpp
// Model
class TaskModel : public QAbstractListModel {
    // Model implementation
};

// View
class TaskView : public QListView {
    // View implementation
};

// Controller
class TaskController : public QObject {
    // Controller implementation
};
```

#### Model-View-ViewModel (MVVM)

For Qt Quick/QML applications:

```cpp
// Model
class TaskModel : public QAbstractListModel {
    // Model implementation
};

// ViewModel
class TaskViewModel : public QObject {
    Q_OBJECT
    Q_PROPERTY(TaskModel* tasks READ tasks CONSTANT)
    Q_PROPERTY(bool hasActiveTasks READ hasActiveTasks NOTIFY hasActiveTasksChanged)
    
public:
    TaskModel* tasks() const;
    bool hasActiveTasks() const;
    
signals:
    void hasActiveTasksChanged();
    
public slots:
    void addTask(const QString& description);
    void removeTask(int index);
};
```

#### QML View
```qml
// View (QML)
ListView {
    model: viewModel.tasks
    delegate: TaskDelegate {
        description: model.description
        onRemoveClicked: viewModel.removeTask(index)
    }
}
```

## C++ Conventions

Follow the standard \1\2) with these Qt-specific additions:

### Naming Conventions

- **Classes**: PascalCase, prefixed with a project-specific identifier for public APIs
  ```cpp
  class BAProjectNameWidget : public QWidget { ... };
  ```

- **Methods**: camelCase
  ```cpp
  void processData(const QByteArray& data);
  ```

- **Signals/Slots**: camelCase, with specific verbs
  ```cpp
  // Signals use past tense for events that have occurred
  signals:
      void dataProcessed(const QByteArray& result);
      void errorOccurred(const QString& message);
  
  // Slots use imperative for actions
  public slots:
      void processData();
      void handleError(const QString& message);
  ```

- **Q_PROPERTY**: camelCase
  ```cpp
  Q_PROPERTY(QString userName READ userName WRITE setUserName NOTIFY userNameChanged)
  ```

### Memory Management

- Use Qt's parent-child mechanism for memory management
- Prefer smart pointers for objects without parents
- Be careful with ownership when connecting signals and slots

```cpp
// Parent-child relationship
QVBoxLayout* layout = new QVBoxLayout(this); // 'this' is the parent
layout->addWidget(new QPushButton("OK", this)); // Parent takes ownership

// Smart pointers for objects without parents
std::unique_ptr<DataProcessor> processor = std::make_unique<DataProcessor>();
```

### Signal-Slot Best Practices

- Use the new connection syntax
- Use lambdas for simple slot implementations
- Connect signals and slots in the constructor or init method

```cpp
// Modern connection syntax
connect(button, &QPushButton::clicked, this, &MyWidget::handleButtonClick);

// Lambda for simple slots
connect(button, &QPushButton::clicked, [this]() {
    statusLabel->setText("Button clicked");
});

// Connections with parameters
connect(networkManager, &QNetworkAccessManager::finished,
        this, &MyClass::handleNetworkReply);
```

## QML Best Practices

### QML Component Organization

- Create reusable components
- Use Qt Quick Controls 2 for standard UI elements
- Keep component files small and focused

```qml
// CustomButton.qml
Button {
    id: root
    
    property color accentColor: "#0066cc"
    
    background: Rectangle {
        color: root.down ? Qt.darker(root.accentColor, 1.2) : root.accentColor
        radius: 4
    }
}
```

### QML-C++ Integration

- Use contexts for simple property exposure
- Use registerType for exposing C++ types to QML
- Create dedicated interface classes for complex logic

```cpp
// In C++
// Setting context properties
QQmlApplicationEngine engine;
engine.rootContext()->setContextProperty("dataModel", &dataModel);

// Registering types
qmlRegisterType<UserModel>("io.bayat.models", 1, 0, "UserModel");
```

```qml
// In QML
import io.bayat.models 1.0

UserModel {
    id: userModel
    // Use the registered C++ type
}
```

### QML Performance

- Limit use of JavaScript for performance-critical code
- Avoid binding loops
- Use Component.onCompleted sparingly
- Prefer Loaders for dynamic content

```qml
// Efficient use of Loader
Loader {
    id: detailLoader
    active: tabBar.currentIndex === 1
    sourceComponent: DetailView { model: detailModel }
}
```

## Performance Optimization

### General Optimization

- Use the Qt Profiler to identify bottlenecks
- Optimize layout operations (avoid frequent layout recalculations)
- Use image caching and scaling appropriately
- Implement model/view optimizations for large data sets

### QML-Specific Optimizations

- Use Item Layers for complex, static components
- Implement incremental rendering for large views
- Use ShaderEffect for custom rendering
- Cache complex components with Loader

```qml
// Use layers for caching complex static elements
Rectangle {
    id: complexItem
    layer.enabled: true
    layer.smooth: true
    // Complex content
}
```

### C++ Optimizations

- Implement custom models for large datasets
- Use Qt's concurrent framework for background processing
- Optimize painting operations in custom widgets
- Use implicit sharing features

```cpp
// Concurrent processing
#include <QtConcurrent>

void MyClass::processData(const QByteArray& data) {
    QFuture<QByteArray> future = QtConcurrent::run([data]() {
        return processDataInBackground(data);
    });
    
    QFutureWatcher<QByteArray>* watcher = new QFutureWatcher<QByteArray>(this);
    connect(watcher, &QFutureWatcher<QByteArray>::finished, this, [this, watcher]() {
        QByteArray result = watcher->result();
        emit dataProcessed(result);
        watcher->deleteLater();
    });
    
    watcher->setFuture(future);
}
```

## Internationalization

### Translation Setup

- Use tr() and qsTr() for all user-visible strings
- Organize translation files (.ts) in the translations directory
- Implement locale switching at runtime

```cpp
// C++ string translation
void MyWidget::setupUi() {
    label->setText(tr("Welcome to the application"));
    submitButton->setText(tr("Submit"));
}
```

```qml
// QML string translation
Text {
    text: qsTr("Welcome to the application")
}
```

### Translation Process

1. Update translation sources:
   ```bash
   lupdate -recursive ./ -ts translations/app_en.ts translations/app_fr.ts
   ```

2. Translate strings using Qt Linguist

3. Release translations:
   ```bash
   lrelease translations/app_*.ts
   ```

4. Load translations at runtime:
   ```cpp
   QTranslator translator;
   if (translator.load(":/translations/app_" + locale + ".qm")) {
       QApplication::installTranslator(&translator);
   }
   ```

## Testing

### Unit Testing

Use Qt Test framework for unit testing:

```cpp
// testcalculator.cpp
#include <QtTest>
#include "../src/calculator.h"

class TestCalculator : public QObject {
    Q_OBJECT
    
private slots:
    void testAddition() {
        Calculator calc;
        QCOMPARE(calc.add(2, 3), 5);
    }
    
    void testSubtraction() {
        Calculator calc;
        QCOMPARE(calc.subtract(5, 3), 2);
    }
};

QTEST_MAIN(TestCalculator)
#include "testcalculator.moc"
```

Add to CMake:
```cmake
add_executable(testcalculator testcalculator.cpp)
target_link_libraries(testcalculator PRIVATE Qt6::Test app_core)
add_test(NAME testcalculator COMMAND testcalculator)
```

### UI Testing

Use Qt Test or Squish for UI testing:

```cpp
// UI test with Qt Test
class TestMainWindow : public QObject {
    Q_OBJECT
    
private slots:
    void testUiInteraction() {
        MainWindow window;
        window.show();
        
        QTest::mouseClick(window.findChild<QPushButton*>("submitButton"), Qt::LeftButton);
        QCOMPARE(window.findChild<QLabel*>("statusLabel")->text(), "Submitted");
    }
};
```

## Deployment

### Build Configuration

Use CMake for build configuration:

```cmake
cmake_minimum_required(VERSION 3.16)
project(MyQtApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick)

qt_add_executable(MyQtApp
    src/main.cpp
    src/application.cpp
    src/core/models/datamodel.cpp
)

target_link_libraries(MyQtApp PRIVATE
    Qt6::Core
    Qt6::Gui
    Qt6::Widgets
    Qt6::Quick
)

qt_add_qml_module(MyQtApp
    URI MyQtApp
    VERSION 1.0
    QML_FILES
        src/ui/views/MainView.qml
        src/ui/views/DetailView.qml
)

qt_add_resources(MyQtApp "assets"
    PREFIX "/"
    FILES
        assets/images/logo.png
        assets/fonts/CustomFont.ttf
)
```

### Deployment Process

- Use Qt's deployment tools (windeployqt, macdeployqt, etc.)
- Create platform-specific installers with appropriate packaging tools
- Sign applications for distribution

```bash
# Windows deployment
windeployqt --qmldir src/ui/views build/release/MyQtApp.exe

# macOS deployment
macdeployqt build/MyQtApp.app -qmldir=src/ui/views -dmg

# Linux AppImage
linuxdeployqt build/MyQtApp -qmldir=src/ui/views -appimage
```

## Resources

- [Qt Documentation](https://doc.qt.io/)
- [Qt Examples](https://doc.qt.io/qt-6/examples-tutorials.html)
- [Qt Best Practices](https://doc.qt.io/qt-6/best-practices.html)
- [Qt Style Guide](https://wiki.qt.io/Qt_Coding_Style)
- [Qt Design Studio](https://www.qt.io/design)