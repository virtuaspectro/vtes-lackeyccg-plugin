# LackeyCCG VTES Plugin

[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)

This is a [LackeyCCG](https://lackeyccg.com) plugin for
[VTES (Vampire: The Eternal Struggle)](https://www.blackchantry.com/products/what-is-vampire-the-eternal-struggle/).

To use it in LackeyCCG, use this update URL: `https://lackey.krcg.org/updatelist.txt`

[Changelog](CHANGELOG.md)

![Dark Pack](https://raw.githubusercontent.com/lionel-panhaleux/krcg/master/dark-pack.png)

## New version generation

This plugin uses [Python](https://python.org) scripts to update the cards list
from the official [VEKN CSV](https://www.vekn.net/card-lists)
and generate the `updatelist.txt` and `version.txt` files.

### Perpare your python environment

Use your favorite python environment, `python -m venv lackey_env` for example. Check
[the official documentation](https://docs.python.org/3/library/venv.html#how-venvs-work)
if you're new to virtual environments.
Then call `make update` to install the Python requirements. You're ready.

### Prepare the plugin update

- To update the cards list: `make cards`
- To generate the plugin list and version files: `make list`

### Put it online

The access to the current update server (`krcg.org`) is private for now.
In the future, I will try to setup the proper Github actions so that every administrator
can update and deploy the plugin.

In the mean time, you can host the plugin your own server with a simple variable change:

```bash
SERVER_HTTP=https://example.com/path_to_plugin make list
SERVER_SSH=example.com:server/path_to_plugin make static
```

You need to be able to connect via `ssh` to your server for this command to work.
Do not forget to regenerate the `updatelist.txt` file when changing the server URL.
