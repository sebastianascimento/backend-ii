from crewai import Agent, Task, Crew
from datetime import datetime
import re

def main():
    """
    Run a simple CrewAI agent that responds to specific inputs
    """
    print("\n=== Simple AI Agent with CrewAI ===\n")
    print("This agent will respond to specific inputs with predefined messages.")
    print("Type 'exit' to quit.\n")
    
    # Create a simple agent
    response_agent = Agent(
        role="Customer Service Assistant",
        goal="Provide helpful and accurate responses to user queries",
        backstory="""You are a friendly customer service assistant designed to help
        users with basic questions. You have a set of predefined responses for
        common queries, and you aim to be helpful and polite in all interactions.""",
        verbose=True
    )
    
    # Define predefined responses for specific inputs
    response_patterns = {
        r"(?i)hello|hi|hey|greetings": "Hello! How can I assist you today?",
        r"(?i)how are you": "I'm functioning well, thank you for asking. How can I help you?",
        r"(?i)what is your name": "My name is SimpleAgent, your virtual assistant.",
        r"(?i)bye|goodbye|exit|quit": "Goodbye! Have a great day!",
        r"(?i)thanks|thank you": "You're welcome! Is there anything else I can help with?",
        r"(?i)weather|forecast": "I'm sorry, I don't have real-time weather data. Please check a weather service for accurate forecasts.",
        r"(?i)time|date": f"The current UTC time is {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}.",
        r"(?i)help|commands": "I can respond to greetings, questions about my name, goodbyes, and basic inquiries.",
    }
    
    # Create a response task for the agent
    def create_response_task(user_input):
        return Task(
            description=f"""Respond to the user query: "{user_input}"
            
            If the query matches any of these patterns, use the corresponding response:
            - Greetings (hello, hi): Respond with a friendly greeting
            - Questions about your identity: Explain you're SimpleAgent
            - Goodbyes: Respond with a polite goodbye
            - Thanks: Acknowledge with "you're welcome"
            - Weather questions: Explain you don't have weather data
            - Time/date questions: Provide the current UTC time
            - Help requests: List what you can respond to
            
            For any other queries, politely explain that you're a simple demo agent with limited capabilities.
            Always maintain a helpful and friendly tone.
            """,
            agent=response_agent,
            expected_output="A courteous and appropriate response to the user query."
        )
    
    # Interactive loop
    while True:
        # Get user input
        user_input = input("\nYou: ")
        
        # Check if user wants to exit
        if user_input.lower() == 'exit':
            print("\nAgent: Goodbye! Have a great day!")
            break
            
        # Check for predefined responses
        response = None
        for pattern, reply in response_patterns.items():
            if re.search(pattern, user_input):
                response = reply
                break
        
        # If no predefined response matches, use the agent
        if not response:
            print("\nAgent is thinking...")
            # Create and execute the task
            task = create_response_task(user_input)
            crew = Crew(
                agents=[response_agent],
                tasks=[task],
                verbose=0
            )
            response = crew.kickoff()
        
        # Print the agent's response
        print(f"\nAgent: {response}")

if __name__ == "__main__":
    main()