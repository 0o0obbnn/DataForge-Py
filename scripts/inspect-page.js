const { chromium } = require('playwright');

async function inspectPage() {
  console.log('🔍 检查前端页面内容...');
  
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();
  
  try {
    // 访问前端页面
    await page.goto('http://localhost:5173', { waitUntil: 'networkidle' });
    
    // 获取页面基本信息
    const title = await page.title();
    console.log(`📄 页面标题: ${title}`);
    
    // 获取页面 HTML 内容
    const html = await page.content();
    console.log(`📝 页面 HTML 长度: ${html.length} 字符`);
    
    // 检查所有可见的文本内容
    const bodyText = await page.locator('body').textContent();
    console.log(`📄 页面文本内容:\n${bodyText}`);
    
    // 检查所有可见的按钮
    const buttons = await page.locator('button').all();
    console.log(`🔘 找到 ${buttons.length} 个按钮:`);
    for (let i = 0; i < buttons.length; i++) {
      const text = await buttons[i].textContent();
      console.log(`  ${i + 1}. "${text}"`);
    }
    
    // 检查所有输入框
    const inputs = await page.locator('input').all();
    console.log(`📝 找到 ${inputs.length} 个输入框:`);
    for (let i = 0; i < inputs.length; i++) {
      const type = await inputs[i].getAttribute('type');
      const placeholder = await inputs[i].getAttribute('placeholder');
      console.log(`  ${i + 1}. type="${type}", placeholder="${placeholder}"`);
    }
    
    // 检查所有链接
    const links = await page.locator('a').all();
    console.log(`🔗 找到 ${links.length} 个链接:`);
    for (let i = 0; i < links.length; i++) {
      const text = await links[i].textContent();
      const href = await links[i].getAttribute('href');
      console.log(`  ${i + 1}. "${text}" -> ${href}`);
    }
    
    // 检查所有标题
    const headings = await page.locator('h1, h2, h3, h4, h5, h6').all();
    console.log(`📋 找到 ${headings.length} 个标题:`);
    for (let i = 0; i < headings.length; i++) {
      const tagName = await headings[i].evaluate(el => el.tagName);
      const text = await headings[i].textContent();
      console.log(`  ${i + 1}. ${tagName}: "${text}"`);
    }
    
    // 截图
    await page.screenshot({ path: 'page-inspection.png', fullPage: true });
    console.log('📸 页面截图已保存: page-inspection.png');
    
  } catch (error) {
    console.error('❌ 检查失败:', error.message);
  } finally {
    await browser.close();
  }
}

inspectPage();
