<template>
  <div class="account-security">
    <a-card title="账户安全" class="security-card">
      <div class="security-items">
        <!-- 登录密码 -->
        <div class="security-item">
          <div class="item-info">
            <div class="item-header">
              <LockOutlined class="item-icon" />
              <h4>登录密码</h4>
            </div>
            <p>定期更新密码有助于保护账户安全</p>
            <div class="security-status">
              <a-tag :color="passwordStrength.color" size="small">
                {{ passwordStrength.text }}
              </a-tag>
              <span class="last-update">上次修改：{{ lastPasswordUpdate }}</span>
            </div>
          </div>
          <a-button type="primary" @click="showChangePasswordModal" :loading="loading">
            <KeyOutlined />
            修改密码
          </a-button>
        </div>

        <!-- 两步验证 -->
        <div class="security-item">
          <div class="item-info">
            <div class="item-header">
              <SecurityScanOutlined class="item-icon" />
              <h4>两步验证</h4>
            </div>
            <p>通过手机短信或身份验证器加强账户安全</p>
            <div class="security-status">
              <a-tag :color="twoFactorEnabled ? 'success' : 'warning'" size="small">
                {{ twoFactorEnabled ? '已启用' : '未启用' }}
              </a-tag>
            </div>
          </div>
          <a-switch
            v-model:checked="twoFactorEnabled"
            @change="handleTwoFactorChange"
            :loading="twoFactorLoading"
          />
        </div>

        <!-- 登录设备管理 -->
        <div class="security-item">
          <div class="item-info">
            <div class="item-header">
              <MobileOutlined class="item-icon" />
              <h4>登录设备管理</h4>
            </div>
            <p>管理已登录的设备，可远程注销可疑设备</p>
            <div class="security-status">
              <a-tag color="blue" size="small">
                {{ activeDevicesCount }} 个活跃设备
              </a-tag>
            </div>
          </div>
          <a-button @click="showDeviceManageModal" :loading="loading">
            <DesktopOutlined />
            管理设备
          </a-button>
        </div>

        <!-- 登录通知 -->
        <div class="security-item">
          <div class="item-info">
            <div class="item-header">
              <NotificationOutlined class="item-icon" />
              <h4>登录通知</h4>
            </div>
            <p>异地登录或新设备登录时发送通知</p>
            <div class="security-status">
              <a-tag :color="loginNotificationEnabled ? 'success' : 'default'" size="small">
                {{ loginNotificationEnabled ? '已开启' : '已关闭' }}
              </a-tag>
            </div>
          </div>
          <a-switch
            v-model:checked="loginNotificationEnabled"
            @change="handleLoginNotificationChange"
            :loading="loading"
          />
        </div>

        <!-- 账户注销 -->
        <div class="security-item danger-item">
          <div class="item-info">
            <div class="item-header">
              <ExclamationCircleOutlined class="item-icon danger-icon" />
              <h4>账户注销</h4>
            </div>
            <p class="danger-text">永久删除账户和所有数据，此操作不可撤销</p>
          </div>
          <a-button danger @click="showDeleteAccountModal" :loading="loading">
            <DeleteOutlined />
            注销账户
          </a-button>
        </div>
      </div>
    </a-card>

    <!-- 修改密码弹窗 -->
    <a-modal
      v-model:open="changePasswordVisible"
      title="修改密码"
      :confirm-loading="passwordLoading"
      @ok="handleChangePassword"
      @cancel="handleCancelChangePassword"
      width="480px"
    >
      <a-form
        ref="passwordFormRef"
        :model="passwordForm"
        layout="vertical"
      >
        <a-form-item
          label="当前密码"
          name="oldPassword"
          :rules="currentPasswordRules"
        >
          <a-input-password
            v-model:value="passwordForm.oldPassword"
            placeholder="请输入当前密码"
            size="large"
            autocomplete="current-password"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item
          label="新密码"
          name="newPassword"
          :rules="newPasswordRules"
        >
          <a-input-password
            v-model:value="passwordForm.newPassword"
            placeholder="请输入新密码"
            size="large"
            autocomplete="new-password"
            @input="handleNewPasswordInput"
          >
            <template #prefix>
              <KeyOutlined />
            </template>
          </a-input-password>

          <!-- 密码强度指示器 -->
          <div v-if="passwordForm.newPassword" class="password-strength">
            <div class="strength-bar">
              <div
                class="strength-level"
                :class="currentPasswordStrength.level"
                :style="{ width: currentPasswordStrength.width }"
              ></div>
            </div>
            <span class="strength-text">{{ currentPasswordStrength.text }}</span>
          </div>
        </a-form-item>

        <a-form-item
          label="确认新密码"
          name="confirmPassword"
          :rules="confirmPasswordRules"
        >
          <a-input-password
            v-model:value="passwordForm.confirmPassword"
            placeholder="请再次输入新密码"
            size="large"
            autocomplete="new-password"
          >
            <template #prefix>
              <CheckOutlined />
            </template>
          </a-input-password>
        </a-form-item>
      </a-form>
    </a-modal>

    <!-- 设备管理弹窗 -->
    <a-modal
      v-model:open="deviceManageVisible"
      title="登录设备管理"
      :footer="null"
      width="720px"
    >
      <div class="device-list">
        <div v-for="device in activeDevices" :key="device.id" class="device-item">
          <div class="device-info">
            <div class="device-header">
              <component :is="getDeviceIcon(device.type)" class="device-type-icon" />
              <div class="device-details">
                <h4>{{ device.name }}</h4>
                <div class="device-meta">
                  <span>{{ device.os }} {{ device.browser }}</span>
                  <a-divider type="vertical" />
                  <span>{{ device.location }}</span>
                  <a-divider type="vertical" />
                  <span>{{ formatTime(device.lastActive) }}</span>
                </div>
              </div>
            </div>
            <div class="device-status">
              <a-tag v-if="device.isCurrent" color="green">当前设备</a-tag>
              <a-tag v-else color="blue">活跃</a-tag>
            </div>
          </div>

          <div class="device-actions">
            <a-button
              v-if="!device.isCurrent"
              type="text"
              danger
              @click="handleRemoteLogout(device.id)"
              :loading="device.loading"
              size="small"
            >
              注销
            </a-button>
          </div>
        </div>
      </div>

      <div class="device-footer">
        <a-button type="primary" danger @click="handleLogoutAllDevices" :loading="logoutAllLoading">
          注销所有其他设备
        </a-button>
      </div>
    </a-modal>

    <!-- 账户注销弹窗 -->
    <a-modal
      v-model:open="deleteAccountVisible"
      title="账户注销确认"
      :confirm-loading="deleteLoading"
      @ok="handleDeleteAccount"
      @cancel="handleCancelDeleteAccount"
      width="480px"
    >
      <div class="delete-warning">
        <ExclamationCircleOutlined class="warning-icon" />
        <div class="warning-content">
          <h4>此操作将永久删除您的账户</h4>
          <ul class="warning-list">
            <li>所有个人数据和文件将被永久删除</li>
            <li>所有生成的数据和配置将无法恢复</li>
            <li>该操作无法撤销</li>
          </ul>
        </div>
      </div>

      <a-form
        ref="deleteFormRef"
        :model="deleteForm"
        layout="vertical"
      >
        <a-form-item
          label="请输入您的密码以确认注销"
          name="password"
          :rules="confirmDeleteRules"
        >
          <a-input-password
            v-model:value="deleteForm.password"
            placeholder="请输入登录密码"
            size="large"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>

        <a-form-item
          name="confirmDelete"
          :rules="[{ required: true, message: '请确认您理解此操作的后果' }]"
        >
          <a-checkbox v-model:checked="deleteForm.confirmDelete">
            我理解此操作将永久删除我的账户和所有数据
          </a-checkbox>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { message, Modal } from 'ant-design-vue'
