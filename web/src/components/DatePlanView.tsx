import { DatePlan } from '../types';

interface Props {
  plan: DatePlan;
  onReset: () => void;
}

export default function DatePlanView({ plan, onReset }: Props) {
  const budgetColor = {
    under: '#4caf50',
    within: '#2196f3',
    over: '#ff9800',
  }[plan.budgetFit];

  return (
    <div className="date-plan">
      <div className="plan-header">
        <h2>Your Date Plan</h2>
        <button onClick={onReset} className="btn-secondary">
          Plan Another Date
        </button>
      </div>

      <div className="plan-summary">
        <p>{plan.summary}</p>
      </div>

      <div className="plan-budget" style={{ borderColor: budgetColor }}>
        <div className="budget-info">
          <span className="budget-label">Total Estimated Cost:</span>
          <span className="budget-amount">Rs.{plan.totalEstimatedCost}</span>
        </div>
        <div className="budget-fit" style={{ color: budgetColor }}>
          {plan.budgetFit === 'under' && 'Under Budget'}
          {plan.budgetFit === 'within' && 'Within Budget'}
          {plan.budgetFit === 'over' && 'Over Budget'}
        </div>
      </div>

      <div className="plan-timeline">
        <h3>Date Timeline</h3>
        {plan.segments.map((segment, index) => (
          <div key={index} className="timeline-segment">
            <div className="segment-number">{index + 1}</div>
            <div className="segment-content">
              <h4>{segment.title}</h4>
              <div className="segment-time">{segment.timeWindow}</div>

              {segment.placeName && (
                <div className="segment-place">
                  <div className="place-name">{segment.placeName}</div>
                  {segment.placeAddress && (
                    <div className="place-address">{segment.placeAddress}</div>
                  )}
                  {segment.placeMapUrl && (
                    <a
                      href={segment.placeMapUrl}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="place-link"
                    >
                      View on Google Maps
                    </a>
                  )}
                </div>
              )}

              {segment.actions && segment.actions.length > 0 && (
                <div className="segment-actions">
                  <strong>What to do:</strong>
                  <ul>
                    {segment.actions.map((action, i) => (
                      <li key={i}>{action}</li>
                    ))}
                  </ul>
                </div>
              )}

              <div className="segment-cost">
                Cost: Rs.{segment.estimatedCost}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="plan-extras">
        <div className="extra-card gift-card">
          <h3>Gift Recommendation</h3>
          <div className="extra-content">
            <div className="extra-idea">{plan.giftRecommendation.idea}</div>
            <div className="extra-reason">{plan.giftRecommendation.reason}</div>
            <div className="extra-cost">
              Estimated Cost: Rs.{plan.giftRecommendation.estimatedCost}
            </div>
          </div>
        </div>

        <div className="extra-card flowers-card">
          <h3>Flowers Recommendation</h3>
          <div className="extra-content">
            <div className="extra-idea">{plan.flowersRecommendation.bouquetType}</div>
            <div className="extra-reason">{plan.flowersRecommendation.explanation}</div>
          </div>
        </div>
      </div>

      <div className="plan-footer">
        <p>Have a wonderful date!</p>
      </div>
    </div>
  );
}
