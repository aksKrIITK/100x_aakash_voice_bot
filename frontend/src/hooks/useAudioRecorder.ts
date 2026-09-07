import { useState, useRef, useCallback } from 'react';
import { getSupportedMimeType } from '../utils/audio';

export interface RecordingResult {
  blob: Blob | null;
  transcript: string;
}

export interface UseAudioRecorderReturn {
  isRecording: boolean;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<RecordingResult>;
  micPermission: 'prompt' | 'granted' | 'denied';
  audioData: number[];
  error: string | null;
  resetError: () => void;
}

export function useAudioRecorder(): UseAudioRecorderReturn {
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [micPermission, setMicPermission] = useState<'prompt' | 'granted' | 'denied'>('prompt');
  const [audioData, setAudioData] = useState<number[]>(new Array(16).fill(5));
  const [error, setError] = useState<string | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Web Speech API recognition instance for real-time browser transcription
  const recognitionRef = useRef<any>(null);
  const speechTranscriptRef = useRef<string>('');

  const stopAudioVisualization = useCallback(() => {
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    if (audioContextRef.current) {
      audioContextRef.current.close().catch(() => {});
      audioContextRef.current = null;
    }
    setAudioData(new Array(16).fill(5));
  }, []);

  const startAudioVisualization = useCallback((stream: MediaStream) => {
    try {
      const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
      const audioCtx = new AudioCtx();
      audioContextRef.current = audioCtx;

      const source = audioCtx.createMediaStreamSource(stream);
      const analyser = audioCtx.createAnalyser();
      analyser.fftSize = 64;
      analyser.smoothingTimeConstant = 0.8;
      source.connect(analyser);
      analyserRef.current = analyser;

      const dataArray = new Uint8Array(analyser.frequencyBinCount);

      const updateData = () => {
        if (!analyserRef.current) return;
        analyserRef.current.getByteFrequencyData(dataArray);

        // Take 16 frequency samples normalized between 5 and 100
        const samples: number[] = [];
        const step = Math.floor(dataArray.length / 16);
        for (let i = 0; i < 16; i++) {
          const val = dataArray[i * step] || 0;
          const normalized = Math.max(5, Math.min(100, (val / 255) * 100));
          samples.push(normalized);
        }
        setAudioData(samples);
        animationFrameRef.current = requestAnimationFrame(updateData);
      };

      updateData();
    } catch {
      // Non-critical visualizer failure
    }
  }, []);

  const startRecording = useCallback(async () => {
    setError(null);
    audioChunksRef.current = [];
    speechTranscriptRef.current = '';

    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setError("Microphone API is not supported in this browser. You can still type your question below.");
      setMicPermission('denied');
      return;
    }

    // Initialize browser SpeechRecognition if supported
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (SpeechRecognition) {
      try {
        const recognition = new SpeechRecognition();
        recognition.continuous = true;
        recognition.interimResults = true;
        recognition.lang = 'en-US';

        recognition.onresult = (event: any) => {
          let currentTranscript = '';
          for (let i = 0; i < event.results.length; i++) {
            currentTranscript += event.results[i][0].transcript;
          }
          speechTranscriptRef.current = currentTranscript.trim();
        };

        recognition.onerror = () => {
          // Non-blocking
        };

        recognition.start();
        recognitionRef.current = recognition;
      } catch {
        // Fallback silently if speech recognition initialization fails
      }
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      streamRef.current = stream;
      setMicPermission('granted');

      const mimeType = getSupportedMimeType();
      const mediaRecorder = new MediaRecorder(stream, { mimeType });
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.start(100);
      setIsRecording(true);
      startAudioVisualization(stream);
    } catch (err: unknown) {
      const errorMsg = err instanceof Error ? err.message : String(err);
      if (errorMsg.includes('Permission') || errorMsg.includes('denied') || errorMsg.includes('NotAllowedError')) {
        setMicPermission('denied');
        setError("Microphone access is disabled. You can still type your question below.");
      } else {
        setError("Could not start microphone recording. Please try again or type your question.");
      }
      setIsRecording(false);
    }
  }, [startAudioVisualization]);

  const stopRecording = useCallback((): Promise<RecordingResult> => {
    return new Promise((resolve) => {
      stopAudioVisualization();
      setIsRecording(false);

      if (recognitionRef.current) {
        try {
          recognitionRef.current.stop();
        } catch {
          // Ignore
        }
        recognitionRef.current = null;
      }

      const capturedTranscript = speechTranscriptRef.current;
      const mediaRecorder = mediaRecorderRef.current;

      if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
          streamRef.current = null;
        }
        resolve({ blob: null, transcript: capturedTranscript });
        return;
      }

      mediaRecorder.onstop = () => {
        const mimeType = mediaRecorder.mimeType || 'audio/webm';
        const blob = new Blob(audioChunksRef.current, { type: mimeType });
        
        if (streamRef.current) {
          streamRef.current.getTracks().forEach(track => track.stop());
          streamRef.current = null;
        }
        mediaRecorderRef.current = null;

        if (blob.size === 0) {
          setError("Empty audio recording detected. Please speak and try again.");
          resolve({ blob: null, transcript: capturedTranscript });
        } else {
          resolve({ blob, transcript: capturedTranscript });
        }
      };

      try {
        mediaRecorder.stop();
      } catch {
        resolve({ blob: null, transcript: capturedTranscript });
      }
    });
  }, [stopAudioVisualization]);

  const resetError = useCallback(() => setError(null), []);

  return {
    isRecording,
    startRecording,
    stopRecording,
    micPermission,
    audioData,
    error,
    resetError
  };
}
