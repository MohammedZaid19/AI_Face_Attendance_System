import streamlit as st
from gemini_chat import ask_gemini_streamlit


# =====================================
# Page Configuration
# =====================================

st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 Gemini AI Attendance Assistant")

st.markdown(
"""
Ask questions about your attendance database using natural language.

### Example Questions

- Who is present today?
- Who is absent today?
- Show today's attendance summary.
- Which student has the highest attendance?
- List all absent students.
- Give attendance statistics.
"""
)

st.divider()

# =====================================
# Chat History
# =====================================

if "chat_history" not in st.session_state:

    st.session_state.chat_history = []

# Display previous messages
for chat in st.session_state.chat_history:

    with st.chat_message(chat["role"]):

        st.markdown(chat["message"])


# =====================================
# User Input
# =====================================

question = st.chat_input(
    "Ask anything about attendance..."
)

if question:

    # User Message
    st.session_state.chat_history.append(
        {
            "role":"user",
            "message":question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    # Gemini Response
    with st.chat_message("assistant"):

        with st.spinner("Gemini is analyzing attendance..."):

            try:

                answer = ask_gemini_streamlit(question)

            except Exception as e:

                answer = f"❌ Error\n\n{e}"

            st.markdown(answer)

    st.session_state.chat_history.append(
        {
            "role":"assistant",
            "message":answer
        }
    )


st.divider()


# =====================================
# Sidebar
# =====================================

with st.sidebar:

    st.header("🤖 Gemini AI")

    st.success("Status : Connected")

    st.write("### Features")

    st.write("✅ Attendance Analytics")

    st.write("✅ Natural Language Queries")

    st.write("✅ Student Insights")

    st.write("✅ AI Generated Answers")

    st.write("### Example")

    if st.button("Who is present today?"):

        st.session_state.chat_history.append(
            {
                "role":"user",
                "message":"Who is present today?"
            }
        )

        st.rerun()

    if st.button("Who is absent today?"):

        st.session_state.chat_history.append(
            {
                "role":"user",
                "message":"Who is absent today?"
            }
        )

        st.rerun()

    if st.button("Attendance Summary"):

        st.session_state.chat_history.append(
            {
                "role":"user",
                "message":"Give today's attendance summary."
            }
        )

        st.rerun()

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.chat_history = []

        st.rerun()
