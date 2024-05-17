import typer
from InquirerPy import prompt
from prompt_toolkit.validation import ValidationError, Validator

from ca_ez_manager.utils.crypto import generate_certificate
from ca_ez_manager.utils.storage import get_ca_list, store_ca


app = typer.Typer()


@app.command(name="create")
def create():
    ca_list = get_ca_list()

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

    store_ca(answers["ca_name"], ca_private_key, ca_cert)
