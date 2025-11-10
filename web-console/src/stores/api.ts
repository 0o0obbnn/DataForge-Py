/**
 * API管理状态管理
 * 管理API Key、调用统计、日志等
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { ApiKey, ApiCallLog, PaginatedResponse } from '@/utils/types'
import { http } from '@/plugins/axios'

export const useApiStore = defineStore('api', () => {
  // 状态
  const apiKeys = ref<ApiKey[]>([])
  const callLogs = ref<ApiCallLog[]>([])
  const statistics = ref({
    totalCalls: 0,
    successCalls: 0,
    errorCalls: 0,
    averageResponseTime: 0,
    callsByDay: [] as Array<{ date: string; count: number }>,
    callsByTemplate: [] as Array<{ templateId: string; templateName: string; count: number }>
  })
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    pageSize: 10,
    total: 0
  })
  const filters = ref({
    timeRange: '7d',
    templateId: 'all',
    statusCode: 'all',
    search: ''
  })

  // 计算属性
  const activeApiKeys = computed(() => 
    apiKeys.value.filter(key => key.isActive)
  )

  const successRate = computed(() => {
    if (statistics.value.totalCalls === 0) return 0
    return Math.round((statistics.value.successCalls / statistics.value.totalCalls) * 100)
  })

  const errorRate = computed(() => {
    if (statistics.value.totalCalls === 0) return 0
    return Math.round((statistics.value.errorCalls / statistics.value.totalCalls) * 100)
  })

  const filteredCallLogs = computed(() => {
    let result = [...callLogs.value]
    
    // 状态码过滤
    if (filters.value.statusCode !== 'all') {
      const statusCode = parseInt(filters.value.statusCode)
      result = result.filter(log => log.statusCode === statusCode)
    }
    
    // 模板过滤
    if (filters.value.templateId !== 'all') {
      result = result.filter(log => log.templateId === filters.value.templateId)
    }
    
    // 搜索过滤
    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      result = result.filter(log => 
        log.templateId.toLowerCase().includes(search) ||
        log.apiKey.toLowerCase().includes(search) ||
        (log.errorMessage && log.errorMessage.toLowerCase().includes(search))
      )
    }
    
    return result
  })

  // Actions
  const fetchApiKeys = async () => {
    try {
      loading.value = true
      
      const response = await http.get<ApiKey[]>('/api/keys')
      apiKeys.value = response.data
      
      return { success: true }
    } catch (error) {
      console.error('获取API Key列表失败:', error)
      return { success: false, message: '获取API Key列表失败' }
    } finally {
      loading.value = false
    }
  }

  const createApiKey = async (name: string) => {
    try {
      loading.value = true
      
      const response = await http.post<ApiKey>('/api/keys', { name })
      apiKeys.value.unshift(response.data)
      
      return { success: true, data: response.data, message: 'API Key创建成功' }
    } catch (error) {
      console.error('创建API Key失败:', error)
      return { success: false, message: '创建API Key失败' }
    } finally {
      loading.value = false
    }
  }

  const updateApiKey = async (keyId: string, updates: Partial<ApiKey>) => {
    try {
      loading.value = true
      
      const response = await http.put<ApiKey>(`/api/keys/${keyId}`, updates)
      
      const index = apiKeys.value.findIndex(key => key.id === keyId)
      if (index > -1) {
        apiKeys.value[index] = response.data
      }
      
      return { success: true, data: response.data, message: 'API Key更新成功' }
    } catch (error) {
      console.error('更新API Key失败:', error)
      return { success: false, message: '更新API Key失败' }
    } finally {
      loading.value = false
    }
  }

  const deleteApiKey = async (keyId: string) => {
    try {
      loading.value = true
      
      await http.delete(`/api/keys/${keyId}`)
      
      const index = apiKeys.value.findIndex(key => key.id === keyId)
      if (index > -1) {
        apiKeys.value.splice(index, 1)
      }
      
      return { success: true, message: 'API Key删除成功' }
    } catch (error) {
      console.error('删除API Key失败:', error)
      return { success: false, message: '删除API Key失败' }
    } finally {
      loading.value = false
    }
  }

  const rotateApiKey = async (keyId: string) => {
    try {
      loading.value = true
      
      const response = await http.post<ApiKey>(`/api/keys/${keyId}/rotate`)
      
      const index = apiKeys.value.findIndex(key => key.id === keyId)
      if (index > -1) {
        apiKeys.value[index] = response.data
      }
      
      return { success: true, data: response.data, message: 'API Key轮换成功' }
    } catch (error) {
      console.error('轮换API Key失败:', error)
      return { success: false, message: '轮换API Key失败' }
    } finally {
      loading.value = false
    }
  }

  const fetchCallLogs = async (page = 1, pageSize = 10) => {
    try {
      loading.value = true
      
      const response = await http.get<PaginatedResponse<ApiCallLog>>('/api/logs', {
        params: {
          page,
          pageSize,
          timeRange: filters.value.timeRange,
          templateId: filters.value.templateId,
          statusCode: filters.value.statusCode,
          search: filters.value.search
        }
      })
      
      callLogs.value = response.data.items
      pagination.value = {
        page: response.data.page,
        pageSize: response.data.pageSize,
        total: response.data.total
      }
      
      return { success: true }
    } catch (error) {
      console.error('获取调用日志失败:', error)
      return { success: false, message: '获取调用日志失败' }
    } finally {
      loading.value = false
    }
  }

  const fetchStatistics = async (timeRange = '7d') => {
    try {
      loading.value = true
      
      const response = await http.get<typeof statistics.value>('/api/statistics', {
        params: { timeRange }
      })
      
      statistics.value = response.data
      
      return { success: true }
    } catch (error) {
      console.error('获取统计数据失败:', error)
      return { success: false, message: '获取统计数据失败' }
    } finally {
      loading.value = false
    }
  }

  const setFilters = (newFilters: Partial<typeof filters.value>) => {
    Object.assign(filters.value, newFilters)
  }

  const clearApiData = () => {
    apiKeys.value = []
    callLogs.value = []
    statistics.value = {
      totalCalls: 0,
      successCalls: 0,
      errorCalls: 0,
      averageResponseTime: 0,
      callsByDay: [],
      callsByTemplate: []
    }
    pagination.value = {
      page: 1,
      pageSize: 10,
      total: 0
    }
  }

  return {
    // 状态
    apiKeys,
    callLogs,
    statistics,
    loading,
    pagination,
    filters,
    
    // 计算属性
    activeApiKeys,
    successRate,
    errorRate,
    filteredCallLogs,
    
    // 方法
    fetchApiKeys,
    createApiKey,
    updateApiKey,
    deleteApiKey,
    rotateApiKey,
    fetchCallLogs,
    fetchStatistics,
    setFilters,
    clearApiData
  }
})





















