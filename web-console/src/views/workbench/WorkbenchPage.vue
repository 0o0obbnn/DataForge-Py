<template>
  <div class="workbench-page">
    <div class="workbench-layout">
      <!-- 顶部全局操作区 -->
      <header class="workbench-header">
        <h1 class="task-name" contenteditable @blur="updateTaskName">
          {{ workbenchStore.currentTaskName }}
        </h1>
      </header>

      <!-- 三栏布局 -->
      <div class="workbench-content">
        <!-- 左侧字段库 -->
        <aside class="field-library">
          <div class="library-header">
            <h2>生成器库</h2>
            <a-button
              size="small"
              :loading="workbenchStore.apiConnecting || workbenchStore.loadingGenerators"
              @click="workbenchStore.loadAvailableGenerators"
            >
              <ReloadOutlined />
            </a-button>
          </div>

          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索生成器..."
            @search="handleSearch"
            allow-clear
          />

          <!-- API 连接状态 -->
          <div class="connection-status">
            <a-space>
              <a-tag :color="workbenchStore.apiConnected ? 'green' : 'red'">
                {{ workbenchStore.apiConnected ? '已连接' : '未连接' }}
              </a-tag>
              <span v-if="workbenchStore.apiHealth" class="generator-count">
                {{ workbenchStore.availableGenerators.length }} 个生成器
              </span>
            </a-space>
          </div>

          <!-- 生成器分类 -->
          <div class="generator-categories" v-if="workbenchStore.apiConnected">
            <a-collapse v-model:activeKey="activeCategories" ghost>
              <a-collapse-panel
                v-for="(generators, category) in filteredCategories"
                :key="category"
                :header="category"
                :show-arrow="generators.length > 0"
              >
                <template #extra>
                  <a-tag size="small">{{ generators.length }}</a-tag>
                </template>

                <div class="generator-list">
                  <div
                    v-for="generator in generators"
                    :key="generator.name"
                    class="generator-item"
                    draggable="true"
                    @dragstart="handleDragStart(generator)"
                    @click="handleGeneratorClick(generator)"
                  >
                    <div class="generator-info">
                      <h4>{{ generator.name }}</h4>
                      <p>{{ generator.description }}</p>
                      <a-tag
                        v-if="generator.parameters.length > 0"
                        size="small"
                        color="blue"
                      >
                        {{ generator.parameters.length }} 参数
                      </a-tag>
                    </div>
                  </div>
                </div>
              </a-collapse-panel>
            </a-collapse>
          </div>

          <!-- 未连接状态 -->
          <div v-else class="no-connection">
            <a-empty
              description="DataForge API 未连接"
              image="/empty-state.svg"
            >
              <a-button
                type="primary"
                @click="workbenchStore.checkApiConnection"
                :loading="workbenchStore.apiConnecting"
              >
                重新连接
              </a-button>
            </a-empty>
          </div>
        </aside>

        <!-- 中间数据结构画布 -->
        <main class="data-canvas">
          <div class="canvas-header">
            <h2>数据结构画布</h2>
            <a-space>
              <a-button
                size="small"
                @click="workbenchStore.resetCanvas"
                :disabled="!workbenchStore.hasFields"
              >
                <ClearOutlined />
                清空画布
              </a-button>
              <a-button
                size="small"
                type="primary"
                @click="previewData"
                :disabled="!workbenchStore.canPreview"
                :loading="previewing"
              >
                <EyeOutlined />
                预览数据
              </a-button>
            </a-space>
          </div>

          <div
            class="canvas-content"
            @drop="handleDrop"
            @dragover="handleDragOver"
            @dragenter="handleDragEnter"
            @dragleave="handleDragLeave"
            :class="{ 'drag-over': isDragOver }"
          >
            <!-- 空状态 -->
            <div v-if="!workbenchStore.hasFields" class="canvas-placeholder">
              <div class="placeholder-content">
                <DatabaseOutlined class="placeholder-icon" />
                <h3>开始创建您的数据结构</h3>
                <p>从左侧生成器库拖拽生成器到这里，或点击生成器添加字段</p>
              </div>
            </div>

            <!-- 字段列表 -->
            <div v-else class="field-list">
              <TransitionGroup name="field" tag="div">
                <div
                  v-for="(field, index) in workbenchStore.fields"
                  :key="field.id"
                  class="field-card"
                  :class="{ 'field-selected': workbenchStore.selectedFieldId === field.id }"
                  @click="handleFieldSelect(field.id)"
                >
                  <div class="field-header">
                    <div class="field-info">
                      <h4 class="field-name">{{ field.name || `字段${index + 1}` }}</h4>
                      <a-tag size="small" color="blue">{{ field.generatorType }}</a-tag>
                    </div>
                    <div class="field-actions">
                      <a-button
                        type="text"
                        size="small"
                        @click.stop="duplicateField(field.id)"
                        title="复制字段"
                      >
                        <CopyOutlined />
                      </a-button>
                      <a-button
                        type="text"
                        size="small"
                        @click.stop="removeField(field.id)"
                        title="删除字段"
                        danger
                      >
                        <DeleteOutlined />
                      </a-button>
                    </div>
                  </div>

                  <div class="field-details">
                    <p class="field-description">{{ getGeneratorDescription(field.generatorType) }}</p>
                    <div v-if="field.parameters && Object.keys(field.parameters).length > 0" class="field-parameters">
                      <a-tag
                        v-for="(value, key) in field.parameters"
                        :key="key"
                        size="small"
                      >
                        {{ key }}: {{ value }}
                      </a-tag>
                    </div>
                  </div>
                </div>
              </TransitionGroup>
            </div>
          </div>

          <!-- 预览数据 -->
          <div v-if="workbenchStore.previewData.length > 0" class="preview-section">
            <div class="preview-header">
              <h3>数据预览</h3>
              <a-button
                size="small"
                @click="workbenchStore.clearPreviewData"
              >
                <CloseOutlined />
              </a-button>
            </div>
            <div class="preview-content">
              <a-table
                :columns="previewColumns"
                :data-source="workbenchStore.previewData"
                :pagination="{ pageSize: 5 }"
                size="small"
                :scroll="{ x: 'max-content' }"
              />
            </div>
          </div>
        </main>

        <!-- 右侧字段配置面板 -->
        <aside class="config-panel">
          <h2>字段配置</h2>

          <!-- 未选中字段 -->
          <div v-if="!workbenchStore.selectedField" class="config-placeholder">
            <div class="placeholder-content">
              <SettingOutlined class="placeholder-icon" />
              <p>请从画布中选择一个字段进行配置</p>
            </div>
          </div>

          <!-- 字段配置表单 -->
          <div v-else class="config-content">
            <a-form
              :model="fieldConfigForm"
              layout="vertical"
              @finish="updateFieldConfig"
            >
              <!-- 基础配置 -->
              <a-form-item
                label="字段名称"
                name="name"
                :rules="[{ required: true, message: '请输入字段名称' }]"
              >
                <a-input
                  v-model:value="fieldConfigForm.name"
                  placeholder="输入字段名称"
                  @blur="updateFieldName"
                />
              </a-form-item>

              <a-form-item label="生成器类型">
                <a-input
                  :value="workbenchStore.selectedField.generatorType"
                  disabled
                  suffix="不可修改"
                />
              </a-form-item>

              <a-form-item label="字段描述">
                <a-textarea
                  v-model:value="fieldConfigForm.description"
                  placeholder="输入字段描述（可选）"
                  :rows="2"
                  @blur="updateFieldDescription"
                />
              </a-form-item>

              <!-- 生成器参数配置 -->
              <a-divider>生成器参数</a-divider>

              <div v-if="selectedGeneratorInfo" class="generator-params">
                <div
                  v-for="paramName in selectedGeneratorInfo.parameters"
                  :key="paramName"
                  class="param-item"
                >
                  <a-form-item :label="paramName">
                    <a-input
                      v-model:value="fieldConfigForm.parameters[paramName]"
                      :placeholder="`输入 ${paramName} 参数值`"
                      @blur="updateFieldParameters"
                    />
                  </a-form-item>
                </div>

                <div v-if="selectedGeneratorInfo.parameters.length === 0" class="no-params">
                  <p>该生成器无需额外参数</p>
                </div>
              </div>

              <!-- 示例参数 -->
              <div v-if="selectedGeneratorInfo?.example_parameters" class="example-params">
                <a-divider>参数示例</a-divider>
                <pre class="example-code">{{ JSON.stringify(selectedGeneratorInfo.example_parameters, null, 2) }}</pre>
                <a-button
                  size="small"
                  @click="applyExampleParams"
                  style="margin-top: 8px;"
                >
                  应用示例参数
                </a-button>
              </div>

              <!-- 操作按钮 -->
              <a-divider />
              <a-space direction="vertical" style="width: 100%;">
                <a-button
                  type="primary"
                  size="small"
                  @click="testFieldGeneration"
                  :loading="testingField"
                  block
                >
                  <PlayCircleOutlined />
                  测试生成
                </a-button>

                <a-button
                  size="small"
                  @click="duplicateCurrentField"
                  block
                >
                  <CopyOutlined />
                  复制字段
                </a-button>

                <a-button
                  danger
                  size="small"
                  @click="removeCurrentField"
                  block
                >
                  <DeleteOutlined />
                  删除字段
                </a-button>
              </a-space>
            </a-form>
          </div>
        </aside>
      </div>

      <!-- 底部控制台 -->
      <footer class="workbench-footer">
        <div class="footer-controls">
          <a-space>
            <a-input-number
              v-model:value="workbenchStore.generationConfig.count"
              :min="1"
              :max="100000"
              placeholder="生成数量"
              style="width: 120px;"
              @change="handleCountChange"
            />
            <a-select
              v-model:value="workbenchStore.generationConfig.format"
              style="width: 120px"
              @change="handleFormatChange"
            >
              <a-select-option value="json">JSON</a-select-option>
              <a-select-option value="csv">CSV</a-select-option>
              <a-select-option value="xml">XML</a-select-option>
              <a-select-option value="sql">SQL</a-select-option>
            </a-select>
            <a-button
              @click="previewData"
              :disabled="!workbenchStore.canPreview"
              :loading="previewing"
            >
              <EyeOutlined />
              预览数据
            </a-button>
            <a-button
              @click="workbenchStore.resetCanvas"
              :disabled="!workbenchStore.hasFields"
            >
              <ClearOutlined />
              重置画布
            </a-button>
            <span v-if="estimatedFileSize" class="file-size-estimate">
              预估大小: {{ estimatedFileSize }}
            </span>
            <a-button
              type="primary"
              @click="generateAndDownload"
              :disabled="!workbenchStore.canGenerate"
              :loading="workbenchStore.isGenerating"
            >
              <DownloadOutlined />
              生成并下载
            </a-button>
          </a-space>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  ReloadOutlined, ClearOutlined, EyeOutlined, DownloadOutlined,
  DatabaseOutlined, SettingOutlined, CopyOutlined, DeleteOutlined,
  CloseOutlined, PlayCircleOutlined
} from '@ant-design/icons-vue'
import { useWorkbenchStore } from '@/stores/workbench'
import { ExportService } from '@/utils/export'
import type { GeneratorInfo } from '@/services/modules/dataforge'
import type { ExportFormat } from '@/utils/export'

