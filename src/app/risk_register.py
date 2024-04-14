import boto3
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import gradio as gr
import pandas as pd

from langchain_core.output_parsers.xml import XMLOutputParser
from langchain_community.chat_models import BedrockChat
from prompts import rr_prompt as prompt

LLM_TEMPERATURE = 0.0
LLM_MODEL_ID = 'anthropic.claude-v2'
LLM_MAX_OUT_TOKENS = 10000

def load_csv_data(
        input_file: str
    ) -> gr.Dataframe:
    input_file = input_file.name
    print(f'Opening CSV: {input_file}')
    df = pd.read_csv(input_file)
    return df

def generate_rr(
        assets: pd.DataFrame,
        scenarios: pd.DataFrame
    ) -> gr.Dataframe:
    parser = XMLOutputParser()

    session = boto3.Session()
    bedrock = session.client('bedrock-runtime')

    llm = BedrockChat(
            model_id = LLM_MODEL_ID, 
            client = bedrock, 
            model_kwargs = {
              "temperature": LLM_TEMPERATURE
            }
          )

    rules = """
        1. Please only output requested schema, do not add any additional information.
    """

    chain = (prompt | llm | parser)
    output = chain.invoke({
      'rules' : rules,
      'assets' : assets.to_xml(root_name='Assets', row_name='Asset', xml_declaration=False), 
      'scenarios' : scenarios.to_xml(root_name='Scenarios', row_name='Scenario', xml_declaration=False)
      })

    print(output)

    flattened_data = []
    for item in output['result'][1]['risks']:
        flattened_dict = {}
        for entry in item['risk']:
            flattened_dict.update(entry)
        flattened_data.append(flattened_dict)

    return pd.DataFrame(flattened_data) 

with gr.Blocks() as app:
  with gr.Row():
    with gr.Accordion(open=False, label='Assets'):
      with gr.Row():
        rr_input_r_assets_f = gr.File(file_types=['.csv', '.xlsx', '.xls'])
      with gr.Row():
        rr_input_r_assets_load_btn = gr.Button('Load assets (CSV)')
      with gr.Row():
        rr_input_r_assets_inv = gr.Dataframe(label='Asset Inventory')
  with gr.Row():
    with gr.Accordion(open=False, label='Risk Scenarios'):
      with gr.Row():
        rr_input_r_scenarios_f = gr.File(file_types=['.csv', '.xlsx', '.xls'])
      with gr.Row():
        rr_input_r_scenarios_load_btn = gr.Button('Load risk scenarios (CSV)')
      with gr.Row():
        rr_input_r_scenarios_reg = gr.Dataframe(label='Risk Scenarios Register')
  with gr.Row():
    rr_create_btn = gr.Button('Create Risk Register')
  with gr.Row():
    rr_create_log = gr.Text(label='Creation log')
  with gr.Row():
    rr_output = gr.Dataframe(label='Generated Risk Register')

  rr_input_r_assets_load_btn.click(
    fn=load_csv_data, 
    inputs=[rr_input_r_assets_f], 
    outputs=[rr_input_r_assets_inv]
    )
  
  rr_input_r_scenarios_load_btn.click(
    fn=load_csv_data, 
    inputs=[rr_input_r_scenarios_f], 
    outputs=[rr_input_r_scenarios_reg]
    )
  
  rr_create_btn.click(
    fn=generate_rr, 
    inputs=[rr_input_r_assets_inv, rr_input_r_scenarios_reg], 
    outputs=[rr_output]
  )

app.launch(server_name='0.0.0.0', server_port=8080)