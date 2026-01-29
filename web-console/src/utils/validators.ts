/**
 * 前端验证函数
 */

import { VALIDATION_RULES } from '@/config/constants'

/**
 * 验证邮箱格式
 */
export function validateEmail(email: string): boolean {
  return VALIDATION_RULES.EMAIL.test(email)
}

/**
 * 验证手机号格式
 */
export function validatePhone(phone: string): boolean {
  return VALIDATION_RULES.PHONE.test(phone)
}

/**
 * 验证身份证号格式
 */
export function validateIdCard(idCard: string): boolean {
  return VALIDATION_RULES.ID_CARD.test(idCard)
}

/**
 * 验证密码强度
 */
export function validatePassword(password: string): {
  isValid: boolean
  strength: 'weak' | 'medium' | 'strong'
  message: string
} {
  if (password.length < 8) {
    return {
      isValid: false,
      strength: 'weak',
      message: '密码长度至少8位'
    }
  }

  let score = 0
  const checks = {
    length: password.length >= 8,
    lowercase: /[a-z]/.test(password),
    uppercase: /[A-Z]/.test(password),
    number: /\d/.test(password),
    special: /[!@#$%^&*(),.?":{}|<>]/.test(password)
  }

  Object.values(checks).forEach(check => {
    if (check) score++
  })

  if (score < 3) {
    return {
      isValid: false,
      strength: 'weak',
      message: '密码强度太弱，请包含大小写字母、数字和特殊字符'
    }
  } else if (score < 5) {
    return {
      isValid: true,
      strength: 'medium',
      message: '密码强度中等'
    }
  } else {
    return {
      isValid: true,
      strength: 'strong',
      message: '密码强度很强'
    }
  }
}

/**
 * 验证确认密码
 */
export function validateConfirmPassword(password: string, confirmPassword: string): boolean {
  return password === confirmPassword
}

/**
 * 验证必填字段
 */
export function validateRequired(value: any): boolean {
  if (typeof value === 'string') {
    return value.trim().length > 0
  }
  return value !== null && value !== undefined
}

/**
 * 验证数字范围
 */
export function validateNumberRange(value: number, min?: number, max?: number): boolean {
  if (min !== undefined && value < min) return false
  if (max !== undefined && value > max) return false
  return true
}

/**
 * 验证字符串长度
 */
export function validateStringLength(value: string, min?: number, max?: number): boolean {
  const length = value.length
  if (min !== undefined && length < min) return false
  if (max !== undefined && length > max) return false
  return true
}

/**
 * 验证URL格式
 */
export function validateUrl(url: string): boolean {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

/**
 * 验证JSON格式
 */
export function validateJson(jsonString: string): boolean {
  try {
    JSON.parse(jsonString)
    return true
  } catch {
    return false
  }
}

/**
 * 验证文件类型
 */
export function validateFileType(file: File, allowedTypes: string[]): boolean {
  const fileType = file.type
  const fileName = file.name
  const fileExtension = fileName.split('.').pop()?.toLowerCase()

  return allowedTypes.some(type =>
    fileType.includes(type) || (fileExtension && type.includes(fileExtension))
  )
}

/**
 * 验证文件大小
 */
export function validateFileSize(file: File, maxSizeInMB: number): boolean {
  const maxSizeInBytes = maxSizeInMB * 1024 * 1024
  return file.size <= maxSizeInBytes
}

/**
 * 验证数组长度
 */
export function validateArrayLength(array: any[], min?: number, max?: number): boolean {
  const length = array.length
  if (min !== undefined && length < min) return false
  if (max !== undefined && length > max) return false
  return true
}

/**
 * 验证对象是否为空
 */
export function validateObjectNotEmpty(obj: Record<string, any>): boolean {
  return Object.keys(obj).length > 0
}

/**
 * 验证是否为有效数字
 */
export function validateNumber(value: any): boolean {
  return !isNaN(Number(value)) && isFinite(Number(value))
}

/**
 * 验证是否为整数
 */
export function validateInteger(value: any): boolean {
  return Number.isInteger(Number(value))
}

/**
 * 验证是否为正数
 */
export function validatePositive(value: number): boolean {
  return value > 0
}

/**
 * 验证是否为非负数
 */
export function validateNonNegative(value: number): boolean {
  return value >= 0
}

/**
 * 验证百分比值
 */
export function validatePercentage(value: number): boolean {
  return value >= 0 && value <= 100
}

/**
 * 验证颜色值（十六进制）
 */
export function validateColor(color: string): boolean {
  return /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(color)
}

/**
 * 验证日期格式
 */
export function validateDate(dateString: string): boolean {
  const date = new Date(dateString)
  return !isNaN(date.getTime())
}

/**
 * 验证日期范围
 */
export function validateDateRange(startDate: string, endDate: string): boolean {
  const start = new Date(startDate)
  const end = new Date(endDate)
  return start <= end
}
