## Filetype: YML

When documenting YAML files, you MUST follow these principles:

- Place descriptive comments directly above the section or key they explain.
- Use `#` for every comment line and keep indentation aligned with the YAML content.
- Document the file’s purpose at the top, then list required and optional keys, including units or allowed values where relevant.

```yaml
# @brief CI pipeline configuration for linting and testing
# @section stages
#   - lint: Run static analysis with flake8
#   - test: Execute unit test suite
stages:
  - lint
  - test

# @section lint job configuration
# @param image           Docker image with Python tooling
# @param script          Commands executed in the job
lint:
  image: python:3.12-slim
  script:
    - pip install -r requirements-dev.txt
    - flake8 src tests
```
