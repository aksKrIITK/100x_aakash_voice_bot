import React from 'react';
import { AlertTriangle, X } from 'lucide-react';

interface ErrorMessageProps {
  message: string | null;
  onClear: () => void;
}

export const ErrorMessage: React.FC<ErrorMessageProps> = ({ message, onClear }) => {
  if (!message) return null;

  return (
    <div className="w-full max-w-3xl mx-auto px-2 sm:px-4 my-2">
      <div className="bg-rose-500/10 border border-rose-500/30 text-rose-300 rounded-xl p-3.5 flex items-start justify-between shadow-lg text-xs sm:text-sm">
        <div className="flex items-start space-x-2.5">
          <AlertTriangle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />
          <div>
            <span className="font-semibold block text-rose-200 mb-0.5">Notice</span>
            <p className="leading-snug">{message}</p>
          </div>
        </div>
        <button
          type="button"
          onClick={onClear}
          className="text-rose-400 hover:text-white p-1 rounded-lg transition-colors"
          aria-label="Dismiss error"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
