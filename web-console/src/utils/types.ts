/**
 * 全局TypeScript类型定义
 */

// 用户相关类型
export interface UserInfo {
  id: string
  username: string
  email: string
  phone?: string
  avatar?: string
  nickname?: string
  role: string
  createdAt: string
  updatedAt: string
}

export interface LoginForm {
  username: string
  password: string
  rememberMe?: boolean
}

export interface RegisterForm {
  email: string
  phone?: string
  password: string
  confirmPassword: string
  verificationCode: string
  agreeTerms: boolean
}

// 字段配置类型
export interface FieldConfig {
  id: string
  name: string
  type: string
  required: boolean
  minValue?: number
  maxValue?: number
  options?: string[]
  customRules?: string
  linkedField?: string
  relationRule?: string
  nullFrequency?: number
  boundaryStrategy?: string
}

export interface DataStructure {
  id: string
  name: string
  fields: FieldConfig[]
  createdAt: string
  updatedAt: string
}

// 模板相关类型
export interface Template {
  id: string
  name: string
  description: string
  creator: string
  createdAt: string
  updatedAt: string
  version: string
  isPublic: boolean
  dataStructure: DataStructure
}

export interface TemplateVersion {
  id: string
  templateId: string
  version: string
  description: string
  createdAt: string
  creator: string
  dataStructure: DataStructure
}

// API相关类型
export interface ApiKey {
  id: string
  key: string
  name: string
  isActive: boolean
  createdAt: string
  lastUsed?: string
}

export interface ApiCallLog {
  id: string
  templateId: string
  apiKey: string
  statusCode: number
  duration: number
  timestamp: string
  errorMessage?: string
}

// 生成配置类型
export interface GenerationConfig {
  count: number
  format: string
  formatOptions?: {
    csvDelimiter?: string
    jsonPrettyPrint?: boolean
    sqlTableName?: string
  }
}

// 响应类型
export interface ApiResponse<T = any> {
  success: boolean
  data: T
  message?: string
  code?: number
}

export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  pageSize: number
  totalPages: number
}

// 表单验证类型
export interface ValidationRule {
  required?: boolean
  min?: number
  max?: number
  pattern?: RegExp
  message?: string
  validator?: (value: any) => boolean | string
}

// 路由元信息类型
export interface RouteMeta {
  title?: string
  requiresAuth?: boolean
  roles?: string[]
  keepAlive?: boolean
}

// 组件Props类型
export interface BaseComponentProps {
  loading?: boolean
  disabled?: boolean
  size?: 'small' | 'middle' | 'large'
}

// 主题类型
export interface ThemeConfig {
  mode: 'light' | 'dark'
  primaryColor: string
  borderRadius: number
  fontSize: number
}
