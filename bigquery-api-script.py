from google.cloud import bigquery
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAIAPI_KEY"))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"creds/bigquery-gpt-api-key.json"
bq_client = bigquery.Client()

query = """
SELECT *
FROM `esb-integrations.mw.mw_storetraffic`
LIMIT 5000
"""

df = bq_client.query(query).to_dataframe()

data_preview = df.to_csv(index = False)
prompt = f"""
You are a helpful data analyst. here is a table of store traffic data:
{data_preview}
Please summarize the top trends, interesting patterns, or anything that stands out.
"""

response = client.chat.completions.create(
    model = "gpt-3.5-turbo",
    messages = [
        {"role": "system", "content": "You are a helpful data analyst."},
        {"role": "user", "content": prompt}
        ],
    temperature = 0.3
)



print(df.head())
print("\n--- ChatGPT Summary ---\n")
print(response.choices[0].message.content)
