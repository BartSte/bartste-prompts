# bartste-prompts

A collection of prompts for the aider AI coding assistant.

## Installation

```bash
pip install bartste-prompts
```

### Command Line Interface

```bash
prompts [options]
```

Run without arguments to see available options.

### How It Works

This package internally executes the `aider` command line tool with:

- The constructed prompt based on your command and files
- Your files added to the editing session
- Default flags: `--yes`, `--no-auto-commit`, `--no-dirty-commit`

Aider's command line arguments cannot be passed so you must configure settings
via aider's environment variables or the config file.

### Available Commands

```bash
prompts docstrings <files...>    # Add docstrings
prompts typehints <files...>     # Add type hints
prompts refactor <files...>      # Refactor code
prompts fix <files...>           # Fix bugs
prompts unittests <files...>     # Add unit tests
```
