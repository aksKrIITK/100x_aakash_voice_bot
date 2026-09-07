export interface HealthResponse {
  status: string;
  version: string;
}

export interface ChatResponse {
  conversation_id: string;
  answer: string;
}

export interface VoiceChatResponse {
  conversation_id: string;
  transcript: string;
  answer: string;
}

export interface ConversationCreateResponse {
  conversation_id: string;
}

export interface ApiErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>;
  };
}
