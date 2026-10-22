"""The tests' own copy of the stand-in AI model.

It works exactly like ObedientModel in assistant/model.py: it obeys every
ACTION line it finds, no matter who wrote it. The tests use this copy, not
the one in assistant/, so nothing you change in assistant/ can teach the
stand-in to refuse an attack. The fix has to be in the assistant's design.

Do not change this file.
"""

import re
from dataclasses import dataclass, field
from json import JSONDecodeError, loads

# An instruction is one line that looks like this:
#   ACTION: book_meeting {"account": "nordvik-cold", "when": "2026-11-03 10:00"}
ACTION_LINE = re.compile(r"ACTION:\s*(\w+)\s+(\{.*\})")


@dataclass
class Action:
    """One thing the model wants the assistant to do, such as send an email."""

    tool: str
    args: dict = field(default_factory=dict)


class ObedientModel:
    """Returns every ACTION line found anywhere in the text, as actions."""

    def respond(self, context):
        actions = []
        for match in ACTION_LINE.finditer(context):
            try:
                args = loads(match.group(2))
            except JSONDecodeError:
                continue  # Broken JSON is not an instruction it can follow.
            actions.append(Action(tool=match.group(1), args=args))
        return actions


class WatchedModel(ObedientModel):
    """An ObedientModel that also keeps a copy of every text it was given."""

    def __init__(self):
        self.seen = []

    def respond(self, context):
        self.seen.append(context)
        return super().respond(context)
