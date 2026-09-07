import React from 'react';

export const Hero: React.FC = () => {
  return (
    <div className="text-center py-6 px-4">
      <div className="inline-block px-3 py-1 mb-3 text-xs font-medium text-blue-400 bg-blue-500/10 border border-blue-500/20 rounded-full">
        Interactive Interview Experience
      </div>
      <h2 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-2">
        Hi, I'm Aakash's AI voice assistant 👋
      </h2>
      <p className="text-slate-300 text-sm sm:text-base max-w-xl mx-auto leading-relaxed">
        Ask me anything about my journey, strengths, personality, and goals.
      </p>
    </div>
  );
};
