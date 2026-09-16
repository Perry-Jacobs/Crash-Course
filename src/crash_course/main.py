# cspell:ignore fasthtml fastlite
from fastcore.xml import FT
from fasthtml.common import Button, Form, Input, Label, Titled, fast_app, serve
from fastlite import database

from .model import Option, Poll

app, rt = fast_app()
db = database("src/database/polls.db")

polls = db.create(Poll, pk="id")
questions = db.create(Option, pk="id")


@rt("/create")
def post(question: str, opt1: str, opt2: str):
    pass


@rt("/create")
def get() -> FT:
    return Titled(
        "Create a poll",
        Form(
            Label("Question", Input(name="Question")),
            Label("Option 1", Input(name="opt1")),
            Label("Option 2", Input(name="opt2")),
            Button("Create Poll", type="submit"),
            action="/create",
            method="post",
        ),
    )


def main() -> None:
    serve(port=3000)


if __name__ == "__main__":
    main()
