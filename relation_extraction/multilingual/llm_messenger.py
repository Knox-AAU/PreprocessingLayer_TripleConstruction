from relation_extraction.API_handler import APIHandler
import requests
import re
from llama_cpp import Llama

class LLMMessenger(APIHandler):

    def API_endpoint():
        return ""

    def send_request(request):

        # Put the location of to the GGUF model that you've download from HuggingFace here
        model_path = "./relation_extraction/multilingual/llama-2-7b-chat.Q2_K.gguf"

        # Create a llama model
        model = Llama(model_path=model_path, n_ctx=4092)

        # Prompt creation
        # system_message = """### Instruction ###
        # When given a sentence and the entity mentions in the sentence, you should perform relation extraction.  This includes marking an entity mention as subject, marking another entity mention as object, and identifying the relation between the subject and object. You should only use entity mentions specified in the prompt. You should only use relations from the list of relations given in the context.

        # ### Context ###
        # List of relations: [location, birthPlace, deathPlace, owns, sibling, child, parent, title, employer, age, residence, headquarter, deathCause, member, foundedBy, religion]

        # ### Input Data ###
        # You should perform relation extraction when prompted with input on the following format:
        # "sentence", [comma_separated_list_of_entity_mentions]

        # ### Output Indicator ###
        # If no relation can be found in the sentence, or the entity mentions have not been specified in the user prompt, you should respond with "undefined". In all other cases, your output should be a list of triples on the following format:
        # <subject, relation, object>

        # """
        # user_message = '"Casper and Rytter has the same mother", [Casper, Rytter]'

        prompt = f"""<s>[INST] <<SYS>>
        {request["system_message"]}
        <</SYS>>
        {request["user_message"]} [/INST]"""

        # Model parameters
        max_tokens = 4092

        # Run the model
        output = model(prompt, max_tokens=max_tokens, echo=True)

        # Print the model output
        # print(output["choices"][0]["text"])
        # with open("LlamaResponse.txt", "w") as file:
        #     # Write content to the file
        #     file.write(output["choices"][0]["text"])

        #response = requests.post(url=LLMMessenger.API_endpoint)
        return output

    def process_message(response):
        print("Recieved response from Llama2...")
        triples = []
        answer = re.split("/INST]", response["choices"][0]["text"])[1]
        llama_triples = re.findall("<[\s\w\d]*,[\s\w\d]*,[\s\w\d]*>|\[[\s\w\d]*,[\s\w\d]*,[\s\w\d]*\]", answer)
        for llama_triple in llama_triples:
            triple = re.split(",", llama_triple.replace("<", "").replace(">", "").replace("]", "").replace("[", ""))
            if len(triple) == 3:
                triple_object = {}
                for i, entry in enumerate(triple):
                    triple_object[i.__str__()] = entry.strip()
                triples.append(triple_object)
        return triples

    def check_validity_of_response(sentence, response, relations):
        triples = []
        valid_entity_mentions = [em["name"] for em in sentence["entityMentions"]]
        for triple in response:
            if triple["0"] in valid_entity_mentions and triple["1"] in relations and triple["2"] in valid_entity_mentions: # 0 = subject, 1 = predicate, and 2 = object
                triples.append([[em["iri"] for em in sentence["entityMentions"] if em["name"] == triple["0"]][0], triple["1"], [em["iri"] for em in sentence["entityMentions"] if em["name"] == triple["2"]][0]])
        return triples

    def prompt_llm(data, relations):
        triples = []
        relations_test = ["married", "location", "birthPlace", "deathPlace", "owns", "sibling", "child", "parent", "title", "employer", "age", "residence", "headquarter", "deathCause", "member", "foundedBy", "religion"]
        relations_text = "[" + ", ".join(["location", "birthPlace", "deathPlace", "owns", "sibling", "child", "parent", "title", "employer", "age", "residence", "headquarter", "deathCause", "member", "foundedBy", "religion"]) + "]"
        system_message = f"""### Instruction ###
        When given a sentence and the entity mentions in the sentence, you should perform relation extraction.  This includes marking an entity mention as subject, marking another entity mention as object, and identifying the relation between the subject and object. You should only use entity mentions specified in the prompt. You should only use relations from the list of relations given in the context.

        ### Context ###
        List of relations: {relations_text}

        ### Input Data ###
        You should perform relation extraction when prompted with input on the following format:
        "sentence", [comma_separated_list_of_entity_mentions]

        ### Output Indicator ###
        If no relation can be found in the sentence, or the entity mentions have not been specified in the user prompt, you should respond with "undefined". In all other cases, your output should be a list of triples on the following format:
        <subject, relation, object>

        """

        request = {"system_message": system_message, "user_message": ""}

        for file in data:
            for sentence in file["sentences"]:
                user_message = f'"{sentence["sentence"]}", ['
                for em in sentence["entityMentions"]:
                    user_message += f"{em['name']}, "
                user_message = user_message[:-2] + ']' #Remove comma and space after last entity mention in message
                request["user_message"] = user_message
                response = LLMMessenger.send_request(request)
                process_response = LLMMessenger.process_message(response)
                triples = LLMMessenger.check_validity_of_response(sentence, process_response, relations_test)
        return triples
