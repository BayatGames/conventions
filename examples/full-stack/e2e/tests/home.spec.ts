import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should display the home page correctly', async ({ page }) => {
    // Navigate to the home page
    await page.goto('http://localhost:3000');

    // Verify page title
    await expect(page).toHaveTitle(/Bayat Full-Stack Application/);

    // Verify navigation elements
    const navigation = page.locator('nav');
    await expect(navigation).toBeVisible();

    // Verify heading content
    const heading = page.locator('h1');
    await expect(heading).toContainText('Welcome');

    // Verify some content is loaded
    const content = page.locator('main');
    await expect(content).toBeVisible();
  });
}); 