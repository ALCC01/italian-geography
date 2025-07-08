#!/usr/bin/env python3

import os
import json

CWD_DIR = os.path.abspath(os.path.dirname(__file__))
BUILDINFO_PATH = os.path.join(CWD_DIR, "../build/buildinfo.json")
README_TEMPLATE_PATH = os.path.join(CWD_DIR, "../templates/README.template.md")

if __name__ == "__main__":
    if not os.path.exists(BUILDINFO_PATH):
        print(f"Build info file not found at {BUILDINFO_PATH}")
        exit(1)

    with open(BUILDINFO_PATH, "r") as file:
        buildinfo = json.load(file)

    if not os.path.exists(README_TEMPLATE_PATH):
        print(f"README template not found at {README_TEMPLATE_PATH}")
        exit(1)

    with open(README_TEMPLATE_PATH, "r") as file:
        readme_template = file.read()

    readme_content = readme_template.format(**buildinfo)

    print(readme_content)
