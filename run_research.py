
import asyncio
import uuid
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(".env")

# Add src directory to python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from langgraph.checkpoint.memory import MemorySaver
from open_deep_research.deep_researcher import deep_researcher, deep_researcher_builder
from langchain_core.messages import HumanMessage
from tool_utils import format_messages, console
from rich.panel import Panel

async def main():
    console.print(Panel("Initializing Deep Research Agent...", title="🚀 Status", border_style="bold blue"))
    
    # Compile the graph with a memory saver checkpointer
    graph = deep_researcher_builder.compile(checkpointer=MemorySaver())
    
    # Configure the run
    thread_id = str(uuid.uuid4())
    config = {
        "configurable": {
            "thread_id": thread_id,
            "allow_clarification": False,  # Disable clarification to skip one structured output step
            "max_concurrent_research_units": 1, # Limit concurrency to avoid rate limits
        }
    }

    # Define the research topic
    topic = "Unity2022最新LTS版本对Native Render Pass的支持情况"
    console.print(Panel(f"Starting research on topic:\n[bold]{topic}[/bold]", title="📋 Research Topic", border_style="yellow"))

    # Invoke the graph
    input_message = {"role": "user", "content": topic}
    
    async for event in graph.astream(
        {"messages": [input_message]}, 
        config,
        stream_mode="updates"
    ):
        # Print stream events to show progress
        for node, values in event.items():
            try:
                console.print(f"\n[bold magenta]--- Node: {node} ---[/bold magenta]")
                
                if values is None:
                    console.print("(No output from node)")
                    continue
                    
                # Handle messages
                if "messages" in values:
                    # Use tool_utils to format and print messages
                    messages = values["messages"]
                    # If it's a single message, wrap it in a list
                    if not isinstance(messages, list):
                        messages = [messages]
                    format_messages(messages)

                # Handle research_brief
                if "research_brief" in values:
                    console.print(Panel(values["research_brief"], title="📝 Research Brief", border_style="cyan"))

                # Handle supervisor_messages
                if "supervisor_messages" in values:
                    sup_msgs = values["supervisor_messages"]
                    if isinstance(sup_msgs, dict) and "value" in sup_msgs:
                        format_messages(sup_msgs["value"])
                    elif isinstance(sup_msgs, list):
                        format_messages(sup_msgs)
                    else:
                        console.print(f"[yellow]Supervisor Messages: {sup_msgs}[/yellow]")

                # Handle researcher_messages
                if "researcher_messages" in values:
                    res_msgs = values["researcher_messages"]
                    if isinstance(res_msgs, dict) and "value" in res_msgs:
                        format_messages(res_msgs["value"])
                    elif isinstance(res_msgs, list):
                        format_messages(res_msgs)

                # Handle compressed_research
                if "compressed_research" in values:
                    console.print(Panel(values["compressed_research"], title="📦 Compressed Research", border_style="green"))

                # Handle notes
                if "notes" in values:
                    notes = values["notes"]
                    if isinstance(notes, list):
                        notes_content = "\n\n".join(str(n) for n in notes)
                    else:
                        notes_content = str(notes)
                    console.print(Panel(notes_content, title="📓 Notes", border_style="magenta"))
                
                # Handle raw_notes
                if "raw_notes" in values:
                    raw_notes = values["raw_notes"]
                    if isinstance(raw_notes, list):
                        for i, note in enumerate(raw_notes):
                            console.print(Panel(note[:500] + ("..." if len(note) > 500 else ""), title=f"📝 Raw Note {i+1}", border_style="dim white"))
                    else:
                         console.print(Panel(str(raw_notes)[:500] + "...", title="📝 Raw Notes", border_style="dim white"))

                if "final_report" in values:
                    report_content = values['final_report']
                    console.print(Panel("Final Report Generated!", title="🎉 Success", border_style="bold green"))
                    
                    # Save report to file
                    report_dir = "report"
                    os.makedirs(report_dir, exist_ok=True)
                    report_file = os.path.join(report_dir, f"research_report_{uuid.uuid4().hex[:8]}.md")
                    
                    with open(report_file, "w", encoding="utf-8") as f:
                        f.write(report_content)
                        
                    console.print(f"Report saved to: [bold underline]{report_file}[/bold underline]")

                if "research_notes" in values:
                    console.print("[italic]Updated research notes.[/italic]")

            except Exception as e:
                console.print(f"[bold red]Error displaying output for node {node}: {e}[/bold red]")
                # Continue execution even if display fails

    console.print(Panel("Research Complete!", title="🏁 Done", border_style="bold blue"))

if __name__ == "__main__":
    asyncio.run(main())
