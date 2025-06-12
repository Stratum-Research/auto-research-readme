"""
Base integration class for auto-research-readme integrations.

This module defines the abstract base class that all integrations must inherit from,
providing a consistent interface for integration discovery and setup.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List

ConfigDict = Dict[str, Any]


class BaseIntegration(ABC):
    """
    Base class for all integrations.

    Each integration represents a service or platform that can be automatically
    configured for a research project (e.g., GitHub Actions, Zenodo metadata, PyPI).
    """

    @abstractmethod
    def is_applicable(self, config: ConfigDict) -> bool:
        """
        Check if this integration should be enabled for the current project.

        Args:
            config: Project configuration dictionary.

        Returns:
            True if integration should be set up, False otherwise.
        """
        pass

    @abstractmethod
    def setup(self, config: ConfigDict) -> str:
        """
        Set up the integration (create files, configurations, etc.).

        Args:
            config: Project configuration dictionary.

        Returns:
            Description of what was set up.

        Raises:
            Exception: If setup fails.
        """
        pass

    @abstractmethod
    def get_requirements(self) -> List[str]:
        """
        Get list of manual steps user needs to complete after setup.

        Returns:
            List of instruction strings for the user.
        """
        pass

    @property
    def name(self) -> str:
        """Get the integration name (class name without 'Integration' suffix)."""
        return self.__class__.__name__.replace("Integration", "")

    def __str__(self) -> str:
        """String representation of the integration."""
        return f"{self.name} Integration"
