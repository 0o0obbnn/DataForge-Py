<template>
  <div class="dataforge-test">
    <a-card title="DataForge API 连接测试" class="test-card">
      <!-- API 连接状态 -->
      <div class="connection-status">
        <h3>连接状态</h3>
        <a-space>
          <a-button 
            type="primary" 
            :loading="apiConnecting" 
            @click="testConnection"
          >
            测试连接
          </a-button>
          <a-tag :color="apiConnected ? 'green' : 'red'">
            {{ apiConnected ? '已连接' : '未连接' }}
          </a-tag>
        </a-space>
        
        <div v-if="apiHealth" class="health-info">
          <p><strong>API 状态:</strong> {{ apiHealth.status }}</p>
          <p><strong>版本:</strong> {{ apiHealth.version }}</p>
          <p><strong>可用生成器数量:</strong> {{ apiHealth.generators_count }}</p>
          <p><strong>检查时间:</strong> {{ formatTime(apiHealth.timestamp) }}</p>
        </div>
      </div>

      <!-- 生成器列表 -->
      <a-divider />
      <div class="generators-section">
        <h3>
          可用生成器 
          <a-button 
            type="text" 
            size="small" 
            :loading="loadingGenerators" 
            @click="loadGenerators"
          >
            刷新
          </a-button>
        </h3>
        
        <div v-if="availableGenerators.length > 0" class="generators-grid">
          <a-card 
            v-for="generator in availableGenerators.slice(0, 12)" 
            :key="generator.name"
            size="small"
            class="generator-card"
          >
            <template #title>
              <a-space>
                <a-tag :color="getGeneratorTypeColor(generator.type)">
                  {{ generator.type }}
                </a-tag>
                {{ generator.name }}
              </a-space>
            </template>
            
            <p class="generator-description">{{ generator.description }}</p>
            <p class="generator-params">
              <strong>支持参数:</strong> 
              {{ generator.parameters.length > 0 ? generator.parameters.join(', ') : '无' }}
            </p>
            
            <a-space>
              <a-button 
                size="small" 
                @click="testGenerator(generator.name)"
                :loading="testingGenerators.includes(generator.name)"
              >
                测试生成
              </a-button>
              <a-button 
                size="small" 
                type="text" 
                @click="showGeneratorDetails(generator.name)"
              >
                详情
              </a-button>
            </a-space>
          </a-card>
        </div>
        
        <a-empty v-else description="暂无可用生成器" />
      </div>

      <!-- 测试结果 -->
      <a-divider />
      <div class="test-results">
        <h3>测试结果</h3>
        <a-textarea 
          v-model:value="testResults" 
          :rows="10" 
          readonly 
          placeholder="测试结果将显示在这里..."
        />
        <a-space style="margin-top: 12px;">
          <a-button @click="clearResults">清除结果</a-button>
          <a-button @click="copyResults" v-if="testResults">复制结果</a-button>
        </a-space>
      </div>
    </a-card>

    <!-- 生成器详情弹窗 -->
    <a-modal
      v-model:open="detailsModalVisible"
      title="生成器详情"
      :footer="null"
      width="600px"
    >
      <div v-if="selectedGeneratorDetails">
        <a-descriptions :column="1" bordered>
          <a-descriptions-item label="名称">
            {{ selectedGeneratorDetails.name }}
          </a-descriptions-item>
          <a-descriptions-item label="类型">
            <a-tag :color="getGeneratorTypeColor(selectedGeneratorDetails.type)">
              {{ selectedGeneratorDetails.type }}
            </a-tag>
          </a-descriptions-item>
          <a-descriptions-item label="描述">
            {{ selectedGeneratorDetails.description }}
          </a-descriptions-item>
          <a-descriptions-item label="支持参数">
            <a-tag 
              v-for="param in selectedGeneratorDetails.parameters" 
              :key="param"
              style="margin-bottom: 4px;"
            >
              {{ param }}
            </a-tag>
            <span v-if="selectedGeneratorDetails.parameters.length === 0">无</span>
          </a-descriptions-item>
          <a-descriptions-item label="示例参数" v-if="selectedGeneratorDetails.example_parameters">
            <pre style="background: #f5f5f5; padding: 8px; border-radius: 4px; font-size: 12px;">{{ JSON.stringify(selectedGeneratorDetails.example_parameters, null, 2) }}</pre>
          </a-descriptions-item>
        </a-descriptions>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import { useWorkbenchStore } from '@/stores/workbench'
