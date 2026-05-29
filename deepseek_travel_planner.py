def process_request(self, system_prompt: str, user_prompt: str) -> str:
    try:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
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