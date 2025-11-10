/**
 * 路由定义
 * 按照项目规范定义所有页面路由
 */

import type { RouteRecordRaw } from 'vue-router'
import type { RouteMeta } from '@/utils/types'

// 扩展路由元信息类型
declare module 'vue-router' {
  interface RouteMeta {
    title?: string
    requiresAuth?: boolean
    roles?: string[]
    keepAlive?: boolean
  }
}

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/workbench'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginPage.vue'),
    meta: {
      title: '登录 - DataForge',
      requiresAuth: false
    }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/auth/RegisterPage.vue'),
    meta: {
      title: '注册 - DataForge',
      requiresAuth: false
    }
  },
  {
    path: '/reset-password',
    name: 'ResetPassword',
    component: () => import('@/views/auth/ResetPasswordPage.vue'),
    meta: {
      title: '重置密码 - DataForge',
      requiresAuth: false
    }
  },
  {
    path: '/workbench',
    name: 'Workbench',
    component: () => import('@/views/workbench/WorkbenchPage.vue'),
    meta: {
      title: '数据生成工作台 - DataForge',
      requiresAuth: true
    }
  },
  {
    path: '/workbench/:templateId',
    name: 'WorkbenchTemplate',
    component: () => import('@/views/workbench/WorkbenchPage.vue'),
    meta: {
      title: '数据生成工作台 - DataForge',
      requiresAuth: true
    }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: () => import('@/views/profile/ProfileLayout.vue'),
    meta: {
      title: '个人中心 - DataForge',
      requiresAuth: true
    },
    children: [
      {
        path: '',
        redirect: 'details'
      },
      {
        path: 'details',
        name: 'ProfileDetails',
        component: () => import('@/views/profile/ProfileDetails.vue'),
        meta: {
          title: '个人资料'
        }
      },
      {
        path: 'security',
        name: 'AccountSecurity',
        component: () => import('@/views/profile/AccountSecurity.vue'),
        meta: {
          title: '账户安全'
        }
      },
      {
        path: 'history',
        name: 'LoginHistory',
        component: () => import('@/views/profile/LoginHistory.vue'),
        meta: {
          title: '登录历史'
        }
      }
    ]
  },
  {
    path: '/templates',
    name: 'Templates',
    component: () => import('@/views/templates/TemplateManager.vue'),
    meta: {
      title: '模板管理 - DataForge',
      requiresAuth: true
    }
  },
  {
    path: '/api',
    name: 'ApiManagement',
    component: () => import('@/views/api/ApiManagementPage.vue'),
    meta: {
      title: 'API管理 - DataForge',
      requiresAuth: true
    }
  },
  {
    path: '/test',
    name: 'DataForgeTest',
    component: () => import('@/views/DataForgeTest.vue'),
    meta: {
      title: 'DataForge API 测试 - DataForge',
      requiresAuth: true
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFoundPage.vue'),
    meta: {
      title: '页面未找到 - DataForge'
    }
  }
]

export default routes
