---
title: Contribute
nav_order: 5
---

# Contribute
{:.no_toc}

This topic describes how to contribute to the Allie SDK project.

* TOC
{:toc}

## Setup

Before you can contribute to the Allie SDK project, you need to have the following installed:
 - Python 3.10+

Install package and dev dependencies:

```bash
uv sync
```

Run the test suite using:

```bash
uv run pytest tests
# python -m pytest
```

## Get the source code and set up a branch

## Code and commit

### How methods should be structured

Methods should either return nothing or the respective result. There are at least two types of results:

- The records returned by a successful GET call.
- Job details returned by async POST, PUT and DELETE calls. 

If you are writing a method for an Alation API async endpoint, make sure you return the job details and map them to a data class, which are defined in `models/job_model.py`. The structure of the returned job details is not completely standardised (especially the nested elements), so if required, create dedicated data classes (if none for your use case exists already). Also make sure that if any details about created or updated objects are returned by the Alation API endpoint (e.g. id and name), that these details are made available via the data class(es) that represent the job details.

> **Note**: An Alation endpoint is considered *async* if it returns a job ID or job name.


### Use Pyrefly for type checking

Either via the command line. Example of a selective check:

```
uvx pyrefly check --summarize-errors allie_sdk/methods/alation_ai_data_product.py
```

Or configure your IDE to use pyrefly for type checking:

| IDE | Setup |
|---|---|
| **PyCharm** | Open **Settings → Python → Type Engine** and select **Pyrefly**, or click the **Types: Built-in** status bar widget and choose **Install and Use Pyrefly**. |
| **VS Code** | Install the **Pyrefly** extension and open a Python file. It discovers your project configuration automatically. |

These steps are documented by [JetBrains](https://www.jetbrains.com/help/pycharm/python-type-engine.html) and [Pyrefly](https://pyrefly.org/en/docs/IDE/). [PyCharm Documentation](https://www.jetbrains.com/help/pycharm/python-type-engine.html?utm_source=chatgpt.com)

## Add tests

## Update documentation

Whenever you update existing functionality or add a new feature, you must update the documentation along with your code.

All of the documentation source files can be found in the `/docs` folder on the main branch. Our documentation is written in Markdown (specifically [kramdown](https://kramdown.gettalong.org/quickref.html)) and built with Jekyll on GitHub Pages. The docs are built automatically anytime a change is made to the main branch.

We use the [Just the Docs](https://github.com/just-the-docs/just-the-docs) theme. Use the [Just the Docs documentation](https://just-the-docs.com/) for help with formatting, layout, and customization features.

If you are just making documentation updates (adding new docs, fixing typos, improving wording) the easiest method is to use the built-in **Edit this file** feature (the pencil icon) or the **Edit this page** link.

To make more significant changes, create a pull request against the main branch.

## Commit changes and open a pull request
