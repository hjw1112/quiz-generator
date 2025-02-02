import json 
import re
import os
import time
import pytesseract 
from PIL import Image
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from ..config.config import Config


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def call_with_retry(agent_executor, query, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return agent_executor.invoke({"text": query})
        except Exception as e:
            print(f"Error: {e} (Attempt {attempt+1}/{retries})")
            time.sleep(delay)
    raise Exception("Failed after multiple attempts.")



def generate_quiz(text):
    llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["text"], 
        template="Learn the text and generate 20 multiple choice(4 choice) questions about the topics in the text. Output the questions and answers(a,b,c,or d) in 2d array dictionary json form without any other response. here is an output example(ignore backslashes):{{'text': 'chemistry', 'output': '[{{\"question\": \"What is the primary focus of chemistry?\", \"a\": \"The study of electrical circuits\", \"b\": \"The study of geographical phenomena\", \"c\": \"The study of matter and its interactions\", \"d\": \"The study of historical events\", \"answer\": \"c\"}}, {{\"question\": \"Which of the following is not a branch of chemistry?\", \"a\": \"Organic Chemistry\", \"b\": \"Physical Chemistry\", \"c\": \"Astrological Chemistry\", \"d\": \"Analytical Chemistry\", \"answer\": \"c\"}}, {{\"question\": \"Chemistry is often called the central science because it bridges which areas?\", \"a\": \"Physics and mathematics\", \"b\": \"Biology and geology\", \"c\": \"Physics and biology\", \"d\": \"Astronomy and Earth science\", \"answer\": \"c\"}}, {{\"question\": \"Which branch of chemistry focuses on carbon-containing compounds?\", \"a\": \"Inorganic Chemistry\", \"b\": \"Physical Chemistry\", \"c\": \"Organic Chemistry\", \"d\": \"Biochemistry\", \"answer\": \"c\"}}, {{\"question\": \"What is the primary method used by chemists to ensure systematic study?\", \"a\": \"The scientific method\", \"b\": \"Traditional observation\", \"c\": \"Mythical reasoning\", \"d\": \"Astrological predictions\", \"answer\": \"a\"}}, {{\"question\": \"What unit system is commonly used in chemistry?\", \"a\": \"Imperial system\", \"b\": \"Metric system\", \"c\": \"U.S. customary units\", \"d\": \"Ancient Egyptian units\", \"answer\": \"b\"}}, {{\"question\": \"Which branch of chemistry deals with the study of reaction rates and mechanisms?\", \"a\": \"Physical Chemistry\", \"b\": \"Analytical Chemistry\", \"c\": \"Biochemistry\", \"d\": \"Kinetics\", \"answer\": \"a\"}}, {{\"question\": \"Which branch of chemistry applies to the study of metals and minerals?\", \"a\": \"Organic Chemistry\", \"b\": \"Inorganic Chemistry\", \"c\": \"Plasmas Chemistry\", \"d\": \"Polymer Chemistry\", \"answer\": \"b\"}}, {{\"question\": \"What is a key application of chemistry in agriculture?\", \"a\": \"Developing new languages\", \"b\": \"Water purification systems\", \"c\": \"Fertilizer and pesticide development\", \"d\": \"Creation of new species\", \"answer\": \"c\"}}, {{\"question\": \"Which type of chemistry involves the study of the energy changes in chemical reactions?\", \"a\": \"Energetic Chemistry\", \"b\": \"Kinetic Chemistry\", \"c\": \"Thermochemistry\", \"d\": \"Chemical Physics\", \"answer\": \"c\"}}, {{\"question\": \"What does the field of analytical chemistry focus on?\", \"a\": \"The creation of art\", \"b\": \"Analyzing compositions of substances\", \"c\": \"The evolution of species\", \"d\": \"Collecting historical data\", \"answer\": \"b\"}}, {{\"question\": \"Biochemistry is a branch of chemistry involved in the study of what?\", \"a\": \"Inorganic materials\", \"b\": \"The human genome\", \"c\": \"Chemical processes in living organisms\", \"d\": \"Artificial intelligence\", \"answer\": \"c\"}}, {{\"question\": \"Which branch of chemistry focuses specifically on crystal structures?\", \"a\": \"Crystallography\", \"b\": \"Astrochemistry\", \"c\": \"Solid State Physics\", \"d\": \"Chemical Botany\", \"answer\": \"a\"}}, {{\"question\": \"In which industry is chemistry NOT commonly applied?\", \"a\": \"Medicine\", \"b\": \"Textiles\", \"c\": \"Coal mining\", \"d\": \"Sculpture\", \"answer\": \"d\"}}, {{\"question\": \"What is an isotope in chemistry?\", \"a\": \"A type of element based on color\", \"b\": \"Atoms of the same element with different numbers of neutrons\", \"c\": \"A rare earth metal\", \"d\": \"A type of bond\", \"answer\": \"b\"}}, {{\"question\": \"What is the role of a catalyst in a chemical reaction?\", \"a\": \"To increase the energy requirement\", \"b\": \"To change the end products\", \"c\": \"To speed up the reaction\", \"d\": \"To decrease the temperature\", \"answer\": \"c\"}}, {{\"question\": \"The pH scale in chemistry is used to measure what?\", \"a\": \"The purity of substances\", \"b\": \"Acidity and basicity of solutions\", \"c\": \"The weight of molecules\", \"d\": \"Temperature consistency\", \"answer\": \"b\"}}, {{\"question\": \"Which element is known as the building block of life in chemistry?\", \"a\": \"Helium\", \"b\": \"Carbon\", \"c\": \"Oxygen\", \"d\": \"Nitrogen\", \"answer\": \"b\"}}, {{\"question\": \"What is Avogadro\'s number used for in chemistry?\", \"a\": \"Calculating the weight of solutions\", \"b\": \"Determining temperature changes\", \"c\": \"Counting atoms or molecules\", \"d\": \"Measuring time intervals\", \"answer\": \"c\"}}, {{\"question\": \"Which of the following is a chemical change?\", \"a\": \"Ice melting\", \"b\": \"Water evaporating\", \"c\": \"Iron rusting\", \"d\": \"Gas compressing\", \"answer\": \"c\"}}]'}} here is the text: {text}"
    )
    chain = prompt | llm
    response = chain.invoke(text) # getting response form ai
    
    

    #parsing response to get 2d array
    content = response.content
    print(content,"content")
    try:
        parsed_content = content.strip('```json\n').strip('```')
        print(parsed_content,"parsed_content")
        array = json.loads(parsed_content)
        print(array,"array")
        # for test
        text = array
        print(text,"text")
        output_text = text.get("output", "")
        print(output_text, "output")
        
        return output_text
    except (json.JSONDecodeError, AttributeError) as e:
        array = []
        return f"error parsing response: {e}"



