import openai
from spider import Spider
import requests, os

headers = {
    'Authorization': os.getenv("SPIDER_API_KEY"),
    'Content-Type': 'application/json',
}

json_data = {"search": "python developer jobs in nepal", "search_limit": 5, "limit": 25, "return_format": "raw"}

response = requests.post('https://api.spider.cloud/search', headers=headers, json=json_data)

# Check if the request was successful
if response.status_code == 200:
    try:
        print(response.json())  # Attempt to parse JSON
    except ValueError:  # Handle JSONDecodeError more gracefully
        print("Invalid JSON response")
        print(response.text)  # Print the raw response for debugging
else:
    print(f"Request failed with status code: {response.status_code}")
    print(response.text)  # Print response for debugging purposes

    

# def search(query, limit=5):
#     """Perform a web search using Spider."""
#     params = {"limit": limit, "fetch_page_content": False}
#     print(f"Searching for: {query}")
#     results = spider_client.search(query, params)
#     print(f"Found {len(results)} results.")
#     print(results)
#     return results

# def openai_request(system_content, user_content):
#     """Helper function to make OpenAI API requests."""
#     response = openai_client.chat.completions.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": system_content},
#             {"role": "user", "content": user_content}
#         ]
#     )
#     return response.choices[0].message.content

# def form_search_query(user_query):
#     """Form a search query from the user's input."""
#     search_query = openai_request(
#         "You are an AI research assistant. Your task is to form an effective search query based on the user's question.",
#         f"User's question: {user_query}\n\nPlease provide a concise and effective search query to find relevant information from the web."
#     )
#     return search_query

# def form_final_answer(user_query, summary):
#     """Form a final answer based on the user's query and the summary."""
#     final_answer = openai_request(
#         """
#         You are an AI research assistant. Your task is to form a comprehensive answer to the user's question based on the provided summary.
#         """,
#         f"User's question: {user_query}\n\nSummary of research:\n{summary}\n\nPlease provide a comprehensive answer to the user's question based on this information."
#     )
#     print("Formed final answer.")
#     return final_answer

# def refine_question(original_question):
#     """Refine the search question based on the evaluation."""
#     print("Refining...")
#     return openai_request(
#         "You are an AI research assistant. Your task is to refine a search query based on the original question",
#         f"Original question: {original_question}\n\nPlease provide a refined search query to find more relevant information from the web."
#     )

# def research(user_query, max_iterations=5):
#     """Perform research on the given question."""
#     print(f"Starting research for: {user_query}")
    
#     search_query = form_search_query(user_query)
#     print(f"Search query: {search_query}")
    
#     search_results = search(search_query)
    
#     print(f"Search results: {search_results}")
    
#     combined_summary = "\n".join([result['description'] for result in search_results['content']])
    
#     final_answer = form_final_answer(user_query, combined_summary)
#     return f"Final Answer:\n{final_answer}\n\nBased on:\n{combined_summary}"



# user_input = "frontend developer job descriptions nepal"

# user_query = refine_question(user_input)
# result = research(user_query)
# print(result)

