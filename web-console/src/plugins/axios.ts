/**
 * Axios HTTP客户端配置
 * 包含请求拦截器、响应拦截器和错误处理
 */

import axios, { type AxiosInstance, type InternalAxiosRequestConfig, type AxiosResponse } from 'axios'
import { message, notification } from 'ant-design-vue'
import { API_BASE_URL, STORAGE_KEYS } from '@/config'
import type { ApiResponse } from '@/utils/types'

// 环境变量配置
const DATAFORGE_API_URL = import.meta.env.VITE_DATAFORGE_API_URL || API_BASE_URL

// DataForge API 专用的axios实例
const dataforgeClient: AxiosInstance = axios.create({
  baseURL: DATAFORGE_API_URL,
  timeout: 60000, // DataForge API 可能需要更长时间处理大量数据
  headers: {
    'Content-Type': 'application/json'
  }
})

// 认证 API 的axios实例（暂时使用模拟响应）
const authClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL + '/api/auth',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 创建默认axios实例（指向DataForge API）
const httpClient: AxiosInstance = dataforgeClient

// DataForge API 请求拦截器
dataforgeClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加请求时间戳（防止缓存）
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    return config
  },
  (error) => {
    console.error('DataForge API 请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// 认证 API 请求拦截器
authClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 添加认证token
    const token = localStorage.getItem(STORAGE_KEYS.USER_TOKEN)
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 添加请求时间戳（防止缓存）
    if (config.method === 'get') {
      config.params = {
        ...config.params,
        _t: Date.now()
      }
    }
    
    return config
  },
  (error) => {
    console.error('认证 API 请求拦截器错误:', error)
    return Promise.reject(error)
  }
)

// DataForge API 响应拦截器
dataforgeClient.interceptors.response.use(
  (response: AxiosResponse) => {
    const { data } = response
    
    // DataForge API 不使用统一的 ApiResponse 格式，直接返回数据
    // 但我们需要包装成统一格式以兼容现有代码
    if (data && typeof data === 'object') {
      if (data.success !== undefined) {
        // 如果已经包含 success 字段，直接返回
        return response
      } else {
        // 包装为统一的 ApiResponse 格式
        response.data = {
          success: true,
          data: data,
          message: '请求成功'
        }
      }
    }
    
    return response
  },
  (error) => {
    console.error('DataForge API 响应拦截器错误:', error)
    return handleApiError(error, 'DataForge API')
  }
)

// 认证 API 响应拦截器
authClient.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    const { data } = response
    
    // 统一处理业务错误
    if (!data.success) {
      const errorMessage = data.message || '请求失败'
      message.error(errorMessage)
      return Promise.reject(new Error(errorMessage))
    }
    
    return response
  },
  (error) => {
    console.error('认证 API 响应拦截器错误:', error)
    return handleApiError(error, '认证 API')
  }
)

// 统一错误处理函数
function handleApiError(error: any, apiType: string = 'API') {
  // 处理HTTP状态码错误
  if (error.response) {
    const { status, data } = error.response
    
    switch (status) {
      case 401:
        // 未授权，清除token并跳转到登录页
        if (apiType === '认证 API') {
          localStorage.removeItem(STORAGE_KEYS.USER_TOKEN)
          localStorage.removeItem(STORAGE_KEYS.USER_INFO)
          window.location.href = '/login'
          message.error('登录已过期，请重新登录')
        } else {
          message.error('DataForge API 访问被拒绝')
        }
        break
        
      case 403:
        message.error(`没有权限访问该${apiType}资源`)
        break
        
      case 404:
        if (apiType === 'DataForge API') {
          message.error('请求的生成器不存在')
        } else {
          message.error('请求的资源不存在')
        }
        break
        
      case 422:
        // 表单验证错误
        if (data.errors) {
          const errorMessages = Object.values(data.errors).flat()
          errorMessages.forEach((msg: any) => message.error(msg))
        } else {
          message.error(data.message || data.detail || '数据验证失败')
        }
        break
        
      case 500:
        if (apiType === 'DataForge API') {
          message.error('DataForge 服务器内部错误')
          // 显示详细错误通知
          if (data?.detail) {
            notification.error({
              message: 'DataForge API 错误',
              description: data.detail,
              duration: 10
            })
          }
        } else {
          message.error('服务器内部错误')
        }
        break
        
      default:
        const errorMsg = data?.message || data?.detail || `${apiType}请求失败 (${status})`
        message.error(errorMsg)
    }
  } else if (error.request) {
    // 网络错误
    if (apiType === 'DataForge API') {
      message.error('无法连接到 DataForge 服务，请检查服务是否启动')
      notification.error({
        message: 'DataForge 连接失败',
        description: '请确保 DataForge API 服务正在运行（默认端口：8000）',
        duration: 15
      })
    } else {
      message.error('网络连接失败，请检查网络设置')
    }
  } else {
    // 其他错误
    message.error(`${apiType}请求配置错误`)
  }
  
  return Promise.reject(error)
}

// 封装常用的HTTP方法
export const http = {
  get: <T = any>(url: string, config?: any): Promise<ApiResponse<T>> => {
    return httpClient.get(url, config).then(res => res.data)
  },
  
  post: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return httpClient.post(url, data, config).then(res => res.data)
  },
  
  put: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return httpClient.put(url, data, config).then(res => res.data)
  },
  
  patch: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return httpClient.patch(url, data, config).then(res => res.data)
  },
  
  delete: <T = any>(url: string, config?: any): Promise<ApiResponse<T>> => {
    return httpClient.delete(url, config).then(res => res.data)
  },
  
  upload: <T = any>(url: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse<T>> => {
    const formData = new FormData()
    formData.append('file', file)
    
    return httpClient.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    }).then(res => res.data)
  }
}

// 认证 API 专用客户端
export const authHttp = {
  get: <T = any>(url: string, config?: any): Promise<ApiResponse<T>> => {
    return authClient.get(url, config).then(res => res.data)
  },
  
  post: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return authClient.post(url, data, config).then(res => res.data)
  },
  
  put: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return authClient.put(url, data, config).then(res => res.data)
  },
  
  patch: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return authClient.patch(url, data, config).then(res => res.data)
  },
  
  delete: <T = any>(url: string, config?: any): Promise<ApiResponse<T>> => {
    return authClient.delete(url, config).then(res => res.data)
  },
  
  upload: <T = any>(url: string, file: File, onProgress?: (progress: number) => void): Promise<ApiResponse<T>> => {
    const formData = new FormData()
    formData.append('file', file)
    
    return authClient.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress && progressEvent.total) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(progress)
        }
      }
    }).then(res => res.data)
  }
}

// DataForge API 专用客户端
export const dataforgeHttp = {
  get: <T = any>(url: string, config?: any): Promise<ApiResponse<T>> => {
    return dataforgeClient.get(url, config).then(res => res.data)
  },
  
  post: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return dataforgeClient.post(url, data, config).then(res => res.data)
  },
  
  put: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return dataforgeClient.put(url, data, config).then(res => res.data)
  },
  
  patch: <T = any>(url: string, data?: any, config?: any): Promise<ApiResponse<T>> => {
    return dataforgeClient.patch(url, data, config).then(res => res.data)
  },
  
  delete: <T = any>(url: string, config?: any): Promise<ApiResponse<T>> => {
    return dataforgeClient.delete(url, config).then(res => res.data)
  }
}

export default httpClient