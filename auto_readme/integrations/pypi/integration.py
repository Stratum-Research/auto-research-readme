"""
PyPI integration for auto-research-readme.

This integration creates GitHub Actions workflows for automated PyPI publishing
when Python packages are detected in the project configuration.
"""

from pathlib import Path
from typing import List

from jinja2 import Environment, FileSystemLoader

from ..base import BaseIntegration, ConfigDict


class PyPIIntegration(BaseIntegration):
    """
    PyPI publishing integration for Python packages.

    This integration creates GitHub Actions workflows for automated
    publishing to PyPI using trusted publishing (OIDC).

    Only applicable for Python packages (type: "python-package").
    """

    def is_applicable(self, config: ConfigDict) -> bool:
        """
        Check if PyPI integration should be enabled.

        Args:
            config: Project configuration dictionary.

        Returns:
            True if project type is 'python-package'.
        """
        project_type = config.get("type", "").lower()
        is_python_package = project_type == "python-package"

        return is_python_package

    def setup(self, config: ConfigDict) -> str:
        """
        Set up PyPI publishing workflow.

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
                title=config.get("title", "Python Package"),
                maintainer=config.get("maintainer", ""),
                package_name=self._get_package_name(config),
            )

            # Write workflow file
            workflow_file = workflows_dir / "pypi-publish.yml"
            workflow_file.write_text(workflow_content, encoding="utf-8")

            return f"Created PyPI publishing workflow at {workflow_file}"

        except Exception as e:
            raise Exception(f"Failed to create PyPI workflow: {e}")

    def get_requirements(self) -> List[str]:
        """
        Get manual steps for PyPI integration.

        Returns:
            List of instructions for the user.
        """
        return [
            "Register your package name on PyPI: https://pypi.org/",
            "Set up trusted publishing in PyPI project settings",
            "Link your GitHub repository to PyPI trusted publishing",
            "Create releases with version tags to trigger automatic publishing",
            "Ensure your pyproject.toml or setup.py is properly configured",
        ]

    def _get_package_name(self, config: ConfigDict) -> str:
        """
        Extract package name from config or title.

        Args:
            config: Project configuration dictionary.

        Returns:
            Package name suitable for PyPI.
        """
        # Use explicit package name if provided
        if config.get("package_name"):
            return config["package_name"]

        # Fall back to title, converting to PyPI-friendly format
        title = config.get("title", "my-package")
        return title.lower().replace("_", "-")
