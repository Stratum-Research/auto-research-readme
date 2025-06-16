import pytest
from unittest.mock import patch, mock_open, MagicMock
from auto_readme.integration.release import release


def test_release_calls_changelog_update_on_new_tag():
    # Simulate config.yaml with a new version and changelog
    config_content = """
version: "1.2.3"
changelog:
  "1.2.3":
    - Added new feature
    """
    with (
        patch("builtins.open", mock_open(read_data=config_content)),
        patch("subprocess.check_output", return_value="v1.2.2\n"),
        patch("subprocess.run", return_value=MagicMock(stdout="")),
        patch(
            "auto_readme.integration.release.changelog.update_changelog"
        ) as mock_update_changelog,
        patch("pathlib.Path.exists", return_value=True),
    ):
        # Ignore SystemExit for this test
        try:
            release.main()
        except SystemExit:
            pass
        # Assert changelog was updated
        mock_update_changelog.assert_called_once()


def test_release_exits_if_tag_exists():
    config_content = """
version: "1.2.3"
changelog:
  "1.2.3":
    - Added new feature
    """
    with (
        patch("builtins.open", mock_open(read_data=config_content)),
        patch("subprocess.check_output", return_value="v1.2.3\n"),
        patch("subprocess.run", return_value=MagicMock(stdout="")),
        patch(
            "auto_readme.integration.release.changelog.update_changelog"
        ) as mock_update_changelog,
        patch("pathlib.Path.exists", return_value=True),
    ):
        with pytest.raises(SystemExit) as excinfo:
            release.main()
        assert excinfo.value.code == 0
        mock_update_changelog.assert_not_called()
