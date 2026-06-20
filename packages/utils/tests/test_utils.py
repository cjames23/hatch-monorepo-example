import pytest

from acme_utils import parse_config, shout


def test_shout_reuses_core():
    assert shout("world") == "HELLO, WORLD!"


def test_parse_config_requires_yaml_feature():
    # acme-utils is installed with features=["yaml"] in the test environment.
    assert parse_config("name: acme\nversion: 1") == {"name": "acme", "version": 1}


def test_parse_config_rejects_non_mapping():
    with pytest.raises(ValueError):
        parse_config("- just\n- a list")
