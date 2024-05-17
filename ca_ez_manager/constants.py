import os
from enum import Enum

# TODO: allow custom directory
home = os.path.expanduser("~")
ca_folder = os.path.join(home, ".ca")


class ActionType(str, Enum):
    CA_CREATE = "CA_CREATE"
    CERT_GENERATE = "CERT_GENERATE"
