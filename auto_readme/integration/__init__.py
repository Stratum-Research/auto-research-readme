"""
Automation integrations for auto-research-readme.

This module provides integration classes for various services (GitHub, Zenodo, PyPI)
that can automatically set up workflows and metadata files for research projects.

The integration system uses a plugin-based architecture where each integration
is auto-discovered and applied based on the project configuration.
"""

from typing import Any, Dict, List

from .platforms.github.integration import GitHubIntegration
from .platforms.pypi.integration import PyPIIntegration
from .platforms.zenodo.integration import ZenodoIntegration

ConfigDict = Dict[str, Any]

# Available integrations
INTEGRATIONS = [
    GitHubIntegration,
    ZenodoIntegration,
    PyPIIntegration,
]


def setup_all_integrations(config: ConfigDict) -> List[str]:
    """
    Set up all applicable integrations for the project.

    Args:
        config: Project configuration dictionary.

    Returns:
        List of integration names that were successfully set up.

    Raises:
        Exception: If any integration setup fails.
    """
    applied_integrations = []

    for integration_class in INTEGRATIONS:
        integration = integration_class()

        if integration.is_applicable(config):
            print(f"📦 Setting up {integration.name} integration...")

            try:
                integration.setup(config)
                applied_integrations.append(integration.name)
                print(f"✓ {integration.name} integration configured")

                # Print requirements if any
                requirements = integration.get_requirements()
                if requirements:
                    print(f"ℹ️  {integration.name} requirements:")
                    for req in requirements:
                        print(f"   • {req}")

            except Exception as e:
                print(f"❌ Failed to setup {integration.name}: {e}")
                raise

    if applied_integrations:
        count = len(applied_integrations)
        print(f"\n🎉 Successfully configured {count} integrations!")
        return applied_integrations
    else:
        print("ℹ️  No integrations were applicable for this project")
        return []


__all__ = [
    "setup_all_integrations",
    "GitHubIntegration",
    "ZenodoIntegration",
    "PyPIIntegration",
    "INTEGRATIONS",
]
