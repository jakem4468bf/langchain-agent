import os
import string
import secrets
import urllib.request
import urllib.parse
from datetime import datetime
from zoneinfo import ZoneInfo

# LangChain imports
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor

# ==========================================
# 1. Provide 4 Custom Tools
# ==========================================

@tool
def get_current_time(timezone_str: str) -> str:
    """Return current date/time for any timezone. timezone_str should be an IANA timezone string like 'America/New_York'."""
    try:
        tz = ZoneInfo(timezone_str)
        return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
    except Exception as e:
        # Handle gracefully by returning the error to the LLM
        return f"Error getting time for timezone '{timezone_str}': {str(e)}"

@tool
def get_weather(location: str) -> str:
    """Fetch real weather from a free API (wttr.in) for a given location."""
    try:
        url = f"https://wttr.in/{urllib.parse.quote(location)}?format=3"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8').strip()
    except Exception as e:
        return f"Error fetching weather for '{location}': {str(e)}"

@tool
def word_count(text: str) -> int:
    """Count words in a given text."""
    try:
        return len(text.split())
    except Exception as e:
        return f"Error counting words: {str(e)}"

@tool
def generate_password(length: int = 12) -> str:
    """Generate a secure random password of a specified length."""
    try:
        if length < 4:
            return "Error: Password length must be at least 4"
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password
    except Exception as e:
        return f"Error generating password: {str(e)}"

def main():
    if not os.environ.get("OPENAI_API_KEY"):
        print("CRITICAL ERROR: OPENAI_API_KEY environment variable is not set.")
        print("Please set it via command line (e.g., 'set OPENAI_API_KEY=your_key') before running the agent.")
        return

    print(f"Your OPENAI_API_KEY is: {os.environ.get('OPENAI_API_KEY')}")

    # Initialize the LangChain Chat model
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

    # Define the tools our agent can use
    tools = [get_current_time, get_weather, word_count, generate_password]

    # Define a system prompt with a clear role/personality
    system_prompt = (
        "You are 'Tony', a tough but helpful AI assistant from the Bronx. You talk like a mobster from The Sopranos. "
        "You love helping people out, but you got an attitude, capisce? You deal with problems head-on. "
        "You got access to some tools. If a tool breaks down, tell the user gracefully but keep the tough guy character, "
        "explain what went wrong, and offer to fix it manually, bing bang boom."
    )

    # Create the prompt structure required by the tool-calling agent
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Construct the agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Construct the executor.
    # handle_parsing_errors=True ensures the agent doesn't crash if LLM outputs invalid tool calls.
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False, 
        handle_parsing_errors=True
    )

    # Initialize conversation memory
    chat_history = []

    print("=====================================================")
    print("Tony is online! Type 'exit' if you know what's good for ya.")
    print("=====================================================")

    # 3. Interactive Conversation Loop
    while True:
        try:
            # Accept user input
            user_input = input("\nYou: ")
            
            # Check for exit commands
            if user_input.lower() in ["exit", "quit"]:
                print("Tony: We're done here. Don't let the door hit ya on the way out.")
                break
            
            if not user_input.strip():
                continue

            # Invoke the agent executor
            response = agent_executor.invoke({
                "input": user_input,
                "chat_history": chat_history
            })

            ai_response = response["output"]
            print(f"\nTony: {ai_response}")

            # Update the history for the next iteration
            chat_history.append(HumanMessage(content=user_input))
            chat_history.append(AIMessage(content=ai_response))

        except KeyboardInterrupt:
            print("\n\nTony: Whoa, where's the fire? I'm outta here.")
            break
        except Exception as e:
            # Handle unexpected global errors without crashing the loop
            print(f"\n[System] An unexpected error occurred: {str(e)}")
            print("[System] The agent intercepted the crash and is ready for the next prompt.")

if __name__ == "__main__":
    main()