const route = useRoute()
const workbenchStore = useWorkbenchStore()

// 响应式数据
const searchKeyword = ref('')
const activeCategories = ref<string[]>(['基础数据', '身份信息', '联系方式'])
const isDragOver = ref(false)
const previewing = ref(false)
const testingField = ref(false)
const estimatedFileSize = ref<string>('')
const fieldConfigForm = ref({
  name: '',
  description: '',
  parameters: {} as Record<string, any>
})

// 搜索和过滤
const filteredCategories = computed(() => {
  if (!searchKeyword.value.trim()) {
    return workbenchStore.generatorCategories
  }

  const filtered: Record<string, GeneratorInfo[]> = {}
  const keyword = searchKeyword.value.toLowerCase()

  Object.entries(workbenchStore.generatorCategories).forEach(([category, generators]) => {
    const matchedGenerators = generators.filter(generator =>
      generator.name.toLowerCase().includes(keyword) ||
      generator.description.toLowerCase().includes(keyword)
    )
    if (matchedGenerators.length > 0) {
      filtered[category] = matchedGenerators
    }
  })

  return filtered
})

// 获取当前选中的生成器信息
const selectedGeneratorInfo = computed(() => {
  if (!workbenchStore.selectedField) return null
  return workbenchStore.availableGenerators.find(
    g => g.name === workbenchStore.selectedField?.generatorType
  )
})

