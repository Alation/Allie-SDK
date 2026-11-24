---
title: Versions
nav_order: 3
---

# Versions
{:.no_toc}

## Python compatibility

Starting with Allie SDK 3.0.0, Python 3.12 is the minimum supported version. This release drops support for Python 3.10 and 3.11. Users of those Python versions can install an earlier SDK release with `pip install "allie-sdk<3"`.

## Alation compatibility

Because the Allie SDK is a client for the Alation REST APIs, you need to make sure the version of Allie SDK you're using is compatible with the version of the Alation that you're using. The Alation REST APIs are versioned and tied directly to the version of the Alation application that you have. To determine what version of the Alation APIs you're using, see [Finding Your Alation Version](https://developer.alation.com/dev/docs/finding-my-alation-version). You can also see what API features are supported for each version by visiting the [Alation developer portal](https://developer.alation.com/dev) and selecting an Alation version. 

Currently, Allie SDK release versions are being tracked via [GitHub releases](https://github.com/Alation/Allie-SDK/releases) and we are working on a way to tie the Allie SDK versions with Alation versions to determine compatibility. More to come on this.
