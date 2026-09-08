import { useState, useEffect, useCallback, useRef } from 'react';
import { apiService } from '../services/api';

export interface UseSpeechSynthesisReturn {
  isSpeaking: boolean;
  isPaused: boolean;
  isSupported: boolean;
  speak: (text: string) => void;
  stop: () => void;
  pause: () => void;
  resume: () => void;
  replay: () => void;
}

export function useSpeechSynthesis(): UseSpeechSynthesisReturn {
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [isSupported, setIsSupported] = useState<boolean>(true);
  const lastSpokenTextRef = useRef<string>('');
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);
  const speechIdRef = useRef<number>(0);

  useEffect(() => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setIsSupported(false);
    }
  }, []);

  const stop = useCallback(() => {
    // Increment ID to cancel all pending async TTS fetch calls
    speechIdRef.current += 1;

    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current.currentTime = 0;
      currentAudioRef.current = null;
    }
    if (isSupported && window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
    setIsSpeaking(false);
    setIsPaused(false);
  }, [isSupported]);

  const speakFallbackBrowser = useCallback((text: string, currentReqId: number) => {
    if (speechIdRef.current !== currentReqId) return;
    if (!isSupported || !window.speechSynthesis || !text) return;

    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = 1.0;
    utterance.pitch = 1.0;

    const voices = window.speechSynthesis.getVoices();
    const englishVoices = voices.filter(v => v.lang.startsWith('en'));

    const maleKeywords = ['david', 'mark', 'george', 'daniel', 'richard', 'james', 'alex', 'fred', 'rishi', 'guy', 'male', 'google uk english male', 'google us english'];
    const femaleKeywords = ['samantha', 'zira', 'jenny', 'victoria', 'karen', 'fiona', 'veena', 'hazel', 'susan', 'female', 'aria', 'eva', 'catherine'];

    const preferredMaleVoice = englishVoices.find(v => {
      const nameLower = v.name.toLowerCase();
      const isFemale = femaleKeywords.some(f => nameLower.includes(f));
      if (isFemale) return false;
      return maleKeywords.some(m => nameLower.includes(m));
    }) || englishVoices.find(v => {
      const nameLower = v.name.toLowerCase();
      return !femaleKeywords.some(f => nameLower.includes(f));
    }) || englishVoices[0];

    if (preferredMaleVoice) {
      utterance.voice = preferredMaleVoice;
    }

    utterance.onstart = () => {
      if (speechIdRef.current === currentReqId) {
        setIsSpeaking(true);
        setIsPaused(false);
      }
    };

    utterance.onend = () => {
      if (speechIdRef.current === currentReqId) {
        setIsSpeaking(false);
        setIsPaused(false);
      }
    };

    utterance.onerror = (e) => {
      if (e.error !== 'canceled' && speechIdRef.current === currentReqId) {
        setIsSpeaking(false);
        setIsPaused(false);
      }
    };

    window.speechSynthesis.speak(utterance);
  }, [isSupported]);

  const speak = useCallback(async (text: string) => {
    if (!text) return;
    stop();

    const currentReqId = speechIdRef.current;
    lastSpokenTextRef.current = text;

    // 1. First try fetching realistic neural Indian English male audio from backend (/api/v1/tts)
    const audioBlob = await apiService.fetchTTSAudio(text, 'en-IN-PrabhatNeural');

    // If a newer speech request came in while fetching, discard this old one
    if (speechIdRef.current !== currentReqId) {
      return;
    }

    if (audioBlob && audioBlob.size > 0) {
      try {
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        currentAudioRef.current = audio;

        audio.onplay = () => {
          if (speechIdRef.current === currentReqId) {
            setIsSpeaking(true);
            setIsPaused(false);
          } else {
            audio.pause();
          }
        };

        audio.onended = () => {
          if (speechIdRef.current === currentReqId) {
            setIsSpeaking(false);
            setIsPaused(false);
          }
          URL.revokeObjectURL(audioUrl);
          currentAudioRef.current = null;
        };

        audio.onerror = () => {
          URL.revokeObjectURL(audioUrl);
          currentAudioRef.current = null;
          if (speechIdRef.current === currentReqId) {
            speakFallbackBrowser(text, currentReqId);
          }
        };

        await audio.play();
        return;
      } catch {
        // Fall back to browser TTS if autoplay policy blocks audio
      }
    }

    // 2. Fallback to browser SpeechSynthesis if request is still active
    if (speechIdRef.current === currentReqId) {
      speakFallbackBrowser(text, currentReqId);
    }
  }, [stop, speakFallbackBrowser]);

  const pause = useCallback(() => {
    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      setIsPaused(true);
    } else if (isSupported && window.speechSynthesis && isSpeaking && !isPaused) {
      window.speechSynthesis.pause();
      setIsPaused(true);
    }
  }, [isSupported, isSpeaking, isPaused]);

  const resume = useCallback(() => {
    if (currentAudioRef.current) {
      currentAudioRef.current.play().catch(() => {});
      setIsPaused(false);
    } else if (isSupported && window.speechSynthesis && isSpeaking && isPaused) {
      window.speechSynthesis.resume();
      setIsPaused(false);
    }
  }, [isSupported, isSpeaking, isPaused]);

  const replay = useCallback(() => {
    if (lastSpokenTextRef.current) {
      speak(lastSpokenTextRef.current);
    }
  }, [speak]);

  return {
    isSpeaking,
    isPaused,
    isSupported,
    speak,
    stop,
    pause,
    resume,
    replay
  };
}
