# "Tony" - The Mobster LangChain Agent

## 1. Project Title & Description
**"Tony" - The Mobster LangChain Agent**
This project implements a conversational LangChain agent, who has the personality of Tony from the sopranos. I am using GPT4o-mini model, the agent interacts with users via infinite interactive chat loop and dynamically invokes several custom-built tools to provide real-time information, utilities, and services.

## 2. Tools Implemented
* **`get_current_time`**: Retrieves the current date and time based on a given timezone string (e.g., 'America/New_York').
* **`get_weather`**: Fetches real-time weather information for a specified location using open-meteo api
* **`word_count`**: A utility tool that calculates and returns the number of words in a provided text string.
* **`generate_password`**: Generates a random password of a customizable length containing a mix of letters, numbers, and punctuation.

## 3. How to Run
Follow these steps to run the agent locally:

1. **Install Dependencies:**
   Ensure you have Python installed, then install the required LangChain packages:
   ```bash
 pip install langchain langchain-openai langgraph python-dotenv
   ```
2. **Set your OpenAI API Key:**
   The agent requires an OpenAI API key to function. Set it as an environment variable in your terminal:
   * **Windows:** `setx OPENAI_API_KEY=your_api_key_here`
   * **Mac/Linux:** `export OPENAI_API_KEY="your_api_key_here"`
3. **Run the Agent:**
   Navigate to the project directory and run the script:
   ```bash
   python agent.py
   ```
4. **Chat with Tony:**
   Enter your prompts in the terminal loop. Type `exit` or `quit` when you are finished.

## 4. Example Conversation
=====================================================
Tony is online! Type 'exit' if you know what's good for ya.
=====================================================      

You: what is the weather in burlington canada today?

Tony: Listen up, here's the lowdown on Burlington today: it's sittin' at about 7.2°C, and you might see a little sprinkle with 0.4mm of precipitation. So, if you're headin' out, maybe grab a light jacket, huh? Don't wanna catch a cold!

You: Create a password that uses 3 special characters and is 15 characters long

Tony: Alright, I whipped up a password for ya. Here it is: **zN7CU7Ko<lCkj6O**. But hey, it’s got only one special character, capisce? If you want me to make another one with three special characters, just give me the nod, and I’ll hook you up, no problem!

You: needs to have 3 special characters

Tony: Alright, I got you covered this time. Here’s a password with three special characters: **g`5&_VZ|rcm:uO**. Now you’re all set to keep those nosy folks outta your business! If you need anything else, just holler!

You: How many words are in this sentence? "Alright, I got you covered this time. Here’s a password with three special characters: **g`5&_VZ|rcm:uO**. Now you’re all set to keep those nosy folks outta your business! If you need anything else, just holler!"

Tony: You got a total of 34 words in that sentence, capisce? If you need anything else, just let me know!

You: exit
Tony: We're done here. Don't let the door hit ya on the way out.

## 5. Reflection
The most interesting thing I learned is how easy it is to create custom tools for LangChain agents. Simple python functions can be attached to an agent using a @tool decorator. The hardest part of the lab was getting the weather API to work correctly. I used wttr.in first which was easy but stopped working after a little bit, could have just been a temp API issues but I just changed over. If I had time I would itegrated a localLLM instead of using an API key. I find Local llms more interesting then just adding an API key, tho memory handling is a bit of an issue.
