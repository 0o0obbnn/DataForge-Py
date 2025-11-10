import { test, expect } from '@playwright/test';

test.describe('DataForge Web Console - Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display login page by default', async ({ page }) => {
    // Check if we're on the login page
    await expect(page).toHaveURL(/.*login/);
    
    // Check for login form elements
    await expect(page.locator('input[type="email"]')).toBeVisible();
    await expect(page.locator('input[type="password"]')).toBeVisible();
    await expect(page.locator('button[type="submit"]')).toBeVisible();
  });

  test('should navigate to register page', async ({ page }) => {
    // Click on register link
    await page.click('text=注册');
    
    // Should navigate to register page
    await expect(page).toHaveURL(/.*register/);
    
    // Check for register form elements
    await expect(page.locator('input[placeholder*="用户名"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="邮箱"]')).toBeVisible();
    await expect(page.locator('input[placeholder*="密码"]')).toBeVisible();
  });

  test('should show validation errors for empty login form', async ({ page }) => {
    // Try to submit empty form
    await page.click('button[type="submit"]');
    
    // Should show validation errors
    await expect(page.locator('.ant-form-item-explain-error')).toBeVisible();
  });

  test('should show validation errors for invalid email', async ({ page }) => {
    // Fill in invalid email
    await page.fill('input[type="email"]', 'invalid-email');
    await page.fill('input[type="password"]', 'password123');
    
    // Submit form
    await page.click('button[type="submit"]');
    
    // Should show email validation error
    await expect(page.locator('.ant-form-item-explain-error')).toContainText('请输入有效的邮箱地址');
  });

  test('should navigate to reset password page', async ({ page }) => {
    // Click on forgot password link
    await page.click('text=忘记密码');
    
    // Should navigate to reset password page
    await expect(page).toHaveURL(/.*reset-password/);
    
    // Check for reset password form
    await expect(page.locator('input[placeholder*="邮箱"]')).toBeVisible();
  });
});
