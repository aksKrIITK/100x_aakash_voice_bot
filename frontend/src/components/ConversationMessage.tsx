import React from 'react';
import { User, Bot, Volume2, Square, Mic } from 'lucide-react';
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

  return (
    <div className={`flex gap-3 my-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shrink-0 mt-1 shadow-md shadow-blue-500/20">
          <Bot className="w-5 h-5" />
        </div>
      )}

      <div
        className={`max-w-[85%] sm:max-w-[75%] rounded-2xl p-4 shadow-lg text-sm leading-relaxed ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-none'
            : 'glass-panel text-slate-100 rounded-bl-none border border-slate-700/60'
        }`}
      >
        {isUser && message.isVoice && (
          <div className="flex items-center gap-1.5 text-[11px] font-medium text-blue-200 mb-1">
            <Mic className="w-3 h-3" /> Voice Input Transcript
          </div>
        )}

        <div className="whitespace-pre-wrap">{message.content}</div>

        {!isUser && isLastAssistantMessage && (
          <div className="mt-3 pt-2 border-t border-slate-700/50 flex items-center gap-2">
            {isSpeakingTTS ? (
              <button
                type="button"
                onClick={onStopSpeech}
                className="px-2.5 py-1 rounded-lg bg-red-500/20 text-red-300 hover:bg-red-500/30 border border-red-500/30 text-xs font-medium flex items-center gap-1 transition-colors"
              >
                <Square className="w-3 h-3 fill-red-400" /> Stop Speaking
              </button>
            ) : (
              <button
                type="button"
                onClick={onReplaySpeech}
                className="px-2.5 py-1 rounded-lg bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 border border-blue-500/30 text-xs font-medium flex items-center gap-1 transition-colors"
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
