import unittest

from prompts.enums import Capability, Command


class TestCapabilityEnum(unittest.TestCase):
    """Tests for the Capability enum."""

    def test_edit_capability_value(self):
        """Capability.EDIT should have the value 'edit'."""
        self.assertEqual(Capability.EDIT.value, "edit")


class TestCommandEnum(unittest.TestCase):
    """Tests for the Command enum and its capabilities mapping."""

    def test_command_values(self):
        """Command enum members should have the correct string values."""
        expected = {
            "DOCSTRINGS": "docstrings",
            "EXPLAIN": "explain",
            "FIX": "fix",
            "REFACTOR": "refactor",
            "TYPEHINTS": "typehints",
            "UNITTESTS": "unittests",
        }
        actual = {member.name: member.value for member in Command}
        self.assertDictEqual(actual, expected)

    def test_capabilities_mapping(self):
        """Each Command.capabilities property should match the defined mapping."""
        edit_commands = {
            Command.DOCSTRINGS,
            Command.FIX,
            Command.REFACTOR,
            Command.TYPEHINTS,
            Command.UNITTESTS,
        }
        for command in Command:
            caps = command.capabilities
            if command in edit_commands:
                self.assertIn(
                    Capability.EDIT,
                    caps,
                    f"{command.name} should include EDIT capability",
                )
            else:
                self.assertEqual(
                    caps, set(), f"{command.name} should have no capabilities"
                )

    def test_unique_values(self):
        """Enum values should be unique."""
        values = [member.value for member in Command]
        self.assertEqual(
            len(values),
            len(set(values)),
            "Command enum values should be unique",
        )


if __name__ == "__main__":
    unittest.main()
