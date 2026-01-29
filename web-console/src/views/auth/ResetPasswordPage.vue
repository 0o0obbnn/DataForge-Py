<template>
  <div class="reset-password-page">
    <div class="reset-container">
      <div class="reset-card">
        <h1 class="reset-title">重置密码</h1>
        <p class="reset-subtitle">请输入您的邮箱，我们将发送重置密码的验证码</p>

        <!-- 步骤指示器 -->
        <a-steps :current="currentStep" size="small" class="reset-steps">
          <a-step title="验证邮箱" />
          <a-step title="重置密码" />
          <a-step title="完成" />
        </a-steps>

        <!-- 步骤1: 验证邮箱 -->
        <div v-if="currentStep === 0" class="step-content">
          <a-form
            ref="emailFormRef"
            :model="emailForm"
            @finish="handleEmailSubmit"
          >
            <a-form-item
              name="email"
              :rules="emailRules"
            >
              <a-input
                v-model:value="emailForm.email"
                placeholder="请输入您的注册邮箱"
                size="large"
                :disabled="loading"
              >
                <template #prefix>
                  <MailOutlined />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item>
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                block
                :loading="loading"
              >
                <SendOutlined />
                发送验证码
              </a-button>
            </a-form-item>
          </a-form>
        </div>

        <!-- 步骤2: 重置密码 -->
        <div v-if="currentStep === 1" class="step-content">
          <a-form
            ref="resetFormRef"
            :model="resetForm"
            @finish="handleResetSubmit"
          >
            <a-form-item>
              <a-input
                :value="emailForm.email"
                disabled
                size="large"
              >
                <template #prefix>
                  <MailOutlined />
                </template>
              </a-input>
            </a-form-item>

            <a-form-item
              name="verificationCode"
              :rules="codeRules"
            >
              <div class="verification-input">
                <a-input
                  v-model:value="resetForm.verificationCode"
                  placeholder="请输入6位验证码"
                  size="large"
                  :disabled="loading"
                  maxlength="6"
                >
                  <template #prefix>
                    <SafetyOutlined />
                  </template>
                </a-input>
                <a-button
                  :loading="codeLoading"
                  :disabled="codeCountdown > 0"
                  @click="resendCode"
                  size="large"
                  class="resend-button"
                >
                  {{ codeCountdown > 0 ? `${codeCountdown}s` : '重新发送' }}
                </a-button>
              </div>
            </a-form-item>

            <a-form-item
              name="newPassword"
              :rules="passwordRules"
            >
              <a-input-password
                v-model:value="resetForm.newPassword"
                placeholder="请输入新密码"
                size="large"
                :disabled="loading"
                @input="handlePasswordInput"
              >
                <template #prefix>
                  <LockOutlined />
                </template>
              </a-input-password>

              <!-- 密码强度指示器 -->
              <div v-if="resetForm.newPassword" class="password-strength">
                <div class="strength-bar">
                  <div
                    class="strength-level"
                    :class="passwordStrength.level"
                    :style="{ width: passwordStrength.width }"
                  ></div>
                </div>
                <span class="strength-text">{{ passwordStrength.text }}</span>
              </div>
            </a-form-item>

            <a-form-item
              name="confirmPassword"
              :rules="confirmPasswordRules"
            >
              <a-input-password
                v-model:value="resetForm.confirmPassword"
                placeholder="请再次输入新密码"
                size="large"
                :disabled="loading"
              >
                <template #prefix>
                  <LockOutlined />
                </template>
              </a-input-password>
            </a-form-item>

            <a-form-item>
              <a-space>
                <a-button @click="goBack" size="large">
                  <ArrowLeftOutlined />
                  返回上一步
                </a-button>
                <a-button
                  type="primary"
                  html-type="submit"
                  size="large"
                  :loading="loading"
                >
                  <CheckOutlined />
                  重置密码
                </a-button>
              </a-space>
            </a-form-item>
          </a-form>
        </div>

        <!-- 步骤3: 完成 -->
        <div v-if="currentStep === 2" class="step-content success-content">
          <div class="success-icon">
            <CheckCircleOutlined />
          </div>
          <h3>密码重置成功！</h3>
          <p>您的密码已成功重置，请使用新密码登录。</p>

          <a-button
            type="primary"
            size="large"
            @click="goToLogin"
            block
          >
            <LoginOutlined />
            前往登录
          </a-button>
        </div>

        <div class="back-to-login">
          <router-link to="/login">
            <ArrowLeftOutlined />
            返回登录页面
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'
import {
  MailOutlined,
  LockOutlined,
  SafetyOutlined,
  SendOutlined,
  ArrowLeftOutlined,
  CheckOutlined,
  LoginOutlined,
  CheckCircleOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, Rule } from 'ant-design-vue/lib/form'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const emailFormRef = ref<FormInstance>()
const resetFormRef = ref<FormInstance>()

// 状态
const currentStep = ref(0)
const loading = ref(false)
const codeLoading = ref(false)
const codeCountdown = ref(0)
let countdownTimer: NodeJS.Timeout | null = null

