<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-card">
        <h1 class="login-title">登录 DataForge</h1>
        <a-form
          ref="formRef"
          :model="loginForm"
          name="login"
          autocomplete="off"
          @finish="handleLogin"
          @finish-failed="handleLoginFailed"
        >
          <a-form-item
            name="username"
            :rules="usernameRules"
          >
            <a-input
              v-model:value="loginForm.username"
              placeholder="请输入您的邮箱或手机号"
              size="large"
              :disabled="loading"
            >
              <template #prefix>
                <UserOutlined />
              </template>
            </a-input>
          </a-form-item>

          <a-form-item
            name="password"
            :rules="passwordRules"
          >
            <a-input-password
              v-model:value="loginForm.password"
              placeholder="请输入登录密码"
              size="large"
              :disabled="loading"
            >
              <template #prefix>
                <LockOutlined />
              </template>
            </a-input-password>
          </a-form-item>

          <a-form-item name="rememberMe">
            <div class="form-extra">
              <a-checkbox v-model:checked="loginForm.rememberMe" :disabled="loading">
                记住我
              </a-checkbox>
              <router-link to="/reset-password" class="forgot-password">
                忘记密码？
              </router-link>
            </div>
          </a-form-item>

          <a-form-item>
            <a-button
              type="primary"
              html-type="submit"
              size="large"
              block
              :loading="loading"
            >
              <template v-if="!loading">
                <LoginOutlined />
                登录
              </template>
              <template v-else>
                登录中...
              </template>
            </a-button>
          </a-form-item>
        </a-form>

        <div class="register-link">
          还没有账户？
          <router-link to="/register">立即注册</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { message } from 'ant-design-vue'
import { UserOutlined, LockOutlined, LoginOutlined } from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, Rule } from 'ant-design-vue/lib/form'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 表单引用
const formRef = ref<FormInstance>()

// 加载状态
const loading = ref(false)

// 表单数据
const loginForm = reactive({
  username: '',
  password: '',
  rememberMe: false
})

// 表单验证规则
const usernameRules: Rule[] = [
  { required: true, message: '请输入邮箱或手机号', trigger: 'blur' },
  { 
    pattern: /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})|^1[3-9]\d{9}$/, 
    message: '请输入有效的邮箱或手机号', 
    trigger: 'blur' 
  }
]

const passwordRules: Rule[] = [
  { required: true, message: '请输入密码', trigger: 'blur' },
  { min: 6, message: '密码长度不能少于6位', trigger: 'blur' },
  { max: 20, message: '密码长度不能超过20位', trigger: 'blur' }
]

// 登录处理
const handleLogin = async () => {
  try {
    loading.value = true
    
    const result = await authStore.login({
      username: loginForm.username.trim(),
      password: loginForm.password,
      rememberMe: loginForm.rememberMe
    })
    
    if (result.success) {
      message.success(result.message)
      
      // 登录成功后跳转
      const redirectPath = (route.query.redirect as string) || '/workbench'
      await router.push(redirectPath)
    } else {
      message.error(result.message)
      // 登录失败时清空密码
      loginForm.password = ''
    }
  } catch (error) {
    console.error('登录错误:', error)
    message.error('登录失败，请稍后重试')
    loginForm.password = ''
  } finally {
    loading.value = false
  }
}

// 表单验证失败处理
const handleLoginFailed = (errorInfo: any) => {
  console.log('表单验证失败:', errorInfo)
  message.warning('请检查表单填写是否正确')
}

// 组件挂载时检查是否已登录
onMounted(() => {
  if (authStore.isAuthenticated) {
    const redirectPath = (route.query.redirect as string) || '/workbench'
    router.replace(redirectPath)
  }
  
  // 如果有记住的用户名，填充表单
  const rememberedUsername = localStorage.getItem('remembered_username')
  if (rememberedUsername) {
    loginForm.username = rememberedUsername
    loginForm.rememberMe = true
  }
})
</script>

<style scoped lang="less">
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--df-primary-bg);
  padding: var(--df-spacing-lg);
}

.login-container {
  width: 100%;
  max-width: 400px;
}

.login-card {
  background: var(--df-secondary-bg);
  border-radius: var(--df-radius-lg);
  padding: var(--df-spacing-xl);
  border: 1px solid var(--df-text-disabled);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.login-title {
  color: var(--df-text-primary);
  text-align: center;
  font-size: var(--df-font-size-2xl);
  font-weight: 600;
  margin-bottom: var(--df-spacing-xl);
  background: linear-gradient(135deg, var(--df-accent-primary), var(--df-accent-success));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.form-extra {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.forgot-password {
  color: var(--df-accent-primary);
  text-decoration: none;
  font-size: var(--df-font-size-sm);
  transition: all var(--df-transition-fast);
  
  &:hover {
    color: var(--df-accent-success);
    text-decoration: underline;
  }
}

.register-link {
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
  
  &.ant-btn-loading {
    background: var(--df-text-disabled);
  }
  
  .anticon {
    margin-right: var(--df-spacing-xs);
  }
}

// 响应式设计
@media (max-width: 480px) {
  .login-page {
    padding: var(--df-spacing-md);
  }
  
  .login-card {
    padding: var(--df-spacing-lg);
  }
}
</style>