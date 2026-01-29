<template>
  <div class="api-management-page">
    <div class="page-header">
      <h1>API 管理</h1>
    </div>

    <div class="page-content">
      <a-tabs v-model:activeKey="activeTab">
        <a-tab-pane key="keys" tab="我的API Key">
          <div class="api-keys-section">
            <div class="section-header">
              <a-button type="primary" @click="generateApiKey">生成新的 API Key</a-button>
            </div>

            <a-table
              :columns="keysColumns"
              :data-source="apiKeysData"
              :pagination="false"
            >
              <template #bodyCell="{ column, record }">
                <template v-if="column.key === 'key'">
                  <span class="api-key-hidden" @click="showFullKey(record.id)">
                    {{ maskApiKey(record.key) }}
                  </span>
                </template>
                <template v-else-if="column.key === 'status'">
                  <a-switch v-model:checked="record.enabled" @change="toggleKeyStatus(record.id)" />
                </template>
                <template v-else-if="column.key === 'actions'">
                  <a-space>
                    <a-popconfirm
                      title="确定删除这个API Key吗？"
                      @confirm="deleteApiKey(record.id)"
                    >
                      <a-button size="small" danger>删除</a-button>
                    </a-popconfirm>
                    <a-button size="small" @click="rotateApiKey(record.id)">轮换</a-button>
                  </a-space>
                </template>
              </template>
            </a-table>
          </div>
        </a-tab-pane>

        <a-tab-pane key="stats" tab="API 调用统计">
          <div class="api-stats-section">
            <div class="stats-filters">
              <a-select v-model:value="timeRange" style="width: 200px">
                <a-select-option value="7d">近7天</a-select-option>
                <a-select-option value="30d">近30天</a-select-option>
                <a-select-option value="90d">近90天</a-select-option>
              </a-select>
            </div>

            <div class="stats-charts">
              <a-card title="调用次数统计" class="chart-card">
                <div class="chart-placeholder">
                  <p>图表功能开发中...</p>
                </div>
              </a-card>
            </div>

            <div class="call-logs">
              <h3>API 调用日志</h3>
              <a-input-search
                v-model:value="logSearch"
                placeholder="筛选日志..."
                style="width: 300px; margin-bottom: 16px"
              />

              <a-table
                :columns="logsColumns"
                :data-source="callLogsData"
                :pagination="logsPagination"
              >
                <template #bodyCell="{ column, record }">
                  <template v-if="column.key === 'status'">
                    <a-tag :color="record.status === 200 ? 'green' : 'red'">
                      {{ record.status }}
                    </a-tag>
                  </template>
                </template>
              </a-table>
            </div>
          </div>
        </a-tab-pane>
      </a-tabs>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { message } from 'ant-design-vue'

const activeTab = ref('keys')
const timeRange = ref('7d')
const logSearch = ref('')

const apiKeysData = ref([
  {
    id: '1',
    key: 'dfk_1234567890abcdef1234567890abcdef12345678',
    created: '2024-09-10 10:30',
    lastUsed: '2024-09-14 14:20',
    enabled: true
  },
  {
    id: '2',
    key: 'dfk_abcdef1234567890abcdef1234567890abcdef12',
    created: '2024-09-08 15:45',
    lastUsed: '2024-09-13 09:15',
    enabled: false
  }
])

const callLogsData = ref([
  {
    id: '1',
    time: '2024-09-14 14:20:15',
    templateId: 'template_001',
    apiKey: 'dfk_12345***',
    status: 200,
    duration: '1.2s'
  },
  {
    id: '2',
    time: '2024-09-14 13:45:32',
    templateId: 'template_002',
    apiKey: 'dfk_12345***',
    status: 500,
    duration: '0.8s'
  }
])

const keysColumns = [
  { title: 'API Key', dataIndex: 'key', key: 'key' },
  { title: '创建时间', dataIndex: 'created', key: 'created' },
  { title: '最近使用', dataIndex: 'lastUsed', key: 'lastUsed' },
  { title: '状态', dataIndex: 'status', key: 'status' },
  { title: '操作', key: 'actions', width: 200 }
]

const logsColumns = [
  { title: '调用时间', dataIndex: 'time', key: 'time' },
  { title: '模板ID', dataIndex: 'templateId', key: 'templateId' },
  { title: 'API Key', dataIndex: 'apiKey', key: 'apiKey' },
  { title: '状态码', dataIndex: 'status', key: 'status' },
  { title: '耗时', dataIndex: 'duration', key: 'duration' }
]

const logsPagination = ref({
  current: 1,
  pageSize: 10,
  total: 2,
  showSizeChanger: true,
  showTotal: (total: number) => `共 ${total} 条记录`
})

const maskApiKey = (key: string) => {
  return key.slice(0, 8) + '***' + key.slice(-4)
}

const showFullKey = (id: string) => {
  message.info('点击显示完整API Key功能开发中')
}

const generateApiKey = async () => {
  try {
    message.success('新的API Key已生成')
    // 刷新列表
  } catch (error) {
    message.error('生成失败')
  }
}

const toggleKeyStatus = (id: string) => {
  message.info('API Key状态已切换')
}

const deleteApiKey = async (id: string) => {
  try {
    message.success('API Key删除成功')
    // 刷新列表
  } catch (error) {
    message.error('删除失败')
  }
}

const rotateApiKey = async (id: string) => {
  try {
    message.success('API Key轮换成功')
    // 刷新列表
  } catch (error) {
    message.error('轮换失败')
  }
}

onMounted(() => {
  // 初始化数据
})
</script>

<style scoped lang="less">
.api-management-page {
  min-height: 100vh;
  background: var(--df-primary-bg);
  padding: var(--df-spacing-lg);
}

.page-header {
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

  :deep(.ant-tabs) {
    .ant-tabs-nav {
      .ant-tabs-tab {
        color: var(--df-text-secondary);

        &.ant-tabs-tab-active {
          color: var(--df-accent-primary);
        }
      }

      .ant-tabs-ink-bar {
        background: var(--df-accent-primary);
      }
    }
  }
}

.api-keys-section {
  .section-header {
    margin-bottom: var(--df-spacing-lg);
  }
}

.api-key-hidden {
  font-family: monospace;
  cursor: pointer;
  color: var(--df-accent-primary);

  &:hover {
    color: var(--df-accent-success);
  }
}

.api-stats-section {
  .stats-filters {
    margin-bottom: var(--df-spacing-lg);
  }

  .stats-charts {
    margin-bottom: var(--df-spacing-xl);
  }

  .chart-card {
    background: transparent;
    border: 1px solid var(--df-text-disabled);

    :deep(.ant-card-head) {
      background: transparent;
      border-bottom-color: var(--df-text-disabled);

      .ant-card-head-title {
        color: var(--df-text-primary);
      }
    }

    .chart-placeholder {
      height: 200px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: var(--df-text-secondary);
    }
  }

  .call-logs {
    h3 {
      color: var(--df-text-primary);
      margin-bottom: var(--df-spacing-md);
    }
  }
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
