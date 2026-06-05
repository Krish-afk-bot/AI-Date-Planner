import { useState } from 'react';
import { DateRequest, DatePlan } from './types';
import DateForm from './components/DateForm';
import DatePlanView from './components/DatePlanView';
import LoadingState from './components/LoadingState';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [datePlan, setDatePlan] = useState<DatePlan | null>(null);
  const [currentStep, setCurrentStep] = useState('venues');
  const [streamingText, setStreamingText] = useState('');

  const handlePlanDate = async (request: DateRequest) => {
    setLoading(true);
    setError(null);
    setDatePlan(null);
    setStreamingText('');
    setCurrentStep('venues');

    try {
      const response = await fetch('/api/plan-date/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
      });

      if (!response.body) {
        throw new Error('No response body');
      }

      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      let buffer = '';

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (!line.startsWith('data: ')) continue;
          const data = JSON.parse(line.slice(6));

          if (data.type === 'status') {
            // Map status message to step key
            if (data.message.includes('venue')) setCurrentStep('venues');
            if (data.message.includes('Crafting') || data.message.includes('perfect')) setCurrentStep('crafting');
          } else if (data.type === 'chunk') {
            setStreamingText(prev => prev + data.text);
            setCurrentStep('crafting');
          } else if (data.type === 'structured') {
            setDatePlan(data.data);
          } else if (data.type === 'done') {
            setLoading(false);
          } else if (data.type === 'error') {
            setError(data.message);
            setLoading(false);
          }
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
      setLoading(false);
    }
  };

  const handleReset = () => {
    setDatePlan(null);
    setError(null);
    setStreamingText('');
  };

  return (
    <div className="app">
      <header className="header">
        <h1>💕 AI Date Planner</h1>
        <p>Personalized date planning powered by AI</p>
      </header>

      <main className="main">
        {error && (
          <div className="error-banner">
            <p>❌ {error}</p>
            <button onClick={() => setError(null)}>Dismiss</button>
          </div>
        )}

        {loading && (
          <LoadingState 
            currentStep={currentStep} 
            streamingText={streamingText}
          />
        )}

        {!loading && !datePlan && (
          <DateForm onSubmit={handlePlanDate} />
        )}

        {!loading && datePlan && (
          <DatePlanView plan={datePlan} onReset={handleReset} />
        )}
      </main>

      <footer className="footer">
        <p>Made with ❤️ using Gemini AI</p>
      </footer>
    </div>
  );
}

export default App;
