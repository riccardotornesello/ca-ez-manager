import os

import typer
from InquirerPy import prompt

from ca_ez_manager.utils.crypto import sign_certificate
from ca_ez_manager.utils.storage import get_ca, store_cert, get_ca_list


app = typer.Typer()


@app.command(name="generate")
def generate():
    ca_list = get_ca_list()
    if len(ca_list) == 0:
        print("[red]No CAs found.[/red]")
        return

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

    ca_private_key, ca_cert = get_ca(answers["ca_name"])

    private_key, csr, cert = sign_certificate(ca_private_key, ca_cert)

    store_cert(answers["ca_name"], answers["common_name"], private_key, cert, csr)
