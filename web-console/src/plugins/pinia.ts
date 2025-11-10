/**
 * Pinia 状态管理配置
 * 包含持久化插件和全局状态配置
 */

import { createPinia } from 'pinia'
import { createPersistedState } from 'pinia-plugin-persistedstate'

const pinia = createPinia()

// 配置持久化插件
pinia.use(
  createPersistedState({
    // 存储键名前缀
    key: (id) => `dataforge_${id}`,
    
    // 存储方式
    storage: localStorage,
    
    // 序列化配置
    serializer: {
      serialize: JSON.stringify,
      deserialize: JSON.parse
    }
  })
)

export default pinia