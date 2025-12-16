import datetime
import string

import pytest
import hypothesis.strategies as st
from hypothesis import given, assume as hypot_assume

from .api_wrapper import BASE_URL, create_person, get_person_by_name, CreateAstronautDutyRequest, create_astronaut_duty, healthcheck

BASE_URL = "http://localhost:3405"

def first_names() -> st.SearchStrategy[str]:
    return st.sampled_from([
        "Alice", "Bob", "Charlie", "Diana", "Ethan",
        "Fiona", "George", "Hannah", "Ian", "Julia",
        "Kevin", "Laura", "Michael", "Nina", "Oliver",
        "Paula", "Quentin", "Rachel", "Sam", "Tina",
        "Uma", "Victor", "Wendy", "Xander", "Yvonne", "Zach",
        "Alexander", "Benjamin", "Charlotte", "Daniel", "Evelyn",
        "Frederick", "Gabriella", "Harold", "Isabella",
        "Jonathan", "Katherine", "Leonardo", "Madeline", "Nathaniel",
        "Olivia", "Penelope", "Quincy", "Rebecca", "Sebastian",
        "Theodore", "Ulysses", "Valentina", "William", "Xavier",
        "Yosef", "Zoe"
    ])

def last_names() -> st.SearchStrategy[str]:
    return st.sampled_from([
        "Anderson", "Brown", "Clark", "Davis", "Evans",
        "Garcia", "Harris", "Johnson", "King", "Lee",
        "Martinez", "Nelson", "O'Connor", "Perez", "Roberts",
        "Smith", "Taylor", "Upton", "Vasquez", "White",
        "Young", "Zimmerman",
        "Adams", "Baker", "Carter", "Diaz", "Edwards",
        "Foster", "Gonzalez", "Hill", "Ingram", "Jackson",
        "Kim", "Lopez", "Moore", "Nguyen", "Ortiz",
        "Patel", "Quinn", "Ramirez", "Sanchez", "Turner",
        "Underwood", "Vargas", "Walker", "Xu", "Yang", "Zhang"
    ])

def usernames():
    # return st.text(alphabet=string.ascii_letters, min_size=1, max_size=20)
    return st.builds(lambda first, last: f"{first} {last}", first=first_names(), last=last_names())

@st.composite
def unique_usernames(draw):
    seen_this_test = draw(st.shared(st.builds(set), key="seen_usernames"))
    while (name := draw(usernames())) in seen_this_test:
        continue
    seen_this_test.add(name)
    return name


def ranks():
    return st.sampled_from(["Commander", "Lieutenant", "Captain", "Major", "Colonel"])    


def user_exists(name: str) -> bool:
    response = get_person_by_name(name)
    return response.status_code == 200

def create_if_not_exists(name: str):
    exists = get_person_by_name(name)
    if exists.status_code == 404:
        create_response = create_person(name)
        assert create_response.status_code == 200
        exists = get_person_by_name(name)
    return exists.status_code == 200

@given(name=unique_usernames())
def test_create_person_success(name):
    exists_response = get_person_by_name(name)
    hypot_assume(exists_response.status_code == 404)

    response = create_person(name)
    assert response.status_code == 200
    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data.get("success") == True
    assert data.get("responseCode") == 200

@given(name=unique_usernames())
def test_create_same_person_twice(name):
    exists_response = get_person_by_name(name)
    hypot_assume(exists_response.status_code == 404)

    response1 = create_person(name)
    assert response1.status_code == 200

    response2 = create_person(name)
    assert response2.status_code == 409

def test_create_astronaut_duty_success():
    name = "TestAstronaut"

    assert create_if_not_exists(name)

    rank = "Commander"
    duty = "Explore Mars"
    duty_start_date = datetime.datetime(2030, 1, 1)

    request = CreateAstronautDutyRequest(
        name=name,
        rank=rank,
        duty=duty,
        duty_start_date=duty_start_date
    )

    response = create_astronaut_duty(request)
    assert response.status_code == 200, response.text
    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data.get("success") == True
    assert data.get("responseCode") == 200

@given(name=unique_usernames())
def test_create_astronaut_duty_person_not_found(name):
    hypot_assume(not user_exists(name))
    create_person(name)
    rank = "Lieutenant"
    duty = "Test Duty"
    duty_start_date = datetime.datetime(2025, 5, 15)

    request = CreateAstronautDutyRequest(
        name=name,
        rank=rank,
        duty=duty,
        duty_start_date=duty_start_date
    )

    response = create_astronaut_duty(request)
    assert response.status_code == 400

@given(name=unique_usernames(), when=st.datetimes(), rank=ranks())
def test_retirement(name, when, rank):
    create_if_not_exists(name)
    hypot_assume(user_exists(name))

    duty = "RETIRED"
    request = CreateAstronautDutyRequest(
        name=name,
        rank=rank,
        duty=duty,
        duty_start_date=when
    )

    response = create_astronaut_duty(request)
    assert response.status_code == 200, response.text

    day_before_retirement = when.date() - datetime.timedelta(days=1)

    data = response.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data.get("success") == True
    assert data.get("responseCode") == 200

    person = get_person_by_name(name)
    hypot_assume(person.status_code == 200)
    try:
        data = person.json()
        assert "person" in data
        person_data = data.get("person")
    except Exception:
        pytest.fail("Response JSON is not in expected format")
    try:
        career_end_date = datetime.datetime.fromisoformat(person_data.get("careerEndDate"))
    except Exception:
        pytest.fail("careerEndDate is not a valid ISO format datetime")
    career_end_day = career_end_date.date()
    assert career_end_day == day_before_retirement