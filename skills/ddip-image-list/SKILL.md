---
name: ddip-image-list
description: List all Docker images available in the dev-docker-image-packages repository. Shows name, version, pre-installed tools, and suggested use cases. Use when the user says "有哪些 image", "list images", "show images", "列出 image", "what images", "可用 image".
---

# ddip-image-list

List all Docker images in `images/` with details.

## Workflow

1. Verify we are in the `dev-docker-image-packages` repository
   - Check that `images/` directory exists

2. Scan `images/*/` and for each:
   - Read `Dockerfile` to extract:
     - `LABEL org.opencontainers.image.version` → version
     - `FROM` → base image
     - `pip install` lines → Python tools
     - `npm install -g` lines → AI CLI tools
     - `apt-get install` lines → system packages
   - Read `README.md` (first paragraph) → description

3. Render result as a formatted markdown table:
   ```
   | Image | Version | Base | Tools | Purpose |
   |-------|---------|------|-------|---------|
   | python | 1.0.0 | python:3.13-slim | poetry, ruff, mypy, pytest | Python dev base |
   ```

4. Append instructions:
   ```
   Say "build image <name>" to trigger remote build.
   Say "create image" to add a new one.
   ```
