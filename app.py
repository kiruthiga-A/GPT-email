import streamlit as st
import openai
import traceback

class ChatGPTApp:
    def __init__(self):
        self.objective_placeholder = "Write an email for"
        self.temperature_options = {
            "Deterministic": 0,
            "Accurate": 0.3,
            "Balanced": 0.5,
            "Creative": 0.7,
            "Diverse": 1
        }

    def run(self):
        self.create_sidebar()
        st.title("ChatGPT Email Prompt Generator")
        self.create_prompt_section()
        self.create_prompt_button()
        self.create_submit_button()

    def create_sidebar(self):
        with st.sidebar:
            self.openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
            "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
            "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
            "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    def create_prompt_section(self):
        # Input fields for various text prompts
        self.objective = st.text_input("Objective (Required) The more clear and detailed the objective the better the email will be.", value=self.objective_placeholder)
        self.persona = st.text_input("Your Persona (E.g: CEO, CTO, Marketer, Account executive, Sales Representative, Engineer, HR etc.,)")
        self.sender_name = st.text_input("Sender's Name", value="[SENDERS NAME]")
        self.receiver_name = st.text_input("Receiver's Name", value="[RECEIVER NAME]")
        self.context = st.text_input("Context of Email (E.g: previous conversation, follow up, )")
        self.num_words = st.text_input("Number of Words", value="75 to 100")
        self.other_constraints = st.text_input("Other Constraints (E.g: Add relevant quote or wise sayings)")
        self.audience = st.text_input("Audience (Job position, Education qualification- Graduate level, 5th grade etc., )")
        self.extra_details = st.text_input("Extra Details: (E.g: What Industry?, readers strength, weakness etc.,)")

        # Dropdown menu for tone
        self.tone_options = ["Professional", "Friendly", "Urgent", "Emotional",
                             "Conversational", "Persuasive", "Positivite", "Direct and witty",
                             "Polite and indirect language", "Sarcastic", "Hopeful", "Encouraging",
                             "apologetic"]
        self.selected_tone = st.selectbox("Tone", self.tone_options)
        self.temperature_string = st.radio(
            "Deterministic Vs Diverse",
            list(self.temperature_options.keys()))

        self.temperature = self.temperature_options.get(self.temperature_string)

    def create_prompt_button(self):
        self.create_button = st.button("Create Prompt", key="Create", on_click=self.create_prompt)

    def create_prompt(self):
        self.prompt_template = []
        # Check if the Objective field is empty
        if self.objective != self.objective_placeholder:
            self.prompt_template.append(f"Objective: {self.objective}")
            st.session_state.create_clicked = True
            self.agg_prompt()
            
        else:
            st.error("Objective cannot be empty, please provide an objective")

    def create_submit_button(self):
        if "create_clicked" in st.session_state:  # Only show the submit button if Create Prompt has been clicked
            submit_button_var = st.button("Submit Prompt", key="Submit")
            if submit_button_var:
                # Check if API token is provided
                if not self.openai_api_key:
                    st.warning("Please enter your OpenAI API key. You can get a key at https://platform.openai.com/account/api-keys")
                else:
                    # Send the edited prompt to the ChatGPT API using the provided token
                    self.call_gpt(st.session_state.prompt_template, self.temperature)
                    st.success("Prompt submitted successfully.")

    def agg_prompt(self):
        # Add other fields to the prompt template if they are not empty
        if self.persona:
            self.prompt_template.append(f"Persona: {self.persona}")
        if self.sender_name:
            self.prompt_template.append(f"Sender's Name: {self.sender_name}")
        if self.receiver_name:
            self.prompt_template.append(f"Receiver's Name: {self.receiver_name}")
        if self.context:
            self.prompt_template.append(f"Context of Email: {self.context}")
        if self.num_words:
            self.prompt_template.append(f"Number of Words: {self.num_words}")
        if self.other_constraints:
            self.prompt_template.append(f"Other Constraints: {self.other_constraints}")
        if self.audience:
            self.prompt_template.append(f"Audience: {self.audience}")
        if self.extra_details:
            self.prompt_template.append(f"Extra Details : {self.extra_details}")

        self.prompt_template.append(f"Tone: {self.selected_tone}")

        # Store the prompt template in a variable for submission
        compiled_prompt = "\n".join(self.prompt_template)

        # Display the populated prompt template
        st.write("Populated Prompt Template:")
        for item in self.prompt_template:
            st.write(item)
        st.session_state.prompt_template = compiled_prompt
        
        # Use HTML and CSS to position the text_area below the submit button
        st.markdown(
            """<style>
            .stTextInput {
                order: 2 !important;
            }
            .stButton {
                order: 1 !important;
            }
            </style>""",
            unsafe_allow_html=True,
        )

        # Text area for editing the prompt (positioned below the submit button)
        st.text_area("Edit Prompt", value=compiled_prompt, on_change=self.update_prompt, key="updated_prompt_text")

    def update_prompt(self):
        st.session_state.prompt_template = st.session_state.updated_prompt_text
        
    def call_gpt(self, prompt_template, temperature):
        try:
            openai.api_key = self.openai_api_key
            result = openai.Completion.create(model="gpt-3.5-turbo-instruct",
                                                prompt=prompt_template,
                                                max_tokens=400,
                                                temperature=temperature)
            st.markdown(result['choices'][0]['text'])
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            print(traceback.format_exc())

if __name__ == "__main__":
    app = ChatGPTApp()
    app.run()
