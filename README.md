# Poetry Private Source Plugin

Poetry plugin that ensures your env is updated with the correct vars to use your (private) source repos.

So far the only kind of private repo supported is AWS CodeArtifact.

I coded this for my own convenience, so I didn't had to set up different `POETRY_HTTP_BASIC_..._PASSWORD` env vars calling aws cli from my `.bash_profile` file.

## Installation

Supposedly you can install this plugin using `self add`

```shell
poetry self add poetry-plugin-up
```

however, this never worked for me.

Instead you just have to remember how you installed `poetry`:

If it was `pipx` then add the plugin like this

```shell
pipx inject poetry poetry-private-source-plugin
```

Or if it was `pip`

```shell
pip install poetry-private-source-plugin
```

If you use `pyenv` to handle different python versions, you must use `pipx` or `pip` from the same version you used to install `poetry`.

## Usage

Just install the plugin and you are done.

If you need to control the TTL of the CodeArtifact token, you can do so by defining the `POETRY_CODEARTIFACT_TOKEN_TTL` env var. Otherwise it's set to 900 seconds.
