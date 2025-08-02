import streamlit as st
from videodb_hackathon.main import run_video_agent  # Your logic to handle video questions

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="🎬 Video Assistant",
    layout="wide", # Use wide layout for more screen space
    initial_sidebar_state="collapsed", # Optional: collapse sidebar by default
)

# --- Custom CSS for a Clean, Gemini-like Theme ---
st.markdown("""
    <style>
    /* General body and main container styling */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f0f2f5; /* Light gray background for the whole page */
        color: #333;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }

    /* Main content area */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 900px; /* Constrain content width for readability */
    }

    /* Header */
    .header-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a73e8; /* Google Blue */
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.1rem;
        color: #5f6368; /* Google Gray */
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Chat History Container */
    .chat-history-container {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08); /* More pronounced shadow */
        padding: 20px;
        min-height: 400px; /* Minimum height for chat area */
        max-height: 60vh; /* Max height for scrollable chat */
        overflow-y: auto; /* Enable scrolling */
        display: flex;
        flex-direction: column;
        gap: 15px; /* Space between messages */
        margin-bottom: 20px;
        border: 1px solid #e0e0e0;
    }

    /* Chat Bubbles */
    .chat-message {
        display: flex;
        align-items: flex-start; /* Align items to the start (top) */
        gap: 10px;
    }
    .chat-message.user {
        justify-content: flex-end; /* User messages to the right */
    }
    .chat-message.agent {
        justify-content: flex-start; /* Agent messages to the left */
    }

    .message-avatar {
        width: 30px;
        height: 30px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.1rem;
        font-weight: bold;
        color: white;
        flex-shrink: 0; /* Prevent avatar from shrinking */
    }
    .user-avatar { background-color: #4285f4; } /* Google Blue */
    .agent-avatar { background-color: #3c4043; } /* Google Dark Gray */

    .message-content {
        padding: 12px 18px;
        border-radius: 18px; /* More rounded bubbles */
        max-width: 75%; /* Limit bubble width */
        font-size: 0.95rem;
        line-height: 1.5;
        word-wrap: break-word; /* Ensure long words wrap */
        white-space: pre-wrap; /* Preserve whitespace and line breaks */
    }
    .user-message {
        background-color: #e6f2ff; /* Lighter blue for user */
        color: #212121;
        border-bottom-right-radius: 4px; /* Slightly less rounded at the corner closest to the avatar */
    }
    .agent-message {
        background-color: #f1f3f4; /* Light gray for agent */
        color: #212121;
        border-bottom-left-radius: 4px;
    }

    .message-meta {
        font-size: 0.75rem;
        color: #70757a;
        margin-top: 5px;
        text-align: right; /* Align meta info with user bubble */
    }
    .chat-message.agent .message-meta {
        text-align: left; /* Align meta info with agent bubble */
    }


    /* Input form container */
    .input-form-container {
        background: #ffffff;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        padding: 20px;
        border: 1px solid #e0e0e0;
    }

    /* Streamlit input widgets customization */
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 1px solid #dadce0; /* Light gray border */
        padding: 10px 15px;
        font-size: 1rem;
        box-shadow: inset 0 1px 2px rgba(0,0,0,0.06);
    }
    .stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: #4285f4; /* Google Blue on focus */
        box-shadow: 0 0 0 1px #4285f4;
        outline: none;
    }

    /* Button styling */
    .stButton > button {
        background-color: #1a73e8; /* Google Blue */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 12px 25px;
        font-size: 1.05rem;
        font-weight: 500;
        transition: background-color 0.2s ease-in-out;
        width: 100%; /* Make button full width in its column */
    }
    .stButton > button:hover {
        background-color: #1565c0; /* Darker blue on hover */
    }
    .stButton > button:active {
        background-color: #0d47a1;
    }
    .stButton > button:focus:not(:active) {
        box-shadow: 0 0 0 3px rgba(66, 133, 244, 0.4); /* Focus ring */
        outline: none;
    }

    /* Warning message */
    .stWarning {
        background-color: #fefce8; /* Light yellow background */
        color: #ca8a04; /* Dark yellow text */
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #fde047;
    }

    /* Spinner */
    .stSpinner > div > div {
        color: #1a73e8; /* Spinner color */
    }

    /* Adjust Streamlit columns padding */
    .st-emotion-cache-1pxpxj8 { /* This is a common class for columns */
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }

    </style>
""", unsafe_allow_html=True)

# --- Header Section ---
st.markdown('<div class="header-title">🎥 Video Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask questions about any video, get summaries, timestamps, and more.</div>', unsafe_allow_html=True)

