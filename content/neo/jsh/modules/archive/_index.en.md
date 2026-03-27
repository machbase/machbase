---
title: "archive"
type: docs
weight: 100
---

The archive module group provides TAR and ZIP utilities for JSH applications.

Both submodules support:

- in-memory archive creation and extraction
- callback-style asynchronous wrappers
- stream-style writer and reader objects
- file-based archive classes for reading and writing `.tar` and `.zip` files

Use `archive/tar` when you need a TAR archive, directory entries, or TAR link metadata.
Use `archive/zip` when you need a ZIP archive that works directly with common ZIP tools.

{{< children_toc />}}
