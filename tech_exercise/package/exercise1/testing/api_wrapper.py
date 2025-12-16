from dataclasses import dataclass
from datetime import datetime
import requests

BASE_URL = "http://localhost:8080"

def healthcheck() -> bool:
    req = requests.get(f"{BASE_URL}/healthcheck")
    return req.status_code == 200

def create_person(name: str) -> requests.Response:
    return requests.post(f"{BASE_URL}/person", json=name)

def get_people() -> requests.Response:
    return requests.get(f"{BASE_URL}/person")

def get_person_by_name(name: str) -> requests.Response:
    return requests.get(f"{BASE_URL}/person/{name}")

def get_astronaut_duties_by_name(name: str) -> requests.Response:
    return requests.get(f"{BASE_URL}/astronautduty/{name}")

@dataclass
class CreateAstronautDutyRequest:
    name: str
    rank: str
    duty: str
    duty_start_date: datetime

def create_astronaut_duty(request: CreateAstronautDutyRequest) -> requests.Response:
    json_payload = {
        "name": request.name,
        "rank": request.rank,
        "dutyTitle": request.duty,
        "dutyStartDate": request.duty_start_date.isoformat()
    }
    return requests.post(f"{BASE_URL}/astronautduty", json=json_payload)

