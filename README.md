# bartste-prompts

A command-line tool to generate prompts for Large Language Models (LLMs) using customizable instruction templates.

## Features

- Generate context-specific prompts for different programming languages
- Customizable instruction templates stored in `_instructions` directory
- Support for multiple output actions (print, JSON, aider integration)
- Strict mode enforcement for shell scripts
- Docstring generation with language-specific conventions

## Installation

```bash
pip install git+https://github.com/bartste/bartste-prompts.git
```

## Usage

### Basic Syntax

```bash
prompts <command> [options]
```

### Custom Instructions Directory

The tool uses instruction templates from `src/prompts/_instructions` by default. You can specify a custom instructions directory using the `--dir` option:

```bash
prompts <command> --dir=~/my-custom-prompts [options]
```

### Working Principles

1. **Command Selection**: Each command (`docstrings`, `explain`, etc.) has its own set of instruction templates
2. **Template Lookup**: For each parameter (files, filetype, user), the tool looks for:
   - Command-specific templates: `_instructions/commands/<command>/<key>.md`
   - Default templates: `_instructions/default/<key>.md`
3. **Template Formatting**: Templates can contain placeholders like `{files}` that get replaced with actual values
4. **Prompt Assembly**: All matched templates are concatenated to form the final prompt

### Examples

1. Add docstrings to Python files:

```bash
prompts docstrings --files=src/main.py --filetype=python
```

2. Explain code with custom instructions:

```bash
prompts explain --files=src/utils.py --user="Explain this utility module"
```

3. Refactor Lua code with strict mode:

```bash
prompts refactor --files=game.lua --filetype=lua
```

4. Generate unit tests for C++ code:

```bash
prompts unittests --files=src/matrix.cpp --filetype=cpp
```

### Available Commands

| Command      | Description                        |
| ------------ | ---------------------------------- |
| `docstrings` | Add docstrings to code             |
| `explain`    | Explain code functionality         |
| `fix`        | Analyze and fix code issues        |
| `refactor`   | Improve code structure and quality |
| `typehints`  | Add type annotations               |
| `unittests`  | Generate unit tests                |

### Options

| Option       | Description                        | Default                              |
| ------------ | ---------------------------------- | ------------------------------------ |
| `--action`   | Output action (print, json, aider) | `print`                              |
| `--dir`      | Custom instructions directory      | Built-in                             |
| `--loglevel` | Logging level                      | `WARNING`                            |
| `--logfile`  | Log file path                      | `~/.local/state/bartste-prompts.log` |
| `--files`    | Files to process                   |                                      |
| `--filetype` | Programming language               |                                      |
| `--user`     | Custom user instructions           |                                      |

## Customization

1. Create a directory for your custom instructions:

```bash
mkdir -p ~/my-custom-prompts/{default,commands}
```

2. Add/override templates:
   - Default templates: `~/my-custom-prompts/default/<key>.md`
   - Command-specific templates: `~/my-custom-prompts/commands/<command>/<key>.md`
3. Use your custom instructions:

```bash
prompts <command> --dir=~/my-custom-prompts [options]
```

## Configuration

The tool uses instruction templates from `src/prompts/_instructions`. You can customize these templates to modify the generated prompts.

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the terms of the MIT license. See [LICENSE](LICENSE) for details.
