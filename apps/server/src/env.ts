import { config as loadDotEnv } from 'dotenv';
import { z } from 'zod';

loadDotEnv({ path: '../../.env' });

const environmentSchema = z.object({
  NODE_ENV: z.enum(['development', 'test', 'production']).default('development'),
  HOST: z.string().min(1).default('127.0.0.1'),
  PORT: z.coerce.number().int().min(1).max(65_535).default(4000),
  LOG_LEVEL: z.enum(['fatal', 'error', 'warn', 'info', 'debug', 'trace', 'silent']).default('info'),
  WEB_ORIGIN: z.string().default('http://127.0.0.1:5173'),
  DATABASE_URL: z
    .string()
    .url()
    .default('postgresql://scotland_yard:scotland_yard_dev@localhost:5432/scotland_yard'),
});

export type ServerEnvironment = z.infer<typeof environmentSchema>;

export function loadEnvironment(source: NodeJS.ProcessEnv = process.env): ServerEnvironment {
  return environmentSchema.parse(source);
}
