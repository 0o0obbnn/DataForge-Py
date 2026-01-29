/**
 * 认证相关 API 服务
 * 包含登录、注册、退出、密码重置等功能
 */

import { http } from '@/plugins/axios'
import type {
  UserInfo,
  LoginForm,
  RegisterForm,
  ApiResponse
} from '@/utils/types'

// 登录请求
export interface LoginRequest {
  username: string
  password: string
  rememberMe?: boolean
}

// 登录响应
export interface LoginResponse {
  user: UserInfo
  token: string
  refreshToken: string
  expiresIn: number
}

// 注册请求
export interface RegisterRequest {
  email: string
  username?: string
  phone?: string
  password: string
  confirmPassword: string
  verificationCode: string
  agreeTerms: boolean
}

// 注册响应
export interface RegisterResponse {
  user: UserInfo
  token: string
  message: string
}

// 密码重置请求
export interface ResetPasswordRequest {
  email: string
  verificationCode: string
  newPassword: string
  confirmPassword: string
}

// 发送验证码请求
export interface SendCodeRequest {
  email?: string
  phone?: string
  type: 'register' | 'reset_password' | 'change_phone' | 'change_email'
}

// 更新个人资料请求
export interface UpdateProfileRequest {
  nickname?: string
  avatar?: string
  phone?: string
}

// 更新个人资料响应
export interface UpdateProfileResponse {
  user: UserInfo
  message: string
}

// 修改邮箱请求
export interface ChangeEmailRequest {
  newEmail: string
  verificationCode: string
  password: string
}

// 头像上传响应
export interface UploadAvatarResponse {
  url: string
  message: string
}

/**
 * 认证 API 服务类
 */
export class AuthService {
  /**
   * 用户登录
   */
  static async login(data: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    return http.post<LoginResponse>('/auth/login', data)
  }

  /**
   * 用户注册
   */
  static async register(data: RegisterRequest): Promise<ApiResponse<RegisterResponse>> {
    return http.post<RegisterResponse>('/auth/register', data)
  }

  /**
   * 用户退出
   */
  static async logout(): Promise<ApiResponse<null>> {
    return http.post<null>('/auth/logout')
  }

  /**
   * 刷新 Token
   */
  static async refreshToken(refreshToken: string): Promise<ApiResponse<{ token: string; expiresIn: number }>> {
    return http.post<{ token: string; expiresIn: number }>('/auth/refresh', {
      refreshToken
    })
  }

  /**
   * 发送验证码
   */
  static async sendVerificationCode(data: SendCodeRequest): Promise<ApiResponse<{ message: string }>> {
    return http.post<{ message: string }>('/auth/send-code', data)
  }

  /**
   * 验证验证码
   */
  static async verifyCode(code: string, email?: string, phone?: string): Promise<ApiResponse<{ valid: boolean }>> {
    return http.post<{ valid: boolean }>('/auth/verify-code', {
      code,
      email,
      phone
    })
  }

  /**
   * 重置密码
   */
  static async resetPassword(data: ResetPasswordRequest): Promise<ApiResponse<{ message: string }>> {
    return http.post<{ message: string }>('/auth/reset-password', data)
  }

  /**
   * 修改密码
   */
  static async changePassword(data: {
    oldPassword: string
    newPassword: string
    confirmPassword: string
  }): Promise<ApiResponse<{ message: string }>> {
    return http.put<{ message: string }>('/auth/change-password', data)
  }

  /**
   * 获取当前用户信息
   */
  static async getCurrentUser(): Promise<ApiResponse<UserInfo>> {
    return http.get<UserInfo>('/auth/me')
  }

  /**
   * 检查用户名/邮箱是否可用
   */
  static async checkAvailability(data: {
    username?: string
    email?: string
  }): Promise<ApiResponse<{ available: boolean; field: string }>> {
    return http.post<{ available: boolean; field: string }>('/auth/check-availability', data)
  }

  /**
   * 更新个人资料
   */
  static async updateProfile(data: UpdateProfileRequest): Promise<ApiResponse<UpdateProfileResponse>> {
    return http.put<UpdateProfileResponse>('/auth/profile', data)
  }

  /**
   * 上传头像
   */
  static async uploadAvatar(file: File): Promise<ApiResponse<UploadAvatarResponse>> {
    const formData = new FormData()
    formData.append('avatar', file)

    return http.post<UploadAvatarResponse>('/auth/upload-avatar', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
  }

  /**
   * 修改邮箱
   */
  static async changeEmail(data: ChangeEmailRequest): Promise<ApiResponse<{ message: string }>> {
    return http.put<{ message: string }>('/auth/change-email', data)
  }

  /**
   * 绑定手机号
   */
  static async bindPhone(data: {
    phone: string
    verificationCode: string
  }): Promise<ApiResponse<{ message: string }>> {
    return http.put<{ message: string }>('/auth/bind-phone', data)
  }

  /**
   * 解绑手机号
   */
  static async unbindPhone(data: {
    password: string
    verificationCode: string
  }): Promise<ApiResponse<{ message: string }>> {
    return http.delete<{ message: string }>('/auth/unbind-phone', { data })
  }
}
