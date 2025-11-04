## Filetype: YAML

- Maintain consistent indentation using two spaces per level; align sequence items and nested mappings for readability.
- Place descriptive comments above related sections or keys with `#` to clarify intent without cluttering inline values.
- Choose quoting deliberately: leave simple scalars unquoted, prefer double quotes for interpolation/escape sequences, and single quotes to preserve literal text.
- Reuse fragments with anchors (`&`) and aliases (`*`), and merge shared mappings via the `<<` key to minimize duplication while keeping context clear.
- Separate multiple documents with `---`, and include an explicit `...` end marker when streaming or piping content that benefits from terminators.
- Handle data typing explicitly by avoiding ambiguous values (such as numbers with leading zeros) and applying tags when precise typing is required.
- Validate structure against schemas (JSON Schema, OpenAPI, Kubernetes CRDs, etc.) whenever possible to catch errors early.
- Lint and test configurations with tools like `yamllint`, `kubeval`, or `spectral`, and design YAML-driven tests using an arrange-act-assert approach.
