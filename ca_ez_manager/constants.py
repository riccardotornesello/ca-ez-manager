from enum import Enum


class ActionType(str, Enum):
    CA_CREATE = "CA_CREATE"
    CERT_GENERATE = "CERT_GENERATE"
