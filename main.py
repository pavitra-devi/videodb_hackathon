import os
from dotenv import load_dotenv
from typing import TypedDict,List
from langgraph.graph import StateGraph, START,END, MessagesState
from videodb_hackathon.utilities import upload_video, index_video, format_timestamp,transcript_to_line, transcript_to_words
from videodb_hackathon.prompts import timestamp_generation_prompt, content_tagging_prompt, ROUTER_PROMPT,search_video_prompt
import videodb
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage
os.environ['GOOGLE_API_KEY'] = os.getenv("GOOGLE_API_KEY", "")


load_dotenv()
api_key = os.getenv('VIDEO_DB_API_KEY')
conn = videodb.connect(api_key=api_key)

model = init_chat_model("gemini-2.0-flash", model_provider="google_genai",temperature=0)



class AgentState(TypedDict):
    question:str
    video_url: str
    raw_transcript : str
    formatted_transcript: str
    spoken_words : str
    transcript_response: str
    content_tagging_response: str
    video_id: str
    video: any
    final_response: str



def timestamp_generator(state:AgentState):
    '''Used to generate Timestamps for a given video content'''
    video_url= state['video_url']
    video = upload_video(video_url)
    state['video'] = video
    transcript= index_video(video)
    # index= video.
    state['raw_transcript'] = transcript
    formatted_transcript = transcript_to_line(transcript)
    state['formatted_transcript'] = formatted_transcript
    response =model.invoke([SystemMessage(content=timestamp_generation_prompt),HumanMessage(content="video transcript :\n"+ formatted_transcript)])
    print(response.content)
    video.delete()
    state['transcript_response'] = response.content
    return {"final_response":response.content}


def content_tagging(state:AgentState):
    '''Used to generate content tagging for a given video content'''
    print("inside content tagging")
    video_url= state['video_url']
    video = upload_video(video_url)
    transcript = index_video(video)
    state['video'] = video
    transcript= index_video(video)
    state['raw_transcript'] = transcript
    formatted_transcript = transcript_to_words(transcript)
    response= model.invoke([SystemMessage(content=content_tagging_prompt), HumanMessage(content="video transcript :\n"+formatted_transcript)])
    print(response.content)
    video.delete()
    state['content_tagging_response'] = response.content
    return {"final_response":response.content}


def search_video(state:AgentState):
    '''Used to search a video for a given query'''
    video_url = state['video_url']
    video = upload_video(video_url)
    transcript = index_video(video)
    query = state['question']
    try:
        results = video.search(query=query)
        print(f"Search results for '{query}':")
        print(results)
        response= model.invoke([SystemMessage(content=search_video_prompt), HumanMessage(content=f"Search results for '{query}':\n{results}")])
        # results.play()
        video.delete()
        return {"final_response": response.content}
    except Exception as e:
        # Handle no results or other errors gracefully
        return {"final_response": f"No results found for '{query}'. ({e})"}




def router(state: AgentState) -> str:
    prompt = ROUTER_PROMPT.format(question=state["question"])
    response = model.invoke([{"role": "user", "content": prompt}])
    tool_name = response.content.strip().lower()
    print(f"[ROUTER] Selected Tool: {tool_name}")
    return tool_name




def router(state: AgentState) -> str:
    prompt = ROUTER_PROMPT.format(question=state["question"])
    response = model.invoke([{"role": "user", "content": prompt}])
    tool_name = response.content.strip().lower()
    print(f"[ROUTER] Selected Tool: {tool_name}")
    return tool_name

def run_video_agent(question: str, video_url: str):
    workflow = StateGraph(AgentState)
    print("*********User query **************:", question)
    # Add nodes (functions)
    workflow.add_node("timestamp_generator", timestamp_generator)
    workflow.add_node("content_tagging", content_tagging)
    workflow.add_node("search_video", search_video)

    # Add router
    workflow.add_conditional_edges(
        START,
        router,
        {
            "timestamp_generator": "timestamp_generator",
            "content_tagging": "content_tagging",
            "search_video": "search_video",
        }
    )

    # All paths go to END after one tool run
    workflow.add_edge("timestamp_generator", END)
    workflow.add_edge("content_tagging", END)
    workflow.add_edge("search_video", END)

    graph = workflow.compile()

    state = {
        "question": question,
        "video_url": video_url,
    }

    for chunk in graph.stream(state):
        for node, update in chunk.items():
            print(f"\n[UPDATE from {node}]:\n", update)

    return update
    # result = graph.invoke(state)
    # return result

# if __name__ == "__main__":
#     question = "Why LLM is being referred as stochastic parrot?"
#     video_url = "https://www.youtube.com/watch?v=67_aMPDk2zw"
#     run_video_agent(question, video_url)
