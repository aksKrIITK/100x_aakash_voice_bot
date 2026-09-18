import React from 'react';
import { User, Bot, Volume2, Square, Mic, Radio } from 'lucide-react';
import { Message } from '../types/conversation';

interface ConversationMessageProps {
  message: Message;
  isLastAssistantMessage: boolean;
  isSpeakingTTS: boolean;
  onReplaySpeech: () => void;
  onStopSpeech: () => void;
}

export const ConversationMessage: React.FC<ConversationMessageProps> = ({
  message,
  isLastAssistantMessage,
  isSpeakingTTS,
  onReplaySpeech,
  onStopSpeech,
}) => {
  const isUser = message.role === 'user';
  const isCurrentlyStreaming = !isUser && isLastAssistantMessage && isSpeakingTTS && message.isStreaming;
  const displayText = message.streamingText || message.content;

  return (
    <div className={`flex gap-3 my-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className={`w-8 h-8 rounded-xl flex items-center justify-center text-white shrink-0 mt-1 shadow-md transition-all ${
          isCurrentlyStreaming
            ? 'bg-gradient-to-tr from-cyan-500 to-blue-600 ring-2 ring-cyan-400/50 shadow-cyan-500/30 animate-pulse'
            : 'bg-gradient-to-tr from-blue-600 to-indigo-600 shadow-blue-500/20'
        }`}>
          <Bot className="w-5 h-5" />
        </div>
      )}

      <div
        className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 shadow-lg text-sm leading-relaxed transition-all ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-none'
            : isCurrentlyStreaming
            ? 'glass-panel text-slate-100 rounded-bl-none border border-cyan-500/40 shadow-cyan-500/10'
            : 'glass-panel text-slate-100 rounded-bl-none border border-slate-700/60'
        }`}
      >
        {isUser && message.isVoice && (
          <div className="flex items-center gap-1.5 text-[11px] font-medium text-blue-200 mb-1">
            <Mic className="w-3 h-3" /> Voice Input Transcript
          </div>
        )}

        {!isUser && isCurrentlyStreaming && (
          <div className="flex items-center gap-1.5 text-[11px] font-medium text-cyan-300 mb-2">
            <Radio className="w-3 h-3 animate-spin" /> Speaking in real-time...
          </div>
        )}

        <div className="whitespace-pre-wrap">
          {displayText}
          {isCurrentlyStreaming && (
            <span className="inline-block w-2 h-2 ml-1.5 rounded-full bg-cyan-400 animate-ping align-middle" />
          )}
        </div>

        {!isUser && isLastAssistantMessage && (
          <div className="mt-3 pt-2 border-t border-slate-700/50 flex items-center gap-2">
            {isSpeakingTTS ? (
              <button
                type="button"
                onClick={onStopSpeech}
                className="px-2.5 py-1 rounded-lg bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30 text-xs font-medium flex items-center gap-1.5 transition-colors"
              >
                <Square className="w-3 h-3 fill-red-400" /> Stop Speaking
              </button>
            ) : (
              <button
                type="button"
                onClick={onReplaySpeech}
                className="px-2.5 py-1 rounded-lg bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 border border-blue-500/30 text-xs font-medium flex items-center gap-1.5 transition-colors"
              >
                <Volume2 className="w-3 h-3" /> Replay Audio
              </button>
            )}
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-xl bg-slate-700 flex items-center justify-center text-slate-200 shrink-0 mt-1">
          <User className="w-5 h-5" />
        </div>
      )}
    </div>
  );
};

