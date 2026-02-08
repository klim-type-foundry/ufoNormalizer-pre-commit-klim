# ufoNormalizer-pre-commit
A [pre-commit](https://pre-commit.com/) hook for [ufoNormalizer](https://github.com/unified-font-object/ufoNormalizer).

This uses a fork of `ufoNormalizer`, specifically for Klim Type Foundry.

## Installation
Add this to your `.pre-commit-config.yaml`:

```yaml
  - repo: https://github.com/klim-type-foundry/ufoNormalizer-pre-commit-klim
    rev: 1.0.2
    hooks:
      - id: ufonormalizer
```

If you want to automatically commit the UFOs after normalisation, add `--autofix`:

```yaml
  - repo: https://github.com/klim-type-foundry/ufoNormalizer-pre-commit-klim
    rev: 1.0.2
    hooks:
      - id: ufonormalizer
        args: [--autofix]
```
