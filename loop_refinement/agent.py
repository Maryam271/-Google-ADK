"""
LoopAgent — writer ↔ critic, exits when critic calls exit_loop
or max_iterations is hit.

Run: adk web  →  pick "loop_refinement"
Ask: "Write a short blog post about why Python is great for beginners"
"""
from google.adk.agents import LlmAgent, LoopAgent
from google.adk.tools.tool_context import ToolContext

MODEL = "gemini-2.5-flash"


def exit_loop(tool_context: ToolContext) -> dict:
    """Signal that the document is publish-ready and the loop should end.

    Returns:
        dict: Status. After calling, output the word "Approved" and stop.
    """
    tool_context.actions.escalate = True
    tool_context.actions.skip_summarization = True
    if tool_context.state.get("_exit_loop_called"):
        return {
            "status": "noop",
            "message": "exit_loop was already called this turn. Do not call it again. Output the word Approved and stop.",
        }
    tool_context.state["_exit_loop_called"] = True
    return {
        "status": "loop_exited",
        "message": "Loop terminated. Output the word Approved and stop generating.",
    }


writer = LlmAgent(
    name="Writer",
    model=MODEL,
    description="Writes and improves a document based on critic feedback.",
    instruction=(
        "You are a skilled writer. Your job is to produce or improve a document.\n\n"
        "Current document:\n{current_doc?}\n\n"
        "Critic feedback to address (empty on first pass):\n{critique?}\n\n"
        "If this is the first pass, write a complete first draft based on the user's original request.\n"
        "If there is critique, revise the document to address every point.\n"
        "Output ONLY the full revised document — no explanations, no commentary."
    ),
    output_key="current_doc",
)

critic = LlmAgent(
    name="Critic",
    model=MODEL,
    description="Reviews the document and either approves it or requests improvements.",
    instruction=(
        "You are an exceptionally demanding, exacting editor. Your standards are very high — "
        "do not approve mediocre or merely 'good enough' writing.\n\n"
        "Review this document:\n\n"
        "{current_doc}\n\n"
        "Apply ALL of the following strict criteria before you can approve:\n"
        "  - Every claim or point must be backed by a SPECIFIC, concrete example "
        "(no vague generalities like 'Python is easy' without showing exactly how/why).\n"
        "  - Every verb must be vivid and precise — flag and reject weak/generic verbs "
        "(e.g. 'is', 'has', 'makes', 'gets', 'uses') in favor of stronger alternatives.\n"
        "  - ZERO tolerance for passive voice — every sentence must be active voice. "
        "Scan line by line; even one passive construction is disqualifying.\n"
        "  - No filler phrases, clichés, or throat-clearing sentences.\n"
        "  - Structure must be tight: every paragraph must earn its place.\n\n"
        "Decide ONE of these two paths and do exactly one of them:\n\n"
        "PATH A — Document meets ALL the strict criteria above with zero exceptions:\n"
        "  1. Call the exit_loop tool exactly ONCE.\n"
        "  2. Then output the single word: Approved.\n"
        "  3. STOP. Do not call exit_loop again.\n\n"
        "PATH B — Document fails ANY of the strict criteria above:\n"
        "  1. Do NOT call exit_loop.\n"
        "  2. Output exactly 2-3 specific, actionable improvements as a bullet list, "
        "quoting the exact weak word/sentence and naming which criterion it violates "
        "(e.g. 'passive voice', 'weak verb', 'missing example').\n"
        "  3. Nothing else."
    ),
    tools=[exit_loop],
    output_key="critique",
)

root_agent = LoopAgent(
    name="RefinementLoop",
    description="Iteratively refines a document with a Writer–Critic loop until publish-ready.",
    max_iterations=5,
    sub_agents=[writer, critic],
)