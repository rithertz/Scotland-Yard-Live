import { describe, expect, it } from 'vitest';
import { healthResponseSchema } from './index.js';

describe('healthResponseSchema', () => {
  it('accepts a valid API liveness response', () => {
    expect(
      healthResponseSchema.safeParse({
        status: 'ok',
        service: 'scotland-yard-live-api',
        timestamp: '2026-11-04T12:00:00.000Z',
      }).success,
    ).toBe(true);
  });

  it('rejects an invalid status', () => {
    expect(
      healthResponseSchema.safeParse({
        status: 'healthy',
        service: 'scotland-yard-live-api',
        timestamp: '2026-11-04T12:00:00.000Z',
      }).success,
    ).toBe(false);
  });
});
