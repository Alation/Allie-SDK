# Alation Allie SDK (Python)

Allie SDK is a Python library that Alation customers and partners can use to increase productivity when interacting with Alation’s [REST APIs](https://developer.alation.com/dev/reference/createtoken). By using the Allie SDK library, you can manage and change many Alation resources programmatically. You can use this library to create your own custom applications.

This repository contains Python source code for the library and documentation showing how to use it. As of June 2024, Python versions 3.10 and up are supported.

Documentation on how to use the SDK can be found at: 
https://alation.github.io/Allie-SDK/

## Support
This is an **open source** project under the [APACHE 2.0 License](https://apache.org/licenses/LICENSE-2.0) and is maintained by everyone in the Alation community. If you encounter a problem or something is not working as expected, open a [GitHub issue](https://github.com/Alation/Allie-SDK/issues) on this repo and someone will get back to you. Please **DO NOT** create an Alation support case.

## License
[APACHE 2.0 License](https://apache.org/licenses/LICENSE-2.0)

## FastMCP server example

The repository ships an example Model Context Protocol server built with [FastMCP](https://github.com/jxnl/fastmcp). The server exposes every Allie SDK method as an MCP tool and authenticates incoming clients with an Alation refresh token.

1. Export the refresh token expected by the server and the credentials the tools should use when they instantiate the Allie SDK client:

   ```bash
   export ALLIE_SDK_EXPECTED_REFRESH_TOKEN="expected-refresh-token"
   export ALATION_HOST="https://your-alation.example.com"
   export ALATION_USER_ID="1"
   export ALATION_VALIDATE_SSL="1"
   ```

2. Start the server:

   ```bash
   python examples/fastmcp_server.py
   ```

3. Connect with the companion client example:

   ```bash
   export ALLIE_SDK_REFRESH_TOKEN="expected-refresh-token"
   python examples/fastmcp_client.py
   ```

The client connects via WebSocket, authenticates with the refresh token and triggers a tool call (``datasource.get_ocf_datasources`` in the example). Adjust the environment variables to match your Alation deployment.