import type { GeneratorInfo } from '@/services/modules/dataforge'
import dayjs from 'dayjs'

const workbenchStore = useWorkbenchStore()

// 响应式数据
const testResults = ref('')
const testingGenerators = ref<string[]>([])
const detailsModalVisible = ref(false)
const selectedGeneratorDetails = ref<GeneratorInfo | null>(null)

// 从 store 获取状态
const {
  apiConnected,
  apiConnecting,
  apiHealth,
  availableGenerators,
  loadingGenerators
} = workbenchStore

// 方法
const testConnection = async () => {
  addTestResult('开始测试 DataForge API 连接...')
  
  const result = await workbenchStore.checkApiConnection()
  
  if (result.connected) {
    addTestResult('✅ API 连接成功！')
    if (result.health) {
      addTestResult(`📊 API 健康状态: ${JSON.stringify(result.health, null, 2)}`)
    }
  } else {
    addTestResult(`❌ API 连接失败: ${result.message}`)
  }
}

const loadGenerators = async () => {
  addTestResult('正在加载生成器列表...')
  
  try {
    await workbenchStore.loadAvailableGenerators()
    addTestResult(`✅ 成功加载 ${availableGenerators.length} 个生成器`)
  } catch (error: any) {
    addTestResult(`❌ 加载生成器失败: ${error.message}`)
  }
}

const testGenerator = async (generatorName: string) => {
  testingGenerators.value.push(generatorName)
  addTestResult(`开始测试生成器: ${generatorName}`)
  
  try {
    const result = await workbenchStore.generatePreviewData(generatorName, {}, 3)
    
    if (result) {
      addTestResult(`✅ ${generatorName} 生成成功:`)
      addTestResult(JSON.stringify(result.data.slice(0, 3), null, 2))
    } else {
      addTestResult(`❌ ${generatorName} 生成失败`)
    }
  } catch (error: any) {
    addTestResult(`❌ ${generatorName} 测试失败: ${error.message}`)
  } finally {
    const index = testingGenerators.value.indexOf(generatorName)
    if (index > -1) {
      testingGenerators.value.splice(index, 1)
    }
  }
}

const showGeneratorDetails = async (generatorName: string) => {
  try {
    // 这里可以调用 API 获取详细信息
    const generator = availableGenerators.find(g => g.name === generatorName)
    if (generator) {
      selectedGeneratorDetails.value = generator
      detailsModalVisible.value = true
    }
  } catch (error: any) {
    message.error(`获取生成器详情失败: ${error.message}`)
  }
}

const addTestResult = (result: string) => {
  const timestamp = dayjs().format('HH:mm:ss')
  testResults.value += `[${timestamp}] ${result}\n`
}

const clearResults = () => {
  testResults.value = ''
}

const copyResults = async () => {
  try {
    await navigator.clipboard.writeText(testResults.value)
    message.success('结果已复制到剪贴板')
  } catch (error) {
    message.error('复制失败')
  }
}

const formatTime = (timestamp: string) => {
  return dayjs(timestamp).format('YYYY-MM-DD HH:mm:ss')
}

const getGeneratorTypeColor = (type: string) => {
  const colors: Record<string, string> = {
    'BASIC': 'blue',
    'NUMERIC': 'green',
    'TEXT': 'orange',
    'DATETIME': 'purple',
    'IDENTIFIER': 'cyan',
    'CONTACT': 'red',
    'NETWORK': 'geekblue',
    'unknown': 'default'
  }
  return colors[type] || 'default'
}

