import React from 'react';
import { Bot, Sparkles, Wifi, WifiOff } from 'lucide-react';

interface HeaderProps {
  isHealthy: boolean;
}

export const Header: React.FC<HeaderProps> = ({ isHealthy }) => {
  return (
    <header className="w-full border-b border-slate-800/80 bg-slate-950/70 backdrop-blur-md sticky top-0 z-40">
      <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold text-white tracking-tight">Aakash AI</h1>
              <span className="px-2 py-0.5 text-[10px] font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-full flex items-center gap-1">
                <Sparkles className="w-3 h-3" /> Voice Agent
              </span>
            </div>
            <p className="text-xs text-slate-400">Personal AI Representative</p>
          </div>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          {isHealthy ? (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Wifi className="w-3 h-3 mr-1.5 animate-pulse" /> Live Server
            </span>
          ) : (
            <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20">
              <WifiOff className="w-3 h-3 mr-1.5" /> Local Fallback Mode
            </span>
          )}
        </div>
      </div>
    </header>
  );
};
