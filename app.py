import streamlit as st

from agent.agent import run_agent
from agent.agent import SYSTEM_PROMPT

# --------------------------------
# Page configuration
# --------------------------------

st.set_page_config(
    page_title="AI Customer Support Agent",
    page_icon="🤖",
    layout="centered"
)


# --------------------------------
# Initialize session state
# --------------------------------

if "agent_messages" not in st.session_state:
    st.session_state.agent_messages = [{
            "role": "system",
            "content": SYSTEM_PROMPT
        }]

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "customer_context" not in st.session_state:
    st.session_state.customer_context = None


# --------------------------------
# Sidebar
# --------------------------------

with st.sidebar:

    st.title("🤖 Support Agent")

    st.write("AI-powered customer support")

    st.divider()

    # New chat button
    if st.button(
        "🆕 New Chat",
        use_container_width=True
    ):
        st.session_state.confirm_new_chat = True


    if st.session_state.get("confirm_new_chat", False):

        st.warning("Start a new conversation?")

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Yes, start new",
                use_container_width=True
            ):

                st.session_state.agent_messages = []
                st.session_state.chat_history = []
                st.session_state.customer_context = None
                st.session_state.confirm_new_chat = False

                st.rerun()

        with col2:

            if st.button(
                "Cancel",
                use_container_width=True
            ):

                st.session_state.confirm_new_chat = False

                st.rerun()

    st.divider()

    # Customer information
    st.subheader("👤 Customer")

    if st.session_state.customer_context:

        customer = st.session_state.customer_context

        st.success("Customer identified")

        st.write(f"**Name:** {customer['name']}")
        st.write(f"**Email:** {customer['email']}")

    else:

        st.info("Customer not identified")

        st.caption(
            "Provide your email in the chat to access "
            "your customer information."
        )


    st.divider()

    st.subheader("⚙️ Agent")

    st.write("🟢 Online")

    st.caption(
        "Connected to AI tools, customer database "
        "and knowledge base."
    )

    st.divider()

    # Agent information
    st.subheader("ℹ️ About")

    st.write(
        "This AI support agent can help with "
        "orders, products, returns, refunds, "
        "shipping, warranties, and support tickets."
    )


# --------------------------------
# Main page
# --------------------------------

st.title("🤖 AI Customer Support Agent")

st.caption(
    "Your AI-powered assistant for orders, returns, "
    "refunds, shipping and support."
)


# --------------------------------
# Welcome message
# --------------------------------

if not st.session_state.chat_history:

    st.markdown(
        """
        👋 **Hello! Welcome to AI Customer Support.**

        I can help you with:

        📦 **Orders**  
        ↩️ **Returns**  
        💰 **Refunds**  
        🚚 **Shipping**  
        🛠️ **Warranty**  
        🎫 **Support tickets**

        What can I help you with today?
        """
    )

suggested_message = None

if not st.session_state.chat_history:

    st.write("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📦 Track my order",
            use_container_width=True
        ):
            suggested_message = "What is the status of my order?"
            

        if st.button(
            "↩️ Return policy",
            use_container_width=True
        ):
            suggested_message = "What is your return policy?"
            

    with col2:

        if st.button(
            "💰 Refund information",
            use_container_width=True
        ):
            suggested_message = "How long does a refund take?"

        if st.button(
            "🎫 Report an issue",
            use_container_width=True
        ):
            suggested_message = "I have a problem with my order."
            




# --------------------------------
# Display previous chat messages
# --------------------------------

for message in st.session_state.chat_history:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------
# Chat input
# --------------------------------

user_message = st.chat_input(
    "Type your message..."
)


if suggested_message:

    user_message = suggested_message

if user_message:

    # --------------------------------
    # Display user message
    # --------------------------------

    with st.chat_message("user"):
        st.write(user_message)

    # Save user message for UI
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_message
    })


    # --------------------------------
    # Run agent
    # --------------------------------

    with st.chat_message("assistant"):

        with st.status("🤖 Working...", expanded=True) as status:

            def show_status(message):
                status.write(message)

            response, customer_context, ticket_info = run_agent(
                user_message,
                st.session_state.agent_messages,
                st.session_state.customer_context,
                status_callback=show_status
            )

            status.update(
                label="✅ Done",
                state="complete",
                expanded=False
            )

        st.write(response)

        if ticket_info and "ticket_id" in ticket_info:

            st.success(
                f"🎫 Support Ticket Created — #{ticket_info['ticket_id']}"
            )

            st.write(f"**Status:** {ticket_info['status']}")

            if ticket_info.get("order_id"):
                st.write(
                    f"**Order:** #{ticket_info['order_id']}"
                )

    # --------------------------------
    # Update customer context
    # --------------------------------

    st.session_state.customer_context = customer_context


    # --------------------------------
    # Display AI response
    # --------------------------------




    # Save AI response for UI
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": response
    })

st.divider()

st.caption(
    "🤖 AI Customer Support Agent • "
    "Powered by LLMs, Tool Calling, RAG & SQLite"
)