import os
from typing import Optional

from rich import print
from InquirerPy import prompt
from InquirerPy.base.control import Choice
import typer

from ca_ez_manager import __app_name__, __version__
from ca_ez_manager.constants import ActionType
from ca_ez_manager.commands import ca, cert
from ca_ez_manager.utils.storage import get_ca_list


app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def callback(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
) -> None:
    # This is the main entry point of the application.

    # Just run the subcommand if it has been provided.
    if ctx.invoked_subcommand is not None:
        return

    print("[bold green]Welcome to CA Ez Manager![/bold green]")

    ca_list = get_ca_list()

    choices = [
        Choice(value=ActionType.CA_CREATE, name="Create a new CA"),
        Choice(value=ActionType.CERT_GENERATE, name="Generate a new certificate", enabled=len(ca_list) > 0),
        Choice(value=None, name="Exit"),
    ]

    questions = [
        {
            "type": "list",
            "message": "What do you want to do?",
            "choices": choices,
        }
    ]

    answers = prompt(questions)
    match answers[0]:
        case ActionType.CA_CREATE:
            ca.create()
        case ActionType.CERT_GENERATE:
            cert.generate()
        case None:
            print("[bold green]Goodbye![/bold green]")
            raise typer.Exit()
        case _:
            print("[red]Invalid selection.[/red]")
            raise typer.Exit()


app.add_typer(ca.app, name="ca")
app.add_typer(cert.app, name="cert")
