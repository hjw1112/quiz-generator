import json 
from langchain.prompts import PromptTemplate
from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, Tool
from langchain_community.tools import DuckDuckGoSearchResults

from config import Config


def generate_quiz(text):
    llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
    prompt = PromptTemplate(
        input_variables=["text"], 
        template="Learn the text and generate 20 multiple choice(4 choice) questions about the topics in the text. Output the questions in 2d array with json form. here is the text: {text}"
    )
    chain = prompt | llm
    response = chain.invoke(text) # getting response form ai
    
    # parsing response to get 2d array
    content = response.content

    try:
        parsed_content = content.strip('```json\n').strip('```')
        array = json.loads(parsed_content)
        # for test
        print(array, "analysed")
        return array
    except (json.JSONDecodeError, AttributeError) as e:
        array = []
        return "error parsing response: {e}"




def generate_quiz_with_internet(text):
    search = DuckDuckGoSearchResults()

    search_tool = Tool(
        name="internet_search",
        func=search.run,
        description="Use this to search the internet for the latest or unknown information."
    )

    llm = ChatOpenAI(model="gpt-4o", api_key=Config.OPENAI_API_KEY)
    prompt_template = PromptTemplate(
        input_variables=["text"], 
        template="Learn the text and generate 20 multiple choice(4 choice) questions about the topics in the text. You may use internet to search about the text if it is needed for generating questions. Output the questions in 2d array with json form. here is the text: {text}"
    )

    prompt = prompt_template.format(text=text)

    agent = initialize_agent(
    tools=[search_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True,
    handle_parsing_errors=True
    )

    response = agent.invoke(prompt)
    print(response)
    return response

response = generate_quiz_with_internet("chemistry")
print(response)



