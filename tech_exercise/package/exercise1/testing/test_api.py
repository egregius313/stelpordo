import string

import pytest
import hypothesis.strategies as st
from hypothesis import given, assume as hypot_assume

from .api_wrapper import BASE_URL, create_person, get_person_by_name

BASE_URL = "http://localhost:3405"

def usernames():
    return st.text(alphabet=string.ascii_letters, min_size=1, max_size=20).filter(lambda s: s.isalpha())

@given(name=usernames())
def test_create_person_success(name):
    response = create_person(name)
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data.get("success") == True
    assert data.get("responseCode") == 200

@given(name=usernames())
def test_create_same_person_twice(name):
    exists_response = get_person_by_name(name)
    hypot_assume(exists_response.status_code == 500)

    response1 = create_person(name)
    assert response1.status_code == 200

    response2 = create_person(name)
    assert response2.status_code == 500
