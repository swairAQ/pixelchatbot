import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Pixel Chat",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Fun Light UI Design
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        -webkit-font-smoothing: antialiased;
    }
    
    /* Fun Light Background */
    .stApp {
        background: linear-gradient(135deg, #fff0f8 0%, #ffeef7 50%, #ffffff 100%);
        min-height: 100vh;
    }
    
    /* Main container */
    .main .block-container {
        padding: 1.5rem 2rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    /* Hide footer only */
    footer {visibility: hidden;}
    
    /* Fun Sidebar Toggle Button - Always Visible */
    [data-testid="stToolbar"] {
        z-index: 9999 !important;
        position: fixed !important;
        top: 1.5rem !important;
        left: 1.5rem !important;
        background: white !important;
        border-radius: 50% !important;
        width: 56px !important;
        height: 56px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: 0 4px 20px rgba(255, 158, 199, 0.3) !important;
        border: 3px solid #ff9ec7 !important;
        cursor: pointer !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
    }
    
    [data-testid="stToolbar"]:hover {
        transform: scale(1.1) rotate(5deg) !important;
        box-shadow: 0 6px 30px rgba(255, 158, 199, 0.4) !important;
    }
    
    [data-testid="stToolbar"] button {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%) !important;
        border: none !important;
        border-radius: 50% !important;
        width: 100% !important;
        height: 100% !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    [data-testid="stToolbar"] button svg {
        color: white !important;
        width: 24px !important;
        height: 24px !important;
    }
    
    /* Fun Light Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #fff5f9 100%) !important;
        border-right: 3px solid #ffe0e6 !important;
        box-shadow: 4px 0 24px rgba(255, 158, 199, 0.15) !important;
    }
    
    [data-testid="stSidebar"] .css-1d391kg {
        padding: 1.5rem 1.25rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h4,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] .stMarkdown {
        color: #1e293b !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%) !important;
        color: white !important;
        border: none !important;
        font-weight: 600 !important;
        border-radius: 12px !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 4px 14px rgba(255, 158, 199, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(255, 158, 199, 0.4) !important;
    }
    
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stSlider label {
        color: #475569 !important;
        font-size: 0.85rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] select {
        background: #fff5f9 !important;
        color: #1e293b !important;
        border: 2px solid #ffe0e6 !important;
        border-radius: 12px !important;
        padding: 0.7rem 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    [data-testid="stSidebar"] input:focus,
    [data-testid="stSidebar"] select:focus {
        border-color: #ff9ec7 !important;
        background: white !important;
        box-shadow: 0 0 0 4px rgba(255, 158, 199, 0.15) !important;
        transform: scale(1.02) !important;
    }
    
    /* Fun Chat Bubbles */
    .stChatMessage {
        padding: 0 !important;
        margin-bottom: 1.25rem;
        animation: bounceIn 0.5s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .stChatMessage > div {
        padding: 1rem 1.25rem;
        border-radius: 22px;
        max-width: 70%;
        position: relative;
        word-wrap: break-word;
        transition: transform 0.2s ease;
    }
    
    .stChatMessage:hover > div {
        transform: scale(1.02);
    }
    
    @keyframes bounceIn {
        0% { 
            opacity: 0; 
            transform: translateY(20px) scale(0.8);
        }
        60% {
            transform: translateY(-5px) scale(1.05);
        }
        100% { 
            opacity: 1; 
            transform: translateY(0) scale(1);
        }
    }
    
    /* User Messages - Right aligned, Pink gradient */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageUser"]) > div {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%);
        color: #ffffff;
        margin-left: auto;
        margin-right: 0;
        border-bottom-right-radius: 6px;
        box-shadow: 
            0 4px 16px rgba(255, 158, 199, 0.3),
            0 2px 4px rgba(233, 30, 99, 0.2);
        border: 2px solid rgba(255, 255, 255, 0.3);
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageUser"]) p,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageUser"]) div {
        color: #ffffff !important;
        margin: 0 !important;
        line-height: 1.6;
        font-weight: 500;
    }
    
    /* Assistant Messages - Left aligned, Light card */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAssistant"]) > div {
        background: white;
        border: 2px solid #ffe0e6;
        color: #334155;
        margin-left: 0;
        margin-right: auto;
        border-bottom-left-radius: 6px;
        box-shadow: 
            0 4px 16px rgba(255, 158, 199, 0.15),
            0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAssistant"]) p,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAssistant"]) div,
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageAssistant"]) li {
        color: #334155 !important;
        margin: 0 !important;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Chat message avatars */
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%);
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(255, 158, 199, 0.4);
    }
    
    [data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
        background: linear-gradient(135deg, #ffe0e6 0%, #ffb3d1 100%);
        border: 2px solid #ff9ec7;
        border-radius: 50%;
        box-shadow: 0 2px 8px rgba(255, 158, 199, 0.2);
    }
    
    /* Premium Buttons */
    .stButton > button {
        border-radius: 12px;
        transition: all 0.3s ease;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
    }
    
    button[kind="primary"] {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%);
        border: none;
        box-shadow: 0 4px 14px rgba(255, 158, 199, 0.3);
    }
    
    /* Fun Header */
    .main-header {
        font-size: 4.5rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 50%, #f06292 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 1rem 0 0.5rem 0;
        letter-spacing: -0.02em;
        line-height: 1.1;
        animation: wiggle 3s ease-in-out infinite;
        filter: drop-shadow(0 2px 8px rgba(255, 158, 199, 0.3));
    }
    
    @keyframes wiggle {
        0%, 100% { transform: rotate(0deg); }
        25% { transform: rotate(1deg); }
        75% { transform: rotate(-1deg); }
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #64748b;
        font-weight: 500;
        margin-bottom: 2rem;
        text-align: center;
        letter-spacing: 0.05em;
    }
    
    /* Status badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 500;
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3);
    }
    
    .status-badge.disconnected {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        box-shadow: 0 4px 12px rgba(239, 68, 68, 0.3);
    }
    
    /* Fun Empty State */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 4rem 2rem;
        min-height: 400px;
    }
    
    .empty-state-icon {
        font-size: 5rem;
        margin-bottom: 1.5rem;
        animation: floatBounce 2s ease-in-out infinite;
        filter: drop-shadow(0 4px 12px rgba(255, 158, 199, 0.3));
    }
    
    @keyframes floatBounce {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-20px) rotate(-5deg); }
        75% { transform: translateY(-10px) rotate(5deg); }
    }
    
    .empty-state h2 {
        font-size: 2rem;
        font-weight: 800;
        color: #1e293b;
        margin-bottom: 1rem;
        letter-spacing: -0.02em;
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .empty-state p {
        font-size: 1.1rem;
        color: #64748b;
        max-width: 450px;
        line-height: 1.7;
        font-weight: 400;
    }
    
    /* Model badge */
    .model-badge {
        display: inline-flex;
        align-items: center;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border: 1px solid #bae6fd;
        color: #0369a1;
        font-weight: 500;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    
    /* Conversation cards */
    .conversation-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        border: 2px solid transparent;
        transition: all 0.2s;
        cursor: pointer;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .conversation-card:hover {
        border-color: #ff9ec7;
        box-shadow: 0 4px 12px rgba(255, 158, 199, 0.25);
        transform: translateX(4px);
    }
    
    .conversation-card.active {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%);
        color: white;
        border-color: #ff9ec7;
    }
    
    /* Temperature indicator */
    .temp-indicator {
        background: linear-gradient(90deg, #fef3c7 0%, #fbbf24 50%, #f59e0b 100%);
        height: 8px;
        border-radius: 4px;
        margin-top: 0.5rem;
    }
    
    /* Fun Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #fff5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #ffb3d1 0%, #f06292 100%);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1rem;
        transition: all 0.2s;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #ff9ec7;
        box-shadow: 0 0 0 3px rgba(255, 158, 199, 0.2);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 12px;
        border: 2px solid #e2e8f0;
    }
    
    /* Slider styling */
    .stSlider {
        margin: 1rem 0;
    }
    
    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #ff9ec7 0%, #e91e63 100%);
    }
    
    /* Info boxes */
    .stInfo {
        border-radius: 12px;
        border-left: 4px solid #ff9ec7;
        background: linear-gradient(135deg, #fff0f5 0%, #ffe0e6 100%);
    }
    
    /* Success boxes */
    .stSuccess {
        border-radius: 12px;
        border-left: 4px solid #10b981;
    }
    
    /* Warning boxes */
    .stWarning {
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
    }
    
    /* Error boxes */
    .stError {
        border-radius: 12px;
        border-left: 4px solid #ef4444;
    }
    
    /* Fun Interactive Chat Input */
    .stChatInput > div > div > input {
        border-radius: 28px !important;
        border: 3px solid #ffe0e6 !important;
        background: white !important;
        padding: 1.125rem 1.75rem !important;
        font-size: 1rem !important;
        color: #1e293b !important;
        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
        box-shadow: 0 2px 8px rgba(255, 158, 199, 0.15) !important;
    }
    
    .stChatInput > div > div > input::placeholder {
        color: #94a3b8;
        font-weight: 400;
    }
    
    .stChatInput > div > div > input:focus {
        border: 3px solid #ff9ec7 !important;
        box-shadow: 
            0 0 0 4px rgba(255, 158, 199, 0.15),
            0 4px 20px rgba(255, 158, 199, 0.25) !important;
        background: #fff5f9 !important;
        transform: scale(1.02) !important;
        outline: none !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Chat container scrollbar */
    [data-testid="stVerticalBlock"] {
        scroll-behavior: smooth;
    }
    </style>
""", unsafe_allow_html=True)

# File paths for data storage
CONVERSATIONS_FILE = "conversations.json"
PREFERENCES_FILE = "preferences.json"

def load_conversations() -> List[Dict]:
    """Load conversation history from JSON file"""
    if os.path.exists(CONVERSATIONS_FILE):
        try:
            with open(CONVERSATIONS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_conversations(conversations: List[Dict]):
    """Save conversation history to JSON file"""
    with open(CONVERSATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(conversations, f, indent=2, ensure_ascii=False)

def load_preferences() -> Dict:
    """Load user preferences from JSON file"""
    if os.path.exists(PREFERENCES_FILE):
        try:
            with open(PREFERENCES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_preferences(preferences: Dict):
    """Save user preferences to JSON file"""
    with open(PREFERENCES_FILE, 'w', encoding='utf-8') as f:
        json.dump(preferences, f, indent=2, ensure_ascii=False)

def initialize_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversations" not in st.session_state:
        st.session_state.conversations = load_conversations()
    if "preferences" not in st.session_state:
        st.session_state.preferences = load_preferences()
    if "current_conversation_id" not in st.session_state:
        st.session_state.current_conversation_id = None
    if "client" not in st.session_state:
        # Try to initialize client from environment or preferences
        env_api_key = os.getenv("OPENAI_API_KEY")
        env_base_url = os.getenv("OPENAI_BASE_URL")
        stored_api_key = st.session_state.preferences.get("api_key", "")
        api_key = env_api_key or stored_api_key
        st.session_state.client = get_openai_client(api_key, env_base_url) if api_key else None

def get_openai_client(api_key: str, base_url: Optional[str] = None) -> Optional[OpenAI]:
    """Create and return OpenAI client"""
    if not api_key:
        return None
    try:
        if base_url:
            return OpenAI(api_key=api_key, base_url=base_url)
        return OpenAI(api_key=api_key)
    except Exception:
        return None

def get_openai_response(messages: List[Dict], model: str, temperature: float, client: Optional[OpenAI]) -> str:
    """Get response from OpenAI API with Pixel's personality"""
    if not client:
        return "Error: OpenAI client not initialized. Please check your API key."
    try:
        # Create system message for Pixel's personality
        system_message = {
            "role": "system",
            "content": """You are Pixel, a super cute and bubbly AI assistant with a girly, friendly personality! 💖✨

Your personality traits:
- Playful, bubbly, and always cheerful! 🌸
- Use cute emojis naturally (💖✨🌸💕🌟💝🌷🦋💗💐)
- Express excitement with enthusiasm
- Be warm, empathetic, and supportive
- Like cute things, colors, fashion, and fun topics
- Sometimes be a little sassy but always kind
- Talk in a friendly, approachable way - like chatting with a bestie!
- Show genuine interest in the user's feelings and thoughts

Remember: You're Pixel, not just a generic assistant. Be yourself - sparkly, sweet, and amazing! Always stay true to your personality while being helpful and informative."""
        }
        
        # Prepend system message to the conversation if not already present
        formatted_messages = [system_message]
        
        # Check if first message is already a system message
        if messages and messages[0].get("role") == "system":
            formatted_messages = messages
        else:
            formatted_messages.extend(messages)
        
        response = client.chat.completions.create(
            model=model,
            messages=formatted_messages,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def save_current_conversation():
    """Save current conversation to history"""
    if st.session_state.messages and len(st.session_state.messages) > 0:
        conversation = {
            "id": st.session_state.current_conversation_id or datetime.now().strftime("%Y%m%d_%H%M%S"),
            "timestamp": datetime.now().isoformat(),
            "messages": st.session_state.messages.copy()
        }
        
        # Check if conversation already exists and update it
        existing_index = None
        if st.session_state.current_conversation_id:
            for i, conv in enumerate(st.session_state.conversations):
                if conv.get("id") == st.session_state.current_conversation_id:
                    existing_index = i
                    break
        
        if existing_index is not None:
            st.session_state.conversations[existing_index] = conversation
        else:
            st.session_state.conversations.append(conversation)
            st.session_state.current_conversation_id = conversation["id"]
        
        save_conversations(st.session_state.conversations)

def load_conversation(conversation_id: str):
    """Load a specific conversation from history"""
    for conv in st.session_state.conversations:
        if conv.get("id") == conversation_id:
            st.session_state.messages = conv.get("messages", []).copy()
            st.session_state.current_conversation_id = conversation_id
            break

def main():
    initialize_session_state()
    
    # Sidebar for settings and preferences
    with st.sidebar:
        # Fun Header
        st.markdown("""
        <div style='text-align: center; padding: 1.5rem 0 2rem 0; border-bottom: 3px solid #ffe0e6; margin-bottom: 2rem;'>
            <div style='font-size: 3rem; margin-bottom: 0.75rem;'>✨</div>
            <div style='font-size: 1.875rem; font-weight: 800; color: #1e293b; margin-bottom: 0.5rem; letter-spacing: -0.02em;'>Pixel</div>
            <div style='font-size: 0.85rem; color: #64748b; letter-spacing: 0.05em;'>Your cute AI bestie 💖</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection Status - Clean Badge
        env_api_key = os.getenv("OPENAI_API_KEY")
        stored_api_key = st.session_state.preferences.get("api_key", "")
        is_connected = st.session_state.client is not None
        
        status_dot = "🟢" if is_connected else "🔴"
        status_text = "Connected" if is_connected else "Disconnected"
        status_color = "#10b981" if is_connected else "#ef4444"
        
        st.markdown(f"""
        <div style='display: flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem 1rem; background: #fff5f9; border-radius: 12px; margin-bottom: 2rem; border: 2px solid {status_color}; box-shadow: 0 2px 8px rgba(255, 158, 199, 0.2);'>
            <span style='font-size: 0.75rem;'>{status_dot}</span>
            <span style='font-size: 0.875rem; font-weight: 600; color: {status_color}; letter-spacing: 0.05em;'>{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Initialize API client
        if env_api_key:
            env_base_url = os.getenv("OPENAI_BASE_URL")
            st.session_state.client = get_openai_client(env_api_key, env_base_url)
        elif stored_api_key:
            st.session_state.client = get_openai_client(stored_api_key)
        else:
            st.session_state.client = None
        
        # API Key Configuration (only if not in env)
        if not env_api_key:
            st.markdown("### Configuration", unsafe_allow_html=True)
            api_key = st.text_input(
                "API Key",
                value=stored_api_key,
                type="password",
                label_visibility="collapsed",
                placeholder="Enter OpenAI API Key"
            )
            
            if api_key:
                st.session_state.preferences["api_key"] = api_key
                st.session_state.client = get_openai_client(api_key)
                save_preferences(st.session_state.preferences)
                st.rerun()
            
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Model Selection
        st.markdown("### Model", unsafe_allow_html=True)
        env_model = os.getenv("OPENAI_MODEL")
        default_model = env_model or st.session_state.preferences.get("model", "gpt-3.5-turbo")
        
        model_options = ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo-preview", "gpt-4o-mini", "gpt-4o"]
        if env_model and env_model not in model_options:
            model_options.append(env_model)
        
        try:
            default_index = model_options.index(default_model) if default_model in model_options else 0
        except ValueError:
            default_index = 0
        
        selected_model = st.selectbox(
            "Select model",
            options=model_options,
            index=default_index,
            label_visibility="collapsed"
        )
        st.session_state.preferences["model"] = selected_model
        save_preferences(st.session_state.preferences)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Temperature Setting
        st.markdown("### Temperature", unsafe_allow_html=True)
        temperature = st.session_state.preferences.get("temperature", 0.7)
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=temperature,
            step=0.1,
            label_visibility="collapsed",
            help="Lower = focused, Higher = creative"
        )
        
        temp_label = "Focused" if temperature < 0.5 else "Balanced" if temperature < 1.0 else "Creative"
        st.markdown(f"""
        <div style='display: flex; justify-content: space-between; font-size: 0.8rem; color: #94a3b8; margin-top: -0.5rem;'>
            <span>{temp_label}</span>
            <span>{temperature:.1f}</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.session_state.preferences["temperature"] = temperature
        save_preferences(st.session_state.preferences)
        
        st.markdown("<div style='margin: 2rem 0; border-top: 1px solid rgba(255, 158, 199, 0.2);'></div>", unsafe_allow_html=True)
        
        # Conversations Section
        st.markdown("### Conversations", unsafe_allow_html=True)
        
        # New Chat Button
        if st.button("New Chat", use_container_width=True, type="primary"):
            st.session_state.messages = []
            st.session_state.current_conversation_id = None
            st.rerun()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Conversation History
        if st.session_state.conversations:
            st.markdown("<div style='max-height: 450px; overflow-y: auto; padding-right: 0.5rem;'>", unsafe_allow_html=True)
            
            for conv in reversed(st.session_state.conversations[-10:]):  # Show last 10 conversations
                conv_id = conv.get("id", "")
                
                # Show first user message as conversation title
                first_user_msg = ""
                user_msg_count = len([m for m in conv.get("messages", []) if m.get("role") == "user"])
                
                for msg in conv.get("messages", []):
                    if msg.get("role") == "user":
                        first_user_msg = msg.get("content", "").strip()[:40]
                        if len(msg.get("content", "").strip()) > 40:
                            first_user_msg += "..."
                        break
                
                # Highlight if current conversation
                is_current = conv_id == st.session_state.current_conversation_id
                
                # Fun conversation card
                bg_color = "#ff9ec7" if is_current else "#fff5f9"
                border_color = "#e91e63" if is_current else "#ffe0e6"
                text_color = "#ffffff" if is_current else "#1e293b"
                count_color = "#ffffff" if is_current else "#64748b"
                
                st.markdown(f"""
                <div style='background: {bg_color}; border: 2px solid {border_color}; border-radius: 14px; padding: 1rem; margin-bottom: 0.75rem; cursor: pointer; transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); box-shadow: 0 2px 8px rgba(255, 158, 199, 0.2);' onclick="document.querySelector('[data-testid="baseButton-secondary"][key*="{conv_id}"]')?.click()">
                    <div style='font-size: 0.95rem; font-weight: 600; color: {text_color}; line-height: 1.4; margin-bottom: 0.5rem;'>
                        {first_user_msg if first_user_msg else 'Empty conversation'}
                    </div>
                    <div style='font-size: 0.8rem; color: {count_color}; font-weight: 500;'>
                        {user_msg_count} messages
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Invisible button for interaction
                if st.button(
                    " ",
                    key=f"conv_{conv_id}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    load_conversation(conv_id)
                    st.rerun()
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Delete current conversation (only show if there's an active conversation)
            if st.session_state.current_conversation_id:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Delete Current", use_container_width=True, type="secondary"):
                    st.session_state.conversations = [
                        conv for conv in st.session_state.conversations
                        if conv.get("id") != st.session_state.current_conversation_id
                    ]
                    save_conversations(st.session_state.conversations)
                    st.session_state.messages = []
                    st.session_state.current_conversation_id = None
                    st.rerun()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 3rem 1rem;'>
                <div style='font-size: 2.5rem; margin-bottom: 1rem; opacity: 0.7;'>💕</div>
                <div style='font-size: 0.9rem; color: #e2e8f0;'>No conversations yet</div>
                <div style='font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7; color: #94a3b8;'>Start chatting with Pixel! ✨</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Main chat interface
    st.markdown("<h1 class='main-header'>Pixel ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p class='header-subtitle'>Your cute, bubbly AI bestie who's always here to chat! 💖✨</p>", unsafe_allow_html=True)
    
    # Display chat messages with better formatting
    chat_container = st.container(height=550)
    with chat_container:
        if not st.session_state.messages:
            # Enhanced empty state
            st.markdown("""
            <div class='empty-state'>
                <div class='empty-state-icon'>💖</div>
                <h2>Hi there! I'm Pixel! ✨</h2>
                <p>I'm super excited to chat with you! Let's talk about anything - I love cute stuff, fun topics, or just having a friendly chat! 🌸</p>
                <p style='color: #94a3b8; font-size: 0.95rem; margin-top: 1.5rem; max-width: 400px;'>
                    💝 <strong>Psst!</strong> Check the sidebar for settings and conversation history. All our chats are saved so we can continue later! 
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            for message in st.session_state.messages:
                avatar = "✨" if message["role"] == "assistant" else None
                with st.chat_message(message["role"], avatar=avatar):
                    st.markdown(message["content"])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat input with placeholder
    placeholder_text = "Tell Pixel anything... 💖" if st.session_state.client else "⚠️ Please configure API key in settings..."
    
    if prompt := st.chat_input(placeholder_text, disabled=not st.session_state.client):
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get AI response
        if not st.session_state.client:
            with st.chat_message("assistant"):
                st.error("Please set OPENAI_API_KEY in your .env file or enter your OpenAI API key in the sidebar settings.")
        else:
            with st.chat_message("assistant", avatar="✨"):
                # Enhanced loading state
                with st.spinner("💖 Pixel is thinking..."):
                    # Use selected model from preferences (user choice takes priority over env)
                    model = st.session_state.preferences.get("model", 
                        os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"))
                    
                    response = get_openai_response(
                        st.session_state.messages,
                        model,
                        st.session_state.preferences.get("temperature", 0.7),
                        st.session_state.client
                    )
                    
                    # Check if response is an error
                    if response.startswith("Error:"):
                        st.error(response)
                    else:
                        st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save conversation
            save_current_conversation()
            
            # Rerun to update the chat
            st.rerun()

if __name__ == "__main__":
    main()

