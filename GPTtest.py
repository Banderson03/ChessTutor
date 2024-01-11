from openai import OpenAI
import pandas as pd
import time

client = OpenAI(api_key="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")


# Creates the assistant
assistant = client.beta.assistants.create(
    name = "ChessGPT",
    instructions = "You are a helpful assistant for an application meant to help new players learn chess. After receiving FEN notation of the current state of the user's chess game, you will provide only a numbered list of 3 suggested moves and a brief explanation for each of why. An example of how these will be formatted is: Bf4 - (Insert explanation).",
    model = "gpt-4-1106-preview"
)

# Creates a thread
thread = thread = client.beta.threads.create()
print(thread)

# Adds a message to a thread
message = client.beta.threads.messages.create(
    thread_id = thread.id,
    role = "user",
    content = "rnbqkb1r/pp1p1ppp/2p1pn2/8/3P4/2N2N2/PPP1PPPP/R1BQKB1R w KQkq - 0 4"
)
print(message)

# Run the Assistant
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)

# Wait for the Assistant's response
while True:
    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )
    if run.status == "completed":
        break
    time.sleep(0.2)

# Display the Assistant's response
run = client.beta.threads.runs.retrieve(
    thread_id = thread.id,
    run_id = run.id
)

messages = client.beta.threads.messages.list(
    thread_id = thread.id
)

for message in reversed(messages.data):
    print(message.role + ": " + message.content[0].text.value)

