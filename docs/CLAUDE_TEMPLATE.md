# CLAUDE.md Template

This template provides a standardized structure for `CLAUDE.md` files across all projects in the systems ecosystem.

## Template Structure

```markdown
# CLAUDE.md - [Project Name]

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

[Brief description of the project's purpose and core functionality]

**Key Innovation:** [Primary technical or conceptual innovation]

**Project Status:** [Research/Development/Production]

## Repository Structure

The project has several key components:

- **[component-name]/**: [Description of component]
- **[component-name]/**: [Description of component]
- **docs/**: Documentation and architecture diagrams

## Build and Development Commands

### Python Components

```bash
# Install dependencies
pip install -r requirements.txt
python -m pip install -e .

# Run tests
python run_tests.py
pytest tests/

# Run specific test
python -m unittest [test.module.path]

# Type checking and linting
mypy src/python/
flake8 src/python/
```

### Java Components

```bash
# Gradle build
./gradlew build
./gradlew test

# Run specific test
./gradlew test --tests=TestName

# Maven build (if applicable)
mvn -B clean package
mvn -B test

# Linting and formatting
mvn -B checkstyle:check
mvn spotless:apply
```

### JavaScript/TypeScript Components

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Run tests
npm test
npx vitest

# Linting and formatting
npm run lint
npm run format
```

### Mojo Components

```bash
# Install dependencies 
magic install

# Run Mojo code
magic run mojo main.mojo
cd [mojo-dir] && magic run mojo main.mojo
```

### Other Useful Commands

```bash
# Pre-commit checks
pre-commit run --all-files

# Run demo (if applicable)
python src/main/python/demo_runner.py
```

## Architectural Patterns

### [Primary Architecture Pattern]

[Description of the main architectural approach used in the project]

**Key Components:**
- **[Component Name]**: [Description and purpose]
- **[Component Name]**: [Description and purpose]
- **[Component Name]**: [Description and purpose]

### [Secondary Patterns] (Optional)

[Additional architectural patterns or frameworks used]

## Code Style Guidelines

### Universal Principles
- **Type Safety**: Strong typing and validation across all languages
- **Meaningful Names**: Descriptive variable/function/class names
- **Error Handling**: Context-rich error messages and proper exception management
- **Documentation**: Clear docstrings/comments for complex logic
- **Security**: No committed secrets, secure coding practices

### Python
- Python 3.8+
- Follow PEP 8 and use snake_case for methods/variables, PascalCase for classes
- Full type annotations for all functions
- Google-style docstrings
- Absolute imports with explicit typing

### Java
- JDK 17-23
- camelCase for methods/variables, PascalCase for classes
- Interfaces prefixed with "I" (e.g., IMemoryModule)
- Javadoc for all public methods and classes
- Custom exception hierarchy for error handling

### JavaScript/TypeScript
- ES6+ features, camelCase for functions/variables
- Prefer const over let, avoid var
- Handle async with async/await and proper error handling
- Strong TypeScript typing where applicable

### Mojo
- Use Mojo 1.0+ syntax, snake_case for functions/variables
- Match Python implementations for feature parity
- Handle Python interop with appropriate ownership transfer
- Document workarounds for current Mojo limitations

## Testing Guidelines

- Follow AAA pattern (Arrange, Act, Assert)
- Mock external dependencies appropriately
- Test both success and failure cases
- Include edge cases and boundary conditions
- Test names should be descriptive of the scenario being tested
- Maintain test coverage above [X]%

## [Project-Specific Sections]

Add project-specific sections as needed:

### Integration Points
[Describe how this project integrates with other systems]

### Performance Considerations
[Key performance patterns and optimizations]

### Multi-Provider Integration (if applicable)
[Description of multi-provider or multi-system integration]

### Evaluation Framework (for research projects)
[Metrics and evaluation approaches]

### Deployment (for production projects)
[Deployment and operational considerations]

## Development Guidelines

### Documentation Standards
- Write clear, concise documentation with proper markdown formatting
- Include diagrams and visualizations where helpful
- Maintain consistent terminology across all documentation
- Update documentation alongside code changes

### Development Process
[Project-specific development workflow, if any]

### Quality Assurance
[Quality gates, review processes, etc.]

## Important Notes

- [Any critical information developers should know]
- [Common pitfalls or gotchas]
- [Links to additional resources]
```

## Usage Instructions

1. **Copy this template** to your project as `CLAUDE.md`
2. **Replace all [bracketed placeholders]** with project-specific information
3. **Remove optional sections** that don't apply to your project
4. **Add project-specific sections** as needed
5. **Maintain consistency** with the unified development ethos

## Customization Guidelines

### Required Sections
- Project Overview
- Build and Development Commands
- Code Style Guidelines
- Testing Guidelines

### Optional Sections
- Repository Structure (recommended for complex projects)
- Architectural Patterns (recommended for projects with unique architectures)
- Project-Specific Sections (add as needed)

### Language-Specific Adaptations
- Include only the languages your project actually uses
- Follow the established patterns for each language
- Maintain consistency with the unified ethos principles

## Template Versioning

**Template Version:** 1.0  
**Last Updated:** [Current Date]  
**Based on Analysis of:** FCF, Project Aria, Anthropic Project, ClaudeMetaResearch