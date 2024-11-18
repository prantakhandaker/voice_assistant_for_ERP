from qdrant_client import QdrantClient
from llama_index.llms.ollama import Ollama
from llama_index.core import SimpleDirectoryReader
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core import ServiceContext, VectorStoreIndex
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.storage.storage_context import StorageContext

import warnings
warnings.filterwarnings("ignore")

# class AIVoiceAssistant:
#     def __init__(self):
#         self._qdrant_url = "http://localhost:6333"
#         self._client = QdrantClient(url=self._qdrant_url, prefer_grpc=False)
#         self._llm = Ollama(model="mistral", request_timeout=120.0)
#         self._service_context = ServiceContext.from_defaults(llm=self._llm, embed_model="local")
#         self._index = None
#         self._create_kb()
#         self._create_chat_engine()

#     def _create_chat_engine(self):
#         memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
#         self._chat_engine = self._index.as_chat_engine(
#             chat_mode="context",
#             memory=memory,
#             system_prompt=self._prompt,
#         )

#     def _create_kb(self):
#         try:
#             reader = SimpleDirectoryReader(
#                 input_files=[r"rag\erp_instructions.txt"]
#             )
#             documents = reader.load_data()
#             vector_store = QdrantVectorStore(client=self._client, collection_name="erp_db")
#             storage_context = StorageContext.from_defaults(vector_store=vector_store)
#             self._index = VectorStoreIndex.from_documents(
#                 documents, service_context=self._service_context, storage_context=storage_context
#             )
#             print("Knowledgebase created successfully!")
#         except Exception as e:
#             print(f"Error while creating knowledgebase: {e}")

#     def interact_with_llm(self, customer_query):
#         AgentChatResponse = self._chat_engine.chat(customer_query)
#         answer = AgentChatResponse.response
#         return answer

#     @property
#     def _prompt(self):
#         return """
#             You are an AI Assistant integrated with an ERP system for employees in a corporate environment in UAE.
#             You can communicate in both English and Arabic.
#             Your tasks include automating fund requests, task tracking
            
#             Follow these steps in your interaction:
#             - Greet the user.
#             - Ask for required details for the task one by one.
#             - Confirm the details before processing the request.
#             - For incomplete inputs, politely ask for the missing information.
#             - If you don’t know the answer, say 'I don’t know'.
            
#             Example Tasks:
#             - Fund request: "Request money for project 223, 500 riyals for tools."
#             - Task update: "Mark task ID 1012 as completed."
            
#             Keep your responses concise and professional.
#             """



import re
import json

class AIVoiceAssistant:
    def __init__(self):
        self._qdrant_url = "http://localhost:6333"
        self._client = QdrantClient(url=self._qdrant_url, prefer_grpc=False)
        self._llm = Ollama(model="mistral", request_timeout=120.0)
        self._service_context = ServiceContext.from_defaults(llm=self._llm, embed_model="local")
        self._index = None
        self.projects = self.load_projects()  # Load projects and budgets
        self._create_kb()
        self._create_chat_engine()

    def _create_chat_engine(self):
        memory = ChatMemoryBuffer.from_defaults(token_limit=1500)
        self._chat_engine = self._index.as_chat_engine(
            chat_mode="context",
            memory=memory,
            system_prompt=self._prompt,
        )

    def _create_kb(self):
        try:
            reader = SimpleDirectoryReader(input_files=["erp_instructions.txt"])
            documents = reader.load_data()
            vector_store = QdrantVectorStore(client=self._client, collection_name="erp_db")
            storage_context = StorageContext.from_defaults(vector_store=vector_store)
            self._index = VectorStoreIndex.from_documents(
                documents, service_context=self._service_context, storage_context=storage_context
            )
            print("Knowledgebase created successfully!")
        except Exception as e:
            print(f"Error while creating knowledgebase: {e}")

    @property
    def _prompt(self):
        return """
        You are an ERP AI Assistant. Your job is to assist employees with fund requests.
        You understand English and Arabic. Follow these instructions:
        - Confirm if the project name or ID exists.
        - Check if the requested amount is within the project's budget.
        - Confirm details before finalizing the request.
        """

    def load_projects(self, file_path='erp_instructions.txt'):
        """Load project IDs, names, and budget limits from the file."""
        projects = {}
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    match = re.match(
                        r"- Project ID: (\d+) \| Name: (.+?) \| Budget: ([\d,]+) Riyals", line
                    )
                    if match:
                        project_id = match.group(1)
                        project_name = match.group(2).strip().lower()
                        budget = float(match.group(3).replace(",", ""))
                        projects[project_name] = {"id": project_id, "budget": budget}
                        projects[project_id] = {"name": project_name, "budget": budget}
        except FileNotFoundError:
            print(f"Error: {file_path} not found.")
        except ValueError:
            print(f"Error: Incorrect format in {file_path}.")
        return projects

    def extract_fund_request(self, text):
        """Extract amount and project name or ID from the employee's speech."""
        # Extract the amount (e.g., "1000$" or "1000 dollars")
        amount_match = re.search(r'(\d+)\s*\$?', text)
        amount = int(amount_match.group(1)) if amount_match else None

        # Extract project name or ID
        project = None
        for key in self.projects.keys():
            if key in text.lower():
                project = key
                break

        return amount, project

    def validate_request(self, amount, project):
        """Validate if the requested amount is within the project's budget."""
        if project in self.projects:
            budget_limit = self.projects[project]["budget"]
            return amount <= budget_limit
        return False

    def save_order(self, order_data, file_path='order.json'):
        """Save the validated order to a JSON file."""
        try:
            with open(file_path, 'a') as file:
                json.dump(order_data, file)
                file.write('\n')  # New line for each order entry
            print("Order saved successfully!")
        except Exception as e:
            print(f"Error saving order: {e}")

    def interact_with_llm(self, customer_query):
        # Get AI response (optional if using to clarify with the user)
        AgentChatResponse = self._chat_engine.chat(customer_query)
        ai_response = AgentChatResponse.response
        print(f"AI Assistant: {ai_response}")

        # Extract details from the query
        amount, project = self.extract_fund_request(customer_query)

        if amount and project:
            # Validate the request
            if self.validate_request(amount, project):
                order_data = {
                    "project_id": self.projects[project].get("id", project),
                    "project_name": self.projects[project].get("name", project),
                    "amount": amount
                }
                # Save order to JSON file
                self.save_order(order_data)
                return f"Request approved: {amount}$ for project {self.projects[project].get('name', project)}."
            else:
                return f"Request denied: Exceeds budget for project {self.projects[project].get('name', project)}."
        else:
            return "Could not understand the project name/ID or amount."


