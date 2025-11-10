import { test, expect } from '@playwright/test';

test.describe('DataForge Web Console - 实际功能测试', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('应该显示登录页面', async ({ page }) => {
    // 检查页面标题
    await expect(page).toHaveTitle(/登录.*DataForge/);
    
    // 检查页面内容
    const bodyText = await page.locator('body').textContent();
    expect(bodyText).toContain('请先登录');
  });

  test('应该能够访问后端 API', async ({ page }) => {
    // 测试后端健康检查
    const response = await page.request.get('http://localhost:8000/health');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('status', 'healthy');
  });

  test('应该能够获取生成器列表', async ({ page }) => {
    // 测试获取生成器列表
    const response = await page.request.get('http://localhost:8000/generators');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(Array.isArray(data)).toBe(true);
    expect(data.length).toBeGreaterThan(0);
  });

  test('应该能够生成测试数据', async ({ page }) => {
    // 测试数据生成 API
    const response = await page.request.post('http://localhost:8000/generate', {
      data: {
        data_type: 'name',
        quantity: 5
      }
    });
    
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('data');
    expect(Array.isArray(data.data)).toBe(true);
    expect(data.data.length).toBe(5);
  });

  test('应该能够访问 API 文档', async ({ page }) => {
    // 访问 Swagger 文档
    await page.goto('http://localhost:8000/docs');
    
    // 检查页面标题
    await expect(page).toHaveTitle(/Swagger UI/);
    
    // 检查是否有 API 端点
    await expect(page.locator('text=POST /generate')).toBeVisible();
    await expect(page.locator('text=GET /health')).toBeVisible();
  });

  test('应该能够访问 OpenAPI 规范', async ({ page }) => {
    // 访问 OpenAPI 规范
    const response = await page.request.get('http://localhost:8000/openapi.json');
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('openapi');
    expect(data).toHaveProperty('info');
    expect(data.info.title).toContain('DataForge');
  });

  test('应该能够处理不同的数据类型', async ({ page }) => {
    const dataTypes = ['name', 'phone', 'id_card', 'email'];
    
    for (const dataType of dataTypes) {
      const response = await page.request.post('http://localhost:8000/generate', {
        data: {
          data_type: dataType,
          quantity: 3
        }
      });
      
      expect(response.status()).toBe(200);
      
      const data = await response.json();
      expect(data).toHaveProperty('data');
      expect(Array.isArray(data.data)).toBe(true);
      expect(data.data.length).toBe(3);
    }
  });

  test('应该能够处理批量生成', async ({ page }) => {
    const response = await page.request.post('http://localhost:8000/generate', {
      data: {
        data_type: 'name',
        quantity: 100
      }
    });
    
    expect(response.status()).toBe(200);
    
    const data = await response.json();
    expect(data).toHaveProperty('data');
    expect(Array.isArray(data.data)).toBe(true);
    expect(data.data.length).toBe(100);
  });

  test('应该能够处理无效请求', async ({ page }) => {
    // 测试无效的数据类型
    const response = await page.request.post('http://localhost:8000/generate', {
      data: {
        data_type: 'invalid_type',
        quantity: 5
      }
    });
    
    expect(response.status()).toBe(422); // 应该是验证错误
  });

  test('应该能够处理缺少参数的请求', async ({ page }) => {
    // 测试缺少必需参数
    const response = await page.request.post('http://localhost:8000/generate', {
      data: {
        data_type: 'name'
        // 缺少 quantity 参数
      }
    });
    
    expect(response.status()).toBe(422); // 应该是验证错误
  });

  test('应该能够处理过大的数量请求', async ({ page }) => {
    // 测试过大的数量
    const response = await page.request.post('http://localhost:8000/generate', {
      data: {
        data_type: 'name',
        quantity: 10000
      }
    });
    
    // 这个测试可能会成功，也可能会有限制，取决于后端实现
    expect([200, 422, 400]).toContain(response.status());
  });
});
