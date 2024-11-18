Here's the content formatted as a `README.md` file:

```markdown
# Build Real-Time AI Voice Assistant With RAG Pipeline And Memory | Mistral LLM | Ollama

This repository contains code for a real-time voice assistant that interacts with an AI model for natural language understanding (NLU). The assistant captures audio input from users, transcribes it, and uses an AI-powered model to generate context-aware responses. It also leverages a knowledge base for enriched interactions and can save critical information into a `.json` file.

## Features

- **Real-Time Audio Recording**: Captures audio input in chunks.
- **Speech-to-Text**: Transcribes recorded audio using `faster_whisper`.
- **AI-Powered NLU**: Interacts with the Mistral LLM (via Ollama) for generating context-aware responses.
- **Knowledge Base Integration**: Uses a Qdrant vector database for enhanced context retention.
- **Memory Persistence**: Saves key conversation data into a `.json` file for future reference.

## Prerequisites

Before running the code, ensure you have the following dependencies installed:

- Python 3.8 or above
- `pyaudio`
- `numpy`
- `faster_whisper`
- `qdrant_client`
- Additional dependencies listed in `requirements.txt`

### Installing Dependencies

```bash
pip install -r requirements.txt
```

## Setup Guide

### Step 1: Clone the Repository

Clone this repository to your local machine.

```bash
git clone git@github.com/prantakhandaker/voice_assistant_for_ERP.git
cd voice_assistant_for_ERP
```

### Step 2: Install and Configure Ollama Mistral

**Ollama** is required for running the Mistral LLM locally.

1. **Download Ollama**: Follow the instructions from the [Ollama official website](https://ollama.com/download) to download and install it on your system.

2. **Download Mistral Model**:
   ```bash
   ollama pull mistral
   ```

3. **Test Ollama Setup**:
   Ensure that Ollama is correctly installed by running:
   ```bash
   ollama list
   ```

### Step 3: Install and Set Up Qdrant Vector Database

**Qdrant** is a vector database used to store and retrieve embeddings for contextual understanding.

1. **Install Qdrant** (if not using Docker):
   ```bash
   pip install qdrant-client
   ```

2. **Run Qdrant via Docker** (recommended for better performance):
   ```bash
   docker run -p 6333:6333 qdrant/qdrant
   ```

3. **Verify Qdrant Setup**:
   Access the Qdrant web UI by navigating to `http://localhost:6333` in your browser.

### Step 4: Run the Voice Assistant

Launch the application using the command:

```bash
python app.py
```

### Step 5: Interact with the Voice Assistant

1. Follow the prompts to speak into your microphone when prompted.
2. The assistant will transcribe your speech and provide AI-powered responses based on context.
3. Important data points from the conversation are saved in a `.json` file for later use.

## Configuration

- Adjust the model size, chunk length, and other parameters in `app.py` as needed.
- Modify the paths and settings related to the knowledge base, AI model, and Qdrant configuration.

## Troubleshooting

- Ensure your system's microphone is properly set up and accessible by the script.
- If you encounter issues with the audio input, check `pyaudio` installation and microphone permissions.
- Use the following command to test `faster_whisper` functionality separately:
  ```bash
  python -m faster_whisper --help
  ```

## Notes

- Make sure to handle exceptions and errors gracefully, especially during audio recording, transcription, and AI interactions.
- This project is designed to work in real-time, so system performance may vary based on hardware capabilities.


## Acknowledgments

- The AI model used in this project is based on `faster_whisper`.
- Special thanks to the developers of `pyaudio`, `numpy`, and `qdrant-client` for their contributions.
```