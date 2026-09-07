import React, { useEffect, useRef } from 'react';
import { Message } from '../types/conversation';
import { ConversationMessage } from './ConversationMessage';
import { TypingIndicator } from './TypingIndicator';

interface ConversationProps {
  messages: Message[];
  isProcessing: boolean;
  isSpeakingTTS: boolean;
  onReplaySpeech: () => void;
  onStopSpeech: () => void;
}

export const Conversation: React.FC<ConversationProps> = ({
  messages,
  isProcessing,
  isSpeakingTTS,
  onReplaySpeech,
  onStopSpeech,
}) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isProcessing]);

  if (messages.length === 0 && !isProcessing) {
    return null;
  }

  // Find index of the last assistant message
  let lastAssistantIdx = -1;
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i].role === 'assistant') {
      lastAssistantIdx = i;
      break;
    }
  }

  return (
    <div className="w-full max-w-3xl mx-auto my-4 px-2 sm:px-4">
      <div className="glass-panel rounded-2xl p-4 max-h-[420px] overflow-y-auto border border-slate-800 shadow-2xl space-y-2">
        {messages.map((msg, index) => (
          <ConversationMessage
            key={msg.id}
            message={msg}
            isLastAssistantMessage={index === lastAssistantIdx}
            isSpeakingTTS={isSpeakingTTS}
            onReplaySpeech={onReplaySpeech}
            onStopSpeech={onStopSpeech}
          />
        ))}

        {isProcessing && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
