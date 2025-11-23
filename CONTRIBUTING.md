# Contributing to Pixel Bot

First off, thank you for considering contributing to Pixel Bot! 🎉

Following these guidelines helps to communicate that you respect the time of the developers managing and developing this open source project. In return, they should reciprocate that respect in addressing your issue, assessing changes, and helping you finalize your pull requests.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and constructive.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates.

When you create a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps to reproduce the problem**
- **Provide specific examples**
- **Describe the behavior you observed and what you expected**
- **Include screenshots if possible**
- **Include your environment details:**
  - OS version (Windows 10/11)
  - Python version (if running from source)
  - Browser and version
  - Whether you're using the .exe or running from source

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description** of the suggested enhancement
- **Provide specific examples** to demonstrate the steps
- **Describe the current behavior** and **explain the behavior you expected**
- **Explain why this enhancement would be useful**

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Follow the coding style** of the project
3. **Write clear commit messages**
4. **Update documentation** if needed
5. **Test your changes** thoroughly
6. **Submit a pull request**

#### Branch Naming Convention

- `feature/feature-name` - New features
- `fix/bug-description` - Bug fixes
- `docs/what-changed` - Documentation updates
- `refactor/what-changed` - Code refactoring
- `test/what-added` - Test additions

#### Commit Message Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `build`: Build system changes
- `ci`: CI/CD changes
- `chore`: Other changes (dependencies, etc.)

**Examples:**
```
feat(monitors): Add support for OCR text monitoring

Implemented text detection using Tesseract OCR.
Monitors can now trigger based on text presence.

Closes #42
```

```
fix(picker): Resolve coordinate offset in multi-monitor setup

The pixel picker was using incorrect coordinates on secondary monitors.
Now properly handles multi-monitor configurations.

Fixes #123
```

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- Windows 10/11

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/flask-exile.git
cd flask-exile

# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r backend\requirements.txt
pip install -r requirements-build.txt  # For building

# Run the application
cd backend
python app.py
```

### Project Structure

```
flask-exile/
├── backend/
│   ├── app.py              # Main Flask application
│   ├── config.py           # Configuration
│   ├── models/             # Data models
│   ├── services/           # Business logic
│   ├── routes/             # API endpoints
│   ├── websocket/          # Socket.IO handlers
│   ├── bot/                # Automation modules
│   └── static/             # Frontend (Vue.js)
├── PixelBot.spec          # PyInstaller config
└── build_standalone.ps1   # Build script
```

## Coding Guidelines

### Python (Backend)

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where possible
- Write docstrings for functions and classes
- Keep functions focused and small
- Use meaningful variable names

**Example:**
```python
def calculate_color_distance(color1: list[int], color2: list[int]) -> float:
    """
    Calculate Euclidean distance between two RGB colors.
    
    Args:
        color1: RGB color as [r, g, b]
        color2: RGB color as [r, g, b]
    
    Returns:
        float: Distance between colors
    """
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5
```

### JavaScript (Frontend)

- Use Vue.js 3 Composition API style
- Keep components focused and reusable
- Use meaningful component and variable names
- Add comments for complex logic

**Example:**
```javascript
// components/MonitorCard.js
const MonitorCard = {
    name: 'MonitorCard',
    props: {
        monitor: {
            type: Object,
            required: true
        }
    },
    template: `
        <div class="monitor-card">
            <!-- Card content -->
        </div>
    `
};
```

### CSS

- Use the existing naming conventions
- Keep selectors specific but not overly nested
- Use CSS variables for theme colors
- Comment complex layouts

## Testing

### Manual Testing

Before submitting a PR, please test:

1. **Basic Functionality:**
   - Creating monitors
   - Editing monitors
   - Deleting monitors
   - Pausing/resuming monitors

2. **Pixel Picker:**
   - Picking pixels
   - Multi-monitor support
   - Coordinate accuracy

3. **Monitoring:**
   - Monitors trigger correctly
   - Actions execute
   - Cooldowns work
   - Master-slave relationships

4. **Build:**
   - Standalone .exe builds successfully
   - .exe runs on clean Windows

### Running From Source

```bash
cd backend
python app.py
```

Open http://localhost:5000 in your browser.

## Documentation

- Update README.md if you change functionality
- Update USER_GUIDE.md for user-facing changes
- Update CHANGELOG.md following Keep a Changelog format
- Add inline comments for complex code
- Update docstrings for API changes

## Questions?

Feel free to ask questions by:
- Opening a [Discussion](https://github.com/wr0b3l/flask-exile/discussions)
- Opening an [Issue](https://github.com/wr0b3l/flask-exile/issues)

## Recognition

Contributors will be recognized in:
- README.md (Contributors section)
- Release notes
- CHANGELOG.md

Thank you for contributing! 🙏


