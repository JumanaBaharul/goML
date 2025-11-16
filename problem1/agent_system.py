"""Multi-agent airline flight information system.

This module implements the Info Agent and QA Agent described in the
specification. It simulates a function-calling workflow by exposing
functions that other modules or tests can import.
"""
from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Dict, Optional


@dataclass(frozen=True)
class FlightRecord:
    """Represents the structured information available for a flight."""

    flight_number: str
    departure_time: str
    destination: str
    status: str

    def to_dict(self) -> Dict[str, str]:
        """Return the record as a plain dictionary."""

        return {
            "flight_number": self.flight_number,
            "departure_time": self.departure_time,
            "destination": self.destination,
            "status": self.status,
        }


# Mock in-memory database for Info Agent.
_FLIGHT_DATABASE: Dict[str, FlightRecord] = {
    "AI123": FlightRecord(
        flight_number="AI123",
        departure_time="08:00 AM",
        destination="Delhi",
        status="Delayed",
    ),
    "AI456": FlightRecord(
        flight_number="AI456",
        departure_time="11:30 AM",
        destination="Mumbai",
        status="On Time",
    ),
    "AI789": FlightRecord(
        flight_number="AI789",
        departure_time="05:45 PM",
        destination="Bengaluru",
        status="Boarding",
    ),
}


def get_flight_info(flight_number: str) -> Dict[str, str]:
    """Return structured flight information.

    Args:
        flight_number: Identifier extracted from the user's query.

    Returns:
        A dictionary with flight metadata or an error message.
    """

    normalized = (flight_number or "").strip().upper()
    record = _FLIGHT_DATABASE.get(normalized)
    if record:
        return record.to_dict()
    return {
        "flight_number": normalized,
        "error": f"Flight {normalized} not found in database.",
    }


def info_agent_request(flight_number: str) -> str:
    """Simulate the Info Agent's JSON-only response."""

    info = get_flight_info(flight_number)
    return json.dumps(info, ensure_ascii=False)


_FLIGHT_PATTERN = re.compile(r"flight\s*([A-Za-z0-9]+)", re.IGNORECASE)


def _extract_flight_number(user_query: str) -> Optional[str]:
    """Extract the flight number token from a query."""

    if not user_query:
        return None
    match = _FLIGHT_PATTERN.search(user_query)
    if not match:
        return None
    return match.group(1).upper()


def qa_agent_respond(user_query: str) -> str:
    """Return an answer in JSON format based on the user's question."""

    flight_number = _extract_flight_number(user_query)
    if not flight_number:
        return json.dumps({"answer": "Flight number not found in query."})

    info_json = info_agent_request(flight_number)
    info = json.loads(info_json)

    if "error" in info:
        return json.dumps({"answer": info["error"]})

    answer = (
        f"Flight {info['flight_number']} departs at {info['departure_time']} "
        f"to {info['destination']}. Current status: {info['status']}."
    )
    return json.dumps({"answer": answer}, ensure_ascii=False)


if __name__ == "__main__":
    sample_questions = [
        "When does Flight AI123 depart?",
        "What is the status of Flight AI999?",
        "Tell me about flight ai456",
        "What's up?",  # missing flight number
    ]

    for question in sample_questions:
        print(qa_agent_respond(question))