// 预览数据的表格列配置
const previewColumns = computed(() => {
  if (workbenchStore.previewData.length === 0) return []

  const firstRow = workbenchStore.previewData[0]
  return Object.keys(firstRow).map(key => ({
    title: key,
    dataIndex: key,
    key: key,
    ellipsis: true,
    width: 150
  }))
})

// 方法
const handleSearch = (value: string) => {
  searchKeyword.value = value
}

const updateTaskName = (event: Event) => {
  const target = event.target as HTMLElement
  const newName = target.textContent || '未命名任务'
  workbenchStore.updateTaskName(newName)
}

// 拖拽处理
const handleDragStart = (generator: GeneratorInfo) => {
  const dragData = {
    type: 'generator',
    generator: generator
  }
  // 存储拖拽数据
  event?.dataTransfer?.setData('text/plain', JSON.stringify(dragData))
}

const handleDragOver = (event: DragEvent) => {
  event.preventDefault()
}

const handleDragEnter = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = true
}

const handleDragLeave = (event: DragEvent) => {
  event.preventDefault()
  // 只有当离开画布区域时才取消高亮
  if (!event.currentTarget?.contains(event.relatedTarget as Node)) {
    isDragOver.value = false
  }
}

const handleDrop = (event: DragEvent) => {
  event.preventDefault()
  isDragOver.value = false

  try {
    const dragDataStr = event.dataTransfer?.getData('text/plain')
    if (!dragDataStr) return

    const dragData = JSON.parse(dragDataStr)
    if (dragData.type === 'generator') {
      addGeneratorToCanvas(dragData.generator)
    }
  } catch (error) {
    console.error('处理拖拽数据失败:', error)
    message.error('添加生成器失败')
  }
}

