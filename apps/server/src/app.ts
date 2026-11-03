import cors from '@fastify/cors';
import Fastify, { type FastifyInstance } from 'fastify';
import { healthResponseSchema } from '@scotland-yard-live/contracts';
import type { DatabaseClient } from '@scotland-yard-live/database';
import type { ServerEnvironment } from './env.js';

interface BuildAppOptions {
  environment: ServerEnvironment;
  database: Pick<DatabaseClient, 'ping'>;
}

export async function buildApp({
  environment,
  database,
}: BuildAppOptions): Promise<FastifyInstance> {
  const app = Fastify({
    logger: {
      level: environment.LOG_LEVEL,
      redact: ['req.headers.authorization', 'req.headers.cookie'],
    },
  });

  await app.register(cors, {
    origin: environment.WEB_ORIGIN.split(',').map((origin) => origin.trim()),
    credentials: true,
  });

  app.get('/health/live', async (_request, reply) => {
    const payload = healthResponseSchema.parse({
      status: 'ok',
      service: 'scotland-yard-live-api',
      timestamp: new Date().toISOString(),
    });
    return reply.code(200).send(payload);
  });

  app.get('/health/ready', async (_request, reply) => {
    try {
      await database.ping();
      return reply.code(200).send({
        status: 'ok',
        service: 'scotland-yard-live-api',
        dependencies: { database: 'available' },
      });
    } catch (error) {
      app.log.error({ err: error }, 'Readiness check failed');
      return reply.code(503).send({
        status: 'unavailable',
        service: 'scotland-yard-live-api',
        dependencies: { database: 'unavailable' },
      });
    }
  });

  return app;
}
