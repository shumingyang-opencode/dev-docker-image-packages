---
name: ddip-install
description: Install all skills from the dev-docker-image-packages repository. Use when the user says "install skills", "setup skills", "安裝技能", "安裝所有技能", or when running the repo for the first time.
compatibility: needs git
---

# ddip-install

Install all ddip skills from `dev-docker-image-packages/skills/` into `~/.agents/skills/`.

## Workflow

1. Locate the repository root (current directory should be `dev-docker-image-packages`)
   - If not inside the repo, ask the user to navigate there first

2. Run the installer:
   ```bash
   bash skills/install.sh
   ```

3. Confirm each skill was installed:
   ```
   [OK] ddip-image-create → ~/.agents/skills/ddip-image-create/
   [OK] ddip-image-list   → ~/.agents/skills/ddip-image-list/
   [OK] ddip-image-build  → ~/.agents/skills/ddip-image-build/
   [OK] ddip-install      → ~/.agents/skills/ddip-install/
   ```

4. Tell the user they can now use:
   - "加 image" / "create image" → create a new Docker image
   - "有哪些 image" / "list images" → list all available images
   - "build image" / "建置 image" → trigger GitHub Actions build
