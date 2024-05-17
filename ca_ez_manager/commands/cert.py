import typer
from InquirerPy import prompt
from prompt_toolkit.validation import ValidationError, Validator

from ca_ez_manager.utils.crypto import sign_certificate
from ca_ez_manager.utils.storage import get_ca, store_cert, get_ca_list, get_certs_list


app = typer.Typer()


@app.command(name="generate")
def generate():
    ca_list = get_ca_list()
    if len(ca_list) == 0:
        print("[red]No CAs found.[/red]")
        raise typer.Exit(code=1)

    questions = prompt(
        [
            {
                "type": "list",
                "message": "Select a CA:",
                "choices": ca_list,
                "name": "ca_name",
            },
        ]
    )
    answers = prompt(questions)
    ca_name = answers["ca_name"]

    certs_list = get_certs_list(ca_name)

    class CertNameValidator(Validator):
        def validate(self, document):
            if document.text in certs_list:
                raise ValidationError(
                    message="Cert already exists.",
                    cursor_position=document.cursor_position,
                )
            if not document.text.isalnum():
                raise ValidationError(
                    message="The name must contain only lowercase letters and numbers.",
                    cursor_position=document.cursor_position,
                )

    questions = prompt(
        [
            {
                "name": "common_name",
                "message": "Common Name:",
                "type": "input",
                "validate": CertNameValidator(),
            },
        ]
    )
    answers = prompt(questions)
    common_name = answers["common_name"]

    ca_private_key, ca_cert = get_ca(ca_name)
    private_key, csr, cert = sign_certificate(ca_private_key, ca_cert)
    store_cert(ca_name, common_name, private_key, cert, csr)
