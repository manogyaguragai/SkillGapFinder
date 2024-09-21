import re
from htmlwebshot import WebShot
from llama_index.tools.duckduckgo import DuckDuckGoSearchToolSpec
from io import BytesIO
import streamlit as st
import difflib

def find_closest_match(urls, job, industry):
  pattern = f"roadmap\\.sh/({job}|{industry})"
  matching_urls = [url for url in urls if re.search(pattern, url)]
    
  if matching_urls:
    return matching_urls[0]  # If an exact match is found, return it
    
  closest_match = difflib.get_close_matches(f"roadmap.sh/{job}", urls, n=1, cutoff=0.6)
    
  if not closest_match:
    closest_match = difflib.get_close_matches(f"roadmap.sh/{industry}", urls, n=1, cutoff=0.6)
    
  return closest_match[0] if closest_match else None

  
  
def get_flowchart(urls, data):
  job = data.get('job')
  industry = data.get('industry')
  
  user_question = f'{job or industry} roadmap from roadmap.sh'  
  
  print(f'Flowchart query: \n\n {user_question}')
  
  tool_spec = DuckDuckGoSearchToolSpec()

  if user_question != "None":
    search_results = tool_spec.duckduckgo_full_search(query=user_question, max_results=5,region="np-np") 
  else:
    search_results = "None"
    
  try:
    urls = [item['href'] for item in search_results]
  except:
    urls = []
  
  best_url = find_closest_match(urls, job, industry)
  
  st.write(best_url)
  
  if isinstance(best_url, list):
     return None
  
  screenshot_buffer = BytesIO()
  
  WebShot.create_pic(self=WebShot(), html=best_url, output=screenshot_buffer)
    
  screenshot_data = screenshot_buffer.getvalue()
  
  screenshot_buffer.close()

  return screenshot_data
  

  
  
  