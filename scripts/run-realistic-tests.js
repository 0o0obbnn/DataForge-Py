const { exec } = require('child_process');
const path = require('path');

console.log('🚀 运行 DataForge 实用测试...\n');

// 运行实用测试
const command = 'npx playwright test tests/ui/realistic.spec.ts --headed --reporter=line';

exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error('❌ 测试执行错误:', error);
    return;
  }
  
  if (stderr) {
    console.error('⚠️ 警告:', stderr);
  }
  
  console.log('📊 测试结果:');
  console.log(stdout);
  
  console.log('\n✅ 测试完成！');
  console.log('📸 截图和视频已保存到 test-results/ 目录');
  console.log('📊 详细报告请访问: http://localhost:9323');
});
