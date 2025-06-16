import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML is required. Please install with 'pip install pyyaml'.")
    sys.exit(1)


def get_version_from_config(config_path="config.yaml"):
    config_file = Path(config_path)
    if not config_file.exists():
        print(f"Config file {config_path} not found.")
        sys.exit(1)
    with open(config_file) as f:
        config = yaml.safe_load(f)
    version = config.get("version")
    if not version:
        print("No 'version' field found in config.yaml.")
        sys.exit(1)
    return version


def tag_exists(tag):
    tags = subprocess.check_output(["git", "tag"], text=True).splitlines()
    return tag in tags


def main():
    version = get_version_from_config()
    tag = f"v{version}"
    if tag_exists(tag):
        print(f"Tag {tag} already exists. No new release created.")
        sys.exit(0)
    # Ensure config.yaml is committed
    result = subprocess.run(
        ["git", "status", "--porcelain", "config.yaml"], capture_output=True, text=True
    )
    if result.stdout.strip():
        print(
            "config.yaml has uncommitted changes. Please commit them before releasing."
        )
        sys.exit(1)
    # Create and push the tag
    subprocess.run(["git", "tag", tag], check=True)
    subprocess.run(["git", "push", "origin", tag], check=True)
    print(f"Created and pushed tag {tag}. All release automations will now run.")

    # Update CHANGELOG.md from config.yaml
    try:
        from auto_readme.integration.release import changelog

        changelog.update_changelog()
    except Exception as e:
        print(f"Warning: Could not update CHANGELOG.md automatically: {e}")


if __name__ == "__main__":
    main()