// 组件挂载时自动测试连接
onMounted(() => {
  addTestResult('DataForge API 测试页面已加载')
})
</script>

<style scoped lang="less">
.dataforge-test {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--df-spacing-lg);
}

.test-card {
  background: var(--df-secondary-bg);
  border: 1px solid var(--df-text-disabled);
  
  :deep(.ant-card-head) {
    background: transparent;
    border-bottom-color: var(--df-text-disabled);
    
    .ant-card-head-title {
      color: var(--df-text-primary);
      font-size: var(--df-font-size-lg);
      font-weight: 600;
    }
  }
  
  :deep(.ant-card-body) {
    background: transparent;
  }
}

.connection-status {
  .health-info {
    margin-top: var(--df-spacing-md);
    padding: var(--df-spacing-md);
    background: var(--df-primary-bg);
    border: 1px solid var(--df-text-disabled);
    border-radius: var(--df-radius-md);
    
    p {
      margin: var(--df-spacing-xs) 0;
      color: var(--df-text-primary);
    }
  }
}

.generators-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--df-spacing-md);
  margin-top: var(--df-spacing-md);
  
  .generator-card {
    background: var(--df-primary-bg);
    border: 1px solid var(--df-text-disabled);
    
    :deep(.ant-card-head) {
      background: transparent;
      border-bottom-color: var(--df-text-disabled);
      
      .ant-card-head-title {
        color: var(--df-text-primary);
        font-size: var(--df-font-size-sm);
      }
    }
    
    :deep(.ant-card-body) {
      background: transparent;
    }
    
    .generator-description {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-sm);
      margin: var(--df-spacing-xs) 0;
    }
    
    .generator-params {
      color: var(--df-text-primary);
      font-size: var(--df-font-size-xs);
      margin: var(--df-spacing-xs) 0;
    }
  }
}

.test-results {
  :deep(.ant-input) {
    background: var(--df-primary-bg);
    border-color: var(--df-text-disabled);
    color: var(--df-text-primary);
    font-family: 'JetBrains Mono', 'Consolas', monospace;
    font-size: var(--df-font-size-xs);
  }
}

:deep(.ant-tag) {
  border-radius: var(--df-radius-sm);
  font-size: var(--df-font-size-xs);
  font-weight: 500;
}

:deep(.ant-btn-primary) {
  background: linear-gradient(135deg, var(--df-accent-primary), var(--df-accent-success));
  border: none;
  font-weight: 500;
  
  &:hover, &:focus {
    background: linear-gradient(135deg, #A855F7, #10B981);
    box-shadow: 0 4px 16px rgba(142, 93, 255, 0.3);
  }
}

:deep(.ant-descriptions-bordered) {
  .ant-descriptions-item-label {
    background: var(--df-primary-bg);
    border-color: var(--df-text-disabled);
    color: var(--df-text-secondary);
    font-weight: 500;
  }
  
  .ant-descriptions-item-content {
    background: var(--df-secondary-bg);
    border-color: var(--df-text-disabled);
    color: var(--df-text-primary);
  }
}

:deep(.ant-modal) {
  .ant-modal-content {
    background: var(--df-secondary-bg);
    border: 1px solid var(--df-text-disabled);
  }
  
  .ant-modal-header {
    background: transparent;
    border-bottom-color: var(--df-text-disabled);
    
    .ant-modal-title {
      color: var(--df-text-primary);
      font-weight: 600;
    }
  }
  
  .ant-modal-body {
    background: transparent;
  }
}

h3 {
  color: var(--df-text-primary);
  font-weight: 600;
  margin-bottom: var(--df-spacing-md);
}

// 响应式设计
@media (max-width: 768px) {
  .dataforge-test {
    padding: var(--df-spacing-md);
  }
  
  .generators-grid {
    grid-template-columns: 1fr;
  }
}
</style>