import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="w-full border-t border-slate-800/60 py-6 mt-8 text-center text-xs text-slate-500">
      <div className="max-w-5xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div>
          <span className="font-semibold text-slate-400">Aakash AI Voice Bot</span> — Talk to an AI that answers as Aakash would.
        </div>
        <div className="flex items-center gap-4 text-slate-400">
          <span>React + Vite</span>
          <span>•</span>
          <span>FastAPI</span>
          <span>•</span>
          <span>OpenAI & Browser Speech</span>
        </div>
      </div>
    </footer>
  );
};
