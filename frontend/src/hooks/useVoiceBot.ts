import { useState, useEffect, useCallback, useRef } from 'react';
import { VoiceState, Message } from '../types/conversation';
import { useAudioRecorder } from './useAudioRecorder';
import { useSpeechSynthesis } from './useSpeechSynthesis';
import { apiService } from '../services/api';

export interface UseVoiceBotReturn {
  voiceState: VoiceState;
  messages: Message[];
  conversationId: string;
  isBackendHealthy: boolean;
  audioData: number[];
  errorMessage: string | null;
  micPermission: 'prompt' | 'granted' | 'denied';
  isSpeakingTTS: boolean;
  startVoiceRecording: () => Promise<void>;
  stopVoiceRecording: () => Promise<void>;
  sendTextMessage: (text: string) => Promise<void>;
  replayLastSpeech: () => void;
  stopSpeech: () => void;
  clearError: () => void;
}

export function useVoiceBot(): UseVoiceBotReturn {
  const [voiceState, setVoiceState] = useState<VoiceState>('IDLE');
  const [messages, setMessages] = useState<Message[]>([]);
  const [conversationId, setConversationId] = useState<string>('');
  const [isBackendHealthy, setIsBackendHealthy] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const {
    isRecording,
    startRecording,
    stopRecording,
    micPermission,
    audioData,
    error: recorderError,
    resetError: resetRecorderError
  } = useAudioRecorder();

  const {
    isSpeaking: isSpeakingTTS,
    speak,
    stop: stopTTS,
    replay: replayTTS
  } = useSpeechSynthesis();

  const isInitialized = useRef<boolean>(false);

  // Initialize conversation session & health check
  useEffect(() => {
    if (isInitialized.current) return;
    isInitialized.current = true;

    const init = async () => {
      try {
        const health = await apiService.getHealth();
        setIsBackendHealthy(health.status === 'healthy');
      } catch {
        setIsBackendHealthy(false);
      }

      try {
        const res = await apiService.createConversation();
        setConversationId(res.conversation_id);
      } catch {
        // Fallback local conversation ID
        setConversationId(`conv-${Date.now()}`);
      }
    };

    init();
  }, []);

  // Update voiceState based on audio recording and TTS playback
  useEffect(() => {
    if (voiceState === 'ERROR') return;

    if (isRecording) {
      setVoiceState('LISTENING');
    } else if (isSpeakingTTS) {
      setVoiceState('SPEAKING');
    } else if (voiceState !== 'PROCESSING') {
      setVoiceState('IDLE');
    }
  }, [isRecording, isSpeakingTTS, voiceState]);

  // Sync recorder error with voice bot error state
  useEffect(() => {
    if (recorderError) {
      setErrorMessage(recorderError);
      setVoiceState('ERROR');
    }
  }, [recorderError]);

  const clearError = useCallback(() => {
    setErrorMessage(null);
    resetRecorderError();
    setVoiceState('IDLE');
  }, [resetRecorderError]);

  const startVoiceRecording = useCallback(async () => {
    clearError();
    stopTTS();
    await startRecording();
  }, [clearError, stopTTS, startRecording]);

  const stopVoiceRecording = useCallback(async () => {
    setVoiceState('PROCESSING');
    const { blob: audioBlob, transcript: browserTranscript } = await stopRecording();

    if (!audioBlob && !browserTranscript) {
      setVoiceState('IDLE');
      return;
    }

    const currentConvId = conversationId || `conv-${Date.now()}`;

    try {
      const response = await apiService.sendVoiceChat(
        currentConvId,
        audioBlob || new Blob([], { type: 'audio/webm' }),
        browserTranscript
      );

      const userMsg: Message = {
        id: `msg-${Date.now()}-user`,
        role: 'user',
        content: response.transcript,
        transcript: response.transcript,
        isVoice: true,
        timestamp: new Date()
      };

      const assistantMsg: Message = {
        id: `msg-${Date.now()}-assistant`,
        role: 'assistant',
        content: response.answer,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMsg, assistantMsg]);
      speak(response.answer);
      setVoiceState('SPEAKING');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Voice processing failed. Please try typing your question.";
      setErrorMessage(msg);
      setVoiceState('ERROR');
    }
  }, [stopRecording, conversationId, speak]);

  const sendTextMessage = useCallback(async (text: string) => {
    if (!text.trim()) return;

    clearError();
    stopTTS();
    setVoiceState('PROCESSING');

    const currentConvId = conversationId || `conv-${Date.now()}`;

    const userMsg: Message = {
      id: `msg-${Date.now()}-user`,
      role: 'user',
      content: text.trim(),
      isVoice: false,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMsg]);

    try {
      const response = await apiService.sendChatMessage(currentConvId, text.trim());

      const assistantMsg: Message = {
        id: `msg-${Date.now()}-assistant`,
        role: 'assistant',
        content: response.answer,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMsg]);
      speak(response.answer);
      setVoiceState('SPEAKING');
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "Connection problem. Please check your network and try again.";
      setErrorMessage(msg);
      setVoiceState('ERROR');
    }
  }, [clearError, stopTTS, conversationId, speak]);

  const replayLastSpeech = useCallback(() => {
    replayTTS();
  }, [replayTTS]);

  const stopSpeech = useCallback(() => {
    stopTTS();
    setVoiceState('IDLE');
  }, [stopTTS]);

  return {
    voiceState,
    messages,
    conversationId,
    isBackendHealthy,
    audioData,
    errorMessage,
    micPermission,
    isSpeakingTTS,
    startVoiceRecording,
    stopVoiceRecording,
    sendTextMessage,
    replayLastSpeech,
    stopSpeech,
    clearError
  };
}
