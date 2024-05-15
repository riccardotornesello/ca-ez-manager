import os

from InquirerPy import prompt
from prompt_toolkit.validation import ValidationError, Validator

from ca_ez_manager.crypto_utils import (
    generate_certificate,
    save_private_key,
    save_certificate,
)
from ca_ez_manager.constants import ca_folder


def create_ca(ca_list):
    class CANameValidator(Validator):
        def validate(self, document):
            if document.text in ca_list:
                raise ValidationError(
                    message="CA already exists.",
                    cursor_position=document.cursor_position,
                )
            if not document.text.isalnum():
                raise ValidationError(
                    message="The name must contain only lowercase letters and numbers.",
                    cursor_position=document.cursor_position,
                )

    answers = prompt(
        [
            {
                "type": "input",
                "message": "Enter the name of the CA:",
                "name": "ca_name",
                "validate": CANameValidator(),
            }
        ]
    )

    ca_private_key, ca_cert = generate_certificate()

    os.makedirs(f"{ca_folder}/{answers['ca_name']}")

    save_private_key(ca_private_key, f"{ca_folder}/{answers['ca_name']}/ca.key")
    save_certificate(ca_cert, f"{ca_folder}/{answers['ca_name']}/ca.pem")
