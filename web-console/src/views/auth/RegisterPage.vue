<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-card">
        <h1 class="register-title">注册 DataForge</h1>
        <p class="register-subtitle">创建您的账户，开始您的数据生成之旅</p>

        <a-form
          ref="formRef"
          :model="registerForm"
          name="register"
          autocomplete="off"
          @finish="handleRegister"
          @finish-failed="handleRegisterFailed"
        >
          <!-- 邮箱 -->
          <a-form-item
            name="email"
            :rules="emailRules"
          >
            <a-input
              v-model:value="registerForm.email"
              placeholder="请输入邮箱地址"
              size="large"
              :disabled="loading"
              @blur="handleEmailBlur"
            >
              <template #prefix>
                <MailOutlined />
              </template>
              <template #suffix>
                <CheckCircleOutlined v-if="emailValid" style="color: #00E676" />
                <CloseCircleOutlined v-else-if="emailChecked" style="color: #FF5252" />
              </template>
            </a-input>
          </a-form-item>

          <!-- 手机号（可选） -->
          <a-form-item
            name="phone"
            :rules="phoneRules"
          >
            <a-input
              v-model:value="registerForm.phone"
              placeholder="请输入手机号（可选）"
              size="large"
              :disabled="loading"
            >
              <template #prefix>
                <PhoneOutlined />
              </template>
            </a-input>
          </a-form-item>

          <!-- 密码 -->
          <a-form-item
            name="password"
            :rules="passwordRules"
          >
            <a-input-password
              v-model:value="registerForm.password"
              placeholder="请设置登录密码"
              size="large"
              :disabled="loading"
              @input="handlePasswordInput"
            >
              <template #prefix>
                <LockOutlined />
              </template>
            </a-input-password>

            <!-- 密码强度指示器 -->
            <div v-if="registerForm.password" class="password-strength">
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

          <!-- 确认密码 -->
          <a-form-item
            name="confirmPassword"
            :rules="confirmPasswordRules"
          >
            <a-input-password
              v-model:value="registerForm.confirmPassword"
              placeholder="请再次输入密码"
              size="large"
              :disabled="loading"
            >
              <template #prefix>
                <LockOutlined />
              </template>
            </a-input-password>
          </a-form-item>

          <!-- 验证码 -->
          <a-form-item
            name="verificationCode"
            :rules="codeRules"
          >
            <div class="verification-input">
              <a-input
                v-model:value="registerForm.verificationCode"
                placeholder="请输入邮箱验证码"
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
                :disabled="!canSendCode || codeCountdown > 0"
                @click="sendVerificationCode"
                size="large"
                class="code-button"
              >
                {{ codeCountdown > 0 ? `${codeCountdown}s` : '发送验证码' }}
              </a-button>
            </div>
          </a-form-item>

          <!-- 服务条款 -->
          <a-form-item
            name="agreeTerms"
            :rules="[{ required: true, message: '请先同意用户协议和隐私政策' }]"
          >
            <a-checkbox v-model:checked="registerForm.agreeTerms" :disabled="loading">
              我已阅读并同意
              <a href="#" @click.prevent class="terms-link">《用户协议》</a>
              和
              <a href="#" @click.prevent class="terms-link">《隐私政策》</a>
            </a-checkbox>
          </a-form-item>

          <!-- 注册按钮 -->
          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              block
              :loading="loading"
              :disabled="!formValid"
            >
              <template v-if="!loading">
                <UserAddOutlined />
                立即注册
              </template>
              <template v-else>
                注册中...
              </template>
            </a-button>
          </a-form-item>
        </a-form>

        <div class="login-link">
          已有账户？
          <router-link to="/login">立即登录</router-link>
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
  PhoneOutlined,
  LockOutlined,
  SafetyOutlined,
  UserAddOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import { debounce } from 'lodash-es'
import type { FormInstance, Rule } from 'ant-design-vue/lib/form'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const formRef = ref<FormInstance>()

// 加载状态
const loading = ref(false)
const codeLoading = ref(false)

// 验证码倒计时
const codeCountdown = ref(0)
let countdownTimer: NodeJS.Timeout | null = null

// 邮箱验证状态
const emailValid = ref(false)
const emailChecked = ref(false)

// 表单数据
const registerForm = reactive({
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  verificationCode: '',
  agreeTerms: false
})