// 生成器点击处理
const handleGeneratorClick = (generator: GeneratorInfo) => {
  addGeneratorToCanvas(generator)
}

// 添加生成器到画布
const addGeneratorToCanvas = (generator: GeneratorInfo) => {
  const fieldConfig = {
    name: generator.name,
    generatorType: generator.name,
    description: generator.description,
    parameters: {},
    required: true
  }

  workbenchStore.addField(fieldConfig)
  message.success(`已添加生成器：${generator.name}`)
}

// 字段管理
const removeField = (fieldId: string) => {
  workbenchStore.removeField(fieldId)
  message.success('字段已删除')
}

const duplicateField = (fieldId: string) => {
  workbenchStore.duplicateField(fieldId)
  message.success('字段已复制')
}

// 获取生成器描述
const getGeneratorDescription = (generatorType: string) => {
  const generator = workbenchStore.availableGenerators.find(g => g.name === generatorType)
  return generator?.description || '无描述'
}

// 字段配置
const updateFieldName = () => {
  if (workbenchStore.selectedField && fieldConfigForm.value.name) {
    workbenchStore.updateField(workbenchStore.selectedField.id, {
      name: fieldConfigForm.value.name
    })
  }
}

const updateFieldDescription = () => {
  if (workbenchStore.selectedField) {
    workbenchStore.updateField(workbenchStore.selectedField.id, {
      description: fieldConfigForm.value.description
    })
  }
}

const updateFieldParameters = () => {
  if (workbenchStore.selectedField) {
    workbenchStore.updateField(workbenchStore.selectedField.id, {
      parameters: { ...fieldConfigForm.value.parameters }
    })
  }
}

// 应用示例参数
const applyExampleParams = () => {
  if (selectedGeneratorInfo.value?.example_parameters) {
    fieldConfigForm.value.parameters = { ...selectedGeneratorInfo.value.example_parameters }
    updateFieldParameters()
    message.success('已应用示例参数')
  }
}

// 测试字段生成
const testFieldGeneration = async () => {
  if (!workbenchStore.selectedField) return

  testingField.value = true
  try {
    const result = await workbenchStore.generatePreviewData(
      workbenchStore.selectedField.generatorType,
      workbenchStore.selectedField.parameters || {},
      3
    )

    if (result) {
      message.success('测试生成成功')
    }
  } catch (error: any) {
    message.error(`测试失败: ${error.message}`)
  } finally {
    testingField.value = false
  }
}

// 复制和删除当前字段
const duplicateCurrentField = () => {
  if (workbenchStore.selectedField) {
    duplicateField(workbenchStore.selectedField.id)
  }
}

const removeCurrentField = () => {
  if (workbenchStore.selectedField) {
    removeField(workbenchStore.selectedField.id)
  }
}