import {
  LockOutlined,
  KeyOutlined,
  SecurityScanOutlined,
  MobileOutlined,
  DesktopOutlined,
  NotificationOutlined,
  ExclamationCircleOutlined,
  DeleteOutlined,
  CheckOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, Rule } from 'ant-design-vue/lib/form'

const authStore = useAuthStore()

// 表单引用
const passwordFormRef = ref<FormInstance>()
const deleteFormRef = ref<FormInstance>()

// 状态
const loading = ref(false)
const passwordLoading = ref(false)
const twoFactorLoading = ref(false)
const logoutAllLoading = ref(false)
const deleteLoading = ref(false)

// 弹窗状态
const changePasswordVisible = ref(false)
const deviceManageVisible = ref(false)
const deleteAccountVisible = ref(false)

// 安全设置状态
const twoFactorEnabled = ref(false)
const loginNotificationEnabled = ref(true)
const activeDevicesCount = ref(3)

// 表单数据
const passwordForm = reactive({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const deleteForm = reactive({
  password: '',
  confirmDelete: false
})

// 模拟设备数据
const activeDevices = ref([
  {
    id: '1',
    name: 'Chrome浏览器',
    type: 'desktop',
    os: 'Windows 11',
    browser: 'Chrome 120.0',
    location: '北京市',
    lastActive: new Date().toISOString(),
    isCurrent: true,
    loading: false
  },
  {
    id: '2',
    name: 'iPhone Safari',
    type: 'mobile',
    os: 'iOS 17.1',
    browser: 'Safari',
    location: '上海市',
    lastActive: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2小时前
    isCurrent: false,
    loading: false
  },
  {
    id: '3',
    name: 'MacBook Safari',
    type: 'desktop',
    os: 'macOS 14.1',
    browser: 'Safari 17.0',
    location: '广州市',
    lastActive: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(), // 24小时前
    isCurrent: false,
    loading: false
  }
])

// 计算属性
const passwordStrength = computed(() => {
  // 模拟密码强度评估
  return { color: 'warning', text: '建议加强' }
})

const lastPasswordUpdate = computed(() => {
  return '30天前'
})

const currentPasswordStrength = computed(() => {
  const password = passwordForm.newPassword
  if (!password) return { level: '', width: '0%', text: '' }

  let score = 0

  // 长度评分
  if (password.length >= 8) score += 25
  else if (password.length >= 6) score += 15

  // 复杂度评分
  if (/[a-z]/.test(password)) score += 15
  if (/[A-Z]/.test(password)) score += 15
  if (/\d/.test(password)) score += 15
  if (/[!@#$%^&*(),.?\":{}|<>]/.test(password)) score += 30

  if (score >= 80) return { level: 'strong', width: '100%', text: '强' }
  if (score >= 60) return { level: 'medium', width: '66%', text: '中' }
  if (score >= 30) return { level: 'weak', width: '33%', text: '弱' }
  return { level: 'very-weak', width: '20%', text: '太弱' }
})

// 验证规则
const currentPasswordRules: Rule[] = [
  { required: true, message: '请输入当前密码', trigger: 'blur' },
  { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
]

const newPasswordRules: Rule[] = [
  { required: true, message: '请设置新密码', trigger: 'blur' },
  { min: 6, message: '新密码长度不能少于6位', trigger: 'blur' },
  { max: 50, message: '新密码长度不能超过50位', trigger: 'blur' },
  {
    validator: (rule, value) => {
      if (!value) return Promise.resolve()
      if (!/(?=.*[a-zA-Z])(?=.*\d)/.test(value)) {
        return Promise.reject('新密码必须包含字母和数字')
      }
      if (value === passwordForm.oldPassword) {
        return Promise.reject('新密码不能与当前密码相同')
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
      if (value && value !== passwordForm.newPassword) {
        return Promise.reject('两次输入的密码不一致')
      }
      return Promise.resolve()
    },
    trigger: 'blur'
  }
]

const confirmDeleteRules: Rule[] = [
  { required: true, message: '请输入密码确认注销', trigger: 'blur' },
  { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
]

// 事件处理
const showChangePasswordModal = () => {
  passwordForm.oldPassword = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  changePasswordVisible.value = true
}

const handleCancelChangePassword = () => {
  changePasswordVisible.value = false
}

const handleNewPasswordInput = () => {
  if (passwordForm.confirmPassword && passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordFormRef.value?.validateFields(['confirmPassword'])
  }
}

const handleChangePassword = async () => {
  try {
    await passwordFormRef.value?.validate()

    passwordLoading.value = true

    const result = await authStore.changePassword(
      passwordForm.oldPassword,
      passwordForm.newPassword,
      passwordForm.confirmPassword
    )

    if (result.success) {
      message.success(result.message)
      changePasswordVisible.value = false
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('修改密码失败:', error)
  } finally {
    passwordLoading.value = false
  }
}

const handleTwoFactorChange = async (checked: boolean) => {
  try {
    twoFactorLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))

    message.success(checked ? '两步验证已启用' : '两步验证已禁用')
  } catch (error) {
    message.error('设置失败，请稍后重试')
    // 回退状态
    twoFactorEnabled.value = !checked
  } finally {
    twoFactorLoading.value = false
  }
}

const handleLoginNotificationChange = async (checked: boolean) => {
  try {
    loading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))

    message.success(checked ? '登录通知已开启' : '登录通知已关闭')
  } catch (error) {
    message.error('设置失败，请稍后重试')
    // 回退状态
    loginNotificationEnabled.value = !checked
  } finally {
    loading.value = false
  }
}

const showDeviceManageModal = () => {
  deviceManageVisible.value = true
}

const getDeviceIcon = (type: string) => {
  switch (type) {
    case 'mobile':
      return MobileOutlined
    case 'desktop':
    default:
      return DesktopOutlined
  }
}

const formatTime = (dateString: string) => {
  const date = new Date(dateString)
  const now = new Date()
  const diff = now.getTime() - date.getTime()

  if (diff < 60 * 1000) return '刚刚'
  if (diff < 60 * 60 * 1000) return `${Math.floor(diff / (60 * 1000))}分钟前`
  if (diff < 24 * 60 * 60 * 1000) return `${Math.floor(diff / (60 * 60 * 1000))}小时前`
  return `${Math.floor(diff / (24 * 60 * 60 * 1000))}天前`
}

const handleRemoteLogout = async (deviceId: string) => {
  try {
    const device = activeDevices.value.find(d => d.id === deviceId)
    if (device) {
      device.loading = true

      // 模拟API调用
      await new Promise(resolve => setTimeout(resolve, 1000))

      // 从列表中移除设备
      const index = activeDevices.value.findIndex(d => d.id === deviceId)
      if (index > -1) {
        activeDevices.value.splice(index, 1)
        activeDevicesCount.value--
      }

      message.success('设备已注销')
    }
  } catch (error) {
    message.error('注销失败，请稍后重试')
  }
}

const handleLogoutAllDevices = async () => {
  Modal.confirm({
    title: '确认注销所有设备？',
    content: '这将注销除当前设备外的所有登录设备，您需要在其他设备上重新登录。',
    okText: '确认',
    cancelText: '取消',
    onOk: async () => {
      try {
        logoutAllLoading.value = true

        // 模拟API调用
        await new Promise(resolve => setTimeout(resolve, 1500))

        // 只保留当前设备
        activeDevices.value = activeDevices.value.filter(d => d.isCurrent)
        activeDevicesCount.value = 1

        message.success('已注销所有其他设备')
      } catch (error) {
        message.error('批量注销失败，请稍后重试')
      } finally {
        logoutAllLoading.value = false
      }
    }
  })
}

const showDeleteAccountModal = () => {
  deleteForm.password = ''
  deleteForm.confirmDelete = false
  deleteAccountVisible.value = true
}

const handleCancelDeleteAccount = () => {
  deleteAccountVisible.value = false
}

const handleDeleteAccount = async () => {
  try {
    await deleteFormRef.value?.validate()

    if (!deleteForm.confirmDelete) {
      message.error('请确认您理解注销账户的后果')
      return
    }

    deleteLoading.value = true

    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 2000))

    message.success('账户注销成功')
    deleteAccountVisible.value = false

    // 注销后跳转到登录页
    setTimeout(() => {
      authStore.logout()
    }, 1000)

  } catch (error) {
    console.error('注销账户失败:', error)
  } finally {
    deleteLoading.value = false
  }
}

// 组件挂载时初始化数据
onMounted(() => {
  // 可以在这里加载用户的安全设置
})
</script>

<style scoped lang="less">
.account-security {
  max-width: 800px;
  margin: 0 auto;
}

.security-card {
  background: var(--df-secondary-bg);
  border: 1px solid var(--df-text-disabled);

  :deep(.ant-card-head) {
    background: transparent;
    border-bottom-color: var(--df-text-disabled);

    .ant-card-head-title {
      color: var(--df-text-primary);
      font-size: var(--df-font-size-lg);
      font-weight: 600;
    }
  }

  :deep(.ant-card-body) {
    background: transparent;
  }
}

.security-items {
  display: flex;
  flex-direction: column;
  gap: var(--df-spacing-lg);
}

.security-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--df-spacing-xl);
  background: var(--df-primary-bg);
  border: 1px solid var(--df-text-disabled);
  border-radius: var(--df-radius-lg);
  transition: all var(--df-transition-normal);

  &:hover {
    border-color: var(--df-accent-primary);
    box-shadow: 0 4px 16px rgba(142, 93, 255, 0.1);
  }

  &.danger-item {
    border-color: rgba(239, 68, 68, 0.3);

    &:hover {
      border-color: rgba(239, 68, 68, 0.6);
      box-shadow: 0 4px 16px rgba(239, 68, 68, 0.1);
    }
  }

  .item-info {
    flex: 1;

    .item-header {
      display: flex;
      align-items: center;
      gap: var(--df-spacing-sm);
      margin-bottom: var(--df-spacing-xs);

      .item-icon {
        font-size: var(--df-font-size-lg);
        color: var(--df-accent-primary);

        &.danger-icon {
          color: var(--df-accent-error);
        }
      }

      h4 {
        color: var(--df-text-primary);
        margin: 0;
        font-size: var(--df-font-size-lg);
        font-weight: 600;
      }
    }

    p {
      color: var(--df-text-secondary);
      margin: 0 0 var(--df-spacing-sm) 0;
      font-size: var(--df-font-size-base);
      line-height: 1.5;

      &.danger-text {
        color: var(--df-accent-error);
        font-weight: 500;
      }
    }

    .security-status {
      display: flex;
      align-items: center;
      gap: var(--df-spacing-md);

      .last-update {
        color: var(--df-text-secondary);
        font-size: var(--df-font-size-sm);
      }
    }
  }
}

