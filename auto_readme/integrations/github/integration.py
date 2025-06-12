"""
GitHub integration for auto-research-readme.

This integration sets up GitHub Actions workflows for automated releases
and documentation updates when git repositories are detected.
"""

from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from ..base import BaseIntegration, ConfigDict


class GitHubIntegration(BaseIntegration):
    """
    GitHub Actions integration for automated repository workflows.

    This integration creates GitHub Actions workflows for:
    - Automated releases on version tags
    - Documentation updates
    - Repository maintenance

    Applicable when a git repository is detected in the project.
    """

    def is_applicable(self, config: ConfigDict) -> bool:
        """
        Check if GitHub integration should be enabled.

        Args:
            config: Project configuration dictionary.

        Returns:
            True if .git directory exists or github_link is specified.
        """
        # Check if we're in a git repository
        git_dir = Path(".git")
        has_git = git_dir.exists()

        # Check if GitHub link is specified in config
        has_github_link = bool(config.get("github_link"))

        return has_git or has_github_link

    def setup(self, config: ConfigDict) -> str:
        """
        Set up GitHub Actions workflow files.

        Args:
            config: Project configuration dictionary.

        Returns:
            Description of what was set up.

        Raises:
            Exception: If workflow file creation fails.
        """
        try:
            # Create .github/workflows directory
            workflows_dir = Path(".github/workflows")
            workflows_dir.mkdir(parents=True, exist_ok=True)

            # Load and render workflow template
            template_dir = Path(__file__).parent
            env = Environment(loader=FileSystemLoader(str(template_dir)))
            template = env.get_template("workflow.yml.j2")

            workflow_content = template.render(
                title=config.get("title", "Repository"),
                github_link=config.get("github_link", ""),
                maintainer=config.get("maintainer", ""),
            )

            # Write workflow file
            workflow_file = workflows_dir / "release.yml"
            workflow_file.write_text(workflow_content, encoding="utf-8")

            return f"Created GitHub Actions workflow at {workflow_file}"

        except Exception as e:
            raise Exception(f"Failed to create GitHub workflow: {e}")

    def get_requirements(self) -> List[str]:
        """
        Get manual steps for GitHub integration.

        Returns:
            List of instructions for the user.
        """
        return [
            "Push this repository to GitHub",
            "Ensure GitHub Actions are enabled in repository settings",
            "Create releases by pushing git tags (e.g., 'git tag v1.0.0 && git push origin v1.0.0')",
        ]
