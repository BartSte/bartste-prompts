# bartste-prompts

A command-line tool to generate prompts for Large Language Models (LLMs) using customizable instruction templates.

## Introduction

`bartste-prompts` is a CLI tool designed for developers to generate prompts for Large Language Models (LLMs). It uses a set of predefined instructions that can be customized per command and per file type. The tool is built with extensibility in mind, allowing users to define their own instructions. The CLI will adapt to custom instructions as a fixed directory structure is assumed.

Key features include:

- Dynamic prompt assembly from markdown instruction templates
- Support for multiple default commands (e.g., explain, fix, refactor, etc.) and file types
- Integration with tools like `aider` for code editing and explanation
- Can be extended with custom instructions
- The CLI adapts to new instructions. No changes in code are necessary.

## Installation

You can install `bartste-prompts` using pip:

```bash
pip install bartste-prompts
```

For development dependencies (testing, linting, etc.), install with:

```bash
pip install bartste-prompts[dev]
```

This will install the `prompts` command-line tool.

## Usage

The basic command structure is:

```bash
prompts <command> [options]
```

### Available Commands

The tool comes with these default commands:

- `docstrings`: Generate docstrings for given files
- `explain`: Explain code functionality
- `fix`: Fix code issues
- `refactor`: Improve code structure
- `typehints`: Add type hints to code
- `unittests`: Generate unit tests

### Common Options

All commands support these options:

- `--action <tool>`: Specify output tool (`print`, `json`, or `aider`)
- `--loglevel <level>`: Set logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`)
- `--logfile <path>`: Specify log file location

### Command-Specific Options

Each command has additional options that correspond to instruction templates. For example:

```bash
# Explain command options
prompts explain --files <files> --filetype <type> --user <text>

# Fix command options
prompts fix --files <files> --filetype <type> --user <text>
```

### Examples

Print prompt for explaining Python code:

```bash
prompts explain --files main.py --filetype python
```

Generate JSON output for adding type hints:

```bash
prompts typehints --files utils.py --filetype python --action json
```

Run aider to fix Lua code:

```bash
prompts fix --files script.lua --filetype lua --user "Fix memory leak" --action aider
```

### Custom Instructions

You can use custom instructions by specifying the `--dir` option. The custom directory must follow the same structure as the default `_instructions` directory. Here's how it works:

#### Directory Structure

```
custom_instructions/
├── commands/
│   ├── <command1>/
│   │   ├── command.md
│   │   ├── <key1>.md --> "Text with {value1} as placeholder."
│   │   └── <key2>/
│   │       └── <value2>.md
│   ├── <command2>/
│   │   └── command.md
│   └── ...
└── default/
    ├── <key1>.md
    └── <key2>/
        └── <value2>.md
```

- **commands/**: Contains subdirectories for each command (e.g., `explain`, `fix`, etc.)

  - Each command directory must contain a `command.md` file (base instruction)
  - Additional markdown files or subdirectories correspond to command options (e.g., `--files`, `--user`, etc.). Here, the files and subdirectories handle the cli values differently:
    - File: The content of the value can be inserted in the markdown using a python placeholder. For example, for the cli option `--files=foo.py`, the "files.md" file contains a placeholder `{files}` which will be replaced by `foo.py`.
    - Subdirectory: The value represents a filename (without extension) of a markdown file within the subdirectory, which will be read.

- **default/**: Contains fallback instructions in case an instruction is not found in the command directory.

Using a fixed directory structure allows the CLI to adapt to the custom instructions. For example, the directory structure above results in the following CLI:

```bash
prompts <command1> --key1 <value1> --key2 <value2>
prompts <command2> --key1 <value1> --key2 <value2>
```

Here, `command2` will fallback to the default directory for options, `key1` represents a file, `value1` will be inserted in `key1.md`, `key2` represents a directory and `value2` is a file within the `key2` directory.

## Troubleshooting

If you encounter any issues, please report them on the issue tracker at: [bartste-prompts issues](https://github.com/BartSte/bartste-prompts/issues)

## Contributing

Contributions are welcome! Please see [CONTRIBUTING](./CONTRIBUTING.md) for more information.

## License

Distributed under the [MIT License](./LICENCE).
