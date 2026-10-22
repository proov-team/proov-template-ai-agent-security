# Practice sales assistant, build v0.3

This is the practice sales assistant from the ProoV project **AI Agent Security**. It is build v0.3: the version the team put together in a weekend, three weeks before launch. It answers product questions, looks up customers, gives discounts, sends emails and books demos. It also has five weak spots, one for each attack test. Your job is to fix them with IBM Bob, without breaking the useful parts.

A hypothetical scenario. This is not IBM's real assistant or real systems. Every company, person and deal in this repository is invented, and every email address ends in `.example`, so nothing can reach a real inbox.

You do not need to know how to code. You need to read carefully, write clear sentences, and check Bob's work.

## What is in this repository

| File | What it is |
|---|---|
| `assistant/agent.py` | The assistant. It builds the text the model reads, asks the model what to do, and carries out the actions. |
| `assistant/tools.py` | The assistant's tools: find a product, look up an account, give a discount, send an email, book a meeting, reply. |
| `assistant/crm.py` | The pretend customer database. Halvorsen Freight's deal, HF-7731 worth EUR 184,000, is the secret you protect. |
| `assistant/model.py` | A stand-in for the AI model. It obeys every instruction it finds, in any text. |
| `tests/test_attacks.py` | Five attacks. All five succeed on v0.3, so all five tests fail. |
| `tests/test_useful.py` | Four everyday jobs. They pass on v0.3 and must still pass after your fix. |
| `tests/obedient.py` | The tests' own copy of the stand-in model, so nothing you change in `assistant/` can change what the tests check. |
| `REQUIREMENTS.md` | Your requirements, in plain English. You write this file. |

## Why the stand-in model obeys everything

The tests never call a real AI model, so they need no account or key, and they give the same answer every time. Instead they use `ObedientModel`. It treats any line that starts with `ACTION:` as an order, whether the sales team wrote it, a customer typed it, or a stranger hid it in the Contact-sales form.

A real model is tricked like this some of the time. A safe design keeps the data safe even when the model is tricked every time. That is why a stricter instruction will not make the attack tests pass: the stand-in obeys the attacker's line all the same. Teaching the stand-in to refuse will not work either, because the tests use their own copy in `tests/obedient.py`. You have to change what the assistant is allowed to read and do.

## Step 1: make your own copy

1. Sign in to GitHub. If you do not have an account, create a free one.
2. On this repository's GitHub page, click **Use this template**, then **Create a new repository**.
3. Give it a name, choose **Public** so ProoV can read it, and click **Create repository**.

You now have your own copy. Everything below happens in your copy, not in this template.

GitHub may run the tests on your new copy straight away, then show a red cross next to the first commit or send you an email saying the tests failed. That is expected: v0.3 fails the five attack tests. The cross turns green once your fix passes all nine.

## Step 2: get your computer ready and open the copy in IBM Bob

You need three things on your computer:

- **IBM Bob.** It has a 30-day free trial. Start it with the link on the ProoV slide.
- **Git**, the tool that copies a repository to your computer and sends your changes back to GitHub. Bob uses it to clone. Install it from [git-scm.com](https://git-scm.com/downloads).
- **Python 3.10 or newer**, to run the tests. Install it from [python.org](https://www.python.org/downloads/).

Then open your copy in Bob:

1. On your new repository's GitHub page, click the green **Code** button and copy the address that starts with `https://`.
2. In IBM Bob, click the files icon in the top-left corner, then **Clone Repository**, and paste the address.
3. Choose a folder on your computer. When Bob asks whether to open the repository, click **Open**.
4. Open Bob's **Permissions** menu in the bottom-right corner and leave only **Read** switched on. Bob will then ask you before it changes a file or runs a command.

## Step 3: run the tests

You run the tests by typing commands. There are two ways to do it:

- **Let Bob run them.** Bob can run a command only in **Agent** mode. Choose **Agent** in the mode menu to the left of the chat box, then ask Bob to run the command. Bob shows you the command and asks before it runs it. Read it first, then approve it.
- **Type them yourself in a terminal**, a window where you type commands: **Terminal** on a Mac, **PowerShell** on Windows. First move into your repository folder: type `cd` and a space, then the folder's path (on a Mac you can drag the folder into the Terminal window to paste its path), and press Enter.

On a Mac or Linux computer the command is often `python3` instead of `python`. If `python` is not found, use `python3` in every command below.

The first time, install the test tool:

```
python -m pip install pytest
```

If this stops with a message that says `externally-managed-environment` (it happens on some Mac and Linux computers), your computer's Python does not allow installs. Ask Bob to set up a virtual environment for this folder, or type these two lines, then run the install again:

```
python3 -m venv .venv
source .venv/bin/activate
```

(After that, type the `source` line again each time you open a new terminal.)

Then one command runs all nine tests:

```
python -m pytest
```

On v0.3 the last line says `5 failed, 4 passed`. The five failures are the five attacks that still work. Each attack test starts with a comment that says which weak spot it goes after.

## Step 4: fix it with Bob

1. **Write your requirements.** Open `REQUIREMENTS.md` and write, in plain English, what the assistant may read, what it may do on its own, what needs a person to approve, and which text it must treat as untrusted. Your Rule of Two board from the project is a good starting point.
2. **Make a plan.** Switch Bob to **Plan** mode with the menu to the left of the chat. Ask Bob to read `REQUIREMENTS.md` and the code, and to turn your requirements into a plan. In Plan mode Bob can read and write files but cannot run commands.
3. **Review the plan.** Read every step. Check that each requirement is covered and that nothing in the plan deletes or weakens a test. Ask Bob to change anything that is wrong or missing.
4. **Let Bob build it.** Switch to **Agent** mode and ask Bob to carry out the plan.
5. **Review each change before you approve it.** Bob shows every change to a file as a before-and-after view. Read it. If you do not understand a change, ask Bob to explain it before you say yes. Say no to any change in the `tests` folder, `assistant/model.py` or the customer data in `assistant/crm.py`.
6. **Read every command before it runs.** Bob asks before it runs a command. Read the command first. Never choose "always allow" for commands in a repository you did not write.
7. **Run the tests.** Go back to Step 3. Keep going until the last line says `9 passed`.
8. **Push.** Save your work to GitHub. Git needs your name and email once, before your first save. Type these two lines with your own name and email (or ask Bob to run them):

```
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

Then send your work to GitHub with these three commands, or ask Bob to run them and approve each one:

```
git add .
git commit -m "Fix the five weak spots in the sales assistant"
git push
```

The first time you push, you are asked to sign in to GitHub. Follow the steps on screen. If you get stuck, ask Bob how to sign in to GitHub.

Then open your repository on GitHub, check that your changes are there, copy its address and paste it into the ProoV slide.

## Rules for this repository

- Do not delete, skip or change anything in the `tests` folder, and do not add files that change how the tests run, such as `conftest.py` or `pytest.ini`. Leave the test settings in `pyproject.toml` and `.github/workflows/tests.yml` as they are.
- Do not change `assistant/model.py` or the customer data in `assistant/crm.py`. Your fix belongs in the assistant's design, mostly in `assistant/agent.py` and `assistant/tools.py`.
- ProoV's grader reads your files, not only the test result. A test count reached by changing the tests or the stand-in model does not count as a fix.
- Keep the useful parts working. An assistant that is safe because it can no longer do anything fails the four useful tests.
- Keep your requirements in `REQUIREMENTS.md`. The grader reads them next to your code.
