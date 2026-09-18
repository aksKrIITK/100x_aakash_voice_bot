import { useState, useEffect, useCallback, useRef } from 'react';
import { VoiceState, Message } from '../types/conversation';
import { useAudioRecorder } from './useAudioRecorder';
import { useSpeechSynthesis, SentenceProgress } from './useSpeechSynthesis';
import { apiService } from '../services/api';
import { getLocalFallbackAnswer } from '../utils/localPersonalityFallback';

export interface UseVoiceBotReturn {
  voiceState: VoiceState;
  messages: Message[];
  conversationId: string;
  isBackendHealthy: boolean;
  audioData: number[];
  errorMessage: string | null;
  micPermission: 'prompt' | 'granted' | 'denied';
  isSpeakingTTS: boolean;
  currentSentenceIndex: number;
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
    currentSentenceIndex,
    speak,
    stop: stopTTS,
    replay: replayTTS
  } = useSpeechSynthesis();

  const isInitialized = useRef<boolean>(false);
  const streamTimerRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const activeAssistantMsgIdRef = useRef<string | null>(null);

  const clearStreamTimer = useCallback(() => {
    if (streamTimerRef.current) {
      clearInterval(streamTimerRef.current);
      streamTimerRef.current = null;
    }
  }, []);

  // Initialize conversation session & health check
  useEffect(() => {
    if (isInitialized.current) return;
    isInitialized.current = true;

    const init = async () => {
      const checkHealth = async () => {
        try {
          const health = await apiService.getHealth();
          if (health && health.status === 'healthy') {
            setIsBackendHealthy(true);
            return true;
          }
        } catch {
          setIsBackendHealthy(false);
        }
        return false;
      };

      const isOk = await checkHealth();
      if (!isOk) {
        setTimeout(checkHealth, 1500);
      }

      try {
        const res = await apiService.createConversation();
        setConversationId(res.conversation_id);
      } catch {
        // Fallback local conversation ID
        setConversationId(`conv-${Date.now()}`);
      }

      // Pre-warm Edge TTS connection in background to eliminate first answer latency
      try {
        apiService.fetchTTSAudio('Hi').catch(() => {});
      } catch {
        // Silent
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

  const handleStartSpeakingWithStream = useCallback(
    async (fullAnswer: string, assistantMsgId: string) => {
      activeAssistantMsgIdRef.current = assistantMsgId;
      clearStreamTimer();

      let prefixText = '';

      const onSentenceStart = (progress: SentenceProgress) => {
        clearStreamTimer();
        const sentenceWords = progress.sentence.split(/\s+/).filter(Boolean);
        if (sentenceWords.length === 0) return;

        let wordIdx = 0;
        const currentSentenceBase = prefixText;
        const intervalMs = Math.max(45, Math.floor((progress.durationMs * 0.88) / sentenceWords.length));

        streamTimerRef.current = setInterval(() => {
          wordIdx++;
          const currentSentenceChunk = sentenceWords.slice(0, wordIdx).join(' ');
          const display = currentSentenceBase
            ? `${currentSentenceBase} ${currentSentenceChunk}`
            : currentSentenceChunk;

          setMessages(prev =>
            prev.map(m =>
              m.id === assistantMsgId
                ? {
                    ...m,
                    content: display,
                    streamingText: display,
                    activeSentenceIndex: progress.index,
                    isStreaming: true
                  }
                : m
            )
          );

          if (wordIdx >= sentenceWords.length) {
            clearStreamTimer();
            prefixText = progress.accumulatedText;
          }
        }, intervalMs);
      };

      const onComplete = () => {
        clearStreamTimer();
        setMessages(prev =>
          prev.map(m =>
            m.id === assistantMsgId
              ? {
                  ...m,
                  content: fullAnswer,
                  streamingText: fullAnswer,
                  isStreaming: false
                }
              : m
          )
        );
        setVoiceState('IDLE');
      };

      await speak(fullAnswer, onSentenceStart, onComplete);
    },
    [clearStreamTimer, speak]
  );

  const startVoiceRecording = useCallback(async () => {
    clearError();
    clearStreamTimer();
    stopTTS();
    await startRecording();
  }, [clearError, clearStreamTimer, stopTTS, startRecording]);

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

      const assistantMsgId = `msg-${Date.now()}-assistant`;
      const assistantMsg: Message = {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        streamingText: '',
        isStreaming: true,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMsg, assistantMsg]);
      setVoiceState('SPEAKING');

      // Start synchronized streaming playback simultaneously
      handleStartSpeakingWithStream(response.answer, assistantMsgId);
    } catch {
      // Local fallback for offline / server reload
      const userText = browserTranscript || "What's your #1 superpower?";
      const fallbackAnswer = getLocalFallbackAnswer(userText);

      const userMsg: Message = {
        id: `msg-${Date.now()}-user`,
        role: 'user',
        content: userText,
        transcript: userText,
        isVoice: true,
        timestamp: new Date()
      };

      const assistantMsgId = `msg-${Date.now()}-assistant`;
      const assistantMsg: Message = {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        streamingText: '',
        isStreaming: true,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMsg, assistantMsg]);
      setVoiceState('SPEAKING');
      handleStartSpeakingWithStream(fallbackAnswer, assistantMsgId);
    }
  }, [stopRecording, conversationId, handleStartSpeakingWithStream]);

  const sendTextMessage = useCallback(
    async (text: string) => {
      if (!text.trim()) return;

      clearError();
      clearStreamTimer();
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

      const assistantMsgId = `msg-${Date.now()}-assistant`;
      const assistantMsg: Message = {
        id: assistantMsgId,
        role: 'assistant',
        content: '',
        streamingText: '',
        isStreaming: true,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, userMsg, assistantMsg]);

      try {
        const response = await apiService.sendChatMessage(currentConvId, text.trim());
        setVoiceState('SPEAKING');
        handleStartSpeakingWithStream(response.answer, assistantMsgId);
      } catch {
        // Fallback gracefully to local personality response
        const fallbackAnswer = getLocalFallbackAnswer(text.trim());
        setVoiceState('SPEAKING');
        handleStartSpeakingWithStream(fallbackAnswer, assistantMsgId);
      }
    },
    [clearError, clearStreamTimer, stopTTS, conversationId, handleStartSpeakingWithStream]
  );

  const stopSpeech = useCallback(() => {
    clearStreamTimer();
    stopTTS();
    // Complete any active streaming messages immediately
    if (activeAssistantMsgIdRef.current) {
      setMessages(prev =>
        prev.map(m =>
          m.id === activeAssistantMsgIdRef.current
            ? { ...m, isStreaming: false }
            : m
        )
      );
    }
    setVoiceState('IDLE');
  }, [clearStreamTimer, stopTTS]);

  const replayLastSpeech = useCallback(() => {
    const lastAssistant = [...messages].reverse().find(m => m.role === 'assistant');
    if (lastAssistant && lastAssistant.content) {
      stopSpeech();
      setVoiceState('SPEAKING');
      handleStartSpeakingWithStream(lastAssistant.content, lastAssistant.id);
    } else {
      replayTTS();
    }
  }, [messages, stopSpeech, handleStartSpeakingWithStream, replayTTS]);

  return {
    voiceState,
    messages,
    conversationId,
    isBackendHealthy,
    audioData,
    errorMessage,
    micPermission,
    isSpeakingTTS,
    currentSentenceIndex,
    startVoiceRecording,
    stopVoiceRecording,
    sendTextMessage,
    replayLastSpeech,
    stopSpeech,
    clearError
  };
}
