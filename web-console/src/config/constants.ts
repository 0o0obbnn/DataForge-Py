/**
 * 全局常量定义
 */

// 数据生成器类型
export const GENERATOR_TYPES = {
  BASIC_INFO: 'basic_info',
  IDENTIFIERS: 'identifiers',
  FINANCE: 'finance',
  AUTH: 'auth',
  DATETIME: 'datetime',
  MARITAL: 'marital'
} as const

// 输出格式
export const OUTPUT_FORMATS = {
  CSV: 'csv',
  JSON: 'json',
  XML: 'xml',
  SQL: 'sql'
} as const

// 用户角色
export const USER_ROLES = {
  ADMIN: 'admin',
  USER: 'user',
  GUEST: 'guest'
} as const

// 字段类型
export const FIELD_TYPES = {
  NAME: 'name',
  ID_CARD: 'id_card',
  PHONE: 'phone',
  EMAIL: 'email',
  BANK_CARD: 'bank_card',
  ADDRESS: 'address',
  DATE: 'date',
  NUMBER: 'number',
  PERCENTAGE: 'percentage',
  BOOLEAN: 'boolean'
} as const

// 验证规则
export const VALIDATION_RULES = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  PHONE: /^1[3-9]\d{9}$/,
  ID_CARD: /^[1-9]\d{5}(18|19|20)\d{2}((0[1-9])|(1[0-2]))(([0-2][1-9])|10|20|30|31)\d{3}[0-9Xx]$/
} as const

// 分页配置
export const PAGINATION = {
  DEFAULT_PAGE_SIZE: 10,
  PAGE_SIZE_OPTIONS: ['10', '20', '50', '100']
} as const

// 主题配置
export const THEME = {
  COLORS: {
    PRIMARY: '#8E5DFF',
    SUCCESS: '#00E676',
    WARNING: '#FFC107',
    ERROR: '#FF5252',
    BACKGROUND: '#1A1A2E',
    CARD_BACKGROUND: '#282845',
    TEXT_PRIMARY: '#E0E0E0',
    TEXT_SECONDARY: '#B0B0B0',
    BORDER: '#4A4A6D'
  }
} as const