// 密码强度指示器
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

// 设备管理
.device-list {
  max-height: 400px;
  overflow-y: auto;
}

.device-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--df-spacing-lg);
  background: var(--df-primary-bg);
  border: 1px solid var(--df-text-disabled);
  border-radius: var(--df-radius-md);
  margin-bottom: var(--df-spacing-md);

  &:hover {
    border-color: var(--df-accent-primary);
    box-shadow: 0 2px 8px rgba(142, 93, 255, 0.1);
  }

  &:last-child {
    margin-bottom: 0;
  }

  .device-info {
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex: 1;

    .device-header {
      display: flex;
      align-items: center;
      gap: var(--df-spacing-md);

      .device-type-icon {
        font-size: var(--df-font-size-xl);
        color: var(--df-accent-primary);
      }

      .device-details {
        h4 {
          color: var(--df-text-primary);
          margin: 0 0 var(--df-spacing-xs) 0;
          font-size: var(--df-font-size-base);
          font-weight: 600;
        }

        .device-meta {
          display: flex;
          align-items: center;
          gap: var(--df-spacing-xs);
          color: var(--df-text-secondary);
          font-size: var(--df-font-size-sm);

          .ant-divider-vertical {
            border-color: var(--df-text-disabled);
          }
        }
      }
    }

    .device-status {
      margin-left: var(--df-spacing-md);
    }
  }

  .device-actions {
    margin-left: var(--df-spacing-lg);
  }
}

