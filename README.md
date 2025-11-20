# Alation Allie SDK (Python)

Allie SDK is a Python library that Alation customers and partners can use to increase productivity when interacting with Alation’s [REST APIs](https://developer.alation.com/dev/reference/createtoken). By using the Allie SDK library, you can manage and change many Alation resources programmatically. You can use this library to create your own custom applications.

This repository contains Python source code for the library and documentation showing how to use it. As of June 2024, Python versions 3.10 and up are supported.

Documentation on how to use the SDK can be found at: 
https://alation.github.io/Allie-SDK/

## Support
This is an **open source** project under the [APACHE 2.0 License](https://apache.org/licenses/LICENSE-2.0) and is maintained by everyone in the Alation community. If you encounter a problem or something is not working as expected, open a [GitHub issue](https://github.com/Alation/Allie-SDK/issues) on this repo and someone will get back to you. Please **DO NOT** create an Alation support case.

## License
[APACHE 2.0 License](https://apache.org/licenses/LICENSE-2.0)

## Set up instruction for developers contributing to Allie-SDK

1. Download the repo.
2. Install `uv` if you haven’t done so already (see also [here](https://github.com/astral-sh/uv)).
3. Within the project root folder run: `uv sync`. This will create the virtual environment and install all the dependencies.

### Local Builds

You can create a local build like so (execute in the project root folder):

```shell
uv build
```

