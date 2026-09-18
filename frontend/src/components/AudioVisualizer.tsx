import React, { useEffect, useState } from 'react';

interface AudioVisualizerProps {
  audioData: number[];
  isListening: boolean;
  isSpeaking?: boolean;
}

export const AudioVisualizer: React.FC<AudioVisualizerProps> = ({
  audioData,
  isListening,
  isSpeaking = false,
}) => {
  const [speakingHeights, setSpeakingHeights] = useState<number[]>(new Array(16).fill(15));

  useEffect(() => {
    if (!isSpeaking) return;

    const interval = setInterval(() => {
      setSpeakingHeights(
        Array.from({ length: 16 }, (_, i) => {
          const base = 25 + Math.sin(Date.now() / 140 + i * 0.4) * 20;
          const jitter = (Math.random() - 0.5) * 45;
          return Math.max(12, Math.min(95, base + jitter));
        })
      );
    }, 80);

    return () => clearInterval(interval);
  }, [isSpeaking]);

  if (!isListening && !isSpeaking) return null;

  return (
    <div className="flex items-center justify-center space-x-1.5 h-12 py-1 px-4 my-2">
      {isListening
        ? audioData.slice(0, 16).map((val, idx) => (
            <div
              key={idx}
              className="w-1.5 bg-gradient-to-t from-red-500 to-rose-400 rounded-full transition-all duration-75"
              style={{ height: `${Math.max(10, val)}%` }}
            />
          ))
        : speakingHeights.map((val, idx) => (
            <div
              key={idx}
              className="w-1.5 bg-gradient-to-t from-cyan-500 to-blue-500 rounded-full transition-all duration-100 shadow-sm shadow-cyan-500/20"
              style={{ height: `${val}%` }}
            />
          ))}
    </div>
  );
};

