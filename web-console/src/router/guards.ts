/**
 * 路由守卫
 * 处理认证检查、权限控制和页面标题更新
 */

import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { message } from 'ant-design-vue'

export function setupRouterGuards(router: Router) {
  // 全局前置守卫
  router.beforeEach(async (to, from, next) => {
    const authStore = useAuthStore()

    // 更新页面标题
    if (to.meta.title) {
      document.title = to.meta.title as string
    }

    // 检查是否需要认证
    if (to.meta.requiresAuth) {
      if (!authStore.isLoggedIn || !authStore.userToken) {
        message.warning('请先登录')
        next({
          path: '/login',
          query: { redirect: to.fullPath }
        })
        return
      }
    }

    // 如果已登录且访问登录/注册页面，重定向到工作台
    if ((to.name === 'Login' || to.name === 'Register') && authStore.isLoggedIn) {
      next('/workbench')
      return
    }

    // 权限检查（未来扩展）
    if (to.meta.roles && Array.isArray(to.meta.roles) && to.meta.roles.length > 0) {
      const userRole = authStore.userInfo?.role
      if (!userRole || !to.meta.roles.includes(userRole)) {
        message.error('没有权限访问该页面')
        next('/workbench')
        return
      }
    }

    next()
  })

  // 全局后置钩子
  router.afterEach((to) => {
    // 页面加载完成后的处理
    console.log(`导航到: ${to.fullPath}`)
  })

  // 路由错误处理
  router.onError((error) => {
    console.error('路由错误:', error)
    message.error('页面加载失败')
  })
}
