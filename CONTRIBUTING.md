# Contributing

   1. Fork the repo, develop and test your code changes.
   2. Ensure commit messages clearly define the changes that have been made.
   3. Create a pull request.
   
## Adding Features

Any features added must be fully tested and documented, with examples supplied in the pull request.
The feature must support the lowest Python version that the SDK supports (see [the travis file](.travis.yml) for all supported versions).  The feature
must not introduce any unnecessary dependencies (although introducing a new third party library
is open for discussion if absolutely required).

## Pre-commit Hook

* Install the [pre-commit framework](https://pre-commit.com/)
* Run `pre-commit install`

## Testing

After cloning the repository, run the following to install dependencies:

```bash
pip install -r requirements.txt
pip install -e .[dev]
```

Running the tests:

```bash
pytest
```

## Coding Style

* The pre-commit hook uses the `black` formatter to auto-format any code when committing,
 along with `flake8` for style guide enforcement.