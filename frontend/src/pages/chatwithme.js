import axios from 'axios';

const OLLAMA_URL = 'http://localhost:11434';

// 1. Generate a response (non-streaming)
export const chatWithOllama = async (messages) => {
  try {
    const response = await axios.post(`${OLLAMA_URL}/api/chat`, {
      model: 'llama3.2:latest',
      messages: messages,  // Your message array
      stream: false,
      options: {
        temperature: 0.7
      }
    });
    return response.data.message.content;
  } catch (error) {
    console.error('Ollama error:', error);
    throw error;
  }
};

// 2. Generate embeddings
export const getEmbedding = async (text) => {
  try {
    const response = await axios.post(`${OLLAMA_URL}/api/embeddings`, {
      model: 'nomic-embed-text',
      prompt: text
    });
    return response.data.embedding;
  } catch (error) {
    console.error('Embedding error:', error);
    throw error;
  }
};

// 3. List available models
export const listModels = async () => {
  try {
    const response = await axios.get(`${OLLAMA_URL}/api/tags`);
    return response.data.models;
  } catch (error) {
    console.error('List models error:', error);
    throw error;
  }
};