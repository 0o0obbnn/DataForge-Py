import { test, expect } from '@playwright/test';

test.describe('DataForge Web Console - Workbench', () => {
  test.beforeEach(async ({ page }) => {
    // Mock authentication - assuming we have a way to bypass login for testing
    await page.goto('/workbench');
    
    // Wait for page to load
    await page.waitForLoadState('networkidle');
  });

  test('should display workbench page with data generation form', async ({ page }) => {
    // Check if we're on the workbench page
    await expect(page).toHaveURL(/.*workbench/);
    
    // Check for main workbench elements
    await expect(page.locator('h1')).toContainText('数据生成工作台');
    
    // Check for data type selection
    await expect(page.locator('.ant-select')).toBeVisible();
    
    // Check for generation form
    await expect(page.locator('form')).toBeVisible();
  });

  test('should allow selecting different data types', async ({ page }) => {
    // Click on data type selector
    await page.click('.ant-select-selector');
    
    // Wait for dropdown to appear
    await page.waitForSelector('.ant-select-dropdown');
    
    // Check for common data types
    await expect(page.locator('.ant-select-item')).toContainText('姓名');
    await expect(page.locator('.ant-select-item')).toContainText('身份证号');
    await expect(page.locator('.ant-select-item')).toContainText('手机号');
  });

  test('should generate data when form is submitted', async ({ page }) => {
    // Select a data type
    await page.click('.ant-select-selector');
    await page.click('.ant-select-item:has-text("姓名")');
    
    // Set quantity
    await page.fill('input[placeholder*="数量"]', '5');
    
    // Submit form
    await page.click('button:has-text("生成数据")');
    
    // Wait for results
    await page.waitForSelector('.ant-table-tbody', { timeout: 10000 });
    
    // Check if data is generated
    await expect(page.locator('.ant-table-tbody tr')).toHaveCount(5);
  });

  test('should allow exporting generated data', async ({ page }) => {
    // Generate some data first
    await page.click('.ant-select-selector');
    await page.click('.ant-select-item:has-text("姓名")');
    await page.fill('input[placeholder*="数量"]', '3');
    await page.click('button:has-text("生成数据")');
    
    // Wait for data to be generated
    await page.waitForSelector('.ant-table-tbody');
    
    // Click export button
    await page.click('button:has-text("导出")');
    
    // Check for export options
    await expect(page.locator('.ant-dropdown-menu')).toBeVisible();
    await expect(page.locator('.ant-dropdown-menu-item:has-text("CSV")')).toBeVisible();
    await expect(page.locator('.ant-dropdown-menu-item:has-text("JSON")')).toBeVisible();
  });

  test('should show validation errors for invalid input', async ({ page }) => {
    // Try to submit without selecting data type
    await page.fill('input[placeholder*="数量"]', '5');
    await page.click('button:has-text("生成数据")');
    
    // Should show validation error
    await expect(page.locator('.ant-form-item-explain-error')).toBeVisible();
  });

  test('should handle large quantity generation', async ({ page }) => {
    // Select data type
    await page.click('.ant-select-selector');
    await page.click('.ant-select-item:has-text("姓名")');
    
    // Set large quantity
    await page.fill('input[placeholder*="数量"]', '1000');
    
    // Submit form
    await page.click('button:has-text("生成数据")');
    
    // Wait for loading to complete
    await page.waitForSelector('.ant-spin', { state: 'hidden', timeout: 30000 });
    
    // Check if data is generated
    await expect(page.locator('.ant-table-tbody tr')).toHaveCount(1000);
  });
});
