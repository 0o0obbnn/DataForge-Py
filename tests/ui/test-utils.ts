import { Page, expect } from '@playwright/test';

/**
 * 测试工具函数
 */
export class TestUtils {
  constructor(private page: Page) {}

  /**
   * 等待页面加载完成
   */
  async waitForPageLoad() {
    await this.page.waitForLoadState('networkidle');
    await this.page.waitForSelector('body', { state: 'visible' });
  }

  /**
   * 模拟用户登录
   */
  async login(email: string = 'test@example.com', password: string = 'password123') {
    await this.page.goto('/login');
    await this.waitForPageLoad();

    await this.page.fill('input[type="email"]', email);
    await this.page.fill('input[type="password"]', password);
    await this.page.click('button[type="submit"]');

    // 等待登录完成，通常会有重定向
    await this.page.waitForURL(/.*(workbench|dashboard)/);
  }

  /**
   * 等待并点击元素
   */
  async clickAndWait(selector: string, timeout: number = 5000) {
    await this.page.waitForSelector(selector, { timeout });
    await this.page.click(selector);
  }

  /**
   * 等待并填充输入框
   */
  async fillAndWait(selector: string, value: string, timeout: number = 5000) {
    await this.page.waitForSelector(selector, { timeout });
    await this.page.fill(selector, value);
  }

  /**
   * 等待元素可见
   */
  async waitForVisible(selector: string, timeout: number = 5000) {
    await this.page.waitForSelector(selector, { state: 'visible', timeout });
  }

  /**
   * 等待元素隐藏
   */
  async waitForHidden(selector: string, timeout: number = 5000) {
    await this.page.waitForSelector(selector, { state: 'hidden', timeout });
  }

  /**
   * 检查元素是否存在
   */
  async isElementVisible(selector: string): Promise<boolean> {
    try {
      await this.page.waitForSelector(selector, { timeout: 1000 });
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 等待 API 请求完成
   */
  async waitForApiResponse(urlPattern: string | RegExp, timeout: number = 10000) {
    await this.page.waitForResponse(response => {
      const url = response.url();
      if (typeof urlPattern === 'string') {
        return url.includes(urlPattern);
      }
      return urlPattern.test(url);
    }, { timeout });
  }

  /**
   * 截取屏幕截图
   */
  async takeScreenshot(name: string) {
    await this.page.screenshot({ path: `screenshots/${name}.png`, fullPage: true });
  }

  /**
   * 检查控制台错误
   */
  async checkConsoleErrors() {
    const errors: string[] = [];

    this.page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });

    return errors;
  }

  /**
   * 模拟网络延迟
   */
  async simulateNetworkDelay(delay: number = 1000) {
    await this.page.route('**/*', route => {
      setTimeout(() => route.continue(), delay);
    });
  }

  /**
   * 模拟网络错误
   */
  async simulateNetworkError(urlPattern: string | RegExp) {
    await this.page.route(urlPattern, route => {
      route.abort('failed');
    });
  }

  /**
   * 等待加载指示器消失
   */
  async waitForLoadingToComplete() {
    await this.page.waitForSelector('.ant-spin', { state: 'hidden', timeout: 30000 });
  }

  /**
   * 检查表格数据
   */
  async checkTableData(tableSelector: string, expectedRowCount: number) {
    await this.page.waitForSelector(tableSelector);
    const rows = await this.page.locator(`${tableSelector} tbody tr`).count();
    expect(rows).toBe(expectedRowCount);
  }

  /**
   * 检查表单验证错误
   */
  async checkFormValidationError(errorText: string) {
    await this.page.waitForSelector('.ant-form-item-explain-error');
    await expect(this.page.locator('.ant-form-item-explain-error')).toContainText(errorText);
  }

  /**
   * 等待通知消息
   */
  async waitForNotification(message?: string) {
    await this.page.waitForSelector('.ant-notification');
    if (message) {
      await expect(this.page.locator('.ant-notification')).toContainText(message);
    }
  }
}
