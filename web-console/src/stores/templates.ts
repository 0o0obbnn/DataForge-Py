/**
 * 模板管理状态管理
 * 管理模板列表、筛选、搜索等
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Template, TemplateVersion, PaginatedResponse } from '@/utils/types'
import { http } from '@/plugins/axios'

export const useTemplatesStore = defineStore('templates', () => {
  // 状态
  const templates = ref<Template[]>([])
  const currentTemplate = ref<Template | null>(null)
  const templateVersions = ref<TemplateVersion[]>([])
  const loading = ref(false)
  const pagination = ref({
    page: 1,
    pageSize: 10,
    total: 0
  })
  const filters = ref({
    search: '',
    creator: 'all',
    sortBy: 'updatedAt',
    sortOrder: 'desc' as 'asc' | 'desc'
  })

  // 计算属性
  const filteredTemplates = computed(() => {
    let result = [...templates.value]
    
    // 搜索过滤
    if (filters.value.search) {
      const search = filters.value.search.toLowerCase()
      result = result.filter(template => 
        template.name.toLowerCase().includes(search) ||
        template.description.toLowerCase().includes(search)
      )
    }
    
    // 创建者过滤
    if (filters.value.creator !== 'all') {
      result = result.filter(template => template.creator === filters.value.creator)
    }
    
    // 排序
    result.sort((a, b) => {
      const aValue = a[filters.value.sortBy as keyof Template]
      const bValue = b[filters.value.sortBy as keyof Template]
      
      if (filters.value.sortOrder === 'asc') {
        return aValue > bValue ? 1 : -1
      } else {
        return aValue < bValue ? 1 : -1
      }
    })
    
    return result
  })

  const totalPages = computed(() => {
    return Math.ceil(pagination.value.total / pagination.value.pageSize)
  })

  // Actions
  const fetchTemplates = async (page = 1, pageSize = 10) => {
    try {
      loading.value = true
      
      const response = await http.get<PaginatedResponse<Template>>('/templates', {
        params: {
          page,
          pageSize,
          search: filters.value.search,
          creator: filters.value.creator,
          sortBy: filters.value.sortBy,
          sortOrder: filters.value.sortOrder
        }
      })
      
      templates.value = response.data.items
      pagination.value = {
        page: response.data.page,
        pageSize: response.data.pageSize,
        total: response.data.total
      }
      
      return { success: true }
    } catch (error) {
      console.error('获取模板列表失败:', error)
      return { success: false, message: '获取模板列表失败' }
    } finally {
      loading.value = false
    }
  }

  const createTemplate = async (templateData: Omit<Template, 'id' | 'createdAt' | 'updatedAt' | 'version'>) => {
    try {
      loading.value = true
      
      const response = await http.post<Template>('/templates', templateData)
      templates.value.unshift(response.data)
      
      return { success: true, data: response.data, message: '模板创建成功' }
    } catch (error) {
      console.error('创建模板失败:', error)
      return { success: false, message: '创建模板失败' }
    } finally {
      loading.value = false
    }
  }

  const updateTemplate = async (templateId: string, updates: Partial<Template>) => {
    try {
      loading.value = true
      
      const response = await http.put<Template>(`/templates/${templateId}`, updates)
      
      const index = templates.value.findIndex(t => t.id === templateId)
      if (index > -1) {
        templates.value[index] = response.data
      }
      
      return { success: true, data: response.data, message: '模板更新成功' }
    } catch (error) {
      console.error('更新模板失败:', error)
      return { success: false, message: '更新模板失败' }
    } finally {
      loading.value = false
    }
  }

  const deleteTemplate = async (templateId: string) => {
    try {
      loading.value = true
      
      await http.delete(`/templates/${templateId}`)
      
      const index = templates.value.findIndex(t => t.id === templateId)
      if (index > -1) {
        templates.value.splice(index, 1)
      }
      
      return { success: true, message: '模板删除成功' }
    } catch (error) {
      console.error('删除模板失败:', error)
      return { success: false, message: '删除模板失败' }
    } finally {
      loading.value = false
    }
  }

  const duplicateTemplate = async (templateId: string) => {
    try {
      loading.value = true
      
      const response = await http.post<Template>(`/templates/${templateId}/duplicate`)
      templates.value.unshift(response.data)
      
      return { success: true, data: response.data, message: '模板复制成功' }
    } catch (error) {
      console.error('复制模板失败:', error)
      return { success: false, message: '复制模板失败' }
    } finally {
      loading.value = false
    }
  }

  const shareTemplate = async (templateId: string, shareData: {
    scope: 'team' | 'users'
    users?: string[]
    permission: 'read' | 'write'
  }) => {
    try {
      loading.value = true
      
      await http.post(`/templates/${templateId}/share`, shareData)
      
      return { success: true, message: '模板分享成功' }
    } catch (error) {
      console.error('分享模板失败:', error)
      return { success: false, message: '分享模板失败' }
    } finally {
      loading.value = false
    }
  }

  const fetchTemplateVersions = async (templateId: string) => {
    try {
      loading.value = true
      
      const response = await http.get<TemplateVersion[]>(`/templates/${templateId}/versions`)
      templateVersions.value = response.data
      
      return { success: true }
    } catch (error) {
      console.error('获取模板版本失败:', error)
      return { success: false, message: '获取模板版本失败' }
    } finally {
      loading.value = false
    }
  }

  const revertToVersion = async (templateId: string, versionId: string) => {
    try {
      loading.value = true
      
      const response = await http.post<Template>(`/templates/${templateId}/revert`, {
        versionId
      })
      
      const index = templates.value.findIndex(t => t.id === templateId)
      if (index > -1) {
        templates.value[index] = response.data
      }
      
      return { success: true, data: response.data, message: '模板回滚成功' }
    } catch (error) {
      console.error('回滚模板失败:', error)
      return { success: false, message: '回滚模板失败' }
    } finally {
      loading.value = false
    }
  }

  const setFilters = (newFilters: Partial<typeof filters.value>) => {
    Object.assign(filters.value, newFilters)
  }

  const setCurrentTemplate = (template: Template | null) => {
    currentTemplate.value = template
  }

  const clearTemplates = () => {
    templates.value = []
    currentTemplate.value = null
    templateVersions.value = []
    pagination.value = {
      page: 1,
      pageSize: 10,
      total: 0
    }
  }

  return {
    // 状态
    templates,
    currentTemplate,
    templateVersions,
    loading,
    pagination,
    filters,
    
    // 计算属性
    filteredTemplates,
    totalPages,
    
    // 方法
    fetchTemplates,
    createTemplate,
    updateTemplate,
    deleteTemplate,
    duplicateTemplate,
    shareTemplate,
    fetchTemplateVersions,
    revertToVersion,
    setFilters,
    setCurrentTemplate,
    clearTemplates
  }
})





















