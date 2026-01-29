import { test, expect } from '@playwright/test';

test.describe('DataForge Web Console - API Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/api-management');
    await page.waitForLoadState('networkidle');
  });

  test('should display API management page', async ({ page }) => {
    // Check if we're on the API management page
    await expect(page).toHaveURL(/.*api-management/);

    // Check for page title
    await expect(page.locator('h1')).toContainText('API 管理');

    // Check for API key section
    await expect(page.locator('text=API 密钥')).toBeVisible();

    // Check for usage statistics
    await expect(page.locator('text=使用统计')).toBeVisible();
  });

  test('should allow generating new API key', async ({ page }) => {
    // Click generate API key button
    await page.click('button:has-text("生成新密钥")');

    // Wait for modal to appear
    await page.waitForSelector('.ant-modal');

    // Fill in key name
    await page.fill('input[placeholder*="密钥名称"]', 'Test API Key');

    // Confirm generation
    await page.click('button:has-text("确认生成")');

    // Check if new key is displayed
    await expect(page.locator('.ant-table-tbody tr')).toContainText('Test API Key');
  });

  test('should allow revoking API key', async ({ page }) => {
    // Find a revoke button for existing key
    const revokeButton = page.locator('button:has-text("撤销")').first();

    if (await revokeButton.isVisible()) {
      await revokeButton.click();

      // Confirm revocation
      await page.click('button:has-text("确认撤销")');

      // Check if key is removed or marked as revoked
      await expect(page.locator('.ant-table-tbody tr')).not.toContainText('Test API Key');
    }
  });

  test('should display API usage statistics', async ({ page }) => {
    // Check for usage statistics cards
    await expect(page.locator('.ant-statistic-title:has-text("总请求数")')).toBeVisible();
    await expect(page.locator('.ant-statistic-title:has-text("今日请求")')).toBeVisible();
    await expect(page.locator('.ant-statistic-title:has-text("剩余配额")')).toBeVisible();
  });

  test('should show API documentation', async ({ page }) => {
    // Click on API documentation tab
    await page.click('text=API 文档');

    // Check for endpoint documentation
    await expect(page.locator('text=POST /api/generate')).toBeVisible();
    await expect(page.locator('text=GET /api/health')).toBeVisible();
  });

  test('should allow testing API endpoints', async ({ page }) => {
    // Navigate to API testing section
    await page.click('text=API 测试');

    // Select an endpoint
    await page.click('.ant-select-selector');
    await page.click('.ant-select-item:has-text("POST /api/generate")');

    // Fill in request body
    await page.fill('textarea[placeholder*="请求体"]', JSON.stringify({
      data_type: 'name',
      quantity: 5
    }));

    // Send request
    await page.click('button:has-text("发送请求")');

    // Check for response
    await expect(page.locator('.ant-typography-code')).toBeVisible();
  });
});
