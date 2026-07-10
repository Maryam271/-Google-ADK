"""
ParallelAgent — three researchers run concurrently, then a synthesizer.

google_search is a Gemini built-in grounding tool.
Rule: agents using google_search must have NO other tools.
Rule: each parallel branch must use a UNIQUE output_key.

Run: adk web  →  pick "parallel_research"
Ask: "Research recipe ideas, travel destinations, and programming languages"
"""
from google.adk.agents import LlmAgent, ParallelAgent, SequentialAgent
from google.adk.tools import google_search

MODEL = "gemini-2.5-flash-lite"

recipe_researcher = LlmAgent(
    name="recipe_ideas_researcher",
    model=MODEL,adk
    description="Researches recipe ideas trends.",
    instruction=(
        "Research the 3 most important recent recipe ideas. "
        "Output a 2-sentence summary."
    ),
    tools=[google_search],
    output_key="recipe_result",
)

travel_researcher = LlmAgent(
    name="travel_destinations_researcher",
    model=MODEL,
    description="Researches travel destinations trends.",
    instruction=(
        "Research the latest  travel destinations. "
        "Output a 2-sentence summary."
    ),
    tools=[google_search],
    output_key="travel_result",
)

prog_researcher = LlmAgent(
    name="programming_languages_researcher",
    model=MODEL,
    description="Researches programming languages methods and tehnique in recent AI trend.",
    instruction=(
        "Research the most promising current programming languages "
        "Output a 2-sentence summary."
    ),
    tools=[google_search],
    output_key="prog_result",
)

research_team = ParallelAgent(
    name="ResearchTeam",
    description="Three concurrent researchers covering Recipe Ideas, travel destinations, and carbon capture.",
    sub_agents=[recipe_researcher, travel_researcher, prog_researcher],
)

synthesizer = LlmAgent(
    name="Synthesizer",
    model=MODEL,
    description="Combines parallel research into a structured report.",
    instruction=(
        "Combine the following research into one structured markdown report with three sections:\n\n"
        "**Recipe Ideas:**\n{recipe_result}\n\n"
        "**travel destinations:**\n{travel_result}\n\n"
        "**programming languages:**\n{prog_result}\n\n"
        "Add a short 'Key Takeaways' section at the end."
    ),
)

root_agent = SequentialAgent(
    name="ResearchAndSynthesize",
    description="Fan-out to three parallel researchers, then synthesize into one report.",
    sub_agents=[research_team, synthesizer],
)