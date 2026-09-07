import {
  HealthResponse,
  ChatResponse,
  VoiceChatResponse,
  ConversationCreateResponse,
  ApiErrorResponse
} from '../types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let errorMessage = 'Network response was not ok';
    try {
      const errData: ApiErrorResponse = await response.json();
      if (errData?.error?.message) {
        errorMessage = errData.error.message;
      }
    } catch {
      errorMessage = `Server error (${response.status})`;
    }
    throw new Error(errorMessage);
  }
  return response.json() as Promise<T>;
}

export const apiService = {
  async getHealth(): Promise<HealthResponse> {
    const res = await fetch(`${API_BASE_URL}/health`, { method: 'GET' });
    return handleResponse<HealthResponse>(res);
  },

  async createConversation(): Promise<ConversationCreateResponse> {
    const res = await fetch(`${API_BASE_URL}/conversations`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' }
    });
    return handleResponse<ConversationCreateResponse>(res);
  },

  async sendChatMessage(conversationId: string, message: string): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ conversation_id: conversationId, message })
    });
    return handleResponse<ChatResponse>(res);
  },

  async sendVoiceChat(conversationId: string, audioBlob: Blob, transcript?: string): Promise<VoiceChatResponse> {
    const formData = new FormData();
    formData.append('conversation_id', conversationId);
    if (transcript && transcript.trim()) {
      formData.append('transcript', transcript.trim());
    }
    
    // Choose correct filename extension based on mime type
    const mimeType = audioBlob.type || 'audio/webm';
    let ext = 'webm';
    if (mimeType.includes('wav')) ext = 'wav';
    else if (mimeType.includes('mp4') || mimeType.includes('m4a')) ext = 'm4a';
    else if (mimeType.includes('ogg')) ext = 'ogg';

    formData.append('audio', audioBlob, `recording.${ext}`);

    const res = await fetch(`${API_BASE_URL}/voice/chat`, {
      method: 'POST',
      body: formData
    });
    return handleResponse<VoiceChatResponse>(res);
  },

  async fetchTTSAudio(text: string, voice: string = 'en-IN-PrabhatNeural'): Promise<Blob | null> {
    try {
      const res = await fetch(`${API_BASE_URL}/tts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text, voice })
      });
      if (res.ok) {
        return await res.blob();
      }
    } catch {
      // Fallback silently if neural TTS is unavailable
    }
    return null;
  }
};
