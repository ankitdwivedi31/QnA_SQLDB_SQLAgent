import pandas as pd
from pyprojroot import here
from sqlalchemy import create_engine
import google.generativeai as genai
from langchain_community.utilities import SQLDatabase
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.agent_toolkits import create_sql_agent
import gradio as gr
import os
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.0)


df = pd.read_csv(here("data/for_upload/Accent.csv"))
db_path = str(here("data")) + "/test_sqldb.db"
db_path = f"sqlite:///{db_path}"
engine = create_engine(db_path)
df.to_sql("Accent", engine, index=False, if_exists='replace')
db = SQLDatabase(engine=engine)

def SQLQnA(input):
    agent_executor = create_sql_agent(model, db=db, verbose=True)
    response = agent_executor.invoke({"input": input})
    response = response['output']
    return response
def main():
    demo = gr.Interface(fn=SQLQnA, inputs=[gr.Textbox(label="Type Your Question",lines = 6)],outputs=[gr.Textbox(label="Answer",lines = 4)],title="Query The SQL Database",
                    description="""This Bot provides answers related to Solution Utilization Data""")
    demo.launch()

if __name__ == "__main__":
    main()