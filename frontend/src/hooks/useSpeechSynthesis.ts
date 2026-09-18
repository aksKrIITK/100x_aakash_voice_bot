import { useState, useEffect, useCallback, useRef } from 'react';
import { apiService } from '../services/api';

export interface SentenceProgress {
  index: number;
  total: number;
  sentence: string;
  accumulatedText: string;
  durationMs: number;
}

export interface UseSpeechSynthesisReturn {
  isSpeaking: boolean;
  isPaused: boolean;
  isSupported: boolean;
  currentSentenceIndex: number;
  speak: (
    text: string,
    onSentenceStart?: (progress: SentenceProgress) => void,
    onComplete?: () => void
  ) => Promise<void>;
  stop: () => void;
  pause: () => void;
  resume: () => void;
  replay: () => void;
}

// Splits full paragraph text into natural human conversational thought clauses / sentences
export function splitIntoConversationalSentences(text: string): string[] {
  if (!text) return [];

  // Clean markdown noise
  const clean = text.replace(/[*#_`~>[\]]/g, '').trim();

  // Split on punctuation while preserving meaning
  const rawChunks = clean.split(/(?<=[.!?])\s+|(?<=\.\.\.)\s+|\n+/);
  const sentences: string[] = [];

  for (const chunk of rawChunks) {
    const trimmed = chunk.trim();
    if (!trimmed) continue;

    // If chunk is excessively long (> 180 chars) and contains commas/semicolons, split for natural breathing
    if (trimmed.length > 180 && (trimmed.includes(', ') || trimmed.includes('; '))) {
      const subParts = trimmed.split(/(?<=,|;)\s+/);
      let currentSub = '';
      for (const part of subParts) {
        if ((currentSub + ' ' + part).length < 140) {
          currentSub = currentSub ? `${currentSub} ${part}` : part;
        } else {
          if (currentSub) sentences.push(currentSub.trim());
          currentSub = part;
        }
      }
      if (currentSub) sentences.push(currentSub.trim());
    } else {
      sentences.push(trimmed);
    }
  }

  return sentences.length > 0 ? sentences : [clean];
}

export function useSpeechSynthesis(): UseSpeechSynthesisReturn {
  const [isSpeaking, setIsSpeaking] = useState<boolean>(false);
  const [isPaused, setIsPaused] = useState<boolean>(false);
  const [isSupported, setIsSupported] = useState<boolean>(true);
  const [currentSentenceIndex, setCurrentSentenceIndex] = useState<number>(0);

  const lastSpokenTextRef = useRef<string>('');
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);
  const speechIdRef = useRef<number>(0);
  const audioCacheRef = useRef<Map<string, Blob>>(new Map());
  const isPlayingRef = useRef<boolean>(false);

  useEffect(() => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      setIsSupported(false);
    }
  }, []);

  const stop = useCallback(() => {
    // Increment ID to cancel all pending async TTS fetch/play chains
    speechIdRef.current += 1;
    isPlayingRef.current = false;

    if (currentAudioRef.current) {
      try {
        currentAudioRef.current.pause();
        currentAudioRef.current.currentTime = 0;
      } catch {
        // Safe ignore
      }
      currentAudioRef.current = null;
    }

    if (isSupported && window.speechSynthesis) {
      try {
        window.speechSynthesis.cancel();
      } catch {
        // Safe ignore
      }
    }

    setIsSpeaking(false);
    setIsPaused(false);
    setCurrentSentenceIndex(0);
  }, [isSupported]);

  // Fallback browser speech synthesis with natural cadence sentence by sentence
  const speakBrowserFallbackQueue = useCallback(
    async (
      sentences: string[],
      currentReqId: number,
      onSentenceStart?: (progress: SentenceProgress) => void,
      onComplete?: () => void
    ) => {
      if (!isSupported || !window.speechSynthesis || speechIdRef.current !== currentReqId) return;

      const voices = window.speechSynthesis.getVoices();
      const englishVoices = voices.filter(v => v.lang.startsWith('en') || v.lang.startsWith('hi'));
      const indianMaleKeywords = ['prabhat', 'ravi', 'rishi', 'en-in', 'india', 'hindi', 'madhur', 'google हिन्दी'];
      const generalMaleKeywords = ['david', 'mark', 'george', 'daniel', 'richard', 'james', 'alex', 'guy', 'male', 'google uk english male'];
      const femaleKeywords = ['samantha', 'zira', 'jenny', 'victoria', 'karen', 'fiona', 'veena', 'hazel', 'susan', 'female', 'aria', 'eva', 'catherine', 'neerja', 'swara'];

      let preferredVoice = englishVoices.find(v => {
        const nameLower = v.name.toLowerCase();
        const langLower = v.lang.toLowerCase();
        if (femaleKeywords.some(f => nameLower.includes(f))) return false;
        return indianMaleKeywords.some(k => nameLower.includes(k) || langLower.includes(k));
      });

      if (!preferredVoice) {
        preferredVoice = englishVoices.find(v => {
          const nameLower = v.name.toLowerCase();
          if (femaleKeywords.some(f => nameLower.includes(f))) return false;
          return generalMaleKeywords.some(m => nameLower.includes(m));
        });
      }

      if (!preferredVoice) {
        preferredVoice = englishVoices.find(v => !femaleKeywords.some(f => v.name.toLowerCase().includes(f))) || englishVoices[0];
      }

      let accumulated = '';
      setIsSpeaking(true);

      for (let i = 0; i < sentences.length; i++) {
        if (speechIdRef.current !== currentReqId) return;

        const sentence = sentences[i];
        accumulated = accumulated ? `${accumulated} ${sentence}` : sentence;
        setCurrentSentenceIndex(i);

        // Word count estimate for timing
        const wordCount = sentence.split(/\s+/).length;
        const estDurationMs = Math.max(1200, wordCount * 280);

        if (onSentenceStart) {
          onSentenceStart({
            index: i,
            total: sentences.length,
            sentence,
            accumulatedText: accumulated,
            durationMs: estDurationMs
          });
        }

        await new Promise<void>((resolve) => {
          if (speechIdRef.current !== currentReqId) {
            resolve();
            return;
          }

          window.speechSynthesis.cancel();
          const utterance = new SpeechSynthesisUtterance(sentence);
          utterance.rate = 0.92;
          utterance.pitch = 0.98;
          if (preferredVoice) utterance.voice = preferredVoice;

          utterance.onend = () => resolve();
          utterance.onerror = () => resolve();

          window.speechSynthesis.speak(utterance);
        });

        // Natural human breath pause between sentences
        if (i < sentences.length - 1 && speechIdRef.current === currentReqId) {
          await new Promise(r => setTimeout(r, 220));
        }
      }

      if (speechIdRef.current === currentReqId) {
        setIsSpeaking(false);
        if (onComplete) onComplete();
      }
    },
    [isSupported]
  );

  // Play individual audio blob using HTML5 Audio
  const playAudioChunk = useCallback((blob: Blob, currentReqId: number): Promise<number> => {
    return new Promise((resolve, reject) => {
      if (speechIdRef.current !== currentReqId) {
        resolve(0);
        return;
      }

      const audioUrl = URL.createObjectURL(blob);
      const audio = new Audio(audioUrl);
      currentAudioRef.current = audio;

      audio.onloadedmetadata = () => {
        const durMs = isFinite(audio.duration) ? Math.round(audio.duration * 1000) : 2000;
        audio.play().catch(err => {
          URL.revokeObjectURL(audioUrl);
          currentAudioRef.current = null;
          reject(err);
        });
        resolve(durMs);
      };

      audio.onerror = (e) => {
        URL.revokeObjectURL(audioUrl);
        currentAudioRef.current = null;
        reject(e);
      };
    });
  }, []);

  const waitForAudioToEnd = useCallback((audio: HTMLAudioElement, currentReqId: number): Promise<void> => {
    return new Promise((resolve) => {
      if (!audio || speechIdRef.current !== currentReqId) {
        resolve();
        return;
      }

      const cleanup = () => {
        audio.removeEventListener('ended', handleEnded);
        audio.removeEventListener('error', handleError);
        resolve();
      };

      const handleEnded = () => cleanup();
      const handleError = () => cleanup();

      audio.addEventListener('ended', handleEnded);
      audio.addEventListener('error', handleError);
    });
  }, []);

  const fetchAudioWithCache = useCallback(async (sentence: string): Promise<Blob | null> => {
    const trimmed = sentence.trim();
    if (!trimmed) return null;

    if (audioCacheRef.current.has(trimmed)) {
      return audioCacheRef.current.get(trimmed)!;
    }

    try {
      const blob = await apiService.fetchTTSAudio(trimmed, 'en-US-AndrewMultilingualNeural');
      if (blob && blob.size > 0) {
        if (audioCacheRef.current.size > 40) {
          const firstKey = audioCacheRef.current.keys().next().value;
          if (firstKey) audioCacheRef.current.delete(firstKey);
        }
        audioCacheRef.current.set(trimmed, blob);
        return blob;
      }
    } catch {
      // Fallback
    }
    return null;
  }, []);

  const speak = useCallback(
    async (
      text: string,
      onSentenceStart?: (progress: SentenceProgress) => void,
      onComplete?: () => void
    ) => {
      if (!text || !text.trim()) return;

      stop();
      const currentReqId = speechIdRef.current;
      isPlayingRef.current = true;
      lastSpokenTextRef.current = text;

      const sentences = splitIntoConversationalSentences(text);
      if (sentences.length === 0) return;

      setIsSpeaking(true);
      setIsPaused(false);

      // Pre-fetch sentence 0 immediately
      let nextBlobPromise: Promise<Blob | null> = fetchAudioWithCache(sentences[0]);
      let accumulated = '';
      let usedNeuralTTS = false;

      for (let i = 0; i < sentences.length; i++) {
        if (speechIdRef.current !== currentReqId) return;

        const sentence = sentences[i];
        accumulated = accumulated ? `${accumulated} ${sentence}` : sentence;
        setCurrentSentenceIndex(i);

        // Simultaneously pre-fetch next sentence (i+1) in background while current plays
        const currentBlobPromise = nextBlobPromise;
        if (i + 1 < sentences.length) {
          nextBlobPromise = fetchAudioWithCache(sentences[i + 1]);
        }

        let audioBlob: Blob | null = null;
        try {
          audioBlob = await currentBlobPromise;
        } catch {
          audioBlob = null;
        }

        if (speechIdRef.current !== currentReqId) return;

        if (audioBlob && audioBlob.size > 0) {
          usedNeuralTTS = true;
          try {
            const estDurationMs = Math.max(1400, sentence.split(/\s+/).length * 300);
            if (onSentenceStart) {
              onSentenceStart({
                index: i,
                total: sentences.length,
                sentence,
                accumulatedText: accumulated,
                durationMs: estDurationMs
              });
            }

            await playAudioChunk(audioBlob, currentReqId);

            if (currentAudioRef.current) {
              await waitForAudioToEnd(currentAudioRef.current, currentReqId);
            }

            // Natural human breath pause between sentences (220-260ms)
            if (i < sentences.length - 1 && speechIdRef.current === currentReqId) {
              await new Promise(r => setTimeout(r, 240));
            }
            continue;
          } catch {
            // If playback failed, fallback
          }
        }

        // If Edge TTS failed on sentence 0, switch to browser speech queue
        if (!usedNeuralTTS && i === 0) {
          await speakBrowserFallbackQueue(sentences, currentReqId, onSentenceStart, onComplete);
          return;
        }
      }

      if (speechIdRef.current === currentReqId) {
        setIsSpeaking(false);
        isPlayingRef.current = false;
        if (onComplete) onComplete();
      }
    },
    [stop, fetchAudioWithCache, playAudioChunk, waitForAudioToEnd, speakBrowserFallbackQueue]
  );

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
    currentSentenceIndex,
    speak,
    stop,
    pause,
    resume,
    replay
  };
}
