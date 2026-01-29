<template>
  <div class="app-layout">
    <!-- 顶部导航栏 -->
    <header class="app-header" v-if="shouldShowHeader">
      <div class="header-content">
        <div class="header-left">
          <router-link to="/workbench" class="logo-link">
            <h1 class="app-title">DataForge</h1>
          </router-link>
        </div>

        <nav class="main-nav">
          <router-link to="/workbench" class="nav-item">
            <DatabaseOutlined />
            <span>工作台</span>
          </router-link>
          <router-link to="/templates" class="nav-item">
            <FileTextOutlined />
            <span>模板管理</span>
          </router-link>
          <router-link to="/api" class="nav-item">
            <ApiOutlined />
            <span>API管理</span>
          </router-link>
        </nav>

        <div class="header-right">
          <a-dropdown v-if="authStore.isAuthenticated">
            <a-button type="text" class="user-menu">
              <a-avatar size="small" :src="authStore.userInfo?.avatar">
                {{ authStore.userInfo?.name?.charAt(0) || 'U' }}
              </a-avatar>
              <span class="username">{{ authStore.userInfo?.name || '用户' }}</span>
              <DownOutlined />
            </a-button>
            <template #overlay>
              <a-menu>
                <a-menu-item @click="goToProfile">
                  <UserOutlined />
                  个人中心
                </a-menu-item>
                <a-menu-divider />
                <a-menu-item @click="handleLogout">
                  <LogoutOutlined />
                  退出登录
                </a-menu-item>
              </a-menu>
            </template>
          </a-dropdown>

          <router-link v-else to="/login" class="login-btn">
            <a-button type="primary">登录</a-button>
          </router-link>
        </div>
      </div>
    </header>

    <!-- 主要内容区域 -->
    <main class="app-main" :class="{ 'with-header': shouldShowHeader }">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Modal } from 'ant-design-vue'
import {
  DatabaseOutlined, FileTextOutlined, ApiOutlined,
  UserOutlined, LogoutOutlined, DownOutlined
} from '@ant-design/icons-vue'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

// 计算是否显示头部导航
const shouldShowHeader = computed(() => {
  const hideHeaderRoutes = ['/login', '/register', '/reset-password']
  return !hideHeaderRoutes.includes(route.path)
})

// 导航方法
const goToProfile = () => {
  router.push('/profile')
}

const handleLogout = () => {
  Modal.confirm({
    title: '确认退出',
    content: '确定要退出登录吗？',
    okText: '确定',
    cancelText: '取消',
    onOk() {
      authStore.logout()
      router.push('/login')
    }
  })
}
</script>

<style scoped lang="less">
.app-layout {
  min-height: 100vh;
  background: var(--df-primary-bg);
}

.app-header {
  background: var(--df-secondary-bg);
  border-bottom: 1px solid var(--df-text-disabled);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;

  .header-content {
    max-width: 1400px;
    margin: 0 auto;
    padding: 0 var(--df-spacing-lg);
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 64px;
  }

  .header-left {
    .logo-link {
      text-decoration: none;

      .app-title {
        color: var(--df-accent-primary);
        font-size: var(--df-font-size-xl);
        font-weight: 700;
        margin: 0;
        background: linear-gradient(135deg, var(--df-accent-primary), var(--df-accent-secondary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
    }
  }

  .main-nav {
    display: flex;
    gap: var(--df-spacing-md);

    .nav-item {
      display: flex;
      align-items: center;
      gap: var(--df-spacing-xs);
      padding: var(--df-spacing-sm) var(--df-spacing-md);
      color: var(--df-text-secondary);
      text-decoration: none;
      border-radius: var(--df-radius-md);
      transition: all 0.2s ease;

      &:hover {
        color: var(--df-text-primary);
        background: rgba(139, 92, 246, 0.1);
      }

      &.router-link-active {
        color: var(--df-accent-primary);
        background: rgba(139, 92, 246, 0.15);
      }

      span {
        font-weight: 500;
      }
    }
  }

  .header-right {
    .user-menu {
      display: flex;
      align-items: center;
      gap: var(--df-spacing-xs);
      color: var(--df-text-primary);

      .username {
        font-weight: 500;
      }
    }

    .login-btn {
      text-decoration: none;
    }
  }
}

.app-main {
  min-height: 100vh;

  &.with-header {
    padding-top: 64px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .app-header {
    .header-content {
      padding: 0 var(--df-spacing-md);
    }

    .main-nav {
      display: none; // 在移动端隐藏导航，可以后续添加移动端菜单
    }
  }
}

@media (max-width: 480px) {
  .app-header {
    .header-content {
      .app-title {
        font-size: var(--df-font-size-lg);
      }

      .user-menu .username {
        display: none;
      }
    }
  }
}
</style>