def generate_quiz_with_internet(text):

    llm = ChatOpenAI(model="gpt-4o", request_timeout=60, max_retries=5, api_key=Config.OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "Get text provided and generate 20 multiple choice(4 choice) questions about the topics in the text. You may use internet to search about the text if it is needed for generating questions. Output the questions and answers(a,b,c,or d) in 2d array with json form without any other response. here is an output example(ignore backslashes): [{{\"question\": \"What is the primary focus of chemistry?\", \"a\": \"The study of electrical circuits\", \"b\": \"The study of geographical phenomena\", \"c\": \"The study of matter and its interactions\", \"d\": \"The study of historical events\", \"answer\": \"c\"}}, {{\"question\": \"Which of the following is not a branch of chemistry?\", \"a\": \"Organic Chemistry\", \"b\": \"Physical Chemistry\", \"c\": \"Astrological Chemistry\", \"d\": \"Analytical Chemistry\", \"answer\": \"c\"}}, {{\"question\": \"Chemistry is often called the central science because it bridges which areas?\", \"a\": \"Physics and mathematics\", \"b\": \"Biology and geology\", \"c\": \"Physics and biology\", \"d\": \"Astronomy and Earth science\", \"answer\": \"c\"}}, {{\"question\": \"Which branch of chemistry focuses on carbon-containing compounds?\", \"a\": \"Inorganic Chemistry\", \"b\": \"Physical Chemistry\", \"c\": \"Organic Chemistry\", \"d\": \"Biochemistry\", \"answer\": \"c\"}}, {{\"question\": \"What is the primary method used by chemists to ensure systematic study?\", \"a\": \"The scientific method\", \"b\": \"Traditional observation\", \"c\": \"Mythical reasoning\", \"d\": \"Astrological predictions\", \"answer\": \"a\"}}, {{\"question\": \"What unit system is commonly used in chemistry?\", \"a\": \"Imperial system\", \"b\": \"Metric system\", \"c\": \"U.S. customary units\", \"d\": \"Ancient Egyptian units\", \"answer\": \"b\"}}, {{\"question\": \"Which branch of chemistry deals with the study of reaction rates and mechanisms?\", \"a\": \"Physical Chemistry\", \"b\": \"Analytical Chemistry\", \"c\": \"Biochemistry\", \"d\": \"Kinetics\", \"answer\": \"a\"}}, {{\"question\": \"Which branch of chemistry applies to the study of metals and minerals?\", \"a\": \"Organic Chemistry\", \"b\": \"Inorganic Chemistry\", \"c\": \"Plasmas Chemistry\", \"d\": \"Polymer Chemistry\", \"answer\": \"b\"}}, {{\"question\": \"What is a key application of chemistry in agriculture?\", \"a\": \"Developing new languages\", \"b\": \"Water purification systems\", \"c\": \"Fertilizer and pesticide development\", \"d\": \"Creation of new species\", \"answer\": \"c\"}}, {{\"question\": \"Which type of chemistry involves the study of the energy changes in chemical reactions?\", \"a\": \"Energetic Chemistry\", \"b\": \"Kinetic Chemistry\", \"c\": \"Thermochemistry\", \"d\": \"Chemical Physics\", \"answer\": \"c\"}}, {{\"question\": \"What does the field of analytical chemistry focus on?\", \"a\": \"The creation of art\", \"b\": \"Analyzing compositions of substances\", \"c\": \"The evolution of species\", \"d\": \"Collecting historical data\", \"answer\": \"b\"}}, {{\"question\": \"Biochemistry is a branch of chemistry involved in the study of what?\", \"a\": \"Inorganic materials\", \"b\": \"The human genome\", \"c\": \"Chemical processes in living organisms\", \"d\": \"Artificial intelligence\", \"answer\": \"c\"}}, {{\"question\": \"Which branch of chemistry focuses specifically on crystal structures?\", \"a\": \"Crystallography\", \"b\": \"Astrochemistry\", \"c\": \"Solid State Physics\", \"d\": \"Chemical Botany\", \"answer\": \"a\"}}, {{\"question\": \"In which industry is chemistry NOT commonly applied?\", \"a\": \"Medicine\", \"b\": \"Textiles\", \"c\": \"Coal mining\", \"d\": \"Sculpture\", \"answer\": \"d\"}}, {{\"question\": \"What is an isotope in chemistry?\", \"a\": \"A type of element based on color\", \"b\": \"Atoms of the same element with different numbers of neutrons\", \"c\": \"A rare earth metal\", \"d\": \"A type of bond\", \"answer\": \"b\"}}, {{\"question\": \"What is the role of a catalyst in a chemical reaction?\", \"a\": \"To increase the energy requirement\", \"b\": \"To change the end products\", \"c\": \"To speed up the reaction\", \"d\": \"To decrease the temperature\", \"answer\": \"c\"}}, {{\"question\": \"The pH scale in chemistry is used to measure what?\", \"a\": \"The purity of substances\", \"b\": \"Acidity and basicity of solutions\", \"c\": \"The weight of molecules\", \"d\": \"Temperature consistency\", \"answer\": \"b\"}}, {{\"question\": \"Which element is known as the building block of life in chemistry?\", \"a\": \"Helium\", \"b\": \"Carbon\", \"c\": \"Oxygen\", \"d\": \"Nitrogen\", \"answer\": \"b\"}}, {{\"question\": \"What is Avogadro\'s number used for in chemistry?\", \"a\": \"Calculating the weight of solutions\", \"b\": \"Determining temperature changes\", \"c\": \"Counting atoms or molecules\", \"d\": \"Measuring time intervals\", \"answer\": \"c\"}}, {{\"question\": \"Which of the following is a chemical change?\", \"a\": \"Ice melting\", \"b\": \"Water evaporating\", \"c\": \"Iron rusting\", \"d\": \"Gas compressing\", \"answer\": \"c\"}}] here is the text: {text}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    search = DuckDuckGoSearchResults()
    tools = [search]
    model_with_tools = llm.bind_tools(tools)


    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    response = call_with_retry(agent_executor, text)
    print(response)

    output_text = response.get("output", "").strip()

    match = re.search(r"```json\n(\[.*?\])\n```", output_text, re.DOTALL)
    if match:
        json_string = match.group(1)
    else:
        json_string = output_text

    try:
        parsed_json = json.loads(json_string)
        clean_json_string = json.dumps(parsed_json, separators=(",", ":"))
        print(clean_json_string)
        return(clean_json_string)
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in 'output' field.")
        return "error"
    