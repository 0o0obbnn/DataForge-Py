/**
 * 全局配置文件
 * 包含API基础URL、应用配置等
 */

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export const APP_CONFIG = {
  name: 'DataForge Web Console',
  version: '1.0.0',
  description: '数据生成工具Web控制台',
  author: 'DataForge Team'
} as const

export const ROUTES = {
  LOGIN: '/login',
  REGISTER: '/register',
  PROFILE: '/profile',
  WORKBENCH: '/workbench',
  TEMPLATES: '/templates',
  API: '/api'
} as const

export const STORAGE_KEYS = {
  USER_TOKEN: 'user_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info',
  REMEMBER_ME: 'remember_me'
} as const