// 预览数据
const previewData = async () => {
  if (!workbenchStore.canPreview) {
    message.warning('请先配置字段信息')
    return
  }

  previewing.value = true
  try {
    // 构建批量生成配置
    const configurations = workbenchStore.fields.map(field => ({
      generator_type: field.generatorType,
      parameters: field.parameters || {}
    }))

    const result = await workbenchStore.generateBatchData(configurations, 5)

    if (result) {
      message.success('预览数据生成成功')
      // 更新文件大小估算
      updateFileSizeEstimate()
    } else {
      message.error('预览数据生成失败')
    }
  } catch (error: any) {
    message.error(`预览失败: ${error.message}`)
  } finally {
    previewing.value = false
  }
}

// 生成并下载数据
const generateAndDownload = async () => {
  if (!workbenchStore.canGenerate) {
    message.warning('请先配置字段和生成参数')
    return
  }

  try {
    workbenchStore.setGenerating(true)

    // 构建批量生成配置
    const configurations = workbenchStore.fields.map(field => ({
      generator_type: field.generatorType,
      parameters: field.parameters || {}
    }))

    // 生成数据
    const result = await workbenchStore.generateBatchData(
      configurations,
      workbenchStore.generationConfig.count
    )

    if (result && result.data) {
      // 验证数据
      const validation = ExportService.validateExportData(result.data)
      if (!validation.valid) {
        message.error(`数据验证失败: ${validation.message}`)
        return
      }

      // 准备导出选项
      const exportOptions = {
        format: workbenchStore.generationConfig.format as ExportFormat,
        filename: `${workbenchStore.currentTaskName}_${result.count}条数据`,
        formatOptions: workbenchStore.generationConfig.formatOptions
      }

      // 导出文件
      await ExportService.exportData(result.data, exportOptions)

      message.success(`成功生成并导出 ${result.count} 条数据`)
    } else {
      message.error('数据生成失败')
    }
  } catch (error: any) {
    message.error(`生成失败: ${error.message}`)
  } finally {
    workbenchStore.setGenerating(false)
  }
}

// 监听选中字段变化，同步到表单
const syncFieldConfigForm = () => {
  if (workbenchStore.selectedField) {
    fieldConfigForm.value = {
      name: workbenchStore.selectedField.name || '',
      description: workbenchStore.selectedField.description || '',
      parameters: { ...workbenchStore.selectedField.parameters }
    }
  }
}

// 计算文件大小估算
const updateFileSizeEstimate = () => {
  if (workbenchStore.previewData.length > 0) {
    const format = workbenchStore.generationConfig.format as ExportFormat
    estimatedFileSize.value = ExportService.estimateFileSize(workbenchStore.previewData, format)
  } else {
    estimatedFileSize.value = ''
  }
}

// 监听配置变化，更新文件大小估算
const handleFormatChange = () => {
  updateFileSizeEstimate()
}

const handleCountChange = () => {
  // 根据预览数据和数量比例估算
  if (workbenchStore.previewData.length > 0 && workbenchStore.generationConfig.count > 0) {
    const ratio = workbenchStore.generationConfig.count / workbenchStore.previewData.length
    const previewSize = ExportService.estimateFileSize(
      workbenchStore.previewData,
      workbenchStore.generationConfig.format as ExportFormat
    )

    // 简单的大小估算
    const sizeMatch = previewSize.match(/(\d+\.?\d*)\s*(\w+)/)
    if (sizeMatch) {
      const [, size, unit] = sizeMatch
      const estimatedSize = parseFloat(size) * ratio
      estimatedFileSize.value = `约 ${estimatedSize.toFixed(1)} ${unit}`
    }
  }
}

// 监听字段选择变化
const handleFieldSelect = (fieldId: string) => {
  workbenchStore.selectField(fieldId)
  syncFieldConfigForm()
}

// 组件挂载
onMounted(async () => {
  // 初始化 DataForge API 连接
  try {
    await workbenchStore.initializeDataForgeConnection()
  } catch (error) {
    console.error('初始化 DataForge 连接失败:', error)
  }

  // 检查是否是加载模板
  const templateId = route.params.templateId as string
  if (templateId) {
    // TODO: 加载指定模板
    console.log('加载模板:', templateId)
  }

  // 监听选中字段变化
  workbenchStore.$subscribe((mutation, state) => {
    if (mutation.type === 'direct' && 'selectedFieldId' in mutation.payload) {
      syncFieldConfigForm()
    }

    // 监听预览数据变化，更新文件大小估算
    if (mutation.type === 'direct' && 'previewData' in mutation.payload) {
      updateFileSizeEstimate()
    }
  })
})
</script>

