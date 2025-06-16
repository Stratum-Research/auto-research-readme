import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Please install with 'pip install pyyaml'.")
    sys.exit(1)


def get_changelog_from_config(config_path="config.yaml"):
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Config file {config_path} not found.")
        sys.exit(1)
    with open(config_file) as f:
        config = yaml.safe_load(f)
    version = config.get("version")
    changelog = config.get("changelog", {})
    changes = changelog.get(str(version), [])
    return version, changes


def append_to_changelog_md(version, changes, changelog_path="CHANGELOG.md"):
    changelog_file = Path(changelog_path)
    entry_header = f"## [{version}]"
    entry = f"{entry_header}\n"
    for change in changes:
        entry += f"- {change}\n"
    entry += "\n"
    # If file doesn't exist, create it
    if not changelog_file.exists():
        changelog_file.write_text(entry, encoding="utf-8")
        print(f"Created {changelog_path} with entry for version {version}.")
        return
    # If entry already exists, do nothing
    with open(changelog_file, "r", encoding="utf-8") as f:
        content = f.read()
        if entry_header in content:
            print(f"CHANGELOG.md already contains entry for version {version}.")
            return
    # Otherwise, prepend the new entry
    new_content = entry + content
    changelog_file.write_text(new_content, encoding="utf-8")
    print(f"Appended entry for version {version} to {changelog_path}.")


def update_changelog(config_path="config.yaml", changelog_path="CHANGELOG.md"):
    version, changes = get_changelog_from_config(config_path)
    if not changes:
        print(f"No changelog entry found for version {version} in {config_path}.")
        return
    append_to_changelog_md(version, changes, changelog_path)


if __name__ == "__main__":
    update_changelog()
