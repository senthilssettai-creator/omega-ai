# omega-ai

A prototype autonomous terminal AI agent with workflow execution, browser automation, memory, and live progress logging.

## Status

- **Production ready?** No. This project is currently an early prototype and should be used for experimentation.
- Recommended improvements before production: stronger error handling, secure configuration, workflow validation, robust persistence, and expanded test coverage.

## Requirements

- Python 3.12 or newer
- `pip` and a virtual environment
- Optional but recommended: `docker` for Docker build actions
- Optional: `OPENROUTER_API_KEY` environment variable for OpenRouter-powered agents

## Installation

1. Clone the repository:

```bash
git clone https://github.com/senthilssettai-creator/omega-ai.git
cd omega-ai
```

2. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Upgrade pip:

```bash
python -m pip install --upgrade pip
```

4. Install the package:

```bash
pip install .
```

5. Install Playwright browsers:

```bash
python -m playwright install chromium
```

6. (Optional) Install testing dependencies:

```bash
pip install .[testing]
```

## Quick verification

```bash
omega status
python -m pytest -q
```

## Environment configuration

Create a `.env` file in the repository root if needed:

```ini
OPENROUTER_API_KEY=your_api_key_here
PLAYWRIGHT_HEADLESS=true
```

## Usage

- Run the API server:

```bash
omega run
```

- List workflows:

```bash
omega workflows
```

- Execute a workflow:

```bash
omega run-workflow <name>
```

- Open the live dashboard:

```bash
omega dashboard
```