// 表单数据
const emailForm = reactive({
  email: ''
})

const resetForm = reactive({
  verificationCode: '',
  newPassword: '',
  confirmPassword: ''
})

// 密码强度计算
const passwordStrength = computed(() => {
  const password = resetForm.newPassword
  if (!password) return { level: '', width: '0%', text: '' }

  let score = 0

  // 长度评分
  if (password.length >= 8) score += 25
  else if (password.length >= 6) score += 15

  // 复杂度评分
  if (/[a-z]/.test(password)) score += 15
  if (/[A-Z]/.test(password)) score += 15
  if (/\d/.test(password)) score += 15
  if (/[!@#$%^&*(),.?":{}|<>]/.test(password)) score += 30

  if (score >= 80) return { level: 'strong', width: '100%', text: '强' }
  if (score >= 60) return { level: 'medium', width: '66%', text: '中' }
  if (score >= 30) return { level: 'weak', width: '33%', text: '弱' }
  return { level: 'very-weak', width: '20%', text: '太弱' }
})

// 验证规则
const emailRules: Rule[] = [
  { required: true, message: '请输入邮箱地址', trigger: 'blur' },
  { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
]

const codeRules: Rule[] = [
  { required: true, message: '请输入验证码', trigger: 'blur' },
  { len: 6, message: '验证码为6位数字', trigger: 'blur' },
  { pattern: /^\d{6}$/, message: '请输入有效的6位数字验证码', trigger: 'blur' }
]

const passwordRules: Rule[] = [
  { required: true, message: '请设置新密码', trigger: 'blur' },
  { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  { max: 50, message: '密码长度不能超过50位', trigger: 'blur' },
  {
    validator: (rule, value) => {
      if (!value) return Promise.resolve()
      if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(value)) {
        return Promise.reject('密码必须包含字母和数字')
      }
      return Promise.resolve()
    },
    trigger: 'blur'
  }
]

const confirmPasswordRules: Rule[] = [
  { required: true, message: '请确认新密码', trigger: 'blur' },
  {
    validator: (rule, value) => {
      if (value && value !== resetForm.newPassword) {
        return Promise.reject('两次输入的密码不一致')
      }
      return Promise.resolve()
    },
    trigger: 'blur'
  }
]

// 事件处理
const handleEmailSubmit = async () => {
  try {
    loading.value = true

    const result = await authStore.sendVerificationCode(
      emailForm.email,
      undefined,
      'reset_password'
    )

    if (result.success) {
      message.success(result.message)
      currentStep.value = 1
      startCountdown()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    message.error('发送验证码失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleResetSubmit = async () => {
  try {
    loading.value = true

    const result = await authStore.resetPassword(
      emailForm.email,
      resetForm.verificationCode,
      resetForm.newPassword,
      resetForm.confirmPassword
    )

    if (result.success) {
      message.success(result.message)
      currentStep.value = 2
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('重置密码失败:', error)
    message.error('重置密码失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handlePasswordInput = () => {
  if (resetForm.confirmPassword && resetForm.newPassword !== resetForm.confirmPassword) {
    resetFormRef.value?.validateFields(['confirmPassword'])
  }
}

const resendCode = async () => {
  try {
    codeLoading.value = true

    const result = await authStore.sendVerificationCode(
      emailForm.email,
      undefined,
      'reset_password'
    )

    if (result.success) {
      message.success(result.message)
      startCountdown()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('重新发送验证码失败:', error)
    message.error('重新发送验证码失败，请稍后重试')
  } finally {
    codeLoading.value = false
  }
}

const startCountdown = () => {
  codeCountdown.value = 60

  countdownTimer = setInterval(() => {
    codeCountdown.value--
    if (codeCountdown.value <= 0) {
      clearInterval(countdownTimer!)
    }
  }, 1000)
}

const goBack = () => {
  currentStep.value = 0
}

const goToLogin = () => {
  router.push('/login')
}

// 组件挂载时检查是否已登录
onMounted(() => {
  if (authStore.isAuthenticated) {
    router.replace('/workbench')
  }
})

// 组件卸载时清理定时器
onMounted(() => {
  return () => {
    if (countdownTimer) {
      clearInterval(countdownTimer)
    }
  }
})
</script>

<style scoped lang="less">
.reset-password-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--df-primary-bg);
  padding: var(--df-spacing-lg);
}

.reset-container {
  width: 100%;
  max-width: 480px;
}

.reset-card {
  background: var(--df-secondary-bg);
  border-radius: var(--df-radius-lg);
  padding: var(--df-spacing-xl);
  border: 1px solid var(--df-text-disabled);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.reset-title {
  color: var(--df-text-primary);
  text-align: center;
  font-size: var(--df-font-size-2xl);
  font-weight: 600;
  margin-bottom: var(--df-spacing-sm);
  background: linear-gradient(135deg, var(--df-accent-primary), var(--df-accent-success));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.reset-subtitle {
  color: var(--df-text-secondary);
  text-align: center;
  font-size: var(--df-font-size-sm);
  margin-bottom: var(--df-spacing-lg);
}

.reset-steps {
  margin-bottom: var(--df-spacing-xl);

  :deep(.ant-steps-item) {
    .ant-steps-item-title {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-sm);
    }

    &.ant-steps-item-active .ant-steps-item-title {
      color: var(--df-text-primary);
    }

    .ant-steps-item-icon {
      background: var(--df-primary-bg);
      border-color: var(--df-text-disabled);

      .ant-steps-icon {
        color: var(--df-text-secondary);
      }
    }

    &.ant-steps-item-active .ant-steps-item-icon {
      background: var(--df-accent-primary);
      border-color: var(--df-accent-primary);

      .ant-steps-icon {
        color: white;
      }
    }

    &.ant-steps-item-finish .ant-steps-item-icon {
      background: var(--df-accent-success);
      border-color: var(--df-accent-success);

      .ant-steps-icon {
        color: white;
      }
    }
  }

  :deep(.ant-steps-item-tail)::after {
    background: var(--df-text-disabled);
  }
}

.step-content {
  margin-bottom: var(--df-spacing-lg);
}

.success-content {
  text-align: center;
  padding: var(--df-spacing-lg) 0;

  .success-icon {
    font-size: 64px;
    color: var(--df-accent-success);
    margin-bottom: var(--df-spacing-lg);
  }

  h3 {
    color: var(--df-text-primary);
    font-size: var(--df-font-size-xl);
    margin-bottom: var(--df-spacing-md);
  }

  p {
    color: var(--df-text-secondary);
    margin-bottom: var(--df-spacing-xl);
  }
}

.verification-input {
  display: flex;
  gap: var(--df-spacing-sm);

  .resend-button {
    min-width: 100px;
    border-color: var(--df-accent-primary);
    color: var(--df-accent-primary);

    &:hover:not(:disabled) {
      border-color: var(--df-accent-success);
      color: var(--df-accent-success);
    }

    &:disabled {
      border-color: var(--df-text-disabled);
      color: var(--df-text-disabled);
      background: transparent;
    }
  }
}

.password-strength {
  margin-top: var(--df-spacing-xs);
  display: flex;
  align-items: center;
  gap: var(--df-spacing-sm);

  .strength-bar {
    flex: 1;
    height: 4px;
    background: var(--df-text-disabled);
    border-radius: 2px;
    overflow: hidden;

    .strength-level {
      height: 100%;
      transition: all 0.3s ease;

      &.very-weak {
        background: #FF5252;
      }

      &.weak {
        background: #FF9800;
      }

      &.medium {
        background: #FFC107;
      }

      &.strong {
        background: #00E676;
      }
    }
  }

  .strength-text {
    font-size: var(--df-font-size-xs);
    color: var(--df-text-secondary);
    min-width: 20px;
  }
}

.back-to-login {
  text-align: center;
  margin-top: var(--df-spacing-lg);

  a {
    color: var(--df-text-secondary);
    text-decoration: none;
    font-size: var(--df-font-size-sm);
    display: inline-flex;
    align-items: center;
    gap: var(--df-spacing-xs);

    &:hover {
      color: var(--df-accent-primary);
      text-decoration: underline;
    }
  }
}

:deep(.ant-form-item) {
  margin-bottom: var(--df-spacing-lg);

  .ant-form-item-explain {
    color: var(--df-accent-error);
  }
}

:deep(.ant-input-affix-wrapper) {
  background: var(--df-primary-bg);
  border-color: var(--df-text-disabled);

  &:hover, &:focus, &.ant-input-affix-wrapper-focused {
    border-color: var(--df-accent-primary);
    box-shadow: 0 0 0 2px rgba(142, 93, 255, 0.1);
  }

  .ant-input {
    background: transparent;
    color: var(--df-text-primary);

    &::placeholder {
      color: var(--df-text-secondary);
    }
  }

  .anticon {
    color: var(--df-text-secondary);
  }
}

:deep(.ant-btn-primary) {
  background: linear-gradient(135deg, var(--df-accent-primary), var(--df-accent-success));
  border: none;
  font-weight: 500;
  height: 44px;

  &:hover, &:focus {
    background: linear-gradient(135deg, #A855F7, #10B981);
    box-shadow: 0 4px 16px rgba(142, 93, 255, 0.3);
  }

  &.ant-btn-loading {
    background: var(--df-text-disabled) !important;
  }

  .anticon {
    margin-right: var(--df-spacing-xs);
  }
}

// 响应式设计
@media (max-width: 480px) {
  .reset-password-page {
    padding: var(--df-spacing-md);
  }

  .reset-card {
    padding: var(--df-spacing-lg);
  }

  .verification-input {
    flex-direction: column;

    .resend-button {
      width: 100%;
    }
  }

  :deep(.ant-space) {
    display: flex !important;
    flex-direction: column;
    width: 100%;

    .ant-btn {
      width: 100%;
    }
  }
}
</style>
