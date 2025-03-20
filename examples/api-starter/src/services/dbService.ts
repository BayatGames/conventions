import { Pool, PoolClient } from 'pg';
import { config } from '../config';
import logger from '../utils/logger';

// Database connection pool
const pool = new Pool({
  host: config.db.host,
  port: config.db.port,
  user: config.db.user,
  password: config.db.password,
  database: config.db.database,
  ssl: config.db.ssl ? { rejectUnauthorized: false } : false,
  max: 20, // Maximum number of clients
  idleTimeoutMillis: 30000, // Client idle timeout
  connectionTimeoutMillis: 2000, // Connection timeout
});

// Handle pool errors
pool.on('error', (err: Error) => {
  logger.error('Unexpected error on idle database client', { error: err.message });
  process.exit(-1);
});

/**
 * Database service
 * Provides methods for database operations with connection management
 */
export class DbService {
  /**
   * Execute a query
   * @param text SQL query text
   * @param params Query parameters
   * @returns Query result
   */
  static async query(text: string, params: any[] = []) {
    const start = Date.now();
    try {
      const res = await pool.query(text, params);
      const duration = Date.now() - start;
      logger.debug('Executed query', {
        query: text,
        duration,
        rows: res.rowCount,
      });
      return res;
    } catch (error: any) {
      logger.error('Error executing query', {
        query: text,
        params,
        error: error.message,
      });
      throw error;
    }
  }

  /**
   * Execute a transaction
   * @param callback Function to execute within transaction
   * @returns Result of callback
   */
  static async transaction<T>(callback: (client: PoolClient) => Promise<T>): Promise<T> {
    const client = await pool.connect();
    try {
      await client.query('BEGIN');
      const result = await callback(client);
      await client.query('COMMIT');
      return result;
    } catch (error) {
      await client.query('ROLLBACK');
      throw error;
    } finally {
      client.release();
    }
  }

  /**
   * Close the database pool
   */
  static async close() {
    logger.info('Closing database pool');
    await pool.end();
  }
} 