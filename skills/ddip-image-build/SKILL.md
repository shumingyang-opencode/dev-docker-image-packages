---
name: ddip-image-build
description: Trigger a remote GitHub Actions build for a Docker image in dev-docker-image-packages. Lists available images, lets the user choose, then runs `gh workflow run`. Use when the user says "build image", "建置 image", "更新 image", "build", "release image", "push image".
compatibility: needs gh (GitHub CLI)
---

# ddip-image-build

Trigger a remote GitHub Actions build for one or all Docker images.

## Workflow

1. Verify we are in the `dev-docker-image-packages` repository

2. Scan `images/*/` to list available images (same display as `ddip-image-list`)

3. Ask the user which image to build:
   - Show the list with numbers
   - Option for "all" (build everything)
   - Or let them type the image name directly

4. Trigger GitHub Actions:
   ```bash
   gh workflow run build-image.yml \
     -f image=<name> \
     --repo shumingyang-opencode/dev-docker-image-packages
   ```
   For all:
   ```bash
   gh workflow run build-image.yml \
     -f image=all \
     --repo shumingyang-opencode/dev-docker-image-packages
   ```

5. Show the workflow run URL:
   ```
   [OK] Build started for python
   → https://github.com/shumingyang-opencode/dev-docker-image-packages/actions/runs/<id>
   ```

## Notes

- The workflow reads `LABEL org.opencontainers.image.version` from each Dockerfile and tags images accordingly.
- Both `:<version>` and `:latest` tags are pushed to GHCR.
- Build happens on GitHub's infrastructure; images appear at `ghcr.io/shumingyang-opencode/<name>`.
