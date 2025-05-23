import os
import requests
import json
from typing import Dict, Any
from crewai import Agent, Task, Crew, Tool
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Get API key from environment (you'll need to set this)
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# Define the BaseModel for weather data
class WeatherData(BaseModel):
    location: str = Field(..., description="The city name or location to get weather for")

class WeatherAgent:
    """A weather agent that fetches and reports weather data."""
    
    def __init__(self):
        """Initialize the weather agent with the necessary tools and configuration."""
        # Create a tool for fetching weather data
        self.fetch_weather_tool = Tool(
            name="fetch_weather",
            description="Fetch current weather data for a location",
            func=self._fetch_weather,
            args_schema=WeatherData
        )
        
        # Create the agent with the weather tool
        self.agent = Agent(
            role="Weather Information Specialist",
            goal="Provide accurate and helpful weather information",
            backstory="""You are an expert meteorologist with years of experience 
            analyzing weather patterns and providing forecasts. You have access to 
            real-time weather data and can provide current conditions for locations 
            around the world.""",
            verbose=True,
            tools=[self.fetch_weather_tool],
            allow_delegation=False
        )
        
        # Keep track of agent's state
        self.query_history = []
        
    def _fetch_weather(self, location: str) -> Dict[str, Any]:
        """
        Fetch weather data from OpenWeatherMap API
        
        Args:
            location: City name or location
            
        Returns:
            Dictionary with weather data
        """
        try:
            if not WEATHER_API_KEY:
                # Return mock data if no API key is available
                print("⚠️ No API key found. Using mock weather data.")
                return self._get_mock_weather_data(location)
            
            # Make API request to OpenWeatherMap
            url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={WEATHER_API_KEY}&units=metric"
            response = requests.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "location": location,
                    "temperature": data["main"]["temp"],
                    "feels_like": data["main"]["feels_like"],
                    "humidity": data["main"]["humidity"],
                    "description": data["weather"][0]["description"],
                    "wind_speed": data["wind"]["speed"],
                    "success": True
                }
            else:
                print(f"❌ Error fetching weather: {response.status_code} - {response.text}")
                return {
                    "location": location,
                    "success": False,
                    "error": f"Error {response.status_code}: {response.text}"
                }
                
        except Exception as e:
            print(f"❌ Exception in weather fetch: {str(e)}")
            return {
                "location": location,
                "success": False,
                "error": str(e)
            }
    
    def _get_mock_weather_data(self, location: str) -> Dict[str, Any]:
        """
        Generate mock weather data for demonstration purposes
        
        Args:
            location: City name or location
            
        Returns:
            Dictionary with mock weather data
        """
        import random
        import datetime
        
        # Generate random but plausible weather data
        temp = round(random.uniform(10, 30), 1)  # Temperature between 10-30°C
        feels_like = temp + random.uniform(-3, 3)  # Feels like +/- 3 degrees
        humidity = random.randint(30, 90)  # Humidity between 30-90%
        
        descriptions = [
            "clear sky", "few clouds", "scattered clouds", 
            "broken clouds", "shower rain", "rain", 
            "thunderstorm", "snow", "mist"
        ]
        
        return {
            "location": location,
            "temperature": temp,
            "feels_like": round(feels_like, 1),
            "humidity": humidity,
            "description": random.choice(descriptions),
            "wind_speed": round(random.uniform(0, 10), 1),
            "disclaimer": "MOCK DATA - No API key provided",
            "timestamp": datetime.datetime.now().isoformat(),
            "success": True
        }
        
    def get_weather(self, location: str) -> str:
        """
        Get weather information for a location
        
        Args:
            location: City name or location
            
        Returns:
            String response with weather information
        """
        # Store query in history
        self.query_history.append(f"Weather in {location}")
        
        # Create a task for the agent
        task = Task(
            description=f"""Find the current weather conditions for {location}.
            
            Focus on:
            - Current temperature
            - Feels like temperature
            - Weather description (sunny, cloudy, etc.)
            - Humidity level
            - Wind speed
            
            Use the fetch_weather tool to get real-time data.
            
            Format your response in a user-friendly way with both factual data
            and a brief interpretation of what the weather means for someone
            planning their day.
            """,
            agent=self.agent,
            expected_output="A complete weather report for the specified location"
        )
        
        # Create the crew with just this agent and task
        crew = Crew(
            agents=[self.agent],
            tasks=[task],
            verbose=1
        )
        
        # Get the result
        try:
            result = crew.kickoff()
            return result
        except Exception as e:
            return f"I encountered an error while fetching weather data: {str(e)}"
    
    def get_history(self) -> str:
        """
        Get the history of weather queries
        
        Returns:
            String with the query history
        """
        if not self.query_history:
            return "You haven't made any weather queries yet."
        
        history_list = "\n".join([f"- {query}" for query in self.query_history])
        return f"Your weather query history:\n{history_list}"


def main():
    """Main function to demonstrate the Weather Agent"""
    print("\n=== Advanced AI Weather Agent with CrewAI ===\n")
    print("This agent fetches real-time weather data and provides weather information.")
    print("Type a city name to get the weather, 'history' to see your query history, or 'exit' to quit.\n")
    
    # Initialize the weather agent
    weather_agent = WeatherAgent()
    
    # Interactive loop
    while True:
        # Get user input
        user_input = input("\nEnter a city name (or 'history'/'exit'): ")
        
        # Check for special commands
        if user_input.lower() == 'exit':
            print("\nThank you for using the Weather Agent. Goodbye!")
            break
        elif user_input.lower() == 'history':
            history = weather_agent.get_history()
            print(f"\n{history}")
        else:
            # Get weather for the specified location
            print(f"\nFetching weather for {user_input}...")
            weather_info = weather_agent.get_weather(user_input)
            print(f"\n{weather_info}")


if __name__ == "__main__":
    main()