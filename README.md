# bartste-prompts

A command-line tool to generate AI prompts for code modifications.

## Overview

This tool generates prompts for:

- **docstrings**: Add Google-style docstrings.
- **typehints**: Enhance code with proper type hints.
- **refactor**: Refactor code following best practices.
- **fix**: Fix issues in the code.
- **unittests**: Generate unit tests for your code.

The prompts can be passed directly to external tools such as `aider` to executed
them using an LLM.

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

Additionally, the prompt can be redirected to an external tool using the `--action` option. Currently, `json` and [aider](https://github.com/paul-gauthier/aider) are supported. For example:

```bash
prompts docstrings --filetype python --action aider myfile.py
```

would pass the prompt directly to aider, adding docstrings to `myfile.py`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing.

## License

See [LICENSE](LICENSE) for licensing details.
