import os
from typing import Optional

from rich import print
from InquirerPy import prompt
from InquirerPy.base.control import Choice
import typer

from ca_ez_manager import __app_name__, __version__
from ca_ez_manager.constants import ActionType
from ca_ez_manager.actions.ca import create_ca
from ca_ez_manager.actions.cert import generate_cert
from ca_ez_manager.constants import ca_folder

app = typer.Typer(add_completion=False)


def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    print("[bold green]Welcome to CA Manager![/bold green]")

    if not os.path.exists(ca_folder):
        os.makedirs(ca_folder)

    choices = [
        Choice(value=ActionType.CREATE_CA, name="Create a new CA"),
        Choice(value=None, name="Exit"),
    ]

    ca_list = os.listdir(ca_folder)
    if len(ca_list) == 0:
        print("[red]No CAs found.[/red]")
    else:
        choices.insert(
            1,
            Choice(
                value=ActionType.GENERATE_CERTIFICATE, name="Generate a new certificate"
            ),
        )

    questions = [
        {
            "type": "list",
            "message": "What do you want to do?",
            "choices": choices,
        }
    ]

    answers = prompt(questions)
    match answers[0]:
        case ActionType.CREATE_CA:
            create_ca(ca_list)
        case ActionType.GENERATE_CERTIFICATE:
            generate_cert(ca_list)
        case None:
            print("[bold green]Goodbye![/bold green]")
            raise typer.Exit()
        case _:
            print("[red]Invalid selection.[/red]")
            raise typer.Exit()
