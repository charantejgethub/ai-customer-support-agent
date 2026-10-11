# AI Customer Support Agent

An LLM-powered customer support application that helps customers retrieve order information, understand store policies, and raise support tickets through a conversational interface.

Built with Python, OpenAI, Streamlit, SQLite, tool calling, and Retrieval-Augmented Generation (RAG).

## Features

- **Conversational AI:** Interacts with customers using an OpenAI language model.
- **Customer Identification:** Identifies customers using their email address.
- **Order Management:** Retrieves customer-specific orders and checks order status.
- **Product Information:** Retrieves product details, prices, and stock availability.
- **Support Ticket Management:** Creates support tickets after customer confirmation and associates tickets with relevant orders.
- **Order Ownership Verification:** Checks that an order belongs to the identified customer before providing order-specific information or creating an order-linked ticket.
- **RAG-Based Knowledge Retrieval:** Uses semantic search and embeddings to retrieve relevant information from store policies.
- **Policy Assistance:** Answers questions about returns, refunds, shipping, and warranties using a local knowledge base.
- **Interactive Web Interface:** Provides a Streamlit chat interface with conversation history, customer information, suggested questions, and processing indicators.
- **Conversation Management:** Maintains conversation state and supports starting a new chat.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Application logic and tool implementation |
| OpenAI API | Language model, tool calling, and text embeddings |
| Streamlit | Interactive chat interface |
| SQLite | Customer, product, order, and ticket storage |
| NumPy | Cosine similarity calculations |
| python-dotenv | Loads API credentials from environment variables |
| RAG | Retrieves relevant policy information |
| Semantic Search | Finds relevant knowledge-base chunks using embeddings |

## Architecture

```text
Customer
   |
   v
Streamlit Chat Interface
   |
   v
AI Agent (OpenAI LLM)
   |
   +--------------------+
   |                    |
   v                    v
Tool Calling         RAG Pipeline
   |                    |
   v                    v
Python Tools        Embeddings
   |                    |
   v                    v
SQLite Database     Policy Knowledge Base
   |                    |
   +---------+----------+
             |
             v
       Agent Response
             |
             v
       Streamlit UI
```

## Project Structure

```text
Ai_customer_support_agent/
├── agent/
│   └── agent.py
├── tools/
│   ├── customer_tools.py
│   ├── order_tools.py
│   ├── product_tools.py
│   ├── ticket_tools.py
│   ├── knowledge_tools.py
│   └── semantic_search.py
├── database/
│   ├── database.py
│   ├── schema.sql
│   └── seed.py
├── knowledge_base/
│   ├── refund_policy.txt
│   ├── return_policy.txt
│   ├── shipping_policy.txt
│   └── warranty_policy.txt
├── data/
├── tests/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

*Note: Update this structure to match the actual files in the repository before publishing.*

## Setup and Installation

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Ai_customer_support_agent
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=your_openai_api_key
```

Replace the placeholder with your own API key. Never commit your real API key to version control.

### 5. Initialize the database

Use the project's database schema and seed script to create the tables and insert sample data. From the project root, run:

```bash
python -m database.seed
```

Ensure the database directory exists and that the initialization script creates or accesses the database at the expected path.

### 6. Prepare the knowledge base

If the required chunk and embedding files are not included in the repository, run the project's document-chunking and embedding-generation scripts in the correct order. These steps require a configured OpenAI API key.

### 7. Start the application

```bash
streamlit run app.py
```

Open the local URL displayed by Streamlit in your browser.

## Example Interactions

**Order lookup**

```text
Customer: What are my orders?
Agent: Retrieves and summarizes the identified customer's orders.
```

**Policy question**

```text
Customer: How long does a refund take?
Agent: Retrieves relevant information from the refund policy.
```

**Support ticket**

```text
Customer: My order arrived damaged.
Agent: Asks for confirmation before creating a support ticket.
Customer: Yes.
Agent: Creates the ticket and returns its identifier and status.
```

## Security Considerations

- API credentials are loaded from environment variables.
- `.env`, the virtual environment, and local SQLite database files are excluded through `.gitignore`.
- Customer-specific order operations use the identified customer's context.
- Order ownership is verified for order-linked support tickets.
- Support tickets require customer confirmation according to the agent's system prompt.

## Future Improvements

- Deploy the application to a hosted environment.
- Add authentication and persistent conversation storage.
- Add structured logging and improved error monitoring.
- Add broader automated tests for agent workflows.
- Improve observability and evaluation of RAG retrieval quality.

## Author

Developed as an AI engineering portfolio project to explore LLM applications, tool calling, semantic search, RAG, and conversational application design.
