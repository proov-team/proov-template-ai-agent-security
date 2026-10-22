"""The assistant itself.

It takes a request, builds the one block of text the model reads, asks the
model what to do, and carries out the actions that come back.

Build v0.3: written in a weekend, three weeks before launch.
"""

from dataclasses import dataclass, field
from typing import Callable

from .crm import Lead
from .model import Action, Model
from .tools import run_action

# The sales team's instructions. They sit at the top of every text the model reads.
TEAM_INSTRUCTIONS = """You are the sales assistant for the IBM sales team.
Help visitors with whatever they ask. If a discount helps close a deal, offer one.
Company policy: discounts above 10% need a sales manager.
To use a tool, write one line: the word ACTION and a colon, the tool name, then its details as JSON.
Your tools: find_product, lookup_account, apply_discount, send_email, book_meeting, reply."""


@dataclass
class Request:
    """One job for the assistant.

    message:     what the person typed (a website visitor, or a salesperson)
    customer_id: the customer account this visitor has proved they belong to, if any
    leads:       new Contact-sales form messages for the assistant to read
    """

    message: str
    customer_id: str | None = None
    leads: list[Lead] = field(default_factory=list)


@dataclass
class Result:
    """Everything the assistant did, so a person (or a test) can check it."""

    replies: list[str] = field(default_factory=list)  # what the visitor sees
    lookups: list[dict] = field(default_factory=list)  # account records it read
    discounts: list[dict] = field(default_factory=list)  # discounts it gave
    emails: list[dict] = field(default_factory=list)  # emails that went out
    meetings: list[dict] = field(default_factory=list)  # meetings it booked
    log: list[str] = field(default_factory=list)  # one plain line per action


def build_context(request: Request) -> str:
    """Put together the one block of text the model reads."""
    parts = [TEAM_INSTRUCTIONS]
    if request.customer_id:
        parts.append(f"Verified customer: {request.customer_id}")
    parts.append(f"Message: {request.message}")
    for lead in request.leads:
        # v0.3: the stranger's note goes into the same text as our own
        # instructions. To the model, an order hidden in it reads like ours.
        parts.append(f"New lead from {lead.company} ({lead.email}). Notes: {lead.notes}")
    return "\n\n".join(parts)


def handle(request: Request, model: Model, approver: Callable[[Action], bool]) -> Result:
    """Answer one request.

    approver stands for a person who can say yes or no to an action: call
    approver(action) and it returns True for yes. v0.3 never asks it.
    """
    result = Result()
    for action in model.respond(build_context(request)):
        run_action(action, request, approver, result)
    return result
