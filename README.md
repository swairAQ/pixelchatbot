# Pixel Chat - Streamlit App

A Python-based Streamlit application with OpenAI chatbot integration that saves user preferences and maintains conversation history. Meet **Pixel** - your cute, bubbly AI bestie! ✨💖

## Features

- ✨ **Pixel - Your AI Bestie**: A super cute and bubbly chatbot with a girly, friendly personality powered by OpenAI's GPT models
- 💬 **Conversation History**: Automatically saves and loads previous conversations
- ⚙️ **User Preferences**: Saves model selection, temperature, and API key settings
- 📝 **Conversation Management**: Create new conversations, load previous ones, and delete conversations

## Installation

1. Clone or download this repository

2. Install required dependencies:

```bash
pip install -r requirements.txt
```

Or using pip:

```bash
pip install streamlit openai
```

## Usage

1. **Set up your OpenAI API Key** (choose one method):

   **Option A: Using .env file (Recommended)**

   - Create a `.env` file in the project root
   - Add your API key: `OPENAI_API_KEY=your_api_key_here`
   - The app will automatically load the key from the environment file

   **Option B: Manual input**

   - Enter your OpenAI API key in the sidebar settings when the app runs

2. Install required dependencies (if not already installed):

```bash
pip install -r requirements.txt
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

4. Select your preferred model (gpt-3.5-turbo, gpt-4, etc.)

5. Adjust the temperature setting for response creativity (0.0 = focused, 2.0 = creative)

6. Start chatting! Your conversations will be automatically saved.

## Features in Detail

### Conversation History

- All conversations are saved to `conversations.json`
- Access previous conversations from the sidebar
- Conversations are timestamped and identified by ID
- View last 10 conversations in the sidebar

### User Preferences

- Preferences are saved to `preferences.json`
- Includes:
  - OpenAI API key (if manually entered, not from .env)
  - Selected model
  - Temperature setting
- Settings persist across app sessions
- **Note**: API key from `.env` file takes priority over manually entered keys

### Conversation Management

- Create new conversations with the "New Conversation" button
- Load previous conversations by clicking on them in the sidebar
- Delete current conversation with the delete button

## File Structure

```
pythonChatbot/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
├── .gitignore         # Git ignore file
├── conversations.json # Conversation history (auto-generated)
└── preferences.json   # User preferences (auto-generated)
```

## Notes

- Make sure to add your OpenAI API key (in `.env` file or manually) to use the chatbot
- The `.env` file is excluded from git for security (see `.gitignore`)
- Conversation and preference files are auto-generated when you first use the app
- These files are excluded from git by default (see `.gitignore`)

## Deployment 🚀

Want to share Pixel with your friends? Check out **[DEPLOYMENT.md](DEPLOYMENT.md)** for free hosting options!

### Quick Deploy Options:
- **Streamlit Community Cloud** (Recommended) - Free, official Streamlit hosting
- **Render** - Free tier available
- **Railway** - Free tier with $5/month credit
- **Fly.io** - Free tier available

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions!

## Requirements

- Python 3.8+
- Streamlit 1.28.0+
- OpenAI 1.3.0+
- python-dotenv 1.0.0+
