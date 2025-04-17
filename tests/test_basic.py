import pytest

from ..src.tasks import generate_unique_id


def test_generate_unique_id_empty():
    assert generate_unique_id([]), 1