.device-footer {
  margin-top: var(--df-spacing-lg);
  padding-top: var(--df-spacing-lg);
  border-top: 1px solid var(--df-text-disabled);
  text-align: center;
}

// 删除账户警告
.delete-warning {
  display: flex;
  gap: var(--df-spacing-md);
  padding: var(--df-spacing-lg);
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
  border-radius: var(--df-radius-md);
  margin-bottom: var(--df-spacing-lg);

  .warning-icon {
    font-size: var(--df-font-size-xl);
    color: var(--df-accent-error);
    margin-top: 2px;
  }

  .warning-content {
    flex: 1;

    h4 {
      color: var(--df-accent-error);
      margin: 0 0 var(--df-spacing-sm) 0;
      font-weight: 600;
    }

    .warning-list {
      margin: 0;
      padding-left: var(--df-spacing-lg);
      color: var(--df-text-primary);

      li {
        margin-bottom: var(--df-spacing-xs);
      }
    }
  }
}

// 全局样式
:deep(.ant-form-item) {
  margin-bottom: var(--df-spacing-lg);

  .ant-form-item-label > label {
    color: var(--df-text-primary);
    font-weight: 600;
    font-size: var(--df-font-size-md);
  }

  .ant-form-item-explain {
    color: var(--df-accent-error);
  }
}

