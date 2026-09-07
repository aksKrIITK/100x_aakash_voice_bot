import React from 'react';

interface AudioVisualizerProps {
  audioData: number[];
  isListening: boolean;
}

export const AudioVisualizer: React.FC<AudioVisualizerProps> = ({ audioData, isListening }) => {
  if (!isListening) return null;

  return (
    <div className="flex items-center justify-center space-x-1.5 h-10 py-1 px-4 my-2">
      {audioData.slice(0, 16).map((val, idx) => (
        <div
          key={idx}
          className="w-1.5 bg-gradient-to-t from-blue-600 to-cyan-400 rounded-full transition-all duration-75"
          style={{ height: `${Math.max(8, val)}%` }}
        />
      ))}
    </div>
  );
};
