/**
 * 用户认证状态管理
 * 管理登录状态、用户信息和认证相关操作
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '@/utils/types'
import { 
  AuthService, 
  type LoginRequest, 
  type RegisterRequest, 
  type UpdateProfileRequest,
  type ChangeEmailRequest 
} from '@/services/modules/auth'
import { STORAGE_KEYS } from '@/config'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const isLoggedIn = ref(false)
  const userToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const userInfo = ref<UserInfo | null>(null)
  const rememberMe = ref(false)
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => isLoggedIn.value && !!userToken.value)
  const userRole = computed(() => userInfo.value?.role || 'guest')
  const userName = computed(() => userInfo.value?.username || '')
  const userEmail = computed(() => userInfo.value?.email || '')

  // Actions
  const login = async (loginData: LoginRequest) => {
    try {
      loading.value = true
      
      const response = await AuthService.login(loginData)
      
      if (response.success && response.data) {
        const { user, token, refreshToken: newRefreshToken, expiresIn } = response.data
        
        // 更新状态
        userToken.value = token
        refreshToken.value = newRefreshToken
        userInfo.value = user
        isLoggedIn.value = true
        rememberMe.value = loginData.rememberMe || false
        
        // 持久化存储
        localStorage.setItem(STORAGE_KEYS.USER_TOKEN, token)
        localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(user))
        
        if (newRefreshToken) {
          localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, newRefreshToken)
        }
        
        if (rememberMe.value) {
          localStorage.setItem(STORAGE_KEYS.REMEMBER_ME, 'true')
        }
        
        // 设置token过期自动刷新
        scheduleTokenRefresh(expiresIn)
        
        return { success: true, message: '登录成功' }
      } else {
        return { success: false, message: response.message || '登录失败' }
      }
    } catch (error: any) {
      console.error('登录失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '登录失败，请检查网络连接' 
      }
    } finally {
      loading.value = false
    }
  }

  const register = async (registerData: RegisterRequest) => {
    try {
      loading.value = true
      
      const response = await AuthService.register(registerData)
      
      if (response.success && response.data) {
        const { user, token } = response.data
        
        // 更新状态
        userToken.value = token
        userInfo.value = user
        isLoggedIn.value = true
        
        // 持久化存储
        localStorage.setItem(STORAGE_KEYS.USER_TOKEN, token)
        localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(user))
        
        return { success: true, message: '注册成功' }
      } else {
        return { success: false, message: response.message || '注册失败' }
      }
    } catch (error: any) {
      console.error('注册失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '注册失败，请稍后重试' 
      }
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    try {
      // 调用后端登出接口
      if (userToken.value) {
        await AuthService.logout()
      }
    } catch (error) {
      console.error('登出请求失败:', error)
    } finally {
      // 清除本地状态
      clearAuthState()
    }
  }

  const clearAuthState = () => {
    isLoggedIn.value = false
    userToken.value = null
    refreshToken.value = null
    userInfo.value = null
    rememberMe.value = false
    
    // 清除本地存储
    localStorage.removeItem(STORAGE_KEYS.USER_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
    localStorage.removeItem(STORAGE_KEYS.USER_INFO)
    localStorage.removeItem(STORAGE_KEYS.REMEMBER_ME)
    
    // 清除token刷新定时器
    clearTokenRefreshTimer()
  }

  const refreshUserInfo = async () => {
    try {
      if (!userToken.value) return
      
      const response = await AuthService.getCurrentUser()
      
      if (response.success && response.data) {
        userInfo.value = response.data
        
        // 更新本地存储
        localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(response.data))
      }
    } catch (error) {
      console.error('刷新用户信息失败:', error)
      // 如果刷新失败，可能是token过期，执行登出
      await logout()
    }
  }

  const updateProfile = async (profileData: UpdateProfileRequest) => {
    try {
      loading.value = true
      
      const response = await AuthService.updateProfile(profileData)
      
      if (response.success && response.data) {
        userInfo.value = response.data.user
        localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(response.data.user))
        
        return { success: true, message: response.data.message || '个人资料更新成功' }
      } else {
        return { success: false, message: response.message || '更新失败' }
      }
    } catch (error: any) {
      console.error('更新个人资料失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '更新失败，请稍后重试' 
      }
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (oldPassword: string, newPassword: string, confirmPassword: string) => {
    try {
      loading.value = true
      
      const response = await AuthService.changePassword({
        oldPassword,
        newPassword,
        confirmPassword
      })
      
      if (response.success) {
        return { success: true, message: response.data?.message || '密码修改成功' }
      } else {
        return { success: false, message: response.message || '密码修改失败' }
      }
    } catch (error: any) {
      console.error('修改密码失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '密码修改失败，请检查原密码' 
      }
    } finally {
      loading.value = false
    }
  }

  const sendVerificationCode = async (email?: string, phone?: string, type: 'register' | 'reset_password' | 'change_phone' | 'change_email' = 'register') => {
    try {
      const response = await AuthService.sendVerificationCode({
        email,
        phone,
        type
      })
      
      if (response.success) {
        return { success: true, message: response.data?.message || '验证码已发送' }
      } else {
        return { success: false, message: response.message || '发送验证码失败' }
      }
    } catch (error: any) {
      console.error('发送验证码失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '发送验证码失败，请稍后重试' 
      }
    }
  }

  const resetPassword = async (email: string, verificationCode: string, newPassword: string, confirmPassword: string) => {
    try {
      loading.value = true
      
      const response = await AuthService.resetPassword({
        email,
        verificationCode,
        newPassword,
        confirmPassword
      })
      
      if (response.success) {
        return { success: true, message: response.data?.message || '密码重置成功' }
      } else {
        return { success: false, message: response.message || '密码重置失败' }
      }
    } catch (error: any) {
      console.error('重置密码失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '密码重置失败，请检查验证码' 
      }
    } finally {
      loading.value = false
    }
  }

  const checkAvailability = async (username?: string, email?: string) => {
    try {
      const response = await AuthService.checkAvailability({
        username,
        email
      })
      
      return response
    } catch (error: any) {
      console.error('检查可用性失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '检查失败' 
      }
    }
  }

  const uploadAvatar = async (file: File) => {
    try {
      loading.value = true
      
      const response = await AuthService.uploadAvatar(file)
      
      if (response.success && response.data) {
        // 更新用户头像URL
        if (userInfo.value) {
          userInfo.value = { ...userInfo.value, avatar: response.data.url }
          localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo.value))
        }
        
        return { success: true, message: response.data.message || '头像上传成功', url: response.data.url }
      } else {
        return { success: false, message: response.message || '头像上传失败' }
      }
    } catch (error: any) {
      console.error('上传头像失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '上传失败，请检查文件格式和大小' 
      }
    } finally {
      loading.value = false
    }
  }

  const changeEmail = async (newEmail: string, verificationCode: string, password: string) => {
    try {
      loading.value = true
      
      const response = await AuthService.changeEmail({
        newEmail,
        verificationCode,
        password
      })
      
      if (response.success) {
        // 更新用户邮箱
        if (userInfo.value) {
          userInfo.value = { ...userInfo.value, email: newEmail }
          localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo.value))
        }
        
        return { success: true, message: response.data?.message || '邮箱修改成功' }
      } else {
        return { success: false, message: response.message || '邮箱修改失败' }
      }
    } catch (error: any) {
      console.error('修改邮箱失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '修改失败，请检查验证码和密码' 
      }
    } finally {
      loading.value = false
    }
  }

  const bindPhone = async (phone: string, verificationCode: string) => {
    try {
      loading.value = true
      
      const response = await AuthService.bindPhone({
        phone,
        verificationCode
      })
      
      if (response.success) {
        // 更新用户手机号
        if (userInfo.value) {
          userInfo.value = { ...userInfo.value, phone }
          localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo.value))
        }
        
        return { success: true, message: response.data?.message || '手机号绑定成功' }
      } else {
        return { success: false, message: response.message || '绑定失败' }
      }
    } catch (error: any) {
      console.error('绑定手机号失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '绑定失败，请检查验证码' 
      }
    } finally {
      loading.value = false
    }
  }

  const unbindPhone = async (password: string, verificationCode: string) => {
    try {
      loading.value = true
      
      const response = await AuthService.unbindPhone({
        password,
        verificationCode
      })
      
      if (response.success) {
        // 清除用户手机号
        if (userInfo.value) {
          userInfo.value = { ...userInfo.value, phone: undefined }
          localStorage.setItem(STORAGE_KEYS.USER_INFO, JSON.stringify(userInfo.value))
        }
        
        return { success: true, message: response.data?.message || '手机号解绑成功' }
      } else {
        return { success: false, message: response.message || '解绑失败' }
      }
    } catch (error: any) {
      console.error('解绑手机号失败:', error)
      return { 
        success: false, 
        message: error.response?.data?.message || '解绑失败，请检查密码和验证码' 
      }
    } finally {
      loading.value = false
    }
  }

  // Token 刷新相关
  let refreshTimer: NodeJS.Timeout | null = null

  const scheduleTokenRefresh = (expiresIn: number) => {
    clearTokenRefreshTimer()
    
    // 在token过期前5分钟刷新
    const refreshTime = Math.max(expiresIn - 5 * 60 * 1000, 60 * 1000)
    
    refreshTimer = setTimeout(() => {
      if (refreshToken.value) {
        refreshAuthToken()
      }
    }, refreshTime)
  }

  const clearTokenRefreshTimer = () => {
    if (refreshTimer) {
      clearTimeout(refreshTimer)
      refreshTimer = null
    }
  }

  const refreshAuthToken = async () => {
    try {
      if (!refreshToken.value) {
        await logout()
        return
      }
      
      const response = await AuthService.refreshToken(refreshToken.value)
      
      if (response.success && response.data) {
        const { token, expiresIn } = response.data
        
        userToken.value = token
        localStorage.setItem(STORAGE_KEYS.USER_TOKEN, token)
        
        // 继续调度下次刷新
        scheduleTokenRefresh(expiresIn)
      } else {
        // 刷新失败，执行登出
        await logout()
      }
    } catch (error) {
      console.error('刷新token失败:', error)
      await logout()
    }
  }

  // 初始化时从本地存储恢复状态
  const initializeAuth = () => {
    const token = localStorage.getItem(STORAGE_KEYS.USER_TOKEN)
    const refresh = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
    const user = localStorage.getItem(STORAGE_KEYS.USER_INFO)
    const remember = localStorage.getItem(STORAGE_KEYS.REMEMBER_ME)
    
    if (token && user) {
      userToken.value = token
      refreshToken.value = refresh
      userInfo.value = JSON.parse(user)
      isLoggedIn.value = true
      rememberMe.value = remember === 'true'
      
      // 验证token是否有效
      refreshUserInfo().catch(() => {
        clearAuthState()
      })
    }
  }

  return {
    // 状态
    isLoggedIn,
    userToken,
    refreshToken,
    userInfo,
    rememberMe,
    loading,
    
    // 计算属性
    isAuthenticated,
    userRole,
    userName,
    userEmail,
    
    // 方法
    login,
    register,
    logout,
    refreshUserInfo,
    updateProfile,
    changePassword,
    sendVerificationCode,
    resetPassword,
    checkAvailability,
    uploadAvatar,
    changeEmail,
    bindPhone,
    unbindPhone,
    refreshAuthToken,
    initializeAuth,
    clearAuthState
  }
}, {
  persist: {
    key: 'dataforge_auth',
    storage: localStorage,
    paths: ['isLoggedIn', 'userToken', 'refreshToken', 'userInfo', 'rememberMe']
  }
})




















