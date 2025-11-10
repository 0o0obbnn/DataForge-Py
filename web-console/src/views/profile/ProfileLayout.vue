<template>
  <div class="profile-layout">
    <a-layout>
      <a-layout-sider width="240" theme="dark" class="profile-sider">
        <a-menu
          v-model:selectedKeys="selectedKeys"
          mode="inline"
          @select="handleMenuSelect"
        >
          <a-menu-item key="details">
            <span>个人资料</span>
          </a-menu-item>
          <a-menu-item key="security">
            <span>账户安全</span>
          </a-menu-item>
          <a-menu-item key="history">
            <span>登录历史</span>
          </a-menu-item>
        </a-menu>
      </a-layout-sider>
      
      <a-layout>
        <a-layout-content class="profile-content">
          <router-view />
        </a-layout-content>
      </a-layout>
    </a-layout>
  </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const selectedKeys = ref(['details'])

// 根据路由更新选中的菜单项
watch(() => route.name, (newName) => {
  if (newName === 'ProfileDetails') selectedKeys.value = ['details']
  else if (newName === 'AccountSecurity') selectedKeys.value = ['security']
  else if (newName === 'LoginHistory') selectedKeys.value = ['history']
}, { immediate: true })

const handleMenuSelect = ({ key }: { key: string }) => {
  router.push({ name: `${key === 'details' ? 'ProfileDetails' : key === 'security' ? 'AccountSecurity' : 'LoginHistory'}` })
}
</script>

<style scoped lang="less">
.profile-layout {
  min-height: 100vh;
  background: var(--df-primary-bg);
  
  .ant-layout {
    background: transparent;
  }
}

.profile-sider {
  background: var(--df-primary-bg) !important;
  border-right: 1px solid var(--df-text-disabled);
}

.profile-content {
  padding: var(--df-spacing-lg);
  background: var(--df-primary-bg);
}
</style>