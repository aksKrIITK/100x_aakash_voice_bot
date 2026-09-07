import React from 'react';
import { Mic, Square, Volume2, Loader2 } from 'lucide-react';
import { VoiceState } from '../types/conversation';

interface MicrophoneButtonProps {
  voiceState: VoiceState;
  onStartRecording: () => void;
  onStopRecording: () => void;
  onStopSpeech: () => void;
}

export const MicrophoneButton: React.FC<MicrophoneButtonProps> = ({
  voiceState,
  onStartRecording,
  onStopRecording,
  onStopSpeech,
}) => {
  if (voiceState === 'LISTENING') {
    return (
      <div className="flex flex-col items-center justify-center my-4">
        <div className="relative">
          <span className="absolute -inset-3 rounded-full bg-red-500/30 animate-ping" />
          <button
            type="button"
            onClick={onStopRecording}
            className="relative w-20 h-20 rounded-full bg-gradient-to-tr from-red-600 to-rose-500 flex items-center justify-center shadow-xl shadow-red-500/30 hover:scale-105 active:scale-95 transition-all text-white"
            aria-label="Stop recording"
          >
            <Square className="w-8 h-8 fill-white" />
          </button>
        </div>
        <p className="mt-3 text-xs font-semibold text-rose-400 tracking-wide uppercase animate-pulse">
          Listening... (Click to Finish)
        </p>
      </div>
    );
  }

  if (voiceState === 'PROCESSING') {
    return (
      <div className="flex flex-col items-center justify-center my-4">
        <div className="w-20 h-20 rounded-full bg-slate-800 border border-blue-500/40 flex items-center justify-center shadow-lg text-blue-400">
          <Loader2 className="w-9 h-9 animate-spin" />
        </div>
        <p className="mt-3 text-xs font-semibold text-blue-400 tracking-wide uppercase">
          Thinking...
        </p>
      </div>
    );
  }

  if (voiceState === 'SPEAKING') {
    return (
      <div className="flex flex-col items-center justify-center my-4">
        <div className="w-20 h-20 rounded-full bg-gradient-to-tr from-indigo-600 to-blue-500 flex items-center justify-center shadow-xl shadow-blue-500/30 text-white animate-pulse">
          <Volume2 className="w-9 h-9" />
        </div>
        <div className="mt-3 flex items-center gap-3">
          <span className="text-xs font-semibold text-indigo-300 tracking-wide uppercase">
            Aakash is speaking...
          </span>
          <button
            type="button"
            onClick={onStopSpeech}
            className="px-3 py-1 text-xs font-medium bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-full border border-slate-700 flex items-center gap-1 transition-colors"
          >
            <Square className="w-3 h-3 fill-slate-300" /> Stop Audio
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center my-4">
      <button
        type="button"
        onClick={onStartRecording}
        className="group relative w-20 h-20 rounded-full bg-gradient-to-tr from-blue-600 via-blue-500 to-indigo-600 flex items-center justify-center shadow-xl shadow-blue-500/30 hover:scale-105 active:scale-95 transition-all text-white"
        aria-label="Start speaking"
      >
        <span className="absolute -inset-1 rounded-full bg-blue-500/20 group-hover:bg-blue-500/40 transition-colors" />
        <Mic className="w-9 h-9 relative z-10" />
      </button>
      <span className="mt-3 text-xs font-semibold text-slate-300 tracking-wide uppercase">
        🎤 Click to Start Speaking
      </span>
    </div>
  );
};
