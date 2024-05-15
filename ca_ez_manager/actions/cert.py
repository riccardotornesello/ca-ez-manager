import os

from InquirerPy import prompt

from ca_ez_manager.crypto_utils import (
    sign_certificate,
    load_private_key,
    load_certificate,
    save_csr,
    save_private_key,
    save_certificate,
)
from ca_ez_manager.constants import ca_folder


def generate_cert(ca_list):
    answers = prompt(
        [
            {
                "type": "list",
                "message": "Select a CA:",
                "choices": ca_list,
                "name": "ca_name",
            },
            {
                "name": "common_name",
                "message": "Common Name:",
                "type": "input",
            },
        ]
    )

    # TODO: check if name already in use

    ca_private_key = load_private_key(f"{ca_folder}/{answers['ca_name']}/ca.key")
    ca_cert = load_certificate(f"{ca_folder}/{answers['ca_name']}/ca.pem")

    private_key, csr, cert = sign_certificate(ca_private_key, ca_cert)

    os.makedirs(
        f"{ca_folder}/{answers['ca_name']}/{answers['common_name']}", exist_ok=True
    )

    save_private_key(
        private_key,
        f"{ca_folder}/{answers['ca_name']}/{answers['common_name']}/{answers['common_name']}.key",
    )
    save_certificate(
        cert,
        f"{ca_folder}/{answers['ca_name']}/{answers['common_name']}/{answers['common_name']}.pem",
    )
    save_csr(
        csr,
        f"{ca_folder}/{answers['ca_name']}/{answers['common_name']}/{answers['common_name']}.csr",
    )
