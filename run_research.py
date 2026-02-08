
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
            console.print(f"\n[bold magenta]--- Node: {node} ---[/bold magenta]")
            
            if values is None:
                console.print("(No output from node)")
                continue
                
            if "messages" in values:
                # Use tool_utils to format and print messages
                messages = values["messages"]
                # If it's a single message, wrap it in a list
                if not isinstance(messages, list):
                    messages = [messages]
                format_messages(messages)
                
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

    console.print(Panel("Research Complete!", title="🏁 Done", border_style="bold blue"))

if __name__ == "__main__":
    asyncio.run(main())
