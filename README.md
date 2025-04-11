# bartste-prompts

A command-line tool to generate AI prompts for code modifications.

## Overview

This tool integrates commands for:

- **docstrings**: Add Google-style docstrings.
- **typehints**: Enhance code with proper type hints.
- **refactor**: Refactor code following best practices.
- **fix**: Fix issues in the code.
- **unittests**: Generate unit tests for your code.

## Installation

Ensure you have Python 3.7+ installed. To install bartste-prompts, you can either:

- Install via pip:

```bash
pip install git+https://github.com/bartste/bartste-prompts.git
```

- Or clone the repository and install it directly:

```bash
pip install .
```

## Usage

Run the tool via command line:

```bash
prompts
```

Or explicitly:

```bash
prompts [command] [options] [files...]
```

Example:

```bash
prompts refactor -f python myfile.py
```

Additionally, a dedicated command for AI assistance is available via the `prompts-aider` function. Run the command:

```bash
prompts-aider
```

This command passes the prompt directly to [aider](https://github.com/paul-gauthier/aider). Ensure the `aider` CLI is installed and accessible in your PATH.

## Features

- Constructs prompt strings in `promptmaker.py` using content from markdown files.
- Offers output as either a formatted string or JSON via the `--json` flag.
- Leverages command definitions and file type selections from CLI arguments in `parser.py`.
- Configures application logging using `logger.py`.
- Entry point provided by `src/prompts/__main__.py`.

## Code Structure

- **src/prompts/promptmaker.py**: Generates combined prompt strings.
- **src/prompts/parser.py**: Handles CLI argument parsing.
- **src/prompts/logger.py**: Manages logging configuration.
- **src/prompts/**main**.py**: Acts as the entry point.

## License

Licensed under the MIT License – see the LICENSE file for details.
