<!--
Document: Angular Development Conventions
Version: 1.0.0
Last Updated: 2025-03-20
Last Updated By: Bayat Platform Team
Change Log:
- 2025-03-20: Initial version
-->

# Angular Development Conventions

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Component Architecture](#component-architecture)
4. [Modules](#modules)
5. [Services and Dependency Injection](#services-and-dependency-injection)
6. [State Management](#state-management)
7. [Routing](#routing)
8. [Forms](#forms)
9. [HTTP and API Communication](#http-and-api-communication)
10. [RxJS Usage](#rxjs-usage)
11. [Performance Optimization](#performance-optimization)
12. [Testing](#testing)
13. [Styling](#styling)
14. [Internationalization](#internationalization)
15. [Accessibility](#accessibility)
16. [Security Best Practices](#security-best-practices)
17. [Build and Deployment](#build-and-deployment)
18. [Documentation](#documentation)

## Introduction

This document outlines the standard conventions and best practices for Angular application development at Bayat. These guidelines aim to ensure consistency, maintainability, and scalability across all Angular projects.

## Project Structure

### Folder Organization

```
src/
├── app/
│   ├── core/                 # Singleton services, app-level components, guards, interceptors
│   │   ├── guards/
│   │   ├── interceptors/
│   │   ├── services/
│   │   └── core.module.ts
│   ├── features/             # Feature modules
│   │   ├── feature-a/
│   │   │   ├── components/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   └── feature-a.module.ts
│   │   └── feature-b/
│   ├── shared/               # Shared components, directives, pipes
│   │   ├── components/
│   │   ├── directives/
│   │   ├── pipes/
│   │   └── shared.module.ts
│   ├── app-routing.module.ts
│   ├── app.component.ts
│   └── app.module.ts
├── assets/                   # Static assets
├── environments/             # Environment configurations
└── styles/                   # Global styles
```

### Naming Conventions

- **Files**: Use kebab-case for all files
  - Example: `user-profile.component.ts`
- **Classes**: Use PascalCase for class names
  - Example: `UserProfileComponent`
- **Methods and Properties**: Use camelCase
  - Example: `getUserData()`
- **Constants**: Use UPPER_SNAKE_CASE for constants
  - Example: `MAX_RETRY_COUNT`
- **Interfaces**: Use PascalCase with 'I' prefix
  - Example: `IUserProfile`
- **Enums**: Use PascalCase
  - Example: `UserRole`

### File Naming

Follow the Angular style guide for file naming:

- `feature-name.component.ts`
- `feature-name.service.ts`
- `feature-name.module.ts`
- `feature-name.directive.ts`
- `feature-name.pipe.ts`
- `feature-name.guard.ts`
- `feature-name.interceptor.ts`
- `feature-name.model.ts`

## Component Architecture

### Component Organization

- Follow the single responsibility principle
- Create smart (container) and presentational (dumb) components
- Keep components small and focused
- Limit component files to 400 lines of code
- Extract reusable logic into services

### Component Decorators

```typescript
@Component({
  selector: 'app-feature-name',
  templateUrl: './feature-name.component.html',
  styleUrls: ['./feature-name.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush
})
```

- Use `OnPush` change detection strategy by default
- Use template and style URLs instead of inline templates and styles for components with significant content
- Prefix component selectors with 'app-' or a project-specific prefix

### Component Lifecycle

- Implement interfaces for lifecycle hooks explicitly
- Clean up subscriptions in `ngOnDestroy`
- Initialize data in `ngOnInit`, not in the constructor
- Use appropriate lifecycle hooks for different tasks

```typescript
export class FeatureComponent implements OnInit, OnDestroy {
  private destroy$ = new Subject<void>();

  constructor(private dataService: DataService) {}

  ngOnInit(): void {
    this.dataService.getData()
      .pipe(takeUntil(this.destroy$))
      .subscribe(data => {
        // Handle data
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }
}
```

## Modules

### Module Organization

- Create feature modules for distinct functional areas
- Use shared modules for reusable components, directives, and pipes
- Use core module for singleton services and app-level components
- Lazy load feature modules when possible

### Module Structure

```typescript
@NgModule({
  declarations: [
    FeatureComponent,
    FeatureListComponent,
    FeatureDetailComponent
  ],
  imports: [
    CommonModule,
    SharedModule,
    FeatureRoutingModule
  ],
  providers: [
    FeatureService
  ]
})
export class FeatureModule { }
```

- Only declare components, directives, and pipes that belong to the module
- Import only what is needed
- Export components, directives, and pipes that should be used by other modules

## Services and Dependency Injection

### Service Organization

- Create services for reusable business logic and data access
- Use the `@Injectable({ providedIn: 'root' })` syntax for app-wide singleton services
- Provide feature-specific services in their respective feature modules

```typescript
@Injectable({
  providedIn: 'root'
})
export class DataService {
  constructor(private http: HttpClient) { }

  getData(): Observable<Data[]> {
    return this.http.get<Data[]>('/api/data');
  }
}
```

### Dependency Injection Best Practices

- Use constructor injection for dependencies
- Keep the number of dependencies manageable (< 7)
- Use interfaces with injection tokens for better abstraction
- Consider using factory providers for complex service creation

## State Management

### Local State

- Use component properties for local state
- Use `BehaviorSubject` or `RxJS` streams for more complex local state

### Global State

For small to medium applications:
- Use services with `BehaviorSubject` for simple global state

For larger applications:
- Use NgRx for complex state management
- Follow the Redux pattern (actions, reducers, selectors, effects)
- Use the facade pattern to abstract state management from components

### NgRx Guidelines (when used)

- Create a clear state interface for each feature
- Use strongly typed actions
- Keep reducers pure and simple
- Use selectors for derived state
- Handle side effects in Effects classes
- Consider using the Entity pattern for collections

## Routing

### Route Configuration

- Use lazy loading for feature modules
- Implement route guards for protected routes
- Use route resolvers for pre-fetching data
- Define clear route parameters and query parameters

```typescript
const routes: Routes = [
  {
    path: 'features',
    loadChildren: () => import('./features/feature.module').then(m => m.FeatureModule),
    canActivate: [AuthGuard]
  },
  {
    path: 'feature/:id',
    component: FeatureDetailComponent,
    resolve: {
      feature: FeatureResolver
    }
  },
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  { path: '**', component: PageNotFoundComponent }
];
```

### Navigation

- Use the Router service for programmatic navigation
- Use routerLink directive for template-based navigation
- Pass state using route parameters, query parameters, or the router state

## Forms

### Form Types

- Use Reactive Forms for complex forms (preferred)
- Use Template-driven forms only for very simple forms

### Reactive Forms Best Practices

- Create form models in the component class
- Use form builders to create form groups
- Implement custom validators for complex validation
- Use form arrays for dynamic form elements

```typescript
export class UserFormComponent implements OnInit {
  userForm: FormGroup;

  constructor(private fb: FormBuilder) { }

  ngOnInit(): void {
    this.userForm = this.fb.group({
      name: ['', [Validators.required, Validators.minLength(2)]],
      email: ['', [Validators.required, Validators.email]],
      address: this.fb.group({
        street: ['', Validators.required],
        city: ['', Validators.required],
        zipCode: ['', [Validators.required, zipCodeValidator]]
      })
    });
  }

  onSubmit(): void {
    if (this.userForm.valid) {
      // Process form data
    }
  }
}
```

### Form Validation

- Display validation messages clearly
- Use consistent validation styling
- Implement cross-field validation when needed
- Disable submit buttons for invalid forms

## HTTP and API Communication

### HTTP Service Pattern

- Create dedicated service classes for API communication
- Return Observables from service methods
- Handle errors appropriately
- Use HTTP interceptors for common tasks (auth, logging, etc.)

```typescript
@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  getItems(): Observable<Item[]> {
    return this.http.get<Item[]>(`${this.apiUrl}/items`)
      .pipe(
        catchError(this.handleError)
      );
  }

  private handleError(error: HttpErrorResponse): Observable<never> {
    // Log error and transform to user-friendly message
    return throwError(() => new Error('An error occurred. Please try again later.'));
  }
}
```

### API Models

- Define interfaces for all API models
- Use type guards for runtime type checking
- Consider using class-transformer for complex transformations

## RxJS Usage

### Observable Best Practices

- Use appropriate operators for different tasks
- Avoid nested subscriptions
- Use the async pipe in templates when possible
- Always unsubscribe from subscriptions
- Use `shareReplay()` for sharing HTTP responses

### Common Patterns

- Use `combineLatest` for combining multiple streams
- Use `switchMap` for dependent HTTP requests
- Use `forkJoin` for parallel HTTP requests
- Use `Subject` or `BehaviorSubject` for event buses

```typescript
// Good example
this.route.paramMap.pipe(
  map(params => params.get('id')),
  filter(id => !!id),
  switchMap(id => this.userService.getUser(id)),
  takeUntil(this.destroy$)
).subscribe(user => {
  this.user = user;
});
```

## Performance Optimization

### Change Detection

- Use OnPush change detection strategy
- Avoid direct DOM manipulation
- Use pure pipes for transformations in templates
- Implement trackBy functions for ngFor directives

```typescript
<div *ngFor="let item of items; trackBy: trackByFn">
  {{ item.name }}
</div>

// In component
trackByFn(index: number, item: any): number {
  return item.id;
}
```

### Lazy Loading

- Lazy load feature modules
- Use dynamic imports for large libraries
- Implement virtual scrolling for long lists
- Use image lazy loading for media-heavy pages

### Bundle Optimization

- Configure proper production builds
- Use tree-shakable providers
- Analyze bundle size regularly
- Consider using web workers for CPU-intensive tasks

## Testing

### Unit Testing

- Test components, services, pipes, and directives
- Use TestBed for Angular-specific testing
- Mock dependencies appropriately
- Focus on behavior, not implementation details

```typescript
describe('UserService', () => {
  let service: UserService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserService]
    });

    service = TestBed.inject(UserService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  it('should retrieve users', () => {
    const mockUsers = [{ id: 1, name: 'John' }];

    service.getUsers().subscribe(users => {
      expect(users).toEqual(mockUsers);
    });

    const req = httpMock.expectOne(`${environment.apiUrl}/users`);
    expect(req.request.method).toBe('GET');
    req.flush(mockUsers);
  });
});
```

### Integration Testing

- Test component interactions
- Test routing and navigation
- Test form validation and submission
- Use page objects for complex component testing

### E2E Testing

- Use Cypress or Protractor for E2E testing
- Focus on critical user flows
- Test across different viewports
- Implement stable selectors for elements

## Styling

### CSS Architecture

- Use SCSS for styling
- Implement a consistent naming convention (BEM recommended)
- Create reusable mixins and functions
- Use variables for colors, spacing, and typography

### Component Styling

- Use component-specific styles with encapsulation
- Create a consistent theme system
- Implement responsive designs with media queries
- Use Angular Material or custom design system components

```scss
// Example SCSS with BEM
.user-card {
  display: flex;
  padding: 1rem;

  &__avatar {
    width: 50px;
    height: 50px;
    border-radius: 50%;
  }

  &__info {
    margin-left: 1rem;
  }

  &--highlighted {
    background-color: var(--highlight-color);
  }
}
```

## Internationalization

- Use Angular i18n or ngx-translate for translations
- Externalize all user-facing strings
- Support right-to-left languages when needed
- Format dates, numbers, and currencies according to locale

```typescript
// Using ngx-translate
<h1>{{ 'WELCOME.TITLE' | translate }}</h1>
<p>{{ 'WELCOME.TEXT' | translate:{ name: username } }}</p>
```

## Accessibility

- Follow WCAG 2.1 AA standards
- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation works
- Test with screen readers
- Support high contrast modes

## Security Best Practices

- Sanitize user input
- Protect against XSS attacks
- Implement proper authentication and authorization
- Use HTTPS for all API communication
- Follow the principle of least privilege
- Keep dependencies updated

```typescript
// Using Angular's built-in sanitization
import { DomSanitizer } from '@angular/platform-browser';

constructor(private sanitizer: DomSanitizer) { }

// In component
safeHtml = this.sanitizer.bypassSecurityTrustHtml(userProvidedHtml);
```

## Build and Deployment

### Build Configuration

- Use environment-specific configuration files
- Optimize production builds
- Implement proper source maps for debugging
- Configure bundle analysis

### Deployment Strategies

- Implement CI/CD pipelines
- Use containerization when appropriate
- Configure proper caching strategies
- Implement feature flags for controlled rollouts

## Documentation

### Code Documentation

- Use JSDoc comments for public APIs
- Document complex logic and algorithms
- Create README files for modules and features
- Maintain up-to-date architecture diagrams

```typescript
/**
 * Retrieves user data from the API
 * @param id The unique identifier of the user
 * @returns An Observable that emits the user data
 * @throws An error if the user is not found
 */
getUser(id: string): Observable<User> {
  return this.http.get<User>(`${this.apiUrl}/users/${id}`);
}
```

### Application Documentation

- Maintain up-to-date README files
- Document environment setup procedures
- Create onboarding guides for new developers
- Document architectural decisions and patterns 