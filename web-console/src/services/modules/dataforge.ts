/**
 * DataForge API 服务
 * 连接后端数据生成服务
 */

import { dataforgeHttp } from '@/plugins/axios'
import type { ApiResponse } from '@/utils/types'

// DataForge API 接口定义
export interface GeneratorInfo {
  name: string
  type: string
  parameters: string[]
  description: string
  example_parameters?: Record<string, any>
}

export interface GeneratorRequest {
  generator_type: string
  count: number
  parameters: Record<string, any>
  should_validate?: boolean
  output_format?: string
}

export interface BatchGeneratorRequest {
  generators: Array<{
    generator_type: string
    parameters: Record<string, any>
    should_validate?: boolean
  }>
  count: number
  output_format?: string
}

export interface GenerationResult {
  success: boolean
  generator_type: string
  count: number
  data: Array<Record<string, any>>
  timestamp: string
  format?: string
}

export interface BatchGenerationResult {
  success: boolean
  generators: string[]
  count: number
  data: Array<Record<string, any>>
  timestamp: string
}

export interface TaskInfo {
  task_id: string
  status: 'pending' | 'running' | 'completed' | 'failed'
  created_at: string
  generator_type: string
  count: number
  progress: number
  result?: GenerationResult
  error?: string
}

export interface HealthStatus {
  status: string
  timestamp: string
  version: string
  generators_count: number
}

/**
 * DataForge API 服务类
 */
export class DataForgeService {
  /**
   * 健康检查
   */
  static async healthCheck(): Promise<ApiResponse<HealthStatus>> {
    return dataforgeHttp.get<HealthStatus>('/health')
  }

  /**
   * 获取所有可用生成器列表
   */
  static async getGenerators(): Promise<ApiResponse<GeneratorInfo[]>> {
    return dataforgeHttp.get<GeneratorInfo[]>('/generators')
  }

  /**
   * 获取指定生成器的详细信息
   */
  static async getGeneratorInfo(generatorName: string): Promise<ApiResponse<GeneratorInfo>> {
    return dataforgeHttp.get<GeneratorInfo>(`/generators/${generatorName}`)
  }

  /**
   * 生成单一类型数据
   */
  static async generateData(
    generatorName: string, 
    request: Omit<GeneratorRequest, 'generator_type'>
  ): Promise<ApiResponse<GenerationResult>> {
    return dataforgeHttp.post<GenerationResult>(`/generate/${generatorName}`, {
      ...request,
      generator_type: generatorName
    })
  }

  /**
   * 批量生成多种类型的关联数据
   */
  static async generateBatchData(request: BatchGeneratorRequest): Promise<ApiResponse<BatchGenerationResult>> {
    return dataforgeHttp.post<BatchGenerationResult>('/batch/generate', request)
  }

  /**
   * 异步生成数据（用于大量数据生成）
   */
  static async generateDataAsync(
    generatorName: string,
    request: Omit<GeneratorRequest, 'generator_type'>
  ): Promise<ApiResponse<TaskInfo>> {
    return dataforgeHttp.post<TaskInfo>(`/generate/async/${generatorName}`, {
      ...request,
      generator_type: generatorName
    })
  }

  /**
   * 获取异步任务状态
   */
  static async getTaskStatus(taskId: string): Promise<ApiResponse<TaskInfo>> {
    return dataforgeHttp.get<TaskInfo>(`/tasks/${taskId}`)
  }

  /**
   * 获取任务列表
   */
  static async getTasks(options?: {
    status?: string
    limit?: number
  }): Promise<ApiResponse<{
    total: number
    filtered: number
    tasks: TaskInfo[]
  }>> {
    const params = new URLSearchParams()
    if (options?.status) {
      params.append('status', options.status)
    }
    if (options?.limit) {
      params.append('limit', options.limit.toString())
    }
    
    const queryString = params.toString()
    return dataforgeHttp.get<{
      total: number
      filtered: number
      tasks: TaskInfo[]
    }>(`/tasks${queryString ? `?${queryString}` : ''}`)
  }

  /**
   * 检查 DataForge API 连接状态
   */
  static async checkConnection(): Promise<{ connected: boolean; message: string; health?: HealthStatus }> {
    try {
      const response = await this.healthCheck()
      if (response.success && response.data) {
        return {
          connected: true,
          message: 'DataForge API 连接正常',
          health: response.data
        }
      } else {
        return {
          connected: false,
          message: 'DataForge API 响应异常'
        }
      }
    } catch (error: any) {
      return {
        connected: false,
        message: `DataForge API 连接失败: ${error.message || '未知错误'}`
      }
    }
  }

  /**
   * 获取生成器分类
   */
  static async getGeneratorCategories(): Promise<ApiResponse<Record<string, GeneratorInfo[]>>> {
    try {
      const response = await this.getGenerators()
      if (response.success && response.data) {
        const categories: Record<string, GeneratorInfo[]> = {
          '基础数据': [],
          '身份信息': [],
          '联系方式': [],
          '数值生成': [],
          '文本生成': [],
          '日期时间': [],
          '网络信息': [],
          '其他': []
        }

        response.data.forEach(generator => {
          const name = generator.name.toLowerCase()
          if (['name', 'idcard', 'gender'].some(keyword => name.includes(keyword))) {
            categories['身份信息'].push(generator)
          } else if (['email', 'phone', 'address'].some(keyword => name.includes(keyword))) {
            categories['联系方式'].push(generator)
          } else if (['integer', 'float', 'number'].some(keyword => name.includes(keyword))) {
            categories['数值生成'].push(generator)
          } else if (['string', 'text', 'word'].some(keyword => name.includes(keyword))) {
            categories['文本生成'].push(generator)
          } else if (['date', 'time', 'datetime'].some(keyword => name.includes(keyword))) {
            categories['日期时间'].push(generator)
          } else if (['ip', 'url', 'domain', 'mac'].some(keyword => name.includes(keyword))) {
            categories['网络信息'].push(generator)
          } else if (['uuid', 'id'].some(keyword => name.includes(keyword))) {
            categories['基础数据'].push(generator)
          } else {
            categories['其他'].push(generator)
          }
        })

        return {
          success: true,
          data: categories,
          message: '生成器分类获取成功'
        }
      } else {
        return {
          success: false,
          message: '获取生成器列表失败',
          data: {}
        }
      }
    } catch (error: any) {
      return {
        success: false,
        message: `分类生成器失败: ${error.message}`,
        data: {}
      }
    }
  }
}