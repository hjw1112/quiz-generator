import json 
import re
import pytesseract 
from PIL import Image
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import OpenAI, ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent


pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

from config import Config



def generate_quiz(text):
    llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["text"], 
        template='Learn the text and generate 20 multiple choice(4 choice) questions about the topics in the text. Output the questions and answers(a,b,c,or d) in 2d array with json form without any other response. here is an output example:{{"question": "Which fruit have red colour?", "a": "apple", "b": "banana", "c": "blueberry", "d": "mango", "answer": "a"}} here is the text: {text}'
    )
    chain = prompt | llm
    response = chain.invoke(text) # getting response form ai
    
    # parsing response to get 2d array
    content = response.content
    print(content)
    try:
        parsed_content = content.strip('```json\n').strip('```')
        array = json.loads(parsed_content)
        # for test
        print(array, "analysed")
        return array
    except (json.JSONDecodeError, AttributeError) as e:
        array = []
        return f"error parsing response: {e}"




def generate_quiz_with_internet(text):

    llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant"),
        ("human", "Get text provided and generate 20 multiple choice(4 choice) questions about the topics in the text. You may use internet to search about the text if it is needed for generating questions. Output the questions and answers(a,b,c,or d) in 2d array with json form without any other response. here is an output example:{{\"question\": \"Which fruit have red colour?\", \"a\": \"apple\", \"b\": \"banana\", \"c\": \"blueberry\", \"d\": \"mango\", \"answer\": \"a\"}} here is the text: {text}"),
        ("placeholder", "{agent_scratchpad}"),
    ])

    search = DuckDuckGoSearchResults()
    tools = [search]
    model_with_tools = llm.bind_tools(tools)


    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    response = agent_executor.invoke({"text": text})
    #print(response)
    #parse and get raw json
    output_text = response.get("output", "")

    match = re.search(r"```json\n(\[.*?\])\n```", output_text, re.DOTALL)
    if match:
        json_data = match.group(1)  # Extract JSON string
        parsed_json = json_data.replace("\n", "").replace("    ", " ")  # Remove newlines and extra spaces
        #print(json_data)  # Print cleaned JSON 
        return parsed_json
    else:
        print("JSON not found.")
        return "error"
    
response = generate_quiz_with_internet("chemistry")
print(response)



