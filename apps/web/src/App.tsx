import { useEffect, useState } from 'react';
import { healthResponseSchema, type HealthResponse } from '@scotland-yard-live/contracts';

const apiBaseUrl = import.meta.env['VITE_API_BASE_URL'] ?? 'http://127.0.0.1:4000';

type ApiStatus = 'checking' | 'online' | 'offline';

export function App() {
  const [apiStatus, setApiStatus] = useState<ApiStatus>('checking');
  const [health, setHealth] = useState<HealthResponse | null>(null);

  useEffect(() => {
    const controller = new AbortController();

    async function checkApi() {
      try {
        const response = await fetch(`${apiBaseUrl}/health/live`, { signal: controller.signal });
        if (!response.ok) throw new Error(`Health endpoint returned ${response.status}`);
        const payload: unknown = await response.json();
        const parsed = healthResponseSchema.parse(payload);
        setHealth(parsed);
        setApiStatus('online');
      } catch {
        if (!controller.signal.aborted) setApiStatus('offline');
      }
    }

    void checkApi();
    return () => controller.abort();
  }, []);

  return (
    <main className="shell">
      <header className="topbar">
        <div className="wordmark">
          <span className="wordmark-mark">SY</span> SCOTLAND YARD{' '}
          <span className="wordmark-live">LIVE</span>
        </div>
        <span className="environment-label">PRIVATE PLAYTEST FOUNDATION</span>
      </header>
      <section className="hero">
        <p className="eyebrow">LONDON · 1960s · THE PURSUIT BEGINS</p>
        <h1>
          The city is your
          <br />
          <em>playing field.</em>
        </h1>
        <p className="intro">
          A private digital table for the classic game of pursuit. Bring your team together. One of
          you is Mr X.
        </p>
        <div className="status-panel" role="status" aria-live="polite">
          <span className={`status-dot status-${apiStatus}`} />
          <div>
            <strong>Development server</strong>
            <p>
              {apiStatus === 'checking'
                ? 'Checking API connection…'
                : apiStatus === 'online'
                  ? `API online · ${health?.service ?? 'server'}`
                  : 'API unavailable · start the backend to connect'}
            </p>
          </div>
        </div>
        <p className="foundation-note">ROOMS AND GAMEPLAY ARE NOT IMPLEMENTED YET</p>
      </section>
      <footer>
        <span>SCOTLAND YARD LIVE</span>
        <span>PHASE 1 · WALKING SKELETON</span>
      </footer>
    </main>
  );
}
