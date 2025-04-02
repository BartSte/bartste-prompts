# bartste-prompts

A collection of prompts for the aider AI coding assistant.

## Installation

```bash
pip install bartste-prompts
```

## Usage

### As a Python module

```python
from prompts import *  # This matches the package name
```

### Command Line Interface

```bash
prompts [options]
```

Run without arguments to see available options.

### Environment Variables

The CLI supports these environment variables:

- `AIDER_READ`: Path(s) to files containing coding conventions. Can be:
  - Single file path: `$HOME/conventions.md`
  - List of paths: `[$HOME/conventions.md, $HOME/python/conventions.md]`
  
  Contents will be provided as context to the AI.

- `AIDER_MODEL`: Name of the AI model to use (e.g. `gpt-4`). 
  If not specified, uses aider's default model.

### Available Commands

```bash
prompts docstrings <files...>    # Add docstrings
prompts typehints <files...>     # Add type hints  
prompts refactor <files...>      # Refactor code
prompts fix <files...>           # Fix bugs
```
