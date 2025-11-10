<template>
  <div class="profile-details">
    <a-card title="个人资料" class="profile-card">
      <div class="profile-content">
        <!-- 头像区域 -->
        <div class="avatar-section">
          <a-avatar :size="80" :src="avatarUrl || '/default-avatar.png'" class="user-avatar">
            <template #icon v-if="!avatarUrl">
              <UserOutlined />
            </template>
          </a-avatar>
          
          <a-upload
            :show-upload-list="false"
            :before-upload="handleAvatarUpload"
            accept="image/*"
            class="avatar-upload"
          >
            <a-button 
              size="small" 
              :loading="avatarUploading"
              class="change-avatar-btn"
            >
              <template v-if="!avatarUploading">
                <CameraOutlined />
                修改头像
              </template>
              <template v-else>
                上传中...
              </template>
            </a-button>
          </a-upload>
        </div>
        
        <!-- 个人资料表单 -->
        <a-form
          ref="profileFormRef"
          :model="profileForm"
          layout="vertical"
          class="profile-form"
          @finish="handleSaveProfile"
        >
          <!-- 昵称 -->
          <a-form-item
            label="昵称"
            name="nickname"
            :rules="nicknameRules"
          >
            <a-input
              v-model:value="profileForm.nickname"
              placeholder="请输入昵称"
              size="large"
              :disabled="loading"
            >
              <template #prefix>
                <UserOutlined />
              </template>
            </a-input>
          </a-form-item>
          
          <!-- 邮箱 -->
          <a-form-item label="邮箱">
            <div class="contact-item">
              <div class="contact-info">
                <MailOutlined class="contact-icon" />
                <span class="contact-text">{{ userEmail || '未绑定' }}</span>
                <a-tag v-if="userEmail" color="success" size="small">已验证</a-tag>
              </div>
              <a-button 
                type="link" 
                size="small"
                @click="showChangeEmailModal"
                :disabled="loading"
              >
                {{ userEmail ? '更换' : '绑定' }}
              </a-button>
            </div>
          </a-form-item>
          
          <!-- 手机号 -->
          <a-form-item label="手机号">
            <div class="contact-item">
              <div class="contact-info">
                <PhoneOutlined class="contact-icon" />
                <span class="contact-text">{{ userPhone || '未绑定' }}</span>
                <a-tag v-if="userPhone" color="success" size="small">已验证</a-tag>
              </div>
              <a-button 
                type="link" 
                size="small"
                @click="showChangePhoneModal"
                :disabled="loading"
              >
                {{ userPhone ? '更换' : '绑定' }}
              </a-button>
            </div>
          </a-form-item>
          
          <!-- 保存按钮 -->
          <a-form-item>
            <a-space>
              <a-button
                type="primary"
                html-type="submit"
                size="large"
                :loading="loading"
              >
                <SaveOutlined />
                保存修改
              </a-button>
              <a-button
                size="large"
                @click="handleReset"
                :disabled="loading"
              >
                <ReloadOutlined />
                重置
              </a-button>
            </a-space>
          </a-form-item>
        </a-form>
      </div>
    </a-card>
    
    <!-- 修改邮箱弹窗 -->
    <a-modal
      v-model:open="emailModalVisible"
      title="修改邮箱"
      :confirm-loading="emailLoading"
      @ok="handleChangeEmail"
      @cancel="handleCancelEmail"
      width="480px"
    >
      <a-form
        ref="emailFormRef"
        :model="emailForm"
        layout="vertical"
      >
        <a-form-item
          label="新邮箱地址"
          name="newEmail"
          :rules="emailRules"
        >
          <a-input
            v-model:value="emailForm.newEmail"
            placeholder="请输入新的邮箱地址"
            size="large"
          >
            <template #prefix>
              <MailOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item
          label="邮箱验证码"
          name="verificationCode"
          :rules="codeRules"
        >
          <div class="verification-input">
            <a-input
              v-model:value="emailForm.verificationCode"
              placeholder="请输入6位验证码"
              size="large"
              maxlength="6"
            >
              <template #prefix>
                <SafetyOutlined />
              </template>
            </a-input>
            <a-button
              :loading="codeLoading"
              :disabled="!emailForm.newEmail || emailCountdown > 0"
              @click="sendEmailCode"
              size="large"
            >
              {{ emailCountdown > 0 ? `${emailCountdown}s` : '发送验证码' }}
            </a-button>
          </div>
        </a-form-item>
        
        <a-form-item
          label="登录密码"
          name="password"
          :rules="passwordRules"
        >
          <a-input-password
            v-model:value="emailForm.password"
            placeholder="请输入登录密码"
            size="large"
          >
            <template #prefix>
              <LockOutlined />
            </template>
          </a-input-password>
        </a-form-item>
      </a-form>
    </a-modal>
    
    <!-- 修改手机号弹窗 -->
    <a-modal
      v-model:open="phoneModalVisible"
      title="绑定手机号"
      :confirm-loading="phoneLoading"
      @ok="handleChangePhone"
      @cancel="handleCancelPhone"
      width="480px"
    >
      <a-form
        ref="phoneFormRef"
        :model="phoneForm"
        layout="vertical"
      >
        <a-form-item
          label="手机号码"
          name="phone"
          :rules="phoneNumberRules"
        >
          <a-input
            v-model:value="phoneForm.phone"
            placeholder="请输入手机号码"
            size="large"
          >
            <template #prefix>
              <PhoneOutlined />
            </template>
          </a-input>
        </a-form-item>
        
        <a-form-item
          label="短信验证码"
          name="verificationCode"
          :rules="codeRules"
        >
          <div class="verification-input">
            <a-input
              v-model:value="phoneForm.verificationCode"
              placeholder="请输入6位验证码"
              size="large"
              maxlength="6"
            >
              <template #prefix>
                <SafetyOutlined />
              </template>
            </a-input>
            <a-button
              :loading="codeLoading"
              :disabled="!phoneForm.phone || phoneCountdown > 0"
              @click="sendPhoneCode"
              size="large"
            >
              {{ phoneCountdown > 0 ? `${phoneCountdown}s` : '发送验证码' }}
            </a-button>
          </div>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { message } from 'ant-design-vue'
