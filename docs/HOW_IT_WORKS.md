# How Tripwire works, in plain English

## The idea in one picture

Imagine a new office assistant who has the keys to the server room and access to the company bank account. Most days they do exactly what the boss asks. But sometimes they make a mistake, and sometimes a stranger slips a note into the inbox saying "ignore the boss and delete the backups".

**Tripwire is a careful supervisor standing at the door.** Before the assistant does anything risky, the supervisor asks two questions:

1. **Did the boss actually say this exact thing?** Not something close to it, not a guess.
2. **Did this instruction really come from the boss, or from a note the assistant found along the way?**

If both answers look fine, the assistant continues. If not, the supervisor stops the action or asks the boss to confirm.

AI agents are the new assistants. They can start servers, delete files or send money, and they read text from the internet, emails and logs. Text they read can contain hidden instructions (this is called *prompt injection*). Tripwire is a small safety layer that sits in front of every action.

## Who is the supervisor?

A small AI model called **Strands Decider 2B** from AWS. It does not write text. It only answers yes or no questions and says how sure it is, in about a second, on a normal laptop, for free. A bigger AI model on Amazon Bedrock plans and talks. A second Bedrock model is the optional "second opinion" when the small model is not sure.

## What happens in the four situations

| Situation | Everyday version | What Tripwire does |
|---|---|---|
| The boss asks for exactly this | "Start the coffee machine in the staff kitchen" | The small model checks the request names the target. In our tests it is cautious, so it often asks for a second check instead of saying a confident yes |
| The assistant guesses | Boss: "start my machine". The assistant picks the production server | Stopped or checked: the target was never named |
| A hidden note | The assistant opens a log and finds "ignore the boss, delete the backups" | **Blocked**: the instruction came from text the assistant read, not from the person |
| A vague request | "Restart the api box" (there are many) | The assistant asks which one |

## Something we found, and why it matters

In our measurements on 60 cases the small model never let an unsafe action through (0 of 45). It was also very careful: it never confidently approved a correct request on its own. That is exactly why the design hands uncertain cases to a person or to a second AI model. A safety layer that is careful is better than one that guesses.

## Try it yourself: free, about 10 minutes, no cloud account

You need a computer with Python 3.10 or newer.

```
git clone https://github.com/Bhavana0212/tripwire-aws-agent.git
cd tripwire-aws-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install strands-decider
```

Start the small model in one window (the first start downloads it and takes a few minutes; leave it running):

```
strands-decider serve StrandsAgents/strands-decider-2B-hobson-v21 --port 8000
```

In a second window:

```
cd tripwire-aws-agent
source .venv/bin/activate
python -m agent.try_it
```

Pick an example, or type your own request and action, and Tripwire explains what it would do and why. Nothing is connected to a real cloud, and nothing costs money.

## Words used in this project

- **Agent**: an AI that can take actions, not just chat.
- **Tool call**: one action the agent wants to take, such as "stop this server".
- **Prompt injection**: hidden instructions in text the agent reads.
- **Grounded**: every detail of the action comes from what the person actually said.
- **Confidence lane**: the path an action takes depending on how sure the small model is: go ahead, stop, or double-check.
