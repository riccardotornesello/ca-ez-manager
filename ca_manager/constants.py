import os
from enum import Enum

# TODO: allow custom directory
home = os.path.expanduser("~")
ca_folder = os.path.join(home, ".ca")


class ActionType(str, Enum):
    CREATE_CA = "CREATE_CA"
    GENERATE_CERTIFICATE = "GENERATE_CERTIFICATE"
