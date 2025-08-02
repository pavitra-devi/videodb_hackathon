# Video Analyzer Chatbot

A powerful chatbot that helps users analyze videos using natural language queries. With just a video URL and your question, you can:

- **Generate video summaries**
- **Create accurate timestamps**
- **Perform Retrieval-Augmented Generation (RAG) on video content**
- **Analyze and tag video content by genre or topic**

## Features
- **One-stop video analysis:** Get summaries, timestamps, content tags, and search results with a single query.
- **Natural language interface:** No technical skills required—just ask your question.
- **Fast and scalable:** Built on modern frameworks for efficient video processing and LLM-powered responses.

## Tech Stack
- **LangGraph:** Orchestrates agentic workflows and tool selection.
- **VideoDB:** Handles video chunking, indexing, and search.
- **Streamlit:** Provides a clean, interactive chat UI.
- **LLM (Google Gemini):** Generates summaries, tags, and answers.

## Usage
1. **Clone the repository and install dependencies**
2. **Set your API keys in a `.env` file**
3. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
4. **Paste a video URL and ask your question!**

## Example Queries
- "Summarize this video."
- "Generate timestamps for the main topics."
- "What genres are present in this video?"
- "Find where the speaker discusses AI ethics."

---

Built with ❤️ using LangGraph, VideoDB, Streamlit, and Gemini LLM.
