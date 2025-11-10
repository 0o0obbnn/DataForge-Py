const { chromium } = require('playwright');

async function testPlaywright() {
  console.log('🚀 启动 Playwright 测试...');
  
  // 启动浏览器
  const browser = await chromium.launch({ 
    headless: false, // 显示浏览器窗口
    slowMo: 1000 // 减慢操作速度以便观察
  });
  
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // 测试后端 API
    console.log('📡 测试后端 API...');
    const apiResponse = await page.request.get('http://localhost:8000/health');
    console.log(`✅ 后端 API 状态: ${apiResponse.status()}`);
    
    // 测试前端页面
    console.log('🌐 测试前端页面...');
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
    
    // 检查页面标题
    const title = await page.title();
    console.log(`📄 页面标题: ${title}`);
    
    // 截图
    await page.screenshot({ path: 'test-screenshot.png' });
    console.log('📸 截图已保存: test-screenshot.png');
    
    // 检查页面元素
    const body = await page.locator('body').textContent();
    console.log(`📝 页面内容长度: ${body.length} 字符`);
    
    console.log('✅ Playwright 测试完成！');
    
  } catch (error) {
    console.error('❌ 测试失败:', error.message);
  } finally {
    await browser.close();
  }
}

testPlaywright();
