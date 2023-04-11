import json
import random

#// Gen recent messages
def get_recent_messages():

    #// Define the file name and learn instruction
    file_name = "stored_data.json"
    learn_instruction = {
        "role": "system",
        "content": "You are trying to have a casual coversation to the user. Ask short questions that are relevant to the subject. You're name is Rachel. The user is called 7-7-4. keep your answers no more than 30 words", 
    }


    #// Initialize messages
    messages = []

    #// Add a random element
    x = random.uniform(0, 1)
    if x < 0.2:
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include some humor, a lot of sarcastic coments, and some random facts about machines."

    else: 
        learn_instruction["content"] = learn_instruction["content"] + " Your response will include asking me to repeat something back to you in general coversation."

    #// Append instruction to messages
    messages.append(learn_instruction)


    #// Get last messages
    try:
        with open(file_name) as user_file:
            data = json.load(user_file)

        #// Append the last five items of date
        if data:
            if len(data) < 5:
                for item in data:
                    messages.append(item)
            else:
                for item in data[-5:]:
                    messages.append(item)

    except Exception as e:
        print(e)
        pass


    #// Return messages
    return messages


#// Store Messages
def store_messages(request_messages, resopnse_message):

    #// Define the file name
    file_name = "stored_data.json"

    #// Get recent messages
    messages = get_recent_messages()[1:]

    #// Add messages to data
    user_message = {"role": "user", "content": request_messages}
    assistant_message = {"role": "assistant", "content": resopnse_message}
    messages.append(user_message)
    messages.append(assistant_message)


    #// Save the updated file
    with open(file_name, "w") as f:
        json.dump(messages, f)

#// Reset messages
def reset_messages():

    #// Overwrite the file
    open("stored_data.json", "w")



    
