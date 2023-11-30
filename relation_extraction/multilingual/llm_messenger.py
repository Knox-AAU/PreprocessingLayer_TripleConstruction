class LLMMessenger:

    def process_message(self, response):
        print("Recieved response from Llama2...")
        print(response.text)


    def costruct_prompt_message(data):
        for file in data:
            for sentence in file["sentences"]:
                prompt_message = sentence["sentence"] + " ("
                for em in sentence["entityMentions"]:
                    prompt_message += f"{em['name']}, "
                prompt_message = prompt_message[:-2] + ")" #Remove comma and space after last entity mention
                print(prompt_message)
                #send_request()