// 密码强度计算
const passwordStrength = computed(() => {
  const password = registerForm.password
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

// 表单验证状态
const formValid = computed(() => {
  return registerForm.email &&
         registerForm.password &&
         registerForm.confirmPassword &&
         registerForm.verificationCode &&
         registerForm.agreeTerms &&
         emailValid.value &&
         registerForm.password === registerForm.confirmPassword
})

// 是否可以发送验证码
const canSendCode = computed(() => {
  return registerForm.email && emailValid.value && !codeLoading.value
})

// 表单验证规则
const emailRules: Rule[] = [
  { required: true, message: '请输入邮箱地址', trigger: 'blur' },
  {
    type: 'email',
    message: '请输入有效的邮箱地址',
    trigger: 'blur'
  }
]

const phoneRules: Rule[] = [
  {
    pattern: /^1[3-9]\d{9}$/,
    message: '请输入有效的手机号',
    trigger: 'blur'
  }
]

const passwordRules: Rule[] = [
  { required: true, message: '请设置密码', trigger: 'blur' },
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
  { required: true, message: '请确认密码', trigger: 'blur' },
  {
    validator: (rule, value) => {
      if (value && value !== registerForm.password) {
        return Promise.reject('两次输入的密码不一致')
      }
      return Promise.resolve()
    },
    trigger: 'blur'
  }
]

const codeRules: Rule[] = [
  { required: true, message: '请输入验证码', trigger: 'blur' },
  { len: 6, message: '验证码为6位数字', trigger: 'blur' },
  { pattern: /^\d{6}$/, message: '请输入有效的6位数字验证码', trigger: 'blur' }
]

// 邮箱检查防抖
const debouncedEmailCheck = debounce(async (email: string) => {
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    emailValid.value = false
    emailChecked.value = false
    return
  }

  try {
    const result = await authStore.checkAvailability(undefined, email)
    if (result.success && result.data) {
      emailValid.value = result.data.available
      emailChecked.value = true
    } else {
      emailValid.value = false
      emailChecked.value = true
    }
  } catch (error) {
    console.error('检查邮箱可用性失败:', error)
    emailValid.value = false
    emailChecked.value = true
  }
}, 500)

// 事件处理
const handleEmailBlur = () => {
  if (registerForm.email) {
    debouncedEmailCheck(registerForm.email)
  }
}

const handlePasswordInput = () => {
  if (registerForm.confirmPassword && registerForm.password !== registerForm.confirmPassword) {
    formRef.value?.validateFields(['confirmPassword'])
  }
}

const sendVerificationCode = async () => {
  if (!canSendCode.value) return

  try {
    codeLoading.value = true

    const result = await authStore.sendVerificationCode(registerForm.email, undefined, 'register')

    if (result.success) {
      message.success(result.message)
      startCountdown()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    message.error('发送验证码失败，请稍后重试')
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

const handleRegister = async () => {
  try {
    loading.value = true

    const result = await authStore.register({
      email: registerForm.email.trim(),
      phone: registerForm.phone?.trim(),
      password: registerForm.password,
      confirmPassword: registerForm.confirmPassword,
      verificationCode: registerForm.verificationCode,
      agreeTerms: registerForm.agreeTerms
    })

    if (result.success) {
      message.success(result.message)

      // 注册成功后跳转到工作台
      await router.push('/workbench')
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('注册错误:', error)
    message.error('注册失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleRegisterFailed = (errorInfo: any) => {
  console.log('表单验证失败:', errorInfo)
  message.warning('请检查表单填写是否正确')
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
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--df-primary-bg);
  padding: var(--df-spacing-lg);
}

.register-container {
  width: 100%;
  max-width: 480px;
}

.register-card {
  background: var(--df-secondary-bg);
  border-radius: var(--df-radius-lg);
  padding: var(--df-spacing-xl);
  border: 1px solid var(--df-text-disabled);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.register-title {
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

.register-subtitle {
  color: var(--df-text-secondary);
  text-align: center;
  font-size: var(--df-font-size-sm);
  margin-bottom: var(--df-spacing-xl);
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

.verification-input {
  display: flex;
  gap: var(--df-spacing-sm);

  .code-button {
    min-width: 120px;
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

.terms-link {
  color: var(--df-accent-primary);
  text-decoration: none;

  &:hover {
    color: var(--df-accent-success);
    text-decoration: underline;
  }
}

.login-link {
  text-align: center;
  margin-top: var(--df-spacing-lg);
  color: var(--df-text-secondary);

  a {
    color: var(--df-accent-primary);
    text-decoration: none;
    font-weight: 500;
    margin-left: var(--df-spacing-xs);

    &:hover {
      color: var(--df-accent-success);
      text-decoration: underline;
    }
  }
}

:deep(.ant-form-item) {
  margin-bottom: var(--df-spacing-lg);

  .ant-form-item-label > label {
    color: var(--df-text-primary);
    font-weight: 500;
  }

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

:deep(.ant-checkbox-wrapper) {
  color: var(--df-text-primary);
  font-size: var(--df-font-size-sm);

  .ant-checkbox {
    .ant-checkbox-inner {
      background: var(--df-primary-bg);
      border-color: var(--df-text-disabled);
    }

    &.ant-checkbox-checked .ant-checkbox-inner {
      background: var(--df-accent-primary);
      border-color: var(--df-accent-primary);
    }
  }

  &:hover .ant-checkbox-inner {
    border-color: var(--df-accent-primary);
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

  &.ant-btn-loading, &:disabled {
    background: var(--df-text-disabled) !important;
  }

  .anticon {
    margin-right: var(--df-spacing-xs);
  }
}

// 响应式设计
@media (max-width: 480px) {
  .register-page {
    padding: var(--df-spacing-md);
  }

  .register-card {
    padding: var(--df-spacing-lg);
  }

  .verification-input {
    flex-direction: column;

    .code-button {
      width: 100%;
    }
  }
}
</style>
