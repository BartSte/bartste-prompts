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

To install `bartste-prompts`, you can either:

- Install via pip:

```bash
pip install git+https://github.com/bartste/bartste-prompts.git
```

- Or clone the repository and install it directly:

```bash
pip install .
```

## Usage

Run the following to get info about the cli:

```bash
prompts --help
```

### Examples

- Generate a prompt that describes a refactor the `myfile.py` file.

  ```bash
  prompts refactor -f python myfile.py
  ```

- Send a prompt for writing docstrings to [aider](https://github.com/paul-gauthier/aider).

  ```bash
  prompts docstrings --filetype python --action aider myfile.py
  ```

  As is shown, a prompt can be redirected to an external tool using the `--action` option. Currently, `json` and [aider](https://github.com/paul-gauthier/aider) are supported.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing.

## License

See [LICENSE](LICENSE) for licensing details.
