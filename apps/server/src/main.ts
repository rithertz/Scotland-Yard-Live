import { createDatabase } from '@scotland-yard-live/database';
import { buildApp } from './app.js';
import { loadEnvironment } from './env.js';

const environment = loadEnvironment();
const database = createDatabase(environment.DATABASE_URL);
const app = await buildApp({ environment, database });

try {
  await app.listen({ host: environment.HOST, port: environment.PORT });
} catch (error) {
  app.log.error(error, 'Failed to start server');
  await app.close();
  await database.close();
  process.exitCode = 1;
}

let shuttingDown = false;

async function shutdown(signal: NodeJS.Signals): Promise<void> {
  if (shuttingDown) return;
  shuttingDown = true;
  app.log.info({ signal }, 'Shutting down');
  await app.close();
  await database.close();
}

for (const signal of ['SIGINT', 'SIGTERM'] as const) {
  process.on(signal, () => {
    void shutdown(signal).catch((error: unknown) => {
      app.log.error({ err: error }, 'Graceful shutdown failed');
      process.exitCode = 1;
    });
  });
}
