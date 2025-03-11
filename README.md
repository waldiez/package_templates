# Package templates

This repository contains a collection of templates for packages meant to be parts of a parent project.
The packages are meant to be used as submodules in a parent project/repository.
They can (and should) be developed and tested independently, as long as meet the requirements of the parent project (see the [Restrictions](#restrictions) section below).

## Templates

- [python_only](./python_only/) - A template for a Python package.
- [ts_only](./ts_only/) - A template for a TypeScript package.
- [both](./both/) - A template for a package that contains both Python and TypeScript code.

### Python only

It includes a minimal cli hello world app using typer. Code formatting and linting is done with multiple tools (`black`, `isort`, `flake8`, `mypy`, `pylint`, `pydocstyle`, `bandit`, `ruff`, `markdownlint`, `yamllint`). Tests are run with `pytest` including coverage with `pytest-cov`. The package is built with hatch, and a `Containerfile` is included to build a container image with podman or docker. Docs are built with `mkdocs` with the `mkdocs-material` theme and several plugins.

### TypeScript only

It includes a minimal react app, built with vite (both as a library and as a standalone static site). Code formatting and linting is done with multiple tools (`eslint`, `prettier`, `stylelint`, `markdownlint`, `yamllint`). Tests are run with `vitest` including coverage with `@vitest/coverage-v8`. The package is built with bun, and a `Dockerfile` is included to build a container image with podman or docker. The docs are built with `typedoc`.

### Both

It includes a minimal Flask app that serves the static site built with vite. It combines the features of the `python_only` and `ts_only` templates. It also includes e2e tests using `playwright` (python).

## Restrictions

### Python project restrictions

With ths repository as a parent project, the following requirements are expected for any Python package (either `python_only` or `both`):

> [!IMPORTANT]
>
> **Required files**
>
> - `pyproject.toml`: the project configuration file
> - README.md: the package description
> - LICENSE: the license file
> - `scripts/version.py`: the script to update the version
>   The script should expect the arguments `--set` or `--get`  
>    and it should either return `x.y.z` or set the version to `x.y.z`.
> - `scripts/clean.py`: the script to cleanup unwanted files
> - `scripts/format.py`: the script to format the code
> - `scripts/lint.py`: the script to lint the code
> - `scripts/test.py`: the script to run the tests
>   After tests, the script should generate a `coverage/lcov.info` file with the coverage report.
>
> **Optional files**
>
> - `Containerfile`: the Podman/Docker container file to build the image
> - `scripts/docs.py`: the script to build the documentation
>   If the file exists, it should expect the argument: `--output`.
> - `scripts/build.py`: the script to build the package
>   If the file exists, it should expect the argument: `--output`.
>   It should also expect the optional argument: `--publish`
>   If the `--publish` argument is provided, the script should publish the package to the PyPI.
> - `scripts/image.py`: the script to build the Podman/Docker image:
>   It should expect the arguments:
>
>      - `--image-name`: the image name
>      - `--image-tag`: the image tag  
>     The script should build the image and tag it with the provided tag.
>     It should also expect the optional argument  
>      - `--push`. If the `--push` argument is provided, the script should push the image to one or more registries.  
>     Additional optional args can be provided to specify the target platforms and/or other build args like  
>      - `--platform`: the target platform

### TypeScript project restrictions

With ths repository as a parent project, the following requirements are expected for any TypeScript package (either `ts_only` or `both`):

> [!IMPORTANT]
>
> **Required files**
>
> - `package.json`: The package.json file must be present in the root of the repository. It must contain a `scripts` object and should also define the `packageManager` field (e.g. `"packageManager": "bun@1.2.5"`, or `"packageManager": "yarn@4.7.0"`)
> - README.md: the package description
> - LICENSE: the license file
>
> **Required scripts**
>
> - `format`: The `format` script must be present in the `package.json` file.
> - `lint`: The `lint` script must be present in the `package.json` file.
> - `clean`: The `clean` script must be present in the `package.json` file.
> - `test`: The `test` script must be present in the `package.json` file. It must generate a `coverage/lcov.info` file with the test coverage report.
> - `build`: The `build` script must be present in the `package.json` file. It must generate the distributable files in the `dist` directory.
>
> **Optional scripts**
>
> - `archive`: The `archive` script is optional. If present, it must generate a tarball of the package in the `out` directory.
> - `publish`: The `publish` script is optional. If present, it must publish the package to the registry.
> - `docs`: The `docs` script is optional. If present, it must generate the documentation in the `site` directory.
> - `image`: The `image` script is optional. If present, it must build a container image of the package.

## License

This project is licensed under the [Apache License, Version 2.0 (Apache-2.0)](https://github.com/waldiez/package_templates/blob/main/LICENSE).
