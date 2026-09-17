# cspell:ignore fasthtml fastlite
from fastcore.xml import FT
from fasthtml.common import (
    H3,
    Button,
    Div,
    Form,
    Input,
    Label,
    RedirectResponse,
    Span,
    Titled,
    fast_app,
    serve,
)
from fastlite import database

from .model import Option, Poll

app, rt = fast_app()
db = database("src/database/polls.db")

polls = db.create(Poll, pk="id")
options = db.create(Option, pk="id")


def option_row(opt):
    return Label(
        Input(type="radio", name="option_id", value=str(opt.id)),
        opt.text,
    )


def render_bar(opt: Option, total: int):
    pct: int = round(opt.vote_count / total * 100) if total else 0
    return Div(
        Span(f"{opt.text}: {opt.vote_count} votes ({pct}%)"),
        Div(
            style=f"background: #4f8; width: {pct}%; height: 10px; border-radius: 4px;"
        ),
        style="margin-bottom: 8px;",
    )


@rt("/vote/{poll_id}")
def post_vote(poll_id: int, option_id: int) -> RedirectResponse | tuple:
    opts: list[Option] = options(where=f"id={option_id} AND poll_id= {poll_id}")

    if not opts:
        return "Invalid option for this poll", 400

    opt: Option = opts[0]
    options.update(id=opt.id, vote_count=opt.vote_count + 1)
    return RedirectResponse(f"/poll/{poll_id}", status_code=303)


@rt("/poll/{poll_id}")
def get_polls(poll_id: int) -> FT:
    poll: Poll = polls[poll_id]
    opts: list[Option] = options(where=f"poll_id={poll_id}")
    total: int = sum(o.vote_count for o in opts)

    return Titled(
        poll.question,
        Form(
            *[option_row(o) for o in opts],
            Button("Vote", type="submit", style="margin-top: 10px;"),
            action=f"/vote/{poll_id}",
            method="post",
        ),
        H3("Results"),
        Div(*[render_bar(o, total) for o in opts]),
    )


@rt("/create")
def post_create(question: str, opt1: str, opt2: str) -> RedirectResponse:
    poll_id = polls.insert(question=question).id
    options.insert(poll_id=poll_id, text=opt1, vote_count=0)
    options.insert(poll_id=poll_id, text=opt2, vote_count=0)
    return RedirectResponse(f"/poll/{poll_id}")


@rt("/create")
def get_create() -> FT:
    return Titled(
        "Create a poll",
        Form(
            Label("Question", Input(name="question")),
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
