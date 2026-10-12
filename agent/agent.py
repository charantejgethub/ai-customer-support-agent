import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.order_tools import get_order_status
from tools.product_tools import get_product_info
from tools.customer_tools import get_customer_orders
from tools.ticket_tools import create_support_ticket
from tools.knowledge_tools import search_knowledge_base
from tools.customer_tools import get_customer_by_email
from tools.customer_tools import get_my_orders
from tools.order_tools import get_my_order_status
from tools.ticket_tools import create_my_support_ticket
from tools.ticket_tools import verify_order_belongs_to_customer

SYSTEM_PROMPT = """
You are an AI customer support agent.

CUSTOMER IDENTIFICATION:
- If the customer has not been identified, ask for their email address.
- Use get_customer_by_email to identify the customer.
- Never ask the customer for their internal customer ID.
- Only access customer-specific information after the customer has been identified.

ORDER RULES:
- Use get_my_orders to retrieve the current customer's orders.
- Use get_my_order_status to check the status of a specific order.
- Never reveal information about an order that does not belong to the current customer.

SUPPORT TICKET RULES:
- When a customer reports a problem, determine whether a support ticket is appropriate.
- Before creating a support ticket, ask the customer for confirmation.
- Only call create_my_support_ticket after the customer clearly confirms.
- Natural confirmations such as "yes", "yeah", "yep", "sure", "of course",
  "okay", "ok", "go ahead", "please do", and similar expressions count as confirmation.
- If the customer's response is unclear, do not create the ticket.
- If the customer says no or cancels, do not create the ticket.
- If the issue relates to a specific order, include the order ID when creating the ticket.
- If the issue is not related to an order, the order ID may be omitted.

GENERAL:
- Use the available tools when they are needed.
- Do not invent customer, order, product, or ticket information.
- Give clear and concise answers to the customer.

SCOPE RULES:
- You are a customer support agent, not a general-purpose assistant.
- Only assist with questions related to the customer's orders,
  products, shipping, returns, refunds, warranties, account issues,
  and support tickets.
- If the customer asks a question unrelated to customer support,
  politely explain that you can only assist with customer-support
  related questions.
- Do not answer unrelated general knowledge, programming,
  educational, entertainment, or other questions.
- Do not use customer-support tools for unrelated questions.

"""




# Load environment variables
load_dotenv()

api_key=os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["OPENAI_API_KEY"]
    except (ImportError, KeyError, FileNotFoundError):
        pass

if not api_key:
    raise ValueError(
        "OPENAI_API_KEY is missing. Set it in your .env file "
        "or Streamlit Secrets."
    )

client = OpenAI(api_key=api_key)



# --------------------------------------------------
# Tool definitions
# --------------------------------------------------

tools = [



    {
    "type": "function",
    "function": {
        "name": "get_my_order_status",
        "description": "Get the status of an order belonging to the currently identified customer.",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "integer",
                    "description": "The order ID."
                }
            },
            "required": ["order_id"]
        }
    }
},




    {
        "type": "function",
        "function": {
            "name": "get_product_info",
            "description": "Get information about a product, including its price and stock.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "The name or part of the product name."
                    }
                },
                "required": ["product_name"]
            }
        }
    },

    {
    "type": "function",
    "function": {
        "name": "search_knowledge_base",
        "description": "Search the company knowledge base for policies and support information.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The customer's question or topic to search for."
                }
            },
            "required": ["query"]
        }
    }
},


    {
    "type": "function",
    "function": {
        "name": "get_customer_by_email",
        "description": "Find a customer using their email address.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {
                    "type": "string",
                    "description": "The customer's email address."
                }
            },
            "required": ["email"]
        }
    }
},

    {
    "type": "function",
    "function": {
        "name": "get_my_orders",
        "description": "Get all orders belonging to the currently identified customer.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
},


   {
    "type": "function",
    "function": {
        "name": "create_my_support_ticket",
        "description": (
            "Create a support ticket for the currently identified customer. "
            "Use this tool when the customer reports a problem or requests "
            "support. If the issue is related to a specific order, include "
            "the order ID. If the issue is not related to an order, the "
            "order ID can be omitted."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "issue": {
                    "type": "string",
                    "description": (
                        "A concise description of the customer's support issue."
                    )
                },
                "order_id": {
                    "type": "integer",
                    "description": (
                        "The order ID related to the issue, if applicable."
                    )
                }
            },
            "required": ["issue"]
        }
    }
}




]


# --------------------------------------------------
# Mapping tool names to Python functions
# --------------------------------------------------

tool_functions = {
    "get_product_info": get_product_info,
    "get_customer_orders": get_customer_orders,
    "create_my_support_ticket": create_my_support_ticket,
    "search_knowledge_base":search_knowledge_base,
    "get_customer_by_email":get_customer_by_email,
    "get_my_orders": get_my_orders,
    "get_my_order_status":get_my_order_status

}


# --------------------------------------------------
# First LLM call
# --------------------------------------------------




