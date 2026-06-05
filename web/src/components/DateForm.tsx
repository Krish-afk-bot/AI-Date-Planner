import React, { useState } from 'react';
import { DateRequest, PersonProfile } from '../types';
import { ChipSelector, PERSONALITY_CHIPS, INTEREST_CHIPS, DISLIKE_CHIPS } from './ChipSelector';

interface Props {
  onSubmit: (request: DateRequest) => void;
}

const defaultProfile = (): Omit<PersonProfile, 'location'> & { location: { city: string; lat?: number; lng?: number } } => ({
  name: '',
  age: 25,
  gender: 'other' as const,
  location: { city: '' },
  personalityTags: [],
  interests: [],
  dislikes: [],
});

const OCCASIONS = [
  { value: 'casual', label: 'Casual Hangout' },
  { value: 'first_date', label: 'First Date' },
  { value: 'anniversary', label: 'Anniversary' },
  { value: 'birthday', label: 'Birthday' },
];

const TIME_SLOTS = ['morning', 'afternoon', 'evening', 'night'];
const CONSTRAINTS = ['vegetarian', 'outdoor', 'quiet', 'alcohol-free', 'pet-friendly'];
const STEPS = ['About You', 'About Partner', 'Date Details'];

export default function DateForm({ onSubmit }: Props) {
  const [step, setStep] = useState(0);
  const [selfProfile, setSelfProfile] = useState(defaultProfile());
  const [partnerProfile, setPartnerProfile] = useState(defaultProfile());
  const [budgetMin, setBudgetMin] = useState(1000);
  const [budgetMax, setBudgetMax] = useState(3000);
  const [occasion, setOccasion] = useState<DateRequest['occasion']>('casual');
  const [maxTravel, setMaxTravel] = useState(10);
  const [timeSlots, setTimeSlots] = useState<string[]>(['evening']);
  const [hardConstraints, setHardConstraints] = useState<string[]>([]);
  const [locationStatus, setLocationStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [userLocation, setUserLocation] = useState<{ lat: number; lng: number } | null>(null);

  const updateSelf = (field: string, value: unknown) =>
    setSelfProfile(prev => ({ ...prev, [field]: value }));
  const updatePartner = (field: string, value: unknown) =>
    setPartnerProfile(prev => ({ ...prev, [field]: value }));

  const requestLocation = () => {
    setLocationStatus('loading');
    navigator.geolocation.getCurrentPosition(
      pos => {
        setUserLocation({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        setLocationStatus('success');
      },
      () => setLocationStatus('error'),
      { timeout: 8000 }
    );
  };

  const toggleSlot = (slot: string) =>
    setTimeSlots(prev =>
      prev.includes(slot) ? prev.filter(s => s !== slot) : [...prev, slot]
    );

  const toggleConstraint = (c: string) =>
    setHardConstraints(prev =>
      prev.includes(c) ? prev.filter(x => x !== c) : [...prev, c]
    );

  const canProceed = () => {
    if (step === 0) return selfProfile.name.trim() && selfProfile.location.city.trim();
    if (step === 1) return partnerProfile.name.trim() && partnerProfile.location.city.trim();
    if (step === 2) return userLocation && timeSlots.length > 0 && budgetMax > budgetMin;
    return false;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!userLocation) return;
    onSubmit({
      selfProfile: { ...selfProfile, location: selfProfile.location },
      partnerProfile: { ...partnerProfile, location: partnerProfile.location },
      budgetMin,
      budgetMax,
      occasion,
      maxTravelDistanceKm: maxTravel,
      preferredTimeSlots: timeSlots,
      hardConstraints,
      userLocation,
    });
  };

  const ProfileStep = ({
    profile,
    update,
    title,
  }: {
    profile: ReturnType<typeof defaultProfile>;
    update: (field: string, value: unknown) => void;
    title: string;
  }) => (
    <div className="form-step">
      <h2>{title}</h2>

      <div className="form-row">
        <div className="form-group">
          <label>Name</label>
          <input
            type="text"
            placeholder="e.g. Priya"
            value={profile.name}
            onChange={e => update('name', e.target.value)}
          />
        </div>
        <div className="form-group">
          <label>Age</label>
          <input
            type="number"
            min={18}
            max={80}
            value={profile.age}
            onChange={e => update('age', parseInt(e.target.value))}
          />
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label>Gender</label>
          <select value={profile.gender} onChange={e => update('gender', e.target.value)}>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other / Prefer not to say</option>
          </select>
        </div>
        <div className="form-group">
          <label>City</label>
          <input
            type="text"
            placeholder="e.g. Bengaluru"
            value={profile.location.city}
            onChange={e => update('location', { ...profile.location, city: e.target.value })}
          />
        </div>
      </div>

      <ChipSelector
        label="Personality"
        chips={PERSONALITY_CHIPS}
        selected={profile.personalityTags}
        onChange={v => update('personalityTags', v)}
        max={5}
      />
      <ChipSelector
        label="Interests"
        chips={INTEREST_CHIPS}
        selected={profile.interests}
        onChange={v => update('interests', v)}
        max={6}
      />
      <ChipSelector
        label="Dislikes"
        chips={DISLIKE_CHIPS}
        selected={profile.dislikes}
        onChange={v => update('dislikes', v)}
        max={4}
      />
    </div>
  );

  return (
    <form className="date-form" onSubmit={handleSubmit}>
      <div className="step-indicator">
        {STEPS.map((label, i) => (
          <div
            key={label}
            className={`step-pill ${i === step ? 'active' : i < step ? 'done' : ''}`}
          >
            <span className="step-pill-num">{i < step ? 'v' : i + 1}</span>
            <span className="step-pill-label">{label}</span>
          </div>
        ))}
      </div>

      {step === 0 && (
        <ProfileStep profile={selfProfile} update={updateSelf} title="About You" />
      )}

      {step === 1 && (
        <ProfileStep profile={partnerProfile} update={updatePartner} title="About Your Partner" />
      )}

      {step === 2 && (
        <div className="form-step">
          <h2>Date Details</h2>

          <div className="form-group">
            <label>Occasion</label>
            <div className="occasion-grid">
              {OCCASIONS.map(o => (
                <button
                  key={o.value}
                  type="button"
                  className={`occasion-btn ${occasion === o.value ? 'active' : ''}`}
                  onClick={() => setOccasion(o.value as DateRequest['occasion'])}
                >
                  {o.label}
                </button>
              ))}
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Budget Min (Rs.)</label>
              <input
                type="number"
                min={500}
                step={500}
                value={budgetMin}
                onChange={e => setBudgetMin(parseInt(e.target.value))}
              />
            </div>
            <div className="form-group">
              <label>Budget Max (Rs.)</label>
              <input
                type="number"
                min={budgetMin + 500}
                step={500}
                value={budgetMax}
                onChange={e => setBudgetMax(parseInt(e.target.value))}
              />
            </div>
          </div>

          <div className="form-group">
            <label>Max Travel Distance: {maxTravel} km</label>
            <input
              type="range"
              min={2}
              max={30}
              value={maxTravel}
              onChange={e => setMaxTravel(parseInt(e.target.value))}
              className="range-input"
            />
          </div>

          <div className="form-group">
            <label>Preferred Time</label>
            <div className="checkbox-group">
              {TIME_SLOTS.map(slot => (
                <label key={slot} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={timeSlots.includes(slot)}
                    onChange={() => toggleSlot(slot)}
                  />
                  {slot.charAt(0).toUpperCase() + slot.slice(1)}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group">
            <label>Hard Constraints</label>
            <div className="checkbox-group">
              {CONSTRAINTS.map(c => (
                <label key={c} className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={hardConstraints.includes(c)}
                    onChange={() => toggleConstraint(c)}
                  />
                  {c.charAt(0).toUpperCase() + c.slice(1).replace('-', ' ')}
                </label>
              ))}
            </div>
          </div>

          <div className="form-group location-group">
            <label>Your Current Location</label>
            {locationStatus === 'idle' && (
              <button type="button" className="btn-location" onClick={requestLocation}>
                Use My Location
              </button>
            )}
            {locationStatus === 'loading' && (
              <div className="location-success">Getting location...</div>
            )}
            {locationStatus === 'success' && userLocation && (
              <div className="location-success">
                Location acquired - {userLocation.lat.toFixed(4)}, {userLocation.lng.toFixed(4)}
              </div>
            )}
            {locationStatus === 'error' && (
              <div className="location-error">
                Could not get location. Please enable location access and try again.
                <button type="button" className="btn-location" style={{ marginTop: '0.5rem' }} onClick={requestLocation}>
                  Retry
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      <div className="form-actions">
        {step > 0 && (
          <button type="button" className="btn-secondary" onClick={() => setStep(s => s - 1)}>
            Back
          </button>
        )}
        {step < 2 ? (
          <button
            type="button"
            className="btn-primary"
            onClick={() => setStep(s => s + 1)}
            disabled={!canProceed()}
          >
            Next
          </button>
        ) : (
          <button
            type="submit"
            className="btn-primary"
            disabled={!canProceed()}
          >
            Plan My Date
          </button>
        )}
      </div>
    </form>
  );
}