:deep(.ant-input-affix-wrapper),
:deep(.ant-input) {
  background: var(--df-primary-bg);
  border-color: var(--df-text-disabled);
  color: var(--df-text-primary);

  &:hover, &:focus, &.ant-input-affix-wrapper-focused {
    border-color: var(--df-accent-primary);
    box-shadow: 0 0 0 2px rgba(142, 93, 255, 0.1);
  }

  input {
    background: transparent !important;
    color: var(--df-text-primary) !important;

    &::placeholder {
      color: var(--df-text-secondary) !important;
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

:deep(.ant-btn-dangerous) {
  border-color: var(--df-accent-error);
  color: var(--df-accent-error);
  background: transparent;

  &:hover, &:focus {
    background: var(--df-accent-error);
    border-color: var(--df-accent-error);
    color: white;
  }
}

:deep(.ant-switch-checked) {
  background-color: var(--df-accent-primary);

  &:hover:not(.ant-switch-disabled) {
    background-color: var(--df-accent-success);
  }
}

:deep(.ant-tag) {
  border-radius: var(--df-radius-sm);
  font-size: var(--df-font-size-xs);
  font-weight: 500;

  &.ant-tag-success {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--df-accent-success);
    color: var(--df-accent-success);
  }

  &.ant-tag-warning {
    background: rgba(245, 158, 11, 0.1);
    border-color: #F59E0B;
    color: #F59E0B;
  }

  &.ant-tag-blue {
    background: rgba(59, 130, 246, 0.1);
    border-color: #3B82F6;
    color: #3B82F6;
  }

  &.ant-tag-green {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--df-accent-success);
    color: var(--df-accent-success);
  }
}

:deep(.ant-modal) {
  .ant-modal-content {
    background: var(--df-secondary-bg);
    border: 1px solid var(--df-text-disabled);
  }

  .ant-modal-header {
    background: transparent;
    border-bottom-color: var(--df-text-disabled);

    .ant-modal-title {
      color: var(--df-text-primary);
      font-weight: 600;
    }
  }

  .ant-modal-body {
    background: transparent;
  }

  .ant-modal-footer {
    background: transparent;
    border-top-color: var(--df-text-disabled);
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

// 响应式设计
@media (max-width: 768px) {
  .account-security {
    max-width: 100%;
    padding: 0 var(--df-spacing-md);
  }

  .security-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--df-spacing-lg);
    padding: var(--df-spacing-lg);

    .item-info {
      width: 100%;
    }
  }

  .device-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--df-spacing-md);

    .device-info {
      width: 100%;
      flex-direction: column;
      align-items: flex-start;

      .device-header {
        width: 100%;
      }

      .device-status {
        margin-left: 0;
        align-self: flex-start;
      }
    }

    .device-actions {
      margin-left: 0;
      align-self: flex-end;
    }
  }
}
</style>