<style scoped lang="less">
.workbench-page {
  min-height: 100vh;
  background: var(--df-primary-bg);
}

.workbench-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.workbench-header {
  background: var(--df-secondary-bg);
  padding: var(--df-spacing-md) var(--df-spacing-lg);
  border-bottom: 1px solid var(--df-text-disabled);

  .task-name {
    color: var(--df-text-primary);
    font-size: var(--df-font-size-xl);
    margin: 0;
    cursor: text;

    &:focus {
      outline: 2px solid var(--df-accent-primary);
      outline-offset: 2px;
    }
  }
}

.workbench-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.field-library {
  width: 280px;
  background: var(--df-primary-bg);
  border-right: 1px solid var(--df-text-disabled);
  padding: var(--df-spacing-md);
  overflow-y: auto;

  .library-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: var(--df-spacing-md);

    h2 {
      color: var(--df-text-primary);
      font-size: var(--df-font-size-lg);
      margin: 0;
    }
  }

  .connection-status {
    margin: var(--df-spacing-md) 0;
    padding: var(--df-spacing-sm);
    background: var(--df-secondary-bg);
    border-radius: var(--df-radius-md);

    .generator-count {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-sm);
    }
  }

  .generator-categories {
    margin-top: var(--df-spacing-md);

    .generator-list {
      display: flex;
      flex-direction: column;
      gap: var(--df-spacing-sm);

      .generator-item {
        background: var(--df-secondary-bg);
        border: 1px solid var(--df-text-disabled);
        border-radius: var(--df-radius-sm);
        padding: var(--df-spacing-sm);
        cursor: pointer;
        transition: all 0.2s ease;

        &:hover {
          border-color: var(--df-accent-primary);
          box-shadow: 0 2px 4px rgba(139, 92, 246, 0.1);
          transform: translateY(-1px);
        }

        .generator-info {
          h4 {
            color: var(--df-text-primary);
            font-size: var(--df-font-size-sm);
            font-weight: 600;
            margin: 0 0 var(--df-spacing-xs) 0;
          }

          p {
            color: var(--df-text-secondary);
            font-size: var(--df-font-size-xs);
            margin: 0;
            line-height: 1.4;
          }
        }
      }
    }
  }

  .no-connection {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    text-align: center;
  }
}

.data-canvas {
  flex: 1;
  background: var(--df-secondary-bg);
  padding: var(--df-spacing-md);
  display: flex;
  flex-direction: column;

  .canvas-header {
    margin-bottom: var(--df-spacing-md);

    h2 {
      color: var(--df-text-primary);
      font-size: var(--df-font-size-lg);
      margin: 0;
    }
  }

  .canvas-content {
    flex: 1;
    border: 2px dashed var(--df-text-disabled);
    border-radius: var(--df-radius-lg);
    display: flex;
    flex-direction: column;
    min-height: 400px;

    &.drag-over {
      border-color: var(--df-accent-primary);
      background: rgba(139, 92, 246, 0.05);
    }

    .canvas-placeholder {
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;

      .placeholder-content {
        text-align: center;
        color: var(--df-text-secondary);

        .placeholder-icon {
          font-size: 48px;
          color: var(--df-text-disabled);
          margin-bottom: var(--df-spacing-md);
        }

        h3 {
          color: var(--df-text-primary);
          margin: var(--df-spacing-md) 0;
        }

        p {
          color: var(--df-text-secondary);
          margin: 0;
        }
      }
    }

    .field-list {
      padding: var(--df-spacing-md);
      display: flex;
      flex-direction: column;
      gap: var(--df-spacing-md);

      .field-card {
        background: var(--df-primary-bg);
        border: 1px solid var(--df-text-disabled);
        border-radius: var(--df-radius-md);
        padding: var(--df-spacing-md);
        cursor: pointer;
        transition: all 0.2s ease;

        &:hover {
          border-color: var(--df-accent-primary);
          box-shadow: 0 2px 8px rgba(139, 92, 246, 0.15);
        }

        &.field-selected {
          border-color: var(--df-accent-primary);
          box-shadow: 0 0 0 1px rgba(139, 92, 246, 0.2);
        }

        .field-header {
          display: flex;
          justify-content: space-between;
          align-items: flex-start;
          margin-bottom: var(--df-spacing-sm);

          .field-info {
            flex: 1;

            .field-name {
              color: var(--df-text-primary);
              font-size: var(--df-font-size-md);
              font-weight: 600;
              margin: 0 0 var(--df-spacing-xs) 0;
            }
          }

          .field-actions {
            display: flex;
            gap: var(--df-spacing-xs);
          }
        }

        .field-details {
          .field-description {
            color: var(--df-text-secondary);
            font-size: var(--df-font-size-sm);
            margin: var(--df-spacing-xs) 0;
          }

          .field-parameters {
            display: flex;
            flex-wrap: wrap;
            gap: var(--df-spacing-xs);
            margin-top: var(--df-spacing-sm);
          }
        }
      }
    }

    .preview-section {
      margin-top: var(--df-spacing-md);
      background: var(--df-primary-bg);
      border: 1px solid var(--df-text-disabled);
      border-radius: var(--df-radius-md);

      .preview-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: var(--df-spacing-md);
        border-bottom: 1px solid var(--df-text-disabled);

        h3 {
          color: var(--df-text-primary);
          margin: 0;
          font-size: var(--df-font-size-md);
          font-weight: 600;
        }
      }

      .preview-content {
        padding: var(--df-spacing-md);
      }
    }
  }
}

