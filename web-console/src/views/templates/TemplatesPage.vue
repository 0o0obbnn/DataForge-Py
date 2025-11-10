<template>
  <div class="templates-page">
    <div class="page-header">
      <h1>模板管理</h1>
      <a-button type="primary" @click="createTemplate">新建模板</a-button>
    </div>
    
    <div class="page-content">
      <div class="filters">
        <a-space>
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索模板名称..."
            @search="handleSearch"
            style="width: 300px"
          />
          <a-select v-model:value="creatorFilter" placeholder="按创建者筛选" style="width: 200px">
            <a-select-option value="">所有创建者</a-select-option>
            <a-select-option value="me">我的模板</a-select-option>
          </a-select>
          <a-select v-model:value="sortBy" placeholder="按时间排序" style="width: 150px">
            <a-select-option value="created">最新创建</a-select-option>
            <a-select-option value="updated">最近修改</a-select-option>
          </a-select>
        </a-space>
      </div>
      
      <a-table
        :columns="columns"
        :data-source="templatesData"
        :pagination="pagination"
        :loading="loading"
        @change="handleTableChange"
      >
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'name'">
            <a @click="editTemplate(record.id)">{{ record.name }}</a>
          </template>
          <template v-else-if="column.key === 'actions'">
            <a-space>
              <a-button size="small" @click="editTemplate(record.id)">编辑</a-button>
              <a-button size="small" @click="copyTemplate(record.id)">复制</a-button>
              <a-button size="small" @click="shareTemplate(record.id)">分享</a-button>
              <a-button size="small" @click="getApiInfo(record.id)">获取API</a-button>
              <a-popconfirm
                title="确定删除这个模板吗？"
                @confirm="deleteTemplate(record.id)"
              >
                <a-button size="small" danger>删除</a-button>
              </a-popconfirm>
            </a-space>
          </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message } from 'ant-design-vue'

const router = useRouter()
const loading = ref(false)
const searchKeyword = ref('')
const creatorFilter = ref('')
const sortBy = ref('created')

const templatesData = ref([
  {
    key: '1',
    id: '1',
    name: '用户注册数据V2',
    creator: '我',
    created: '2024-09-14 10:30',
    updated: '2024-09-14 14:20',
    description: '包含完整用户注册信息的数据模板'
  },
  {
    key: '2',
    id: '2',
    name: '金融交易记录',
    creator: '张三',
    created: '2024-09-13 15:45',
    updated: '2024-09-13 16:10',
    description: '生成模拟金融交易数据'
  }
])

const columns = [
  {
    title: '模板名称',
    dataIndex: 'name',
    key: 'name',
  },
  {
    title: '创建者',
    dataIndex: 'creator',
    key: 'creator',
  },
  {
    title: '创建时间',
    dataIndex: 'created',
    key: 'created',
  },
  {
    title: '修改时间',
    dataIndex: 'updated',
    key: 'updated',
  },
  {
    title: '描述',
    dataIndex: 'description',
    key: 'description',
    ellipsis: true,
  },
  {
    title: '操作',
    key: 'actions',
    width: 300,
  }
]

const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 2,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条记录`
})

const createTemplate = () => {
  router.push('/workbench')
}

const editTemplate = (id: string) => {
  router.push(`/workbench/${id}`)
}

const copyTemplate = async (id: string) => {
  try {
    message.success('模板复制成功')
    // 刷新列表
  } catch (error) {
    message.error('复制失败')
  }
}

const shareTemplate = (id: string) => {
  message.info('分享功能开发中')
}

const getApiInfo = (id: string) => {
  message.info('API信息功能开发中')
}

const deleteTemplate = async (id: string) => {
  try {
    message.success('模板删除成功')
    // 刷新列表
  } catch (error) {
    message.error('删除失败')
  }
}

const handleSearch = (value: string) => {
  console.log('搜索:', value)
}

const handleTableChange = (pag: any) => {
  pagination.value.current = pag.current
  pagination.value.pageSize = pag.pageSize
  // 重新加载数据
}

onMounted(() => {
  // 加载模板列表
})
</script>

<style scoped lang="less">
.templates-page {
  min-height: 100vh;
  background: var(--df-primary-bg);
  padding: var(--df-spacing-lg);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--df-spacing-lg);
  
  h1 {
    color: var(--df-text-primary);
    font-size: var(--df-font-size-2xl);
    margin: 0;
  }
}

.page-content {
  background: var(--df-secondary-bg);
  border-radius: var(--df-radius-lg);
  padding: var(--df-spacing-lg);
  border: 1px solid var(--df-text-disabled);
}

.filters {
  margin-bottom: var(--df-spacing-lg);
}

:deep(.ant-table) {
  background: transparent;
  
  .ant-table-thead > tr > th {
    background: var(--df-primary-bg);
    color: var(--df-text-primary);
    border-bottom-color: var(--df-text-disabled);
  }
  
  .ant-table-tbody > tr > td {
    background: transparent;
    color: var(--df-text-primary);
    border-bottom-color: var(--df-text-disabled);
  }
  
  .ant-table-tbody > tr:hover > td {
    background: rgba(142, 93, 255, 0.1);
  }
}
</style>