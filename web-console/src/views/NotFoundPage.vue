<template>
  <div class="not-found-page">
    <a-result
      status="404"
      title="404"
      sub-title="抱歉，您访问的页面不存在。"
    >
      <template #extra>
        <a-button type="primary" @click="goHome">返回首页</a-button>
      </template>
    </a-result>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const goHome = () => {
  router.push('/workbench')
}
</script>

<style scoped lang="less">
.not-found-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--df-primary-bg);
  
  :deep(.ant-result) {
    .ant-result-title {
      color: var(--df-text-primary);
    }
    
    .ant-result-subtitle {
      color: var(--df-text-secondary);
    }
  }
}
</style>