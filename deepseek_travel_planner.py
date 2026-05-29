import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


class TravelPlanner:
    def __init__(self):
        self.client = OpenAI(
            api_key=DEEPSEEK_API_KEY,
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"

    def process_request(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                stream=False
            )

            answer = response.choices[0].message.content

            if answer:
                st.markdown(answer)
                return answer
            else:
                st.warning("The API responded, but the answer was empty.")
                return ""

        except Exception as e:
            st.error(f"Error: {str(e)}")
            return f"Error: {str(e)}"


def get_system_prompts():
    return {
        "Trip Itinerary": """You are a travel expert who creates detailed and personalized trip itineraries.

Follow these guidelines:
1. Start with an overview of the destination
2. Include a day-by-day breakdown of activities
3. Suggest must-visit attractions and hidden gems
4. Provide recommendations for local cuisine and dining
5. Include transportation tips and options
6. Add cultural or historical context for key locations
7. Offer packing tips based on the destination's climate""",

        "Travel Tips": """You are a seasoned traveler who provides practical advice for smooth trips.

Provide tips on:
1. Best times to visit specific destinations
2. Budgeting and saving money while traveling
3. Navigating local customs and etiquette
4. Staying safe and healthy during travel
5. Packing efficiently for different types of trips
6. Finding affordable accommodations and flights
7. Making the most of layovers and short trips""",

        "Destination Recommendations": """You are a travel guide who suggests destinations based on user preferences.

Consider:
1. The traveler's interests, such as adventure, relaxation, or culture
2. Budget constraints
3. Preferred climate and season
4. Travel duration
5. Group size and demographics
6. Accessibility and travel restrictions
7. Unique experiences or events happening at the destination"""
    }


def get_example_prompts():
    return {
        "Trip Itinerary": {
            "placeholder": "Example: Plan a 7-day trip to Korea focusing on culture and food",
            "default": "문화와 음식 체험을 위한 7일간 한국 여행"
        },
        "Travel Tips": {
            "placeholder": "Example: What are the best ways to save money while traveling in Europe?",
            "default": "한국 여행 중 교통비와 식비를 절약하는 방법을 알려줘"
        },
        "Destination Recommendations": {
            "placeholder": "Example: I want a relaxing beach vacation with good food and clear water",
            "default": "문화와 음식 체험을 좋아하는 사람에게 한국 여행지를 추천해줘"
        }
    }


def main():
    st.set_page_config(
        page_title="DeepSeek Travel Assistant",
        page_icon="✈️",
        layout="wide"
    )

    st.title("✈️ DeepSeek Travel Assistant")
    st.markdown("Powered by DeepSeek API chat model.")

    if not DEEPSEEK_API_KEY:
        st.error("DEEPSEEK_API_KEY is missing. Please set it in Render Environment Variables.")
        return

    system_prompts = get_system_prompts()
    example_prompts = get_example_prompts()

    st.sidebar.title("Settings")

    mode = st.sidebar.selectbox(
        "Choose Mode",
        ["Trip Itinerary", "Travel Tips", "Destination Recommendations"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Current Mode:** {mode}")
    st.sidebar.markdown("**Mode Description:**")
    st.sidebar.markdown(system_prompts[mode].replace("\n", "\n\n"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Input for {mode}")

        user_prompt = st.text_area(
            "Enter your travel preferences or questions:",
            height=300,
            placeholder=example_prompts[mode]["placeholder"],
            value=example_prompts[mode]["default"]
        )

        process_button = st.button(
            "✈️ Process",
            type="primary",
            use_container_width=True
        )

    with col2:
        st.markdown("### Output")

        if process_button:
            if user_prompt.strip():
                with st.spinner("Planning your trip..."):
                    assistant = TravelPlanner()
                    assistant.process_request(system_prompts[mode], user_prompt)
            else:
                st.warning("⚠️ Please enter some input!")


if __name__ == "__main__":
    main()