# How to navigate the repo

The main code base of Allie-SDK is within the `allie_sdk` folder. Inside this folder you can find:
- The `core` folder which includes core functionality used across all the methods and also essential functionality around authentication etc. 
- The `methods` folder includes dedicated files for each Alation Alation API endpoint and lists all the methods that are available for this API endpoint.
- The `models` folder includes dedicated files for each Alation Alation API endpoint and lists all the data classes required for this API endpoint. The data classes are used with the related method file in the `methods` folder.
- The `alation.py` holds the `Alation` class, which is the main entry point to interacting with the Allie-SDK.

All our tests are in the `tests` folder. The subfolder structure is the same as for the `allie_sdk` folder. For nearly each file in `allie_sdk` you should find a file in the related subfolder under `tests` and that file will be usually prefixed with `test_`.

In the `examples` folder you should find one file/example for each file in `allie_sdk/methods` that shows how to use each of the methods. This is the help developers understand how these methods can be used. The intention here is also to have real world examples that you can run against your Alation server (whereas the tests use a mocker to similate the requests).

In the `example_errors` folder you should find one file/example for each file in `allie_sdk/methods` that shows how to use each of the methods, but in this case, we make the request call fail on purpose so that you can see what error messages look like.

The `docs` folder has the main documentation. The `docs/pages/reference` subfolder should include a file/documentation for each file in `allie_sdk/methods`. 

# Setup commands

```shell
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

# Code Style

- use Python type hints
- use double quotes instead of single quotes were possible

# Code Standards

- always add logging
- no failing silently (always throw errors)
- robust error handling
- use the most up-to-date packages and technologies
