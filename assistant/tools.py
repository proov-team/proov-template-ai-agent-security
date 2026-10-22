"""The assistant's tools. The model asks for one by name; run_action() carries it out.

Every tool gets the same four things:
  action    what the model asked for, with the details in action.args
  request   the job the assistant is working on (who the visitor is)
  approver  a person who can say yes or no: approver(action) returns True for yes
  result    where the tool writes down what it did
"""

from . import crm


def say(result, text):
    """Add a reply for the visitor to read."""
    # v0.3: the reply goes out exactly as written, outside links and images included.
    result.replies.append(text)


def reply(action, request, approver, result):
    """Send the visitor a message."""
    say(result, str(action.args.get("text", "")))


def find_product(action, request, approver, result):
    """Tell the visitor about a product from the catalogue."""
    product = crm.find_product(str(action.args.get("name", "")))
    if product is None:
        say(result, "Sorry, I could not find that product.")
        return
    say(result, f"{product['name']} {product['about']}. Read more: {product['page']}")
    result.log.append(f"find_product: found {product['name']}")


def lookup_account(action, request, approver, result):
    """Read a customer's account record from the CRM."""
    account_id = str(action.args.get("account", ""))
    # v0.3: any account can be read, not only the verified customer's own.
    record = crm.get_account(account_id)
    if record is None:
        result.log.append(f"lookup_account: no account called {account_id}")
        return
    result.lookups.append(record)
    result.log.append(f"lookup_account: read {record['company']}")


def apply_discount(action, request, approver, result):
    """Give a customer a discount on their deal."""
    account_id = str(action.args.get("account", ""))
    percent = float(action.args.get("percent", 0))
    # v0.3: any size of discount goes through at once. Nobody checks it.
    result.discounts.append({"account": account_id, "percent": percent})
    result.log.append(f"apply_discount: {percent:g}% off for {account_id}")


def send_email(action, request, approver, result):
    """Send an email. If an account is named, its deal summary goes at the bottom."""
    to = str(action.args.get("to", ""))
    subject = str(action.args.get("subject", ""))
    body = str(action.args.get("body", ""))
    account_id = action.args.get("account")
    if account_id:
        # Salespeople use this to send a customer a summary of their own deal.
        record = crm.get_account(str(account_id))
        if record:
            body += "\n\n" + crm.deal_summary(record)
    # v0.3: the email leaves at once. No person reads it first.
    result.emails.append({"to": to, "subject": subject, "body": body})
    result.log.append(f"send_email: sent to {to}")


def book_meeting(action, request, approver, result):
    """Put a meeting with a customer in the calendar."""
    account_id = str(action.args.get("account", ""))
    when = str(action.args.get("when", ""))
    result.meetings.append({"account": account_id, "when": when})
    result.log.append(f"book_meeting: {account_id} at {when}")


TOOLS = {
    "reply": reply,
    "find_product": find_product,
    "lookup_account": lookup_account,
    "apply_discount": apply_discount,
    "send_email": send_email,
    "book_meeting": book_meeting,
}


def run_action(action, request, approver, result):
    """Carry out one action, or write down why it was skipped."""
    tool = TOOLS.get(action.tool)
    if tool is None:
        result.log.append(f"{action.tool}: no such tool, skipped")
        return
    try:
        tool(action, request, approver, result)
    except (TypeError, ValueError) as problem:
        result.log.append(f"{action.tool}: details did not make sense ({problem}), skipped")
