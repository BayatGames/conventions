# Internationalization and Localization Standards

This document outlines the standards and best practices for internationalization (i18n) and localization (l10n) across all Bayat projects.

## Definitions

- **Internationalization (i18n)**: The design and development of a product to enable localization for target audiences that vary in culture, region, or language.
- **Localization (l10n)**: The adaptation of a product or content to meet the language, cultural, and other requirements of a specific target market.

## General Principles

- Design with internationalization in mind from the beginning
- Separate UI text from code
- Support right-to-left (RTL) languages where applicable
- Follow locale-specific formatting conventions
- Consider cultural differences in design elements
- Ensure adequate space for text expansion in translated content

## Text and Content

### String Externalization

- Store all user-facing strings in dedicated resource files
- Never hardcode text strings in the application code
- Use string interpolation with named parameters instead of positional ones
- Provide context comments for translators

### Format Example (JSON):
```json
{
  "welcome_message": {
    "text": "Welcome, {username}!",
    "context": "Greeting displayed on the dashboard after login"
  }
}
```

### Text Guidelines

- Avoid idioms, slang, and culture-specific references
- Use clear, concise language
- Keep sentences short and simple
- Avoid humor that may not translate well
- Use symbols and icons that are universally understood

## Date, Time, and Number Formatting

- Use library functions for date, time, and number formatting
- Never assume a specific date/time format (MM/DD/YYYY vs. DD/MM/YYYY)
- Support different calendar systems when relevant
- Format currency with appropriate symbols and decimal separators
- Use appropriate separators for thousands (comma, period, space)

## Character Sets and Encoding

- Use UTF-8 encoding for all text
- Ensure fonts support all required character sets
- Test with non-Latin characters
- Properly handle input, storage, and display of non-ASCII characters

## Right-to-Left (RTL) Support

- Use CSS logical properties (start/end) instead of left/right
- Test layouts with RTL languages
- Ensure bidirectional text rendering works correctly
- Consider the directionality of UI elements (e.g., icons, sliders)

## Images and Media

- Avoid text in images
- If text in images is necessary, provide localized versions
- Be aware of cultural sensitivities regarding imagery
- Provide alt text for images that can be localized

## Development Practices

### Code-level Practices

- Use a robust i18n framework or library for your technology stack
- Support plural forms with appropriate rules
- Handle gendered language appropriately
- Implement locale fallbacks for missing translations

### Examples of Frameworks

- React: react-i18next, FormatJS
- Angular: ngx-translate, Angular i18n
- iOS: NSLocalizedString, Strings files
- Android: Resources framework, String resources
- Flutter: flutter_localizations, intl package

## Locale Selection and Detection

- Allow users to explicitly select their preferred language
- Use browser/device language settings as the default
- Save language preferences for returning users
- Consider location-based defaults when appropriate

## Testing

- Test with pseudo-localization to identify hardcoded strings
- Perform linguistic testing with native speakers
- Test with different locale settings
- Verify proper expansion space for languages that require more characters
- Test all supported input methods
- Verify RTL layout if applicable

## Translation Process

### Translation Management

- Use a Translation Management System (TMS)
- Provide context and screenshots for translators
- Establish a glossary of product-specific terms
- Maintain version control for translations

### Continuous Localization

- Integrate localization into the CI/CD pipeline
- Automate extraction of translatable strings
- Set up notification systems for new or changed strings
- Establish a prompt translation cadence

## File Organization

### Directory Structure

```
/src
  /locales
    /en-US
      common.json
      homepage.json
      settings.json
    /fr-FR
      common.json
      homepage.json
      settings.json
    /de-DE
      ...
```

### Naming Conventions

- Use ISO language and country codes (e.g., en-US, fr-FR)
- Group related strings in logical files
- Use consistent key naming conventions (e.g., camelCase or snake_case)

## Documentation

- Document supported languages and locales
- Provide guidelines for adding new languages
- Document any locale-specific features or limitations
- Maintain a changelog of translation updates

## Performance Considerations

- Load only the required language resources
- Consider lazy-loading additional languages
- Optimize locale data file sizes
- Cache locale information appropriately 