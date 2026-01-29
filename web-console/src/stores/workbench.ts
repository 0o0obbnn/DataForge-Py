/**
 * 数据生成工作台状态管理
 * 管理数据结构、字段配置、生成配置等，集成 DataForge API
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { message, notification } from 'ant-design-vue'
import type { FieldConfig, DataStructure, GenerationConfig } from '@/utils/types'
import type { GenerationTemplate } from '@/services/template'
import { OUTPUT_FORMATS } from '@/config/constants'
import {
  DataForgeService,
  type GeneratorInfo,
  type GenerationResult,
  type TaskInfo,
  type HealthStatus
} from '@/services/modules/dataforge'

export const useWorkbenchStore = defineStore('workbench', () => {
  // 原有状态
  const currentTaskName = ref('未命名任务')
  const fields = ref<FieldConfig[]>([])
  const selectedFieldId = ref<string | null>(null)
  const generationConfig = ref<GenerationConfig>({
    count: 1000,
    format: OUTPUT_FORMATS.CSV,
    formatOptions: {
      csvDelimiter: ',',
      jsonPrettyPrint: true,
      sqlTableName: 'generated_data'
    }
  })
  const isGenerating = ref(false)
  const previewData = ref<any[]>([])
  const validationResults = ref<any[]>([])

  // DataForge API 状态
  const apiConnected = ref(false)
  const apiConnecting = ref(false)
  const apiHealth = ref<HealthStatus | null>(null)
  const availableGenerators = ref<GeneratorInfo[]>([])
  const generatorCategories = ref<Record<string, GeneratorInfo[]>>({})
  const loadingGenerators = ref(false)
  const activeTasks = ref<TaskInfo[]>([])
  const lastGenerationResult = ref<GenerationResult | null>(null)

  // 计算属性
  const selectedField = computed(() => {
    if (!selectedFieldId.value) return null
    return fields.value.find(field => field.id === selectedFieldId.value) || null
  })

  const hasFields = computed(() => fields.value.length > 0)

  const canPreview = computed(() => {
    return hasFields.value && fields.value.every(field =>
      !field.required || (field.name && field.name.trim() !== '')
    )
  })

  const canGenerate = computed(() => {
    return canPreview.value && generationConfig.value.count > 0
  })

  const canSaveTemplate = computed(() => {
    return hasFields.value && currentTaskName.value.trim() !== ''
  })

  // Actions
  const addField = (fieldConfig: Omit<FieldConfig, 'id'>) => {
    const newField: FieldConfig = {
      ...fieldConfig,
      id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    }
    fields.value.push(newField)
    selectField(newField.id)
  }

  const removeField = (fieldId: string) => {
    const index = fields.value.findIndex(field => field.id === fieldId)
    if (index > -1) {
      fields.value.splice(index, 1)

      // 如果删除的是当前选中的字段，清除选中状态
      if (selectedFieldId.value === fieldId) {
        selectedFieldId.value = null
      }
    }
  }

  const updateField = (fieldId: string, updates: Partial<FieldConfig>) => {
    const field = fields.value.find(f => f.id === fieldId)
    if (field) {
      Object.assign(field, updates)
    }
  }

  const selectField = (fieldId: string) => {
    selectedFieldId.value = fieldId
  }

  const clearSelection = () => {
    selectedFieldId.value = null
  }

  const updateTaskName = (name: string) => {
    currentTaskName.value = name
  }

  const updateGenerationConfig = (config: Partial<GenerationConfig>) => {
    Object.assign(generationConfig.value, config)
  }

  const resetCanvas = () => {
    fields.value = []
    selectedFieldId.value = null
    currentTaskName.value = '未命名任务'
    previewData.value = []
    validationResults.value = []
  }

  const duplicateField = (fieldId: string) => {
    const field = fields.value.find(f => f.id === fieldId)
    if (field) {
      const duplicatedField: FieldConfig = {
        ...field,
        id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        name: `${field.name} - 副本`
      }
      fields.value.push(duplicatedField)
    }
  }

  const moveField = (fieldId: string, newIndex: number) => {
    const currentIndex = fields.value.findIndex(f => f.id === fieldId)
    if (currentIndex > -1 && newIndex >= 0 && newIndex < fields.value.length) {
      const field = fields.value.splice(currentIndex, 1)[0]
      fields.value.splice(newIndex, 0, field)
    }
  }

  const setPreviewData = (data: any[], validation: any[] = []) => {
    previewData.value = data
    validationResults.value = validation
  }

  const clearPreviewData = () => {
    previewData.value = []
    validationResults.value = []
  }

  const setGenerating = (generating: boolean) => {
    isGenerating.value = generating
  }

  const loadTemplate = (template: DataStructure | GenerationTemplate) => {
    if ('metadata' in template) {
      // 新的 GenerationTemplate 格式
      const generationTemplate = template as GenerationTemplate
      currentTaskName.value = generationTemplate.name
      fields.value = generationTemplate.fields.map(field => ({
        ...field,
        id: field.id || `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      }))
      generationConfig.value = { ...generationTemplate.generationConfig }
      selectedFieldId.value = null

      message.success(`已加载模板: ${generationTemplate.name}`)
    } else {
      // 旧的 DataStructure 格式（向后兼容）
      const dataStructure = template as DataStructure
      currentTaskName.value = dataStructure.name
      fields.value = dataStructure.fields.map(field => ({
        ...field,
        id: `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
      }))
      selectedFieldId.value = null

      message.success(`已加载数据结构: ${dataStructure.name}`)
    }
  }

  const saveAsTemplate = (templateData: {
    name: string
    description: string
    category: string
    tags?: string[]
    isPublic?: boolean
  }) => {
    if (!hasFields.value) {
      message.warning('请先配置字段信息')
      return null
    }

    // 构建模板对象
    const template: Omit<GenerationTemplate, 'id' | 'metadata' | 'statistics'> = {
      name: templateData.name,
      description: templateData.description,
      category: templateData.category,
      fields: fields.value,
      generationConfig: generationConfig.value
    }

    return template
  }

  const exportCurrentAsTemplate = (): GenerationTemplate | null => {
    if (!hasFields.value) {
      message.warning('请先配置字段信息')
      return null
    }

    const template: GenerationTemplate = {
      id: `template_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: currentTaskName.value,
      description: `从工作台导出的模板`,
      category: 'custom',
      fields: fields.value,
      generationConfig: generationConfig.value,
      metadata: {
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        author: 'current_user',
        version: '1.0.0',
        tags: [],
        isPublic: false
      },
      statistics: {
        usageCount: 0,
        downloadCount: 0,
        rating: 0,
        reviews: 0
      }
    }

    return template
  }

  const exportDataStructure = (): DataStructure => {
    return {
      id: `structure_${Date.now()}`,
      name: currentTaskName.value,
      fields: fields.value,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
  }

  // DataForge API 方法
  const checkApiConnection = async () => {
    try {
      apiConnecting.value = true
      const connectionResult = await DataForgeService.checkConnection()

      apiConnected.value = connectionResult.connected
      apiHealth.value = connectionResult.health || null

      if (connectionResult.connected) {
        message.success('DataForge API 连接成功')
      } else {
        message.error(connectionResult.message)
      }

      return connectionResult
    } catch (error: any) {
      apiConnected.value = false
      apiHealth.value = null
      message.error(`连接检查失败: ${error.message}`)
      return { connected: false, message: error.message }
    } finally {
      apiConnecting.value = false
    }
  }

  const loadAvailableGenerators = async () => {
    try {
      loadingGenerators.value = true

      // 加载生成器列表
      const generatorsResponse = await DataForgeService.getGenerators()
      if (generatorsResponse.success && generatorsResponse.data) {
        availableGenerators.value = generatorsResponse.data
      }

      // 加载生成器分类
      const categoriesResponse = await DataForgeService.getGeneratorCategories()
      if (categoriesResponse.success && categoriesResponse.data) {
        generatorCategories.value = categoriesResponse.data
      }

      message.success(`已加载 ${availableGenerators.value.length} 个生成器`)

    } catch (error: any) {
      message.error(`加载生成器失败: ${error.message}`)
    } finally {
      loadingGenerators.value = false
    }
  }

  const generatePreviewData = async (generatorName: string, parameters: Record<string, any> = {}, count: number = 5) => {
    try {
      const response = await DataForgeService.generateData(generatorName, {
        count,
        parameters,
        should_validate: true,
        output_format: 'json'
      })

      if (response.success && response.data) {
        setPreviewData(response.data.data)
        message.success(`生成 ${response.data.count} 条预览数据`)
        return response.data
      } else {
        message.error('预览数据生成失败')
        return null
      }
    } catch (error: any) {
      message.error(`预览生成失败: ${error.message}`)
      return null
    }
  }

  const generateBatchData = async (configurations: Array<{
    generator_type: string
    parameters: Record<string, any>
  }>, count: number = 100) => {
    try {
      isGenerating.value = true

      const response = await DataForgeService.generateBatchData({
        generators: configurations,
        count,
        output_format: 'json'
      })

      if (response.success && response.data) {
        lastGenerationResult.value = response.data as any
        message.success(`成功生成 ${response.data.count} 条数据`)
        return response.data
      } else {
        message.error('批量数据生成失败')
        return null
      }
    } catch (error: any) {
      message.error(`批量生成失败: ${error.message}`)
      return null
    } finally {
      isGenerating.value = false
    }
  }

  const generateLargeDataAsync = async (
    generatorName: string,
    parameters: Record<string, any> = {},
    count: number = 10000
  ) => {
    try {
      const response = await DataForgeService.generateDataAsync(generatorName, {
        count,
        parameters,
        should_validate: true,
        output_format: 'json'
      })

      if (response.success && response.data) {
        // 添加到活跃任务列表
        activeTasks.value.push(response.data)

        notification.success({
          message: '异步任务已创建',
          description: `任务ID: ${response.data.task_id}，正在生成 ${count} 条数据`,
          duration: 10
        })

        return response.data
      } else {
        message.error('异步任务创建失败')
        return null
      }
    } catch (error: any) {
      message.error(`异步任务创建失败: ${error.message}`)
      return null
    }
  }

  const checkTaskStatus = async (taskId: string) => {
    try {
      const response = await DataForgeService.getTaskStatus(taskId)

      if (response.success && response.data) {
        // 更新任务状态
        const taskIndex = activeTasks.value.findIndex(task => task.task_id === taskId)
        if (taskIndex > -1) {
          activeTasks.value[taskIndex] = response.data
        }

        // 如果任务完成，显示通知
        if (response.data.status === 'completed') {
          notification.success({
            message: '数据生成完成',
            description: `任务 ${taskId} 已完成，生成了 ${response.data.result?.count || 0} 条数据`,
            duration: 10
          })
        } else if (response.data.status === 'failed') {
          notification.error({
            message: '数据生成失败',
            description: `任务 ${taskId} 失败: ${response.data.error}`,
            duration: 15
          })
        }

        return response.data
      }

      return null
    } catch (error: any) {
      message.error(`检查任务状态失败: ${error.message}`)
      return null
    }
  }

  const removeTask = (taskId: string) => {
    const index = activeTasks.value.findIndex(task => task.task_id === taskId)
    if (index > -1) {
      activeTasks.value.splice(index, 1)
    }
  }

  const clearCompletedTasks = () => {
    activeTasks.value = activeTasks.value.filter(
      task => !['completed', 'failed'].includes(task.status)
    )
  }

  const initializeDataForgeConnection = async () => {
    await checkApiConnection()
    if (apiConnected.value) {
      await loadAvailableGenerators()
    }
  }

  return {
    // 原有状态
    currentTaskName,
    fields,
    selectedFieldId,
    generationConfig,
    isGenerating,
    previewData,
    validationResults,

    // DataForge API 状态
    apiConnected,
    apiConnecting,
    apiHealth,
    availableGenerators,
    generatorCategories,
    loadingGenerators,
    activeTasks,
    lastGenerationResult,

    // 原有计算属性
    selectedField,
    hasFields,
    canPreview,
    canGenerate,
    canSaveTemplate,

    // 原有方法
    addField,
    removeField,
    updateField,
    selectField,
    clearSelection,
    updateTaskName,
    updateGenerationConfig,
    resetCanvas,
    duplicateField,
    moveField,
    setPreviewData,
    clearPreviewData,
    setGenerating,
    loadTemplate,
    saveAsTemplate,
    exportCurrentAsTemplate,
    exportDataStructure,

    // DataForge API 方法
    checkApiConnection,
    loadAvailableGenerators,
    generatePreviewData,
    generateBatchData,
    generateLargeDataAsync,
    checkTaskStatus,
    removeTask,
    clearCompletedTasks,
    initializeDataForgeConnection
  }
})
