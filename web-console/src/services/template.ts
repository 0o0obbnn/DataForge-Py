/**
 * 模板管理服务
 * 处理数据生成模板的保存、加载、分享等功能
 */

import { message } from 'ant-design-vue'
import dayjs from 'dayjs'

export interface TemplateField {
  id: string
  name: string
  generatorType: string
  description?: string
  parameters: Record<string, any>
  required: boolean
}

export interface GenerationTemplate {
  id: string
  name: string
  description: string
  category: string
  fields: TemplateField[]
  generationConfig: {
    count: number
    format: 'json' | 'csv' | 'xml' | 'sql'
    formatOptions?: Record<string, any>
  }
  metadata: {
    createdAt: string
    updatedAt: string
    author: string
    version: string
    tags: string[]
    isPublic: boolean
  }
  statistics?: {
    usageCount: number
    downloadCount: number
    rating: number
    reviews: number
  }
}

export interface TemplateCategory {
  id: string
  name: string
  description: string
  icon: string
  templateCount: number
}

/**
 * 模板管理服务
 */
export class TemplateService {
  private static readonly STORAGE_KEY = 'dataforge_templates'
  private static readonly CATEGORIES_KEY = 'dataforge_template_categories'

  /**
   * 获取所有模板
   */
  static getAllTemplates(): GenerationTemplate[] {
    try {
      const stored = localStorage.getItem(this.STORAGE_KEY)
      return stored ? JSON.parse(stored) : []
    } catch (error) {
      console.error('获取模板失败:', error)
      return []
    }
  }

  /**
   * 根据ID获取模板
   */
  static getTemplateById(id: string): GenerationTemplate | null {
    const templates = this.getAllTemplates()
    return templates.find(template => template.id === id) || null
  }

