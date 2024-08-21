import requests
from taipy.gui import Gui, State, notify
import authorisation_file

# LLM will use context to set its behaviour
context = ("The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\n",)
conversation = {
    "Conversation": ["Human: Hello, who are you?", "AI: I am an AI created by Google. How can I help you today?"]
}
current_user_message = ""

# Current message being typed by the user
current_user_message = ""

API_URL = authorisation_file.API_URL
headers = {"Authorization": f"Bearer {authorisation_file.HUGGINGFACE_ACCESS_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def request(prompt: str) -> str:
    """
    Send a prompt to the HuggingFace API and return the response.

    Args:
        - state: The current state of the app.
        - prompt: The prompt to send to the API.

    Returns:
        The response from the API.
    """
    output = query(
        {
            "inputs": prompt
        }
    )

    if "error" in output:
        return output.get("error", "An error occurred.")
    
    print(output)
    return output[0]["generated_text"]

def send_message(state: State) -> None:
    """
    Send the user's message to the API and update the conversation.

    Args:
        - state: The current state of the app.
    """
    # Check if the model is still loading
    if "loading" in state.context:
        notify(state, "The model is still loading. Please wait a moment before sending another message.", "info")
        return
    
    # Add the user's message to the context
    state.context += (f"Human: \n {state.current_user_message}\n\n AI:",)
    
    # Convert the context tuple to a single string to send as a prompt
    prompt = "".join(state.context)
    
    # Send the user's message to the API and get the response
    answer = request(prompt).replace("\n", "")
    
    # If the model is loading, store this state in the context
    if "Model loading" in answer:
        state.context += ("loading",)
        notify(state, "The model is currently loading. Please wait a moment and try again.", "info")
        return

    # Remove "loading" state if present
    state.context = tuple(x for x in state.context if x != "loading")

    # Update the context with the AI's answer
    state.context += (f"AI: {answer}\n",)

    # Update the conversation history
    state.conversation["Conversation"] += [f"Human: {state.current_user_message}", f"AI: {answer}"]
    
    # Clear the input field
    state.current_user_message = ""

def style_conv(state: State, idx: int, row: int) -> str:
    """
    Apply a style to the conversation table depending on the message's author.

    Args:
        - state: The current state of the app.
        - idx: The index of the message in the table.
        - row: The row of the message in the table.

    Returns:
        The style to apply to the message.
    """
    if idx is None:
        return None
    elif idx % 2 == 0:
        return "user_message"
    else:
        return "gpt_message"


page = """
<|{conversation}|table|show_all|style=style_conv|>
<|{current_user_message}|input|label=Write your message here...|on_action=send_message|class_name=fullwidth|>
"""

if __name__ == "__main__":
    Gui(page).run(dark_mode=True, title="Taipy Chat")


