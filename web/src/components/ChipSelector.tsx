import React from 'react';
import './ChipSelector.css';

const PERSONALITY_CHIPS = [
  'Introvert', 'Extrovert', 'Foodie', 'Adventurous', 'Romantic',
  'Homebody', 'Artsy', 'Sporty', 'Nature Lover', 'Bookworm',
  'Music Lover', 'Shopaholic', 'Night Owl', 'Minimalist', 'Trendy',
  'Traditional', 'Spiritual', 'Fitness Freak', 'Tech Geek', 'Chill'
];

const INTEREST_CHIPS = [
  'Fine Dining', 'Street Food', 'Movies', 'Live Music', 'Art Galleries',
  'Hiking', 'Shopping', 'Cafés', 'Cooking', 'Dancing',
  'Board Games', 'Photography', 'Yoga', 'Gaming', 'Cricket',
  'Theatre', 'Cycling', 'Stargazing', 'Pottery', 'Karaoke'
];

const DISLIKE_CHIPS = [
  'Crowds', 'Spicy Food', 'Loud Places', 'Outdoor Heat', 'Horror',
  'Non-veg Food', 'Alcohol', 'Smoking Areas', 'Late Nights', 'Long Drives'
];

interface ChipSelectorProps {
  label: string;
  chips: string[];
  selected: string[];
  onChange: (selected: string[]) => void;
  max?: number;
}

const ChipSelector: React.FC<ChipSelectorProps> = ({ label, chips, selected, onChange, max = 6 }) => {
  const toggle = (chip: string) => {
    if (selected.includes(chip)) {
      onChange(selected.filter(c => c !== chip));
    } else if (selected.length < max) {
      onChange([...selected, chip]);
    }
  };

  return (
    <div className="chip-selector">
      <label className="chip-label">{label} <span>(pick up to {max})</span></label>
      <div className="chip-grid">
        {chips.map(chip => (
          <button
            key={chip}
            type="button"
            className={`chip ${selected.includes(chip) ? 'chip--selected' : ''}`}
            onClick={() => toggle(chip)}
          >
            {chip}
          </button>
        ))}
      </div>
      {selected.length > 0 && (
        <div className="chip-summary">Selected: {selected.join(', ')}</div>
      )}
    </div>
  );
};

export { ChipSelector, PERSONALITY_CHIPS, INTEREST_CHIPS, DISLIKE_CHIPS };
