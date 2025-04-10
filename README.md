# bartste-prompts

A command-line tool to generate AI prompts for code modifications.

## Overview

This tool integrates commands for:
- **docstrings**: Add Google-style docstrings.
- **typehints**: Enhance code with proper type hints.
- **refactor**: Refactor code following best practices.
- **fix**: Fix issues in the code.
- **unittests**: Generate unit tests for your code.

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
- **src/prompts/__main__.py**: Acts as the entry point.

## License

Licensed under the MIT License – see the LICENSE file for details.
