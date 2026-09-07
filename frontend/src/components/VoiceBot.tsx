import React from 'react';
import { useVoiceBot } from '../hooks/useVoiceBot';
import { Header } from './Header';
import { Hero } from './Hero';
import { MicrophoneButton } from './MicrophoneButton';
import { AudioVisualizer } from './AudioVisualizer';
import { Conversation } from './Conversation';
import { SuggestedQuestions } from './SuggestedQuestions';
import { TextInput } from './TextInput';
import { ErrorMessage } from './ErrorMessage';
import { Footer } from './Footer';

export const VoiceBot: React.FC = () => {
  const {
    voiceState,
    messages,
    isBackendHealthy,
    audioData,
    errorMessage,
    isSpeakingTTS,
    startVoiceRecording,
    stopVoiceRecording,
    sendTextMessage,
    replayLastSpeech,
    stopSpeech,
    clearError
  } = useVoiceBot();

  const isBusy = voiceState === 'PROCESSING' || voiceState === 'LISTENING';

  return (
    <div className="min-h-screen flex flex-col justify-between bg-slate-950 text-slate-100">
      <div>
        <Header isHealthy={isBackendHealthy} />

        <main className="max-w-4xl mx-auto px-4 py-4">
          <Hero />

          <ErrorMessage message={errorMessage} onClear={clearError} />

          {/* Primary Microphone UI & Visualizer */}
          <div className="my-2">
            <MicrophoneButton
              voiceState={voiceState}
              onStartRecording={startVoiceRecording}
              onStopRecording={stopVoiceRecording}
              onStopSpeech={stopSpeech}
            />

            <AudioVisualizer
              audioData={audioData}
              isListening={voiceState === 'LISTENING'}
            />
          </div>

          {/* Chat Feed */}
          <Conversation
            messages={messages}
            isProcessing={voiceState === 'PROCESSING'}
            isSpeakingTTS={isSpeakingTTS}
            onReplaySpeech={replayLastSpeech}
            onStopSpeech={stopSpeech}
          />

          {/* Quick Prompts */}
          <SuggestedQuestions
            onSelectQuestion={sendTextMessage}
            disabled={isBusy}
          />

          {/* Text Input Fallback */}
          <TextInput
            onSend={sendTextMessage}
            disabled={isBusy}
          />
        </main>
      </div>

      <Footer />
    </div>
  );
};
