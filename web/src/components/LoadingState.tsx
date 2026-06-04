import React from 'react';
import './LoadingState.css';

const STEPS = [
  { key: 'venues',  label: 'Searching venues near you' },
  { key: 'gifts',   label: 'Finding the perfect gift' },
  { key: 'flowers', label: 'Selecting your bouquet' },
  { key: 'crafting',label: 'Writing your date story' },
];

interface LoadingStateProps {
  currentStep: string;
  streamingText: string;
}

const LoadingState: React.FC<LoadingStateProps> = ({ currentStep, streamingText }) => {
  return (
    <div className="loading-wrap">
      <div className="loading-header">
        <h2>Creating your perfect date</h2>
        <p>This usually takes 10–15 seconds</p>
      </div>

      <div className="step-list">
        {STEPS.map((step, i) => {
          const stepIndex = STEPS.findIndex(s => s.key === currentStep);
          const state = i < stepIndex ? 'done' : i === stepIndex ? 'active' : 'pending';
          
          return (
            <div 
              key={step.key} 
              className={`step step--${state}`} 
              style={{ animationDelay: `${i * 0.1}s` }}
            >
              <div className="step-dot">
                {state === 'done' && (
                  <svg width="10" height="10" viewBox="0 0 10 10">
                    <path 
                      d="M2 5l2.5 2.5L8 3" 
                      stroke="currentColor" 
                      strokeWidth="1.5" 
                      fill="none" 
                      strokeLinecap="round"
                    />
                  </svg>
                )}
              </div>
              <span>{step.label}</span>
            </div>
          );
        })}
      </div>

      {streamingText && (
        <div className="stream-preview">
          <div className="stream-label">Your date plan is appearing...</div>
          <div className="stream-text">
            {streamingText}
            <span className="cursor">|</span>
          </div>
        </div>
      )}
    </div>
  );
};

export default LoadingState;
