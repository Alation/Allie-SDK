---
title: Logging
nav_order: 8
---

# Logging
{:.no_toc}

The Allie SDK uses Python's built-in [logging module](https://docs.python.org/3/library/logging.html) to log messages. By default, the SDK logs messages to the console.

You can configure the logging behavior by setting the `ALLIE_SDK_LOG_LEVEL` and `ALLIE_SDK_LOG_HANDLERS` environment variables. The following log handlers can be enabled:

* `console_for_allie`: Logs messages to the console. This is the default handler.
* `file_for_allie`: Logs messages to a file named `allie-sdk-<date>.log` in the `logs` directory.
* `api_json`: Logs API request and response details to a file named `alation-rest-<date>.json` in the `logs` directory.

The handlers can be specified as a comma-separated list. For example, to enable both console and file logging, set the environment variable as follows:

```bash
export ALATION_SDK_LOG_HANDLERS="console_for_allie,file_for_allie"
```