  /**
   * 保存模板
   */
  static saveTemplate(template: Omit<GenerationTemplate, 'id' | 'metadata'>): GenerationTemplate {
    const templates = this.getAllTemplates()
    
    const newTemplate: GenerationTemplate = {
      ...template,
      id: this.generateId(),
      metadata: {
        createdAt: dayjs().toISOString(),
        updatedAt: dayjs().toISOString(),
        author: 'current_user', // TODO: 从认证系统获取
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

    templates.push(newTemplate)
    this.saveTemplates(templates)
    
    message.success(`模板 "${template.name}" 已保存`)
    return newTemplate
  }

  /**
   * 更新模板
   */
  static updateTemplate(id: string, updates: Partial<GenerationTemplate>): boolean {
    const templates = this.getAllTemplates()
    const index = templates.findIndex(template => template.id === id)
    
    if (index === -1) {
      message.error('模板不存在')
      return false
    }

    templates[index] = {
      ...templates[index],
      ...updates,
      metadata: {
        ...templates[index].metadata,
        ...updates.metadata,
        updatedAt: dayjs().toISOString()
      }
    }

    this.saveTemplates(templates)
    message.success('模板已更新')
    return true
  }

  /**
   * 删除模板
   */
  static deleteTemplate(id: string): boolean {
    const templates = this.getAllTemplates()
    const index = templates.findIndex(template => template.id === id)
    
    if (index === -1) {
      message.error('模板不存在')
      return false
    }

    const templateName = templates[index].name
    templates.splice(index, 1)
    this.saveTemplates(templates)
    
    message.success(`模板 "${templateName}" 已删除`)
    return true
  }

  /**
   * 复制模板
   */
  static duplicateTemplate(id: string): GenerationTemplate | null {
    const template = this.getTemplateById(id)
    if (!template) {
      message.error('模板不存在')
      return null
    }

    const duplicatedTemplate = this.saveTemplate({
      ...template,
      name: `${template.name} (副本)`,
      description: template.description,
      category: template.category,
      fields: template.fields.map(field => ({
        ...field,
        id: this.generateId() // 生成新的字段ID
      })),
      generationConfig: { ...template.generationConfig }
    })

    return duplicatedTemplate
  }

  /**
   * 搜索模板
   */
  static searchTemplates(query: string, filters?: {
    category?: string
    tags?: string[]
    author?: string
    isPublic?: boolean
  }): GenerationTemplate[] {
    let templates = this.getAllTemplates()

    // 应用过滤器
    if (filters) {
      if (filters.category) {
        templates = templates.filter(t => t.category === filters.category)
      }
      if (filters.tags && filters.tags.length > 0) {
        templates = templates.filter(t => 
          filters.tags!.some(tag => t.metadata.tags.includes(tag))
        )
      }
      if (filters.author) {
        templates = templates.filter(t => t.metadata.author === filters.author)
      }
      if (filters.isPublic !== undefined) {
        templates = templates.filter(t => t.metadata.isPublic === filters.isPublic)
      }
    }

    // 应用搜索查询
    if (query.trim()) {
      const searchTerm = query.toLowerCase()
      templates = templates.filter(template =>
        template.name.toLowerCase().includes(searchTerm) ||
        template.description.toLowerCase().includes(searchTerm) ||
        template.metadata.tags.some(tag => tag.toLowerCase().includes(searchTerm))
      )
    }

    return templates
  }

  /**
   * 获取模板分类
   */
  static getTemplateCategories(): TemplateCategory[] {
    try {
      const stored = localStorage.getItem(this.CATEGORIES_KEY)
      const categories = stored ? JSON.parse(stored) : this.getDefaultCategories()
      
      // 更新模板数量
      const templates = this.getAllTemplates()
      return categories.map((category: TemplateCategory) => ({
        ...category,
        templateCount: templates.filter(t => t.category === category.id).length
      }))
    } catch (error) {
      console.error('获取分类失败:', error)
      return this.getDefaultCategories()
    }
  }

  /**
   * 导出模板
   */
  static exportTemplate(id: string): void {
    const template = this.getTemplateById(id)
    if (!template) {
      message.error('模板不存在')
      return
    }

    try {
      const exportData = {
        ...template,
        exportedAt: dayjs().toISOString(),
        exportVersion: '1.0'
      }

      const blob = new Blob([JSON.stringify(exportData, null, 2)], {
        type: 'application/json'
      })
      
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = `${template.name.replace(/[^a-zA-Z0-9]/g, '_')}_template.json`
      
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      URL.revokeObjectURL(url)
      
      message.success('模板已导出')
    } catch (error) {
      message.error('导出失败')
      console.error('导出模板失败:', error)
    }
  }

  /**
   * 导入模板
   */
  static async importTemplate(file: File): Promise<GenerationTemplate | null> {
    try {
      const text = await file.text()
      const importData = JSON.parse(text)
      
      // 验证模板格式
      if (!this.validateTemplateFormat(importData)) {
        message.error('模板格式无效')
        return null
      }

      // 生成新ID避免冲突
      const template: GenerationTemplate = {
        ...importData,
        id: this.generateId(),
        metadata: {
          ...importData.metadata,
          createdAt: dayjs().toISOString(),
          updatedAt: dayjs().toISOString()
        }
      }

      const templates = this.getAllTemplates()
      templates.push(template)
      this.saveTemplates(templates)
      
      message.success(`模板 "${template.name}" 导入成功`)
      return template
    } catch (error) {
      message.error('导入失败：文件格式错误')
      console.error('导入模板失败:', error)
      return null
    }
  }

  /**
   * 更新模板统计
   */
  static updateTemplateStats(id: string, statsUpdate: Partial<GenerationTemplate['statistics']>): boolean {
    const templates = this.getAllTemplates()
    const index = templates.findIndex(template => template.id === id)
    
    if (index === -1) return false

    templates[index].statistics = {
      ...templates[index].statistics!,
      ...statsUpdate
    }

    this.saveTemplates(templates)
    return true
  }

  /**
   * 增加使用次数
   */
  static incrementUsageCount(id: string): void {
    const template = this.getTemplateById(id)
    if (template && template.statistics) {
      this.updateTemplateStats(id, {
        usageCount: template.statistics.usageCount + 1
      })
    }
  }

  /**
   * 私有方法：保存模板到localStorage
   */
  private static saveTemplates(templates: GenerationTemplate[]): void {
    try {
      localStorage.setItem(this.STORAGE_KEY, JSON.stringify(templates))
    } catch (error) {
      message.error('保存模板失败：存储空间不足')
      console.error('保存模板失败:', error)
    }
  }

  /**
   * 私有方法：生成唯一ID
   */
  private static generateId(): string {
    return `template_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  /**
   * 私有方法：获取默认分类
   */
  private static getDefaultCategories(): TemplateCategory[] {
    return [
      {
        id: 'user_data',
        name: '用户数据',
        description: '用户信息、个人资料等相关数据模板',
        icon: 'UserOutlined',
        templateCount: 0
      },
      {
        id: 'business_data',
        name: '业务数据',
        description: '订单、产品、交易等业务相关数据模板',
        icon: 'ShoppingOutlined',
        templateCount: 0
      },
      {
        id: 'financial_data',
        name: '金融数据',
        description: '银行、支付、财务等金融相关数据模板',
        icon: 'BankOutlined',
        templateCount: 0
      },
      {
        id: 'testing_data',
        name: '测试数据',
        description: '软件测试、性能测试等测试用数据模板',
        icon: 'BugOutlined',
        templateCount: 0
      },
      {
        id: 'demo_data',
        name: '演示数据',
        description: '产品演示、培训等场景用数据模板',
        icon: 'PlayCircleOutlined',
        templateCount: 0
      }
    ]
  }

  /**
   * 私有方法：验证模板格式
   */
  private static validateTemplateFormat(data: any): boolean {
    const requiredFields = ['name', 'description', 'category', 'fields', 'generationConfig']
    return requiredFields.every(field => field in data) &&
           Array.isArray(data.fields) &&
           typeof data.generationConfig === 'object'
  }
}