import streamlit as st
from openai import OpenAI
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# App version
APP_VERSION = "1.0.0"

# OpenAI Base URL
OPENAI_BASE_URL = "https://openai.dplit.com/v1/"

# Page configuration
st.set_page_config(
    page_title="Pixel Chat",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items=None
)

# Basic UI Styling
st.markdown("""
    <style>
    footer {visibility: hidden;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #fff5f9 !important;
    }
    
    [data-testid="stSidebar"] .stButton > button {
        background: #ff9ec7 !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
    }
    
    /* Chat messages */
    [data-testid="stChatMessageUser"] > div > div {
        background: #ff9ec7 !important;
        color: white !important;
        border-radius: 16px 16px 4px 16px !important;
    }
    
    [data-testid="stChatMessageAssistant"] > div {
        background: white !important;
        border: 1px solid #ffe0e6 !important;
        border-radius: 16px 16px 16px 4px !important;
    }
    
    /* Header */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        color: #e91e63;
        margin: 1rem 0 0.5rem 0;
    }
    
    .header-subtitle {
        font-size: 1rem;
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    /* Empty state */
    .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 4rem 2rem;
    }
    
    .empty-state-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .empty-state h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .empty-state p {
        color: #64748b;
        max-width: 450px;
    }
    
    /* Chat input */
    .stChatInput > div > div > input {
        border-radius: 20px !important;
        border: 2px solid #ffe0e6 !important;
    }
    
    .stChatInput > div > div > input:focus {
        border-color: #ff9ec7 !important;
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
        # For testing: only use stored preferences, not env variables
        # env_api_key = os.getenv("OPENAI_API_KEY")  # Disabled for testing
        stored_api_key = st.session_state.preferences.get("api_key", "")
        if stored_api_key:
            # Use custom base URL for all client initializations
            st.session_state.client = get_openai_client(stored_api_key, OPENAI_BASE_URL)
        else:
            st.session_state.client = None

def get_openai_client(api_key: str, base_url: Optional[str] = None) -> Optional[OpenAI]:
    """Create and return OpenAI client"""
    if not api_key:
        return None
    try:
        # Use custom base URL if provided, otherwise use default
        url = base_url or OPENAI_BASE_URL
        return OpenAI(api_key=api_key, base_url=url)
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
            <div style='font-size: 0.85rem; color: #64748b; letter-spacing: 0.05em;'>Your AI bestie \n\n Inspired by Marwa 💖</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Connection Status - Clean Badge
        # For testing: always ask user for API key (don't read from env)
        # env_api_key = os.getenv("OPENAI_API_KEY")  # Disabled for testing
        env_api_key = None  # Always None to force manual entry
        stored_api_key = st.session_state.preferences.get("api_key", "")
        is_connected = st.session_state.client is not None
        
        status_dot = "🟢" if is_connected else "🔴"
        status_text = "Connected" if is_connected else "Disconnected"
        status_color = "#10b981" if is_connected else "#ef4444"
        
        st.markdown(f"""
        <div style='display: flex; align-items: flex-start; justify-content: center; gap: 0.5rem; padding: 0.75rem 1rem; background: #fff5f9; border-radius: 12px; margin-bottom: 2rem; border: 2px solid {status_color}; box-shadow: 0 2px 8px rgba(255, 158, 199, 0.2);'>
            <span style='font-size: 0.75rem;'>{status_dot}</span>
            <span style='font-size: 0.875rem; font-weight: 600; color: {status_color}; letter-spacing: 0.05em;'>{status_text}</span>
        </div>
        """, unsafe_allow_html=True)
        
        # API Key Configuration (always show for testing)
        st.markdown("### Configuration", unsafe_allow_html=True)
        
        # Don't show stored API key to user - show placeholder instead if connected
        if is_connected:
            # Show placeholder instead of actual key
            api_key_input = st.text_input(
                "API Key",
                value="",  # Empty to hide stored key
                type="password",
                label_visibility="collapsed",
                placeholder="API key is saved and connected ✅ (enter new key to change)"
            )
            
            # Allow user to change API key
            if api_key_input:
                st.session_state.preferences["api_key"] = api_key_input
                save_preferences(st.session_state.preferences)
                new_client = get_openai_client(api_key_input, OPENAI_BASE_URL)
                if new_client:
                    st.session_state.client = new_client
                    st.success("✅ API key updated and connected!")
                    st.rerun()
                else:
                    st.session_state.client = None
                    st.error("❌ Invalid API key. Please check and try again.")
        else:
            # Not connected - show input for entering key
            api_key_input = st.text_input(
                "API Key",
                value="",  # Always empty - don't show stored key
                type="password",
                label_visibility="collapsed",
                placeholder="Enter OpenAI API Key"
            )
            
            # Update API key if provided
            if api_key_input:
                st.session_state.preferences["api_key"] = api_key_input
                save_preferences(st.session_state.preferences)
                new_client = get_openai_client(api_key_input, OPENAI_BASE_URL)
                if new_client:
                    st.session_state.client = new_client
                    st.success("✅ API key saved and connected!")
                    st.rerun()
                else:
                    st.session_state.client = None
                    st.error("❌ Invalid API key. Please check and try again.")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Initialize API client (only from stored preferences, not env)
        if stored_api_key and not st.session_state.client:
            # Only initialize if not already set (to avoid overriding just-set client)
            st.session_state.client = get_openai_client(stored_api_key, OPENAI_BASE_URL)
        elif not stored_api_key:
            st.session_state.client = None
        
        # Model Selection
        st.markdown("### Model", unsafe_allow_html=True)
        # For testing: don't use env model
        # env_model = os.getenv("OPENAI_MODEL")  # Disabled for testing
        env_model = None
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
            label_visibility="collapsed",
            disabled=False
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
                
                # Fun conversation card - properly clickable with visible content
                bg_color = "#ff9ec7" if is_current else "#fff5f9"
                border_color = "#e91e63" if is_current else "#ffe0e6"
                text_color = "#ffffff" if is_current else "#1e293b"
                count_color = "#ffffff" if is_current else "#64748b"
                
                # Create plain button text (truncate long titles)
                display_title = (first_user_msg if first_user_msg else 'Empty conversation')[:35]
                if len(first_user_msg or '') > 35:
                    display_title += "..."
                button_text = f"{display_title} • {user_msg_count} msgs"
                
                # Check if button is clicked
                if st.button(
                    button_text,
                    key=f"conv_{conv_id}",
                    use_container_width=True,
                    type="primary" if is_current else "secondary"
                ):
                    load_conversation(conv_id)
                    st.rerun()
                
                # Style the button to look like a card
                st.markdown(f"""
                <style>
                    [data-testid="baseButton-{'primary' if is_current else 'secondary'}"][key*="conv_{conv_id}"] {{
                        background: {bg_color} !important;
                        border: 2px solid {border_color} !important;
                        border-radius: 14px !important;
                        padding: 1rem !important;
                        margin-bottom: 0.75rem !important;
                        height: auto !important;
                        min-height: auto !important;
                        transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) !important;
                        box-shadow: 0 2px 8px rgba(255, 158, 199, 0.2) !important;
                        cursor: pointer !important;
                        text-align: left !important;
                        justify-content: flex-start !important;
                    }}
                    [data-testid="baseButton-{'primary' if is_current else 'secondary'}"][key*="conv_{conv_id}"]:hover {{
                        transform: translateY(-2px) scale(1.02) !important;
                        box-shadow: 0 4px 12px rgba(255, 158, 199, 0.3) !important;
                    }}
                    [data-testid="baseButton-{'primary' if is_current else 'secondary'}"][key*="conv_{conv_id}"] > div {{
                        width: 100% !important;
                        text-align: left !important;
                        color: {text_color} !important;
                        font-size: 0.9rem !important;
                        font-weight: 600 !important;
                        line-height: 1.4 !important;
                        white-space: nowrap !important;
                        overflow: hidden !important;
                        text-overflow: ellipsis !important;
                    }}
                </style>
                """, unsafe_allow_html=True)
            
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
        
        # Version display at bottom of sidebar
        st.markdown("<div style='margin-top: 3rem; border-top: 1px solid rgba(255, 158, 199, 0.2); padding-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style='text-align: center; padding: 0.5rem 0;'>
            <div style='font-size: 0.75rem; color: #94a3b8; opacity: 0.7;'>Version {APP_VERSION}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Inject additional CSS to override Streamlit defaults
    st.markdown("""
    <style>
    /* Force override Streamlit's default chat message styles */
    div[data-testid="stChatMessageUser"] > div > div {
        background: linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%) !important;
        border-radius: 20px 20px 6px 20px !important;
    }
    
    div[data-testid="stChatMessageAssistant"] > div > div {
        background: linear-gradient(135deg, #ffffff 0%, #fff5f9 100%) !important;
        border: 2px solid #ffe0e6 !important;
        border-radius: 20px 20px 20px 6px !important;
    }
    
    /* Use JavaScript to apply styles after DOM loads */
    </style>
    <script>
    function applyChatStyles() {
        // Force style user messages
        document.querySelectorAll('[data-testid="stChatMessageUser"]').forEach(msg => {
            const contentDiv = msg.querySelector('div > div');
            if (contentDiv) {
                contentDiv.style.background = 'linear-gradient(135deg, #ff9ec7 0%, #e91e63 100%)';
                contentDiv.style.borderRadius = '20px 20px 6px 20px';
                contentDiv.style.padding = '1rem 1.25rem';
                contentDiv.style.boxShadow = '0 4px 12px rgba(255, 158, 199, 0.35), 0 2px 4px rgba(233, 30, 99, 0.2)';
                contentDiv.style.color = 'white';
            }
        });
        
        // Force style assistant messages
        document.querySelectorAll('[data-testid="stChatMessageAssistant"]').forEach(msg => {
            const contentDiv = msg.querySelector('div > div');
            if (contentDiv) {
                contentDiv.style.background = 'linear-gradient(135deg, #ffffff 0%, #fff5f9 100%)';
                contentDiv.style.border = '2px solid #ffe0e6';
                contentDiv.style.borderRadius = '20px 20px 20px 6px';
                contentDiv.style.padding = '1rem 1.25rem';
                contentDiv.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.08), 0 2px 4px rgba(255, 158, 199, 0.1)';
                contentDiv.style.color = '#1e293b';
            }
        });
        
        // Style text in messages
        document.querySelectorAll('[data-testid="stChatMessageUser"] .stMarkdown, [data-testid="stChatMessageUser"] p, [data-testid="stChatMessageUser"] span').forEach(el => {
            el.style.color = 'white';
        });
        
        document.querySelectorAll('[data-testid="stChatMessageAssistant"] .stMarkdown, [data-testid="stChatMessageAssistant"] .stMarkdown *').forEach(el => {
            el.style.color = '#1e293b';
        });
    }
    
    // Apply immediately and watch for new messages
    applyChatStyles();
    setInterval(applyChatStyles, 500);
    
    // Also apply when DOM is updated
    const observer = new MutationObserver(applyChatStyles);
    observer.observe(document.body, { childList: true, subtree: true });
    </script>
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
                    # Render markdown properly - CSS will force dark text for assistant
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
                st.error("Please enter your OpenAI API key in the sidebar settings.")
        else:
            with st.chat_message("assistant", avatar="✨"):
                # Enhanced loading state
                with st.spinner("💖 Pixel is thinking..."):
                    # Use selected model from preferences (for testing: no env fallback)
                    model = st.session_state.preferences.get("model", "gpt-3.5-turbo")
                    
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
                        # Render markdown - CSS will force dark text
                        st.markdown(response)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            
            # Save conversation
            save_current_conversation()
            
            # Rerun to update the chat
            st.rerun()

if __name__ == "__main__":
    main()

