import os
import shutil
from typing import List

from ca_ez_manager.utils.crypto import (
    save_private_key,
    save_certificate,
    save_csr,
    load_private_key,
    load_certificate,
)


# TODO: allow custom directory
user_home = os.path.expanduser("~")
ca_root_folder = os.path.join(user_home, ".ca")

NECESSARY_CA_FILES = ["ca.key", "ca.pem"]
NECESSARY_CERT_FILES = ["cert.key", "cert.pem", "cert.csr"]


def init_storage():
    if not os.path.exists(ca_root_folder):
        os.makedirs(ca_root_folder)


def get_ca_list() -> List[str]:
    init_storage()

    # Get the list of subdirectories in the CA folder
    subdirs = os.listdir(ca_root_folder)

    # Filter out only the directories
    subdirs = [d for d in subdirs if os.path.isdir(f"{ca_root_folder}/{d}")]

    # Return only the directories that contain the necessary files
    return [d for d in subdirs if all(os.path.exists(f"{ca_root_folder}/{d}/{fn}") for fn in NECESSARY_CA_FILES)]


def store_ca(ca_name: str, private_key, cert):
    selected_ca_folder = f"{ca_root_folder}/{ca_name}"

    if os.path.exists(selected_ca_folder):
        raise FileExistsError(f"CA {ca_name} already exists")

    os.makedirs(selected_ca_folder)

    save_private_key(private_key, f"{ca_root_folder}/{ca_name}/ca.key")
    save_certificate(cert, f"{ca_root_folder}/{ca_name}/ca.pem")


def get_ca(ca_name: str):
    selected_ca_folder = f"{ca_root_folder}/{ca_name}"

    for fn in NECESSARY_CA_FILES:
        if not os.path.exists(f"{selected_ca_folder}/{fn}"):
            raise FileNotFoundError(f"CA {ca_name} not found")

    private_key = load_private_key(f"{selected_ca_folder}/ca.key")
    cert = load_certificate(f"{selected_ca_folder}/ca.pem")

    return private_key, cert


def store_cert(ca_name: str, cert_name: str, private_key, cert, csr):
    selected_ca_folder = f"{ca_root_folder}/{ca_name}"
    cert_folder = f"{selected_ca_folder}/{cert_name}"

    if os.path.exists(cert_folder):
        raise FileExistsError(f"Certificate {cert_name} already exists")

    os.makedirs(cert_folder)

    save_private_key(private_key, f"{cert_folder}/{cert_name}.key")
    save_certificate(cert, f"{cert_folder}/{cert_name}.pem")
    save_csr(csr, f"{cert_folder}/{cert_name}.csr")


def get_certs_list(ca_name: str):
    selected_ca_folder = f"{ca_root_folder}/{ca_name}"

    if not os.path.exists(selected_ca_folder):
        raise FileNotFoundError(f"CA {ca_name} not found")

    # Get the list of subdirectories in the CA folder
    subdirs = os.listdir(selected_ca_folder)

    # Filter out only the directories
    subdirs = [d for d in subdirs if os.path.isdir(f"{selected_ca_folder}/{d}")]

    # Return only the directories that contain the necessary files
    return [d for d in subdirs if all(os.path.exists(f"{selected_ca_folder}/{d}/{fn}") for fn in NECESSARY_CERT_FILES)]


def delete_ca(ca_name: str):
    selected_ca_folder = f"{ca_root_folder}/{ca_name}"

    if not os.path.exists(selected_ca_folder):
        raise FileNotFoundError(f"CA {ca_name} not found")

    shutil.rmtree(selected_ca_folder)
