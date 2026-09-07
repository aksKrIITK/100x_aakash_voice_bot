import React from 'react';
import { Bot } from 'lucide-react';

export const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-3 my-3 justify-start items-center">
      <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-600 flex items-center justify-center text-white shrink-0 shadow-md shadow-blue-500/20">
        <Bot className="w-5 h-5" />
      </div>
      <div className="glass-panel text-slate-300 rounded-2xl rounded-bl-none px-4 py-3 border border-slate-700/60 flex items-center space-x-2">
        <span className="text-xs font-medium text-slate-400">Aakash is thinking</span>
        <div className="flex space-x-1">
          <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.3s]" />
          <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce [animation-delay:-0.15s]" />
          <div className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce" />
        </div>
      </div>
    </div>
  );
};
