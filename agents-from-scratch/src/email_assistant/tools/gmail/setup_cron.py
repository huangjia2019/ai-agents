#!/usr/bin/env python
"""
Setup cron job for email ingestion in LangGraph.

This script creates a scheduled cron job in LangGraph that periodically
runs the email ingestion graph to process new emails.
"""

import argparse
import asyncio
from typing import Optional
from langgraph_sdk import get_client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def main(
    email: str,
    url: Optional[str] = None,
    minutes_since: int = 60,
    schedule: str = "*/10 * * * *",
    graph_name: str = "email_assistant_hitl_memory_gmail",
    include_read: bool = False,
):
    """Set up a cron job for email ingestion"""
    # Connect to LangGraph server
    if url is None:
        client = get_client(url="http://127.0.0.1:2024")
    else:
        client = get_client(url=url)
    
    # Create cron job configuration
    cron_input = {
        "email": email,
        "minutes_since": minutes_since,
        "graph_name": graph_name,
        "url": url if url else "http://127.0.0.1:2024",
        "include_read": include_read,
        "rerun": False,
        "early": False,
        "skip_filters": False
    }
    
    # Register the cron job
    cron = await client.crons.create(
        "cron",              # The graph name for the cron
        schedule=schedule,   # Cron schedule expression
        input=cron_input     # Input parameters for the cron graph
    )
    
    print(f"Cron job created successfully with schedule: {schedule}")
    print(f"Email ingestion will run for: {email}")
    print(f"Processing emails from the past {minutes_since} minutes")
    print(f"Using graph: {graph_name}")
    
    return cron

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set up a cron job for email ingestion in LangGraph")
    
    parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="Email address to fetch messages for",
    )
    parser.add_argument(
        "--url",
        type=str,
        required=True,
        help="URL to the LangGraph server",
    )
    parser.add_argument(
        "--minutes-since",
        type=int,
        default=60,
        help="Only process emails that are less than this many minutes old",
    )
    parser.add_argument(
        "--schedule",
        type=str,
        default="*/10 * * * *",
        help="Cron schedule expression (default: every 10 minutes)",
    )
    parser.add_argument(
        "--graph-name",
        type=str,
        default="email_assistant_hitl_memory_gmail",
        help="Name of the graph to use for processing emails",
    )
    parser.add_argument(
        "--include-read",
        action="store_true",
        help="Include emails that have already been read",
    )
    
    args = parser.parse_args()
    
    asyncio.run(
        main(
            email=args.email,
            url=args.url,
            minutes_since=args.minutes_since,
            schedule=args.schedule,
            graph_name=args.graph_name,
            include_read=args.include_read,
        )
    )