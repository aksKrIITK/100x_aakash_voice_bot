import React from 'react';
import { HelpCircle } from 'lucide-react';

interface SuggestedQuestionsProps {
  onSelectQuestion: (question: string) => void;
  disabled: boolean;
}

const SUGGESTED_QUESTIONS = [
  "Tell me about your journey",
  "What's your biggest strength?",
  "What do you want to improve?",
  "How do you push your limits?",
  "What motivates you?"
];

export const SuggestedQuestions: React.FC<SuggestedQuestionsProps> = ({
  onSelectQuestion,
  disabled
}) => {
  return (
    <div className="w-full max-w-3xl mx-auto my-4 px-2 sm:px-4">
      <div className="flex items-center gap-1.5 mb-2 text-xs font-semibold text-slate-400 uppercase tracking-wider">
        <HelpCircle className="w-3.5 h-3.5 text-blue-400" /> Suggested Interview Questions
      </div>
      <div className="flex flex-wrap gap-2">
        {SUGGESTED_QUESTIONS.map((q, idx) => (
          <button
            key={idx}
            type="button"
            disabled={disabled}
            onClick={() => onSelectQuestion(q)}
            className="px-3 py-1.5 text-xs font-medium bg-slate-900/80 hover:bg-slate-800 text-slate-300 hover:text-white rounded-xl border border-slate-700/60 hover:border-blue-500/40 transition-all disabled:opacity-50 disabled:cursor-not-allowed text-left active:scale-95 shadow-sm"
          >
            {q}
          </button>
        ))}
      </div>
    </div>
  );
};
