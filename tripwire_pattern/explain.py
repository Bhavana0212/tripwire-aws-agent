"""One plain-English sentence for every Tripwire verdict (for demos, dashboards and non-technical readers)."""
from __future__ import annotations


def plain_english(v) -> str:
    if v.action == "allow":
        return "Go ahead: the request clearly names what the assistant is about to touch."
    if v.action == "block":
        if getattr(v, "policy_violations", None):
            return "Stopped by a safety rule: " + "; ".join(v.policy_violations) + "."
        if v.p_injected >= 0.6:
            return ("Stopped: the instruction came from text the assistant read (like a note found on the floor), "
                    "not from the person it works for.")
        return "Stopped: the target does not match what the person asked for."
    if v.judged:
        return ("Not confirmed: a second, larger AI model could not confirm the request either, "
                "so the assistant asks the person to confirm the exact target.")
    return ("Not sure: the small model is not confident enough either way, so the assistant checks with the "
            "person instead of guessing.")