# --- State Setup ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []  # [{"role": ..., "content": ..., "video_url": ...}]
if "current_video_url_input" not in st.session_state:
    st.session_state.current_video_url_input = "" # Holds the URL typed in the box
if "current_question_input" not in st.session_state:
    st.session_state.current_question_input = "" # Holds the question typed in the box
if "last_processed_video_url" not in st.session_state:
    st.session_state.last_processed_video_url = "" # Stores the URL from the last successful submission

# --- Chat History Display ---
if st.session_state.chat_history:
    st.markdown('<div class="chat-history-container">', unsafe_allow_html=True)
    for message in st.session_state.chat_history:
        role = message["role"]
        content = message["content"]
        video_url_info = message.get("video_url", "") # Get video_url if it exists

        if role == "user":
            st.markdown(f"""
                <div class="chat-message user">
                    <div class="message-content user-message">{content}</div>
                    <div class="message-avatar user-avatar">You</div>
                </div>
                <div class="message-meta" style="text-align: right;">For: {video_url_info}</div>
            """, unsafe_allow_html=True)
        elif role == "agent":
            st.markdown(f"""
                <div class="chat-message agent">
                    <div class="message-avatar agent-avatar">AI</div>
                    <div class="message-content agent-message">{content}</div>
                </div>
                <div class="message-meta" style="text-align: left;"></div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- Input Form ---
# We use a standard form WITHOUT clear_on_submit=True to persist inputs
# We'll manage clearing manually.
with st.container(): # Use a container for the input section
    st.markdown('<div class="input-form-container">', unsafe_allow_html=True)
    with st.form("video_chat_form", clear_on_submit=False): # IMPORTANT: No clear_on_submit
        col1, col2 = st.columns([3, 1]) # Column for URL, column for Question and Send

        with col1:
            # Use st.session_state.current_video_url_input for initial value and to manage persistence
            video_url_input = st.text_input(
                "Video URL",
                value=st.session_state.current_video_url_input,
                placeholder="Paste YouTube, Vimeo, or direct video URL...",
                help="The URL of the video you want to analyze.",
                key="video_url_input_widget" # Unique key for the widget
            )
        with col2:
            # Question input - use st.session_state.current_question_input for initial value
            question_input = st.text_area(
                "Your Question",
                value=st.session_state.current_question_input,
                placeholder="e.g., Summarize this video. What are the main topics?",
                height=60, # Adjust height
                key="question_input_widget" # Unique key for the widget
            )

        # Sync input widget values with session state on every run
        # This is crucial for persistence
        if st.session_state.video_url_input_widget != st.session_state.current_video_url_input:
            st.session_state.current_video_url_input = st.session_state.video_url_input_widget
        if st.session_state.question_input_widget != st.session_state.current_question_input:
            st.session_state.current_question_input = st.session_state.question_input_widget


        # Submit button
        submitted = st.form_submit_button("Send 🚀")

    st.markdown('</div>', unsafe_allow_html=True) # Close input form container div

# --- Logic after Submission ---
if submitted:
    # Update session state with what was in the input fields upon submission
    st.session_state.current_video_url_input = video_url_input
    st.session_state.current_question_input = question_input

    if not video_url_input or not question_input:
        st.warning("Please provide both the video URL and your question.")
    else:
        # Check if the video URL has changed from the last processed one
        # If it has, we might want to clear the question input for a fresh start.
        if video_url_input != st.session_state.last_processed_video_url:
            st.session_state.last_processed_video_url = video_url_input
            # Clear question input if a new video URL is submitted
            st.session_state.current_question_input = "" # Clear the question input box

        # Add user message to history
        st.session_state.chat_history.append({
            "role": "user", "content": question_input, "video_url": video_url_input
        })

        with st.spinner("The assistant is thinking..."):
            try:
                # Call your backend logic
                result = run_video_agent(question_input, video_url_input)

                if isinstance(result, dict):
                    # if "final_response" in result:
                    agent_msg = result.get("final_response", "No response generated.")
                    # else:
                        # result_content = result.get('video', None)
                        # result_content.play()
                
                
                else:
                    agent_msg = str(result)

                st.session_state.chat_history.append({
                    "role": "agent", "content": agent_msg, "video_url": video_url_input # Store URL with agent response too for consistency
                })

            except Exception as e:
                st.session_state.chat_history.append({
                    "role": "agent", "content": f"❌ An error occurred: {e}. Please try again or check the URL.", "video_url": video_url_input
                })
        # Important: Rerun the app to update the chat display immediately
        st.rerun()

# --- Footer ---
st.markdown("---")
st.caption("Built with 💙 using Streamlit & LangGraph.")