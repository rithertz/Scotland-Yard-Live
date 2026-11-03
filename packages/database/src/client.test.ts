import { describe, expect, it } from 'vitest';
import { createDatabase } from './client.js';

describe('createDatabase', () => {
  it('creates a database client with health and lifecycle methods', () => {
    const database = createDatabase('postgresql://localhost:5432/test');

    expect(database.db).toBeDefined();
    expect(database.ping).toBeTypeOf('function');
    expect(database.close).toBeTypeOf('function');
  });
});
