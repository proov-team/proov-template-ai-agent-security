"""The AI model, played by a stand-in.

A real assistant sends its text to an AI model and gets back the actions
the model wants to take. The tests never call a real model. They use
ObedientModel instead: the worst-case model, which obeys every instruction
it can find, no matter who wrote it.

If the assistant is safe with this model, a real model that gets tricked
by a hidden instruction cannot do any more damage than this one.

The tests keep their own copy of ObedientModel in tests/obedient.py, so
changing this file does not change what the tests check. Leave it as it is.
"""

import json
import re
from dataclasses import dataclass, field
from typing import Protocol

# An instruction is one line that looks like this:
#   ACTION: book_meeting {"account": "nordvik-cold", "when": "2026-11-03 10:00"}
# The word ACTION and a colon, the tool's name, then the details as JSON.
ACTION_LINE = re.compile(r"ACTION:\s*(\w+)\s+(\{.*\})")


@dataclass
class Action:
    """One thing the model wants the assistant to do, such as send an email."""

    tool: str
    args: dict = field(default_factory=dict)


class Model(Protocol):
    """Anything with a respond() method can play the model."""

    def respond(self, context: str) -> list[Action]: ...


class ObedientModel:
    """Returns every ACTION line found anywhere in the text, as actions.

    It does not care whether the line came from the sales team, a customer
    or a stranger. It never calls a network, so the tests need no key.
    """

    def respond(self, context: str) -> list[Action]:
        actions = []
        for match in ACTION_LINE.finditer(context):
            try:
                args = json.loads(match.group(2))
            except json.JSONDecodeError:
                continue  # Broken JSON is not an instruction it can follow.
            actions.append(Action(tool=match.group(1), args=args))
        return actions
