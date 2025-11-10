import { test, expect } from '@playwright/test';

test.describe('DataForge Web Console - Templates Management', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/templates');
    await page.waitForLoadState('networkidle');
  });

  test('should display templates page', async ({ page }) => {
    // Check if we're on the templates page
    await expect(page).toHaveURL(/.*templates/);
    
    // Check for page title
    await expect(page.locator('h1')).toContainText('模板管理');
    
    // Check for template list
    await expect(page.locator('.ant-table')).toBeVisible();
  });

  test('should allow creating new template', async ({ page }) => {
    // Click create template button
    await page.click('button:has-text("创建模板")');
    
    // Wait for modal to appear
    await page.waitForSelector('.ant-modal');
    
    // Fill in template details
    await page.fill('input[placeholder*="模板名称"]', 'Test Template');
    await page.fill('textarea[placeholder*="描述"]', 'Test template description');
    
    // Select data types
    await page.click('.ant-select-selector');
    await page.click('.ant-select-item:has-text("姓名")');
    await page.click('.ant-select-item:has-text("手机号")');
    
    // Save template
    await page.click('button:has-text("保存")');
    
    // Check if template is created
    await expect(page.locator('.ant-table-tbody tr')).toContainText('Test Template');
  });

  test('should allow editing existing template', async ({ page }) => {
    // Find edit button for first template
    const editButton = page.locator('button:has-text("编辑")').first();
    
    if (await editButton.isVisible()) {
      await editButton.click();
      
      // Wait for modal to appear
      await page.waitForSelector('.ant-modal');
      
      // Modify template name
      await page.fill('input[placeholder*="模板名称"]', 'Updated Template');
      
      // Save changes
      await page.click('button:has-text("保存")');
      
      // Check if template is updated
      await expect(page.locator('.ant-table-tbody tr')).toContainText('Updated Template');
    }
  });

  test('should allow deleting template', async ({ page }) => {
    // Find delete button for first template
    const deleteButton = page.locator('button:has-text("删除")').first();
    
    if (await deleteButton.isVisible()) {
      await deleteButton.click();
      
      // Confirm deletion
      await page.click('button:has-text("确认删除")');
      
      // Check if template is removed
      await expect(page.locator('.ant-table-tbody tr')).toHaveCount(0);
    }
  });

  test('should allow using template for data generation', async ({ page }) => {
    // Find use template button
    const useButton = page.locator('button:has-text("使用")').first();
    
    if (await useButton.isVisible()) {
      await useButton.click();
      
      // Should navigate to workbench with template applied
      await expect(page).toHaveURL(/.*workbench/);
      
      // Check if template data types are pre-selected
      await expect(page.locator('.ant-select-selection-item')).toBeVisible();
    }
  });

  test('should allow searching templates', async ({ page }) => {
    // Use search input
    await page.fill('input[placeholder*="搜索模板"]', 'Test');
    
    // Check if results are filtered
    await expect(page.locator('.ant-table-tbody tr')).toContainText('Test');
  });

  test('should display template statistics', async ({ page }) => {
    // Check for template statistics
    await expect(page.locator('.ant-statistic-title:has-text("总模板数")')).toBeVisible();
    await expect(page.locator('.ant-statistic-title:has-text("使用次数")')).toBeVisible();
  });
});