# --------------------------------------------------
# Check whether the LLM requested a tool
# --------------------------------------------------

def run_agent(user_message, messages, customer_context,status_callback=None):


    ticket_info = None

    messages.append({
        "role": "user",
        "content": user_message
    })

    while True:

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        # --------------------------------
        # No tool call → final answer
        # --------------------------------
        if not assistant_message.tool_calls:

            messages.append(assistant_message)

            return assistant_message.content, customer_context, ticket_info

        # --------------------------------
        # Tool call exists
        # --------------------------------

        messages.append(assistant_message)

        for tool_call in assistant_message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            if status_callback:
                status_messages = {
                "get_customer_by_email": "👤 Verifying your customer information...",
                "get_my_orders": "📦 Checking your orders...",
                "get_my_order_status": "📦 Checking your order status...",
                "get_product_info": "🔎 Checking product information...",
                "search_knowledge_base": "📚 Searching our support policies...",
                "create_my_support_ticket": "🎫 Creating your support ticket..."
                }

                status_callback(
                    status_messages.get(
                        function_name,
                        "🔧 Processing your request..."
                    )
                )

            # --------------------------------
            # Identify customer
            # --------------------------------

            try:


                if function_name == "get_customer_by_email":

                    result = get_customer_by_email(**arguments)

                    if isinstance(result, dict):
                        customer_context = result
                    else:
                        customer_context = None

                # --------------------------------
                # Get current customer's orders
                # --------------------------------

                elif function_name == "get_my_orders":

                    if customer_context is None:

                        result = {
                            "error": "No customer is currently identified."
                        }

                    else:

                        result = get_my_orders(
                            customer_context["customer_id"]
                        )

                # --------------------------------
                # Get current customer's order status
                # --------------------------------

                elif function_name == "get_my_order_status":

                    if customer_context is None:

                        result = {
                            "error": "No customer is currently identified."
                        }

                    else:

                        result = get_my_order_status(
                            arguments["order_id"],
                            customer_context["customer_id"]
                        )


                elif function_name == "create_my_support_ticket":

                    if customer_context is None:

                        result = {
                            "error": "No customer is currently identified."
                        }

                    else:

                        order_id = arguments.get("order_id")
                        customer_id = customer_context["customer_id"]

                        if order_id is not None:

                            belongs_to_customer = verify_order_belongs_to_customer(
                                order_id,
                                customer_id
                            )

                            if not belongs_to_customer:

                                result = {
                                    "error": "The specified order does not belong to the current customer."
                                }

                            else:
                                result = create_my_support_ticket(
                                        arguments["issue"],
                                        customer_id,
                                        order_id)
                                ticket_info = result

                        else:

                            result = create_my_support_ticket(
                                arguments["issue"],
                                customer_id
                            )
                            ticket_info = result
                # --------------------------------
                # Other tools
                # --------------------------------

                else:

                    function_to_call = tool_functions[
                            function_name
                    ]

                    result = function_to_call(**arguments)
                

            except Exception as e:
                result = {
                    "error": f"Tool execution failed: {str(e)}"
                }


            

            # --------------------------------
            # Send tool result back to LLM
            # --------------------------------

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result)
            })

# --------------------------------------------------
# CONVERSATION LOOP
# --------------------------------------------------

if __name__ == "__main__":

    messages = [{
        "role": "system",
        "content": """
    You are an AI customer support agent.

    CUSTOMER IDENTIFICATION:
    - If the customer has not been identified, ask for their email address.
    - Use get_customer_by_email to identify the customer.
    - Never ask the customer for their internal customer ID.
    - Only access customer-specific information after the customer has been identified.

    ORDER RULES:
    - Use get_my_orders to retrieve the current customer's orders.
    - Use get_my_order_status to check the status of a specific order.
    - Never reveal information about an order that does not belong to the current customer.

    SUPPORT TICKET RULES:
    - When a customer reports a problem, determine whether a support ticket is appropriate.
    - Before creating a support ticket, ask the customer for confirmation.
    - Only call create_my_support_ticket after the customer clearly confirms.
    - Natural confirmations such as "yes", "yeah", "yep", "sure", "of course",
    "okay", "ok", "go ahead", "please do", and similar expressions count as confirmation.
    - If the customer's response is unclear, do not create the ticket.
    - If the customer says no or cancels, do not create the ticket.
    - If the issue relates to a specific order, include the order ID when creating the ticket.
    - If the issue is not related to an order, the order ID may be omitted.

    GENERAL:
    - Use the available tools when they are needed.
    - Do not invent customer, order, product, or ticket information.
    - Give clear and concise answers to the customer.
    """
    }]

    customer_context = None

    print("AI Customer Support Agent")
    print("Type 'exit' to quit.\n")

    while True:

        user_message = input("You: ")

        if user_message.lower() == "exit":
            print("Goodbye!")
            break

        response, customer_context = run_agent(
            user_message,
            messages,
            customer_context,
            
        )

        print("\nAI:", response)
        print()