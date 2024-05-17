from enum import Enum


class ActionType(str, Enum):
    CA_CREATE = "CA_CREATE"
    CA_DELETE = "CA_DELETE"
    CERT_GENERATE = "CERT_GENERATE"
