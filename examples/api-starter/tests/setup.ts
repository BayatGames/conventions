import dotenv from 'dotenv';
import path from 'path';

// Load environment variables from .env.test file if it exists, otherwise from .env
const envFile = path.resolve(process.cwd(), '.env.test');
dotenv.config({ path: envFile });

// Set test timeout
jest.setTimeout(30000);

// Global beforeAll hook
beforeAll(async () => {
  console.log('Setting up tests...');
  // Add any global setup logic here (e.g., database setup)
});

// Global afterAll hook
afterAll(async () => {
  console.log('Cleaning up tests...');
  // Add any global cleanup logic here (e.g., database cleanup)
}); 