import {
  UserOutlined,
  MailOutlined,
  PhoneOutlined,
  CameraOutlined,
  SaveOutlined,
  ReloadOutlined,
  SafetyOutlined,
  LockOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'
import type { FormInstance, Rule } from 'ant-design-vue/lib/form'

const authStore = useAuthStore()

// 表单引用
const profileFormRef = ref<FormInstance>()
const emailFormRef = ref<FormInstance>()
const phoneFormRef = ref<FormInstance>()

// 状态
const loading = ref(false)
const avatarUploading = ref(false)
const emailModalVisible = ref(false)
const phoneModalVisible = ref(false)
const emailLoading = ref(false)
const phoneLoading = ref(false)
const codeLoading = ref(false)

// 倒计时
const emailCountdown = ref(0)
const phoneCountdown = ref(0)
let emailTimer: NodeJS.Timeout | null = null
let phoneTimer: NodeJS.Timeout | null = null

// 表单数据
const profileForm = reactive({
  nickname: ''
})

const emailForm = reactive({
  newEmail: '',
  verificationCode: '',
  password: ''
})

const phoneForm = reactive({
  phone: '',
  verificationCode: ''
})

// 计算属性
const userEmail = computed(() => authStore.userInfo?.email)
const userPhone = computed(() => authStore.userInfo?.phone)
const avatarUrl = computed(() => authStore.userInfo?.avatar)

// 验证规则
const nicknameRules: Rule[] = [
  { required: true, message: '请输入昵称', trigger: 'blur' },
  { min: 2, max: 20, message: '昵称长度为2-20个字符', trigger: 'blur' },
  { pattern: /^[\u4e00-\u9fa5a-zA-Z0-9_]+$/, message: '昵称只能包含中文、英文、数字和下划线', trigger: 'blur' }
]

const emailRules: Rule[] = [
  { required: true, message: '请输入邮箱地址', trigger: 'blur' },
  { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
]

const phoneNumberRules: Rule[] = [
  { required: true, message: '请输入手机号码', trigger: 'blur' },
  { pattern: /^1[3-9]\d{9}$/, message: '请输入有效的手机号码', trigger: 'blur' }
]

const codeRules: Rule[] = [
  { required: true, message: '请输入验证码', trigger: 'blur' },
  { len: 6, message: '验证码为6位数字', trigger: 'blur' },
  { pattern: /^\d{6}$/, message: '请输入有效的6位数字验证码', trigger: 'blur' }
]

const passwordRules: Rule[] = [
  { required: true, message: '请输入登录密码', trigger: 'blur' },
  { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
]

// 事件处理
const handleSaveProfile = async () => {
  try {
    loading.value = true
    
    const result = await authStore.updateProfile({
      nickname: profileForm.nickname.trim()
    })
    
    if (result.success) {
      message.success(result.message)
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('更新资料失败:', error)
    message.error('更新失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const handleReset = () => {
  initializeProfileForm()
  message.info('已重置为当前用户信息')
}

const handleAvatarUpload = async (file: File) => {
  // 验证文件类型
  const isImage = file.type.startsWith('image/')
  if (!isImage) {
    message.error('只能上传图片文件')
    return false
  }
  
  // 验证文件大小（2MB）
  const isLt2M = file.size / 1024 / 1024 < 2
  if (!isLt2M) {
    message.error('图片大小不能超过 2MB')
    return false
  }
  
  try {
    avatarUploading.value = true
    
    const result = await authStore.uploadAvatar(file)
    
    if (result.success) {
      message.success(result.message)
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('头像上传失败:', error)
    message.error('上传失败，请稍后重试')
  } finally {
    avatarUploading.value = false
  }
  
  return false // 阻止默认上传行为
}

// 邮箱修改
const showChangeEmailModal = () => {
  emailForm.newEmail = ''
  emailForm.verificationCode = ''
  emailForm.password = ''
  emailModalVisible.value = true
}

const handleCancelEmail = () => {
  emailModalVisible.value = false
  clearEmailTimer()
}

const sendEmailCode = async () => {
  if (!emailForm.newEmail) {
    message.warning('请先输入新邮箱地址')
    return
  }
  
  try {
    codeLoading.value = true
    
    const result = await authStore.sendVerificationCode(emailForm.newEmail, undefined, 'change_email')
    
    if (result.success) {
      message.success(result.message)
      startEmailCountdown()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    message.error('发送失败，请稍后重试')
  } finally {
    codeLoading.value = false
  }
}

const startEmailCountdown = () => {
  clearEmailTimer()
  emailCountdown.value = 60
  
  emailTimer = setInterval(() => {
    emailCountdown.value--
    if (emailCountdown.value <= 0) {
      clearEmailTimer()
    }
  }, 1000)
}

const clearEmailTimer = () => {
  if (emailTimer) {
    clearInterval(emailTimer)
    emailTimer = null
    emailCountdown.value = 0
  }
}

const handleChangeEmail = async () => {
  try {
    await emailFormRef.value?.validate()
    
    emailLoading.value = true
    
    const result = await authStore.changeEmail(
      emailForm.newEmail,
      emailForm.verificationCode,
      emailForm.password
    )
    
    if (result.success) {
      message.success(result.message)
      emailModalVisible.value = false
      clearEmailTimer()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('修改邮箱失败:', error)
  } finally {
    emailLoading.value = false
  }
}

// 手机号修改
const showChangePhoneModal = () => {
  phoneForm.phone = ''
  phoneForm.verificationCode = ''
  phoneModalVisible.value = true
}

const handleCancelPhone = () => {
  phoneModalVisible.value = false
  clearPhoneTimer()
}

const sendPhoneCode = async () => {
  if (!phoneForm.phone) {
    message.warning('请先输入手机号码')
    return
  }
  
  try {
    codeLoading.value = true
    
    const result = await authStore.sendVerificationCode(undefined, phoneForm.phone, 'change_phone')
    
    if (result.success) {
      message.success(result.message)
      startPhoneCountdown()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('发送验证码失败:', error)
    message.error('发送失败，请稍后重试')
  } finally {
    codeLoading.value = false
  }
}

const startPhoneCountdown = () => {
  clearPhoneTimer()
  phoneCountdown.value = 60
  
  phoneTimer = setInterval(() => {
    phoneCountdown.value--
    if (phoneCountdown.value <= 0) {
      clearPhoneTimer()
    }
  }, 1000)
}

const clearPhoneTimer = () => {
  if (phoneTimer) {
    clearInterval(phoneTimer)
    phoneTimer = null
    phoneCountdown.value = 0
  }
}

const handleChangePhone = async () => {
  try {
    await phoneFormRef.value?.validate()
    
    phoneLoading.value = true
    
    const result = await authStore.bindPhone(
      phoneForm.phone,
      phoneForm.verificationCode
    )
    
    if (result.success) {
      message.success(result.message)
      phoneModalVisible.value = false
      clearPhoneTimer()
    } else {
      message.error(result.message)
    }
  } catch (error) {
    console.error('绑定手机号失败:', error)
  } finally {
    phoneLoading.value = false
  }
}

// 初始化表单数据
const initializeProfileForm = () => {
  if (authStore.userInfo) {
    profileForm.nickname = authStore.userInfo.username || ''
  }
}

// 组件挂载时初始化
onMounted(() => {
  initializeProfileForm()
})

// 组件卸载时清理定时器
onMounted(() => {
  return () => {
    clearEmailTimer()
    clearPhoneTimer()
  }
})
</script>

<style scoped lang="less">
.profile-details {
  max-width: 800px;
  margin: 0 auto;
}

.profile-card {
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

.profile-content {
  display: flex;
  gap: var(--df-spacing-xl);
  align-items: flex-start;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
  }
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--df-spacing-md);
  min-width: 120px;
  
  .user-avatar {
    border: 3px solid var(--df-accent-primary);
    box-shadow: 0 4px 12px rgba(142, 93, 255, 0.3);
  }
  
  .change-avatar-btn {
    width: 100px;
    font-size: var(--df-font-size-xs);
    border-color: var(--df-accent-primary);
    color: var(--df-accent-primary);
    
    &:hover {
      border-color: var(--df-accent-success);
      color: var(--df-accent-success);
    }
    
    .anticon {
      margin-right: var(--df-spacing-xs);
    }
  }
}

.profile-form {
  flex: 1;
  min-width: 0;
}

.contact-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--df-spacing-md);
  background: var(--df-primary-bg);
  border: 1px solid var(--df-text-disabled);
  border-radius: var(--df-radius-md);
  
  &:hover {
    border-color: var(--df-accent-primary);
    box-shadow: 0 2px 8px rgba(142, 93, 255, 0.1);
  }
}

.contact-info {
  display: flex;
  align-items: center;
  gap: var(--df-spacing-sm);
  flex: 1;
  
  .contact-icon {
    color: var(--df-text-secondary);
    font-size: var(--df-font-size-md);
  }
  
  .contact-text {
    color: var(--df-text-primary);
    font-weight: 500;
  }
}

.verification-input {
  display: flex;
  gap: var(--df-spacing-sm);
  
  .ant-input-wrapper {
    flex: 1;
  }
  
  .ant-btn {
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
  
  @media (max-width: 480px) {
    flex-direction: column;
    
    .ant-btn {
      width: 100%;
    }
  }
}

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

:deep(.ant-btn:not(.ant-btn-primary)) {
  border-color: var(--df-text-disabled);
  color: var(--df-text-primary);
  background: var(--df-secondary-bg);
  
  &:hover {
    border-color: var(--df-accent-primary);
    color: var(--df-accent-primary);
  }
  
  .anticon {
    margin-right: var(--df-spacing-xs);
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
    
    .ant-btn {
      margin-right: var(--df-spacing-sm);
    }
  }
}

:deep(.ant-tag) {
  border-radius: var(--df-radius-sm);
  font-size: var(--df-font-size-xs);
  
  &.ant-tag-success {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--df-accent-success);
    color: var(--df-accent-success);
  }
}

:deep(.ant-upload) {
  .ant-upload-btn {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    box-shadow: none !important;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .profile-details {
    max-width: 100%;
    padding: 0 var(--df-spacing-md);
  }
  
  .profile-card {
    margin: 0;
    
    :deep(.ant-card-body) {
      padding: var(--df-spacing-lg);
    }
  }
  
  .contact-item {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--df-spacing-sm);
  }
}
</style>