.config-panel {
  width: 320px;
  background: var(--df-primary-bg);
  border-left: 1px solid var(--df-text-disabled);
  padding: var(--df-spacing-md);
  overflow-y: auto;

  h2 {
    color: var(--df-text-primary);
    font-size: var(--df-font-size-lg);
    margin-bottom: var(--df-spacing-md);
  }

  .config-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 200px;
    text-align: center;
    color: var(--df-text-secondary);

    .placeholder-content {
      .placeholder-icon {
        font-size: 48px;
        color: var(--df-text-disabled);
        margin-bottom: var(--df-spacing-md);
      }

      p {
        margin: 0;
      }
    }
  }

  .config-content {
    .generator-params {
      .param-item {
        margin-bottom: var(--df-spacing-sm);
      }

      .no-params {
        text-align: center;
        color: var(--df-text-secondary);
        padding: var(--df-spacing-lg);
        background: var(--df-secondary-bg);
        border-radius: var(--df-radius-md);

        p {
          margin: 0;
          font-size: var(--df-font-size-sm);
        }
      }
    }

    .example-params {
      .example-code {
        background: var(--df-secondary-bg);
        border: 1px solid var(--df-text-disabled);
        border-radius: var(--df-radius-sm);
        padding: var(--df-spacing-sm);
        font-family: 'JetBrains Mono', 'Consolas', monospace;
        font-size: var(--df-font-size-xs);
        color: var(--df-text-primary);
        white-space: pre-wrap;
        overflow-x: auto;
      }
    }
  }
}

.workbench-footer {
  background: var(--df-secondary-bg);
  padding: var(--df-spacing-md) var(--df-spacing-lg);
  border-top: 1px solid var(--df-text-disabled);

  .footer-controls {
    display: flex;
    justify-content: center;

    .file-size-estimate {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-sm);
      padding: 0 var(--df-spacing-md);
      align-self: center;
    }
  }
}

// 字段过渡动画
.field-enter-active,
.field-leave-active {
  transition: all 0.3s ease;
}

.field-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.field-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

// 响应式设计
@media (max-width: 1200px) {
  .workbench-content {
    .field-library {
      width: 260px;
    }

    .config-panel {
      width: 300px;
    }
  }
}

@media (max-width: 768px) {
  .workbench-content {
    flex-direction: column;

    .field-library,
    .config-panel {
      width: 100%;
      max-height: 200px;
      border: 1px solid var(--df-text-disabled);
      border-radius: var(--df-radius-md);
      margin-bottom: var(--df-spacing-md);
    }

    .field-library {
      border-right: none;
      border-bottom: 1px solid var(--df-text-disabled);
    }

    .config-panel {
      border-left: none;
    }
  }

  .workbench-footer {
    .footer-controls {
      :deep(.ant-space) {
        flex-wrap: wrap;
        justify-content: center;
      }
    }
  }
}
</style>
