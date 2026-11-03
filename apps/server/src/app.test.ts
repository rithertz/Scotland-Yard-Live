import { afterEach, describe, expect, it, vi } from 'vitest';
import { buildApp } from './app.js';
import { loadEnvironment } from './env.js';

const environment = loadEnvironment({ NODE_ENV: 'test' });

describe('health routes', () => {
  afterEach(() => vi.restoreAllMocks());

  it('reports liveness without requiring database access', async () => {
    const database = { ping: vi.fn().mockRejectedValue(new Error('database down')) };
    const app = await buildApp({ environment, database });

    const response = await app.inject({ method: 'GET', url: '/health/live' });

    expect(response.statusCode).toBe(200);
    expect(response.json().status).toBe('ok');
    expect(database.ping).not.toHaveBeenCalled();
    await app.close();
  });

  it('reports readiness when the database responds', async () => {
    const database = { ping: vi.fn().mockResolvedValue(undefined) };
    const app = await buildApp({ environment, database });

    const response = await app.inject({ method: 'GET', url: '/health/ready' });

    expect(response.statusCode).toBe(200);
    expect(response.json().dependencies.database).toBe('available');
    await app.close();
  });

  it('reports unavailable readiness when the database fails', async () => {
    const database = { ping: vi.fn().mockRejectedValue(new Error('database down')) };
    const app = await buildApp({ environment, database });

    const response = await app.inject({ method: 'GET', url: '/health/ready' });

    expect(response.statusCode).toBe(503);
    expect(response.json().dependencies.database).toBe('unavailable');
    await app.close();
  });
});
