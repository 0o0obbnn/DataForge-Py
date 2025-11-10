<template>
  <div class="login-history">
    <a-card title="登录历史" class="history-card">
      <template #extra>
        <a-space>
          <a-button @click="exportHistory" :loading="exportLoading" size="small">
            <DownloadOutlined />
            导出
          </a-button>
          <a-button @click="refreshHistory" :loading="loading" size="small">
            <ReloadOutlined />
            刷新
          </a-button>
        </a-space>
      </template>
      
      <!-- 筛选器 -->
      <div class="filter-section">
        <a-row :gutter="[16, 16]">
          <a-col :xs="24" :sm="12" :md="6">
            <a-select
              v-model:value="filters.status"
              placeholder="登录状态"
              allow-clear
              style="width: 100%"
              @change="handleFilterChange"
            >
              <a-select-option value="success">成功</a-select-option>
              <a-select-option value="failed">失败</a-select-option>
              <a-select-option value="suspicious">可疑</a-select-option>
            </a-select>
          </a-col>
          
          <a-col :xs="24" :sm="12" :md="6">
            <a-select
              v-model:value="filters.deviceType"
              placeholder="设备类型"
              allow-clear
              style="width: 100%"
              @change="handleFilterChange"
            >
              <a-select-option value="desktop">桌面端</a-select-option>
              <a-select-option value="mobile">移动端</a-select-option>
              <a-select-option value="tablet">平板</a-select-option>
            </a-select>
          </a-col>
          
          <a-col :xs="24" :sm="12" :md="8">
            <a-range-picker
              v-model:value="filters.timeRange"
              format="YYYY-MM-DD"
              style="width: 100%"
              @change="handleFilterChange"
              :placeholder="['开始日期', '结束日期']"
            />
          </a-col>
          
          <a-col :xs="24" :sm="12" :md="4">
            <a-button @click="clearFilters" style="width: 100%">
              <ClearOutlined />
              清除筛选
            </a-button>
          </a-col>
        </a-row>
      </div>
      
      <!-- 统计信息 -->
      <div class="stats-section">
        <a-row :gutter="16">
          <a-col :xs="12" :sm="6">
            <a-statistic 
              title="总登录次数" 
              :value="stats.totalLogins" 
              :value-style="{ color: 'var(--df-text-primary)' }"
            />
          </a-col>
          <a-col :xs="12" :sm="6">
            <a-statistic 
              title="成功登录" 
              :value="stats.successLogins" 
              :value-style="{ color: 'var(--df-accent-success)' }"
            />
          </a-col>
          <a-col :xs="12" :sm="6">
            <a-statistic 
              title="失败登录" 
              :value="stats.failedLogins" 
              :value-style="{ color: 'var(--df-accent-error)' }"
            />
          </a-col>
          <a-col :xs="12" :sm="6">
            <a-statistic 
              title="可疑活动" 
              :value="stats.suspiciousLogins" 
              :value-style="{ color: 'var(--df-accent-warning)' }"
            />
          </a-col>
        </a-row>
      </div>
      
      <!-- 数据表格 -->
      <a-table
        :columns="columns"
        :data-source="filteredHistoryData"
        :pagination="pagination"
        :loading="loading"
        @change="handleTableChange"
        :scroll="{ x: 800 }"
        size="small"
      >
        <template #bodyCell="{ column, record }">
          <!-- 状态列 -->
          <template v-if="column.key === 'status'">
            <a-tag :color="getStatusColor(record.status)" size="small">
              <component :is="getStatusIcon(record.status)" />
              {{ getStatusText(record.status) }}
            </a-tag>
          </template>
          
          <!-- 设备列 -->
          <template v-if="column.key === 'device'">
            <div class="device-info">
              <component :is="getDeviceIcon(record.deviceType)" class="device-icon" />
              <div class="device-details">
                <div class="device-name">{{ record.device }}</div>
                <div class="device-os">{{ record.os }}</div>
              </div>
            </div>
          </template>
          
          <!-- 位置列 -->
          <template v-if="column.key === 'location'">
            <div class="location-info">
              <EnvironmentOutlined class="location-icon" />
              <div>
                <div class="location-city">{{ record.location }}</div>
                <div class="location-ip">{{ record.ip }}</div>
              </div>
            </div>
          </template>
          
          <!-- 时间列 -->
          <template v-if="column.key === 'time'">
            <div class="time-info">
              <div class="time-date">{{ formatDate(record.time) }}</div>
              <div class="time-relative">{{ getRelativeTime(record.time) }}</div>
            </div>
          </template>
          
          <!-- 操作列 -->
          <template v-if="column.key === 'actions'">
            <a-space>
              <a-button 
                type="text" 
                size="small"
                @click="showLocationDetails(record)"
                title="查看位置详情"
              >
                <EnvironmentOutlined />
              </a-button>
              <a-button 
                v-if="record.status === 'suspicious'" 
                type="text" 
                size="small"
                @click="markAsSafe(record)"
                title="标记为安全"
              >
                <SafetyCertificateOutlined />
              </a-button>
              <a-button 
                v-if="record.status !== 'failed'" 
                type="text" 
                danger 
                size="small"
                @click="reportSuspicious(record)"
                title="举报可疑"
              >
                <ExclamationCircleOutlined />
              </a-button>
            </a-space>
          </template>
        </template>
      </a-table>
    </a-card>
    
    <!-- 位置详情弹窗 -->
    <a-modal
      v-model:open="locationModalVisible"
      title="登录位置详情"
      :footer="null"
      width="600px"
    >
      <div v-if="selectedRecord" class="location-details">
        <a-descriptions :column="2" bordered size="small">
          <a-descriptions-item label="IP地址">
            {{ selectedRecord.ip }}
          </a-descriptions-item>
          <a-descriptions-item label="ISP">
            {{ selectedRecord.isp || '未知' }}
          </a-descriptions-item>
          <a-descriptions-item label="国家/地区">
            {{ selectedRecord.country || '中国' }}
          </a-descriptions-item>
          <a-descriptions-item label="省/市">
            {{ selectedRecord.location }}
          </a-descriptions-item>
          <a-descriptions-item label="经纬度" :span="2">
            {{ selectedRecord.coordinates || '暂无数据' }}
          </a-descriptions-item>
          <a-descriptions-item label="时区" :span="2">
            {{ selectedRecord.timezone || 'Asia/Shanghai' }}
          </a-descriptions-item>
        </a-descriptions>
        
        <div class="security-assessment">
          <h4>安全评估</h4>
          <a-row :gutter="16">
            <a-col :span="12">
              <div class="risk-indicator">
                <span class="risk-label">风险等级:</span>
                <a-tag :color="getRiskColor(selectedRecord.riskLevel)">
                  {{ getRiskText(selectedRecord.riskLevel) }}
                </a-tag>
              </div>
            </a-col>
            <a-col :span="12">
              <div class="risk-indicator">
                <span class="risk-label">首次登录:</span>
                <a-tag :color="selectedRecord.isFirstTime ? 'orange' : 'green'">
                  {{ selectedRecord.isFirstTime ? '是' : '否' }}
                </a-tag>
              </div>
            </a-col>
          </a-row>
          
          <div v-if="selectedRecord.riskFactors?.length" class="risk-factors">
            <h5>风险因素:</h5>
            <ul>
              <li v-for="factor in selectedRecord.riskFactors" :key="factor">
                {{ factor }}
              </li>
            </ul>
          </div>
        </div>
      </div>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { message } from 'ant-design-vue'
import {
  ReloadOutlined,
  DownloadOutlined,
  ClearOutlined,
  EnvironmentOutlined,
  SafetyCertificateOutlined,
  ExclamationCircleOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  WarningOutlined,
  DesktopOutlined,
  MobileOutlined,
  TabletOutlined
} from '@ant-design/icons-vue'
import type { Dayjs } from 'dayjs'
import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/zh-cn'

dayjs.extend(relativeTime)
dayjs.locale('zh-cn')

// 接口定义
interface LoginRecord {
  id: string
  time: string
  location: string
  device: string
  os: string
  deviceType: 'desktop' | 'mobile' | 'tablet'
  ip: string
  status: 'success' | 'failed' | 'suspicious'
  isp?: string
  country?: string
  coordinates?: string
  timezone?: string
  riskLevel: 'low' | 'medium' | 'high'
  isFirstTime: boolean
  riskFactors?: string[]
  userAgent: string
  sessionId: string
}

// 状态
const loading = ref(false)
const exportLoading = ref(false)
const locationModalVisible = ref(false)
const selectedRecord = ref<LoginRecord | null>(null)

// 筛选器
const filters = reactive({
  status: undefined as string | undefined,
  deviceType: undefined as string | undefined,
  timeRange: undefined as [Dayjs, Dayjs] | undefined
})

// 模拟数据
const historyData = ref<LoginRecord[]>([
  {
    id: '1',
    time: new Date().toISOString(),
    location: '北京市',
    device: 'Chrome 125.0',
    os: 'Windows 11',
    deviceType: 'desktop',
    ip: '59.172.25.89',
    status: 'success',
    isp: '中国联通',
    country: '中国',
    coordinates: '116.4074, 39.9042',
    timezone: 'Asia/Shanghai',
    riskLevel: 'low',
    isFirstTime: false,
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    sessionId: 'sess_1234567890'
  },
  {
    id: '2',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
    location: '上海市',
    device: 'Safari 17.0',
    os: 'macOS Sonoma',
    deviceType: 'desktop',
    ip: '60.173.25.100',
    status: 'success',
    isp: '中国电信',
    country: '中国',
    coordinates: '121.4737, 31.2304',
    timezone: 'Asia/Shanghai',
    riskLevel: 'low',
    isFirstTime: false,
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15',
    sessionId: 'sess_0987654321'
  },
  {
    id: '3',
    time: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(),
    location: '广州市',
    device: 'Chrome Mobile',
    os: 'Android 14',
    deviceType: 'mobile',
    ip: '14.215.158.74',
    status: 'suspicious',
    isp: '中国移动',
    country: '中国',
    coordinates: '113.2644, 23.1291',
    timezone: 'Asia/Shanghai',
    riskLevel: 'medium',
    isFirstTime: true,
    riskFactors: ['首次从该设备登录', '异常登录时间', '地理位置异常'],
    userAgent: 'Mozilla/5.0 (Linux; Android 14; SM-G991B) AppleWebKit/537.36',
    sessionId: 'sess_1357924680'
  },
  {
    id: '4',
    time: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
    location: '深圳市',
    device: 'Firefox 119.0',
    os: 'Ubuntu 22.04',
    deviceType: 'desktop',
    ip: '183.2.172.185',
    status: 'failed',
    isp: '中国电信',
    country: '中国',
    riskLevel: 'high',
    isFirstTime: true,
    riskFactors: ['密码错误', '可疑IP地址', '多次尝试失败'],
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64; rv:119.0) Gecko/20100101 Firefox/119.0',
    sessionId: 'sess_2468135790'
  }
])

// 表格列定义
const columns = [
  {
    title: '登录时间',
    dataIndex: 'time',
    key: 'time',
    width: 180,
    sorter: (a: LoginRecord, b: LoginRecord) => new Date(a.time).getTime() - new Date(b.time).getTime()
  },
  {
    title: '位置/IP',
    dataIndex: 'location',
    key: 'location',
    width: 200
  },
  {
    title: '设备信息',
    dataIndex: 'device',
    key: 'device',
    width: 250
  },
  {
    title: '状态',
    dataIndex: 'status',
    key: 'status',
    width: 120,
    filters: [
      { text: '成功', value: 'success' },
      { text: '失败', value: 'failed' },
      { text: '可疑', value: 'suspicious' }
    ]
  },
  {
    title: '操作',
    key: 'actions',
    width: 120,
    fixed: 'right'
  }
]

// 分页配置
const pagination = ref({
  current: 1,
  pageSize: 10,
  total: 0,
  showSizeChanger: true,
  showQuickJumper: true,
  showTotal: (total: number) => `共 ${total} 条记录`
})

// 计算属性
const filteredHistoryData = computed(() => {
  let data = [...historyData.value]
  
  // 状态筛选
  if (filters.status) {
    data = data.filter(item => item.status === filters.status)
  }
  
  // 设备类型筛选
  if (filters.deviceType) {
    data = data.filter(item => item.deviceType === filters.deviceType)
  }
  
  // 时间范围筛选
  if (filters.timeRange && filters.timeRange.length === 2) {
    const [start, end] = filters.timeRange
    data = data.filter(item => {
      const itemDate = dayjs(item.time)
      return itemDate.isAfter(start.startOf('day')) && itemDate.isBefore(end.endOf('day'))
    })
  }
  
  // 更新分页总数
  pagination.value.total = data.length
  
  return data
})

const stats = computed(() => {
  const data = filteredHistoryData.value
  return {
    totalLogins: data.length,
    successLogins: data.filter(item => item.status === 'success').length,
    failedLogins: data.filter(item => item.status === 'failed').length,
    suspiciousLogins: data.filter(item => item.status === 'suspicious').length
  }
})

// 工具函数
const getStatusColor = (status: string) => {
  switch (status) {
    case 'success': return 'success'
    case 'failed': return 'error'
    case 'suspicious': return 'warning'
    default: return 'default'
  }
}

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'success': return CheckCircleOutlined
    case 'failed': return CloseCircleOutlined
    case 'suspicious': return WarningOutlined
    default: return CheckCircleOutlined
  }
}

const getStatusText = (status: string) => {
  switch (status) {
    case 'success': return '成功'
    case 'failed': return '失败'
    case 'suspicious': return '可疑'
    default: return '未知'
  }
}

const getDeviceIcon = (deviceType: string) => {
  switch (deviceType) {
    case 'mobile': return MobileOutlined
    case 'tablet': return TabletOutlined
    case 'desktop':
    default: return DesktopOutlined
  }
}

const getRiskColor = (riskLevel: string) => {
  switch (riskLevel) {
    case 'low': return 'success'
    case 'medium': return 'warning'
    case 'high': return 'error'
    default: return 'default'
  }
}

const getRiskText = (riskLevel: string) => {
  switch (riskLevel) {
    case 'low': return '低风险'
    case 'medium': return '中风险'
    case 'high': return '高风险'
    default: return '未知'
  }
}

const formatDate = (dateString: string) => {
  return dayjs(dateString).format('YYYY-MM-DD HH:mm:ss')
}

const getRelativeTime = (dateString: string) => {
  return dayjs(dateString).fromNow()
}

// 事件处理
const refreshHistory = async () => {
  loading.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    message.success('登录历史已刷新')
  } catch (error) {
    console.error('刷新失败:', error)
    message.error('刷新失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const exportHistory = async () => {
  exportLoading.value = true
  try {
    // 模拟导出
    await new Promise(resolve => setTimeout(resolve, 1500))
    message.success('登录历史已导出')
  } catch (error) {
    console.error('导出失败:', error)
    message.error('导出失败，请稍后重试')
  } finally {
    exportLoading.value = false
  }
}

const handleFilterChange = () => {
  // 重置分页
  pagination.value.current = 1
}

const clearFilters = () => {
  filters.status = undefined
  filters.deviceType = undefined
  filters.timeRange = undefined
  pagination.value.current = 1
}

const handleTableChange = (pag: any, tableFilters: any, sorter: any) => {
  pagination.value.current = pag.current
  pagination.value.pageSize = pag.pageSize
  
  // 处理表格筛选
  if (tableFilters.status) {
    filters.status = tableFilters.status[0]
  }
}

const showLocationDetails = (record: LoginRecord) => {
  selectedRecord.value = record
  locationModalVisible.value = true
}

const markAsSafe = async (record: LoginRecord) => {
  try {
    loading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 更新记录状态
    const index = historyData.value.findIndex(item => item.id === record.id)
    if (index !== -1) {
      historyData.value[index].status = 'success'
      historyData.value[index].riskLevel = 'low'
      historyData.value[index].riskFactors = []
    }
    
    message.success('已标记为安全登录')
  } catch (error) {
    message.error('操作失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const reportSuspicious = async (record: LoginRecord) => {
  try {
    loading.value = true
    
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 500))
    
    // 更新记录状态
    const index = historyData.value.findIndex(item => item.id === record.id)
    if (index !== -1) {
      historyData.value[index].status = 'suspicious'
      historyData.value[index].riskLevel = 'high'
      if (!historyData.value[index].riskFactors) {
        historyData.value[index].riskFactors = []
      }
      historyData.value[index].riskFactors!.push('用户举报')
    }
    
    message.success('已举报为可疑活动')
  } catch (error) {
    message.error('操作失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 组件挂载时初始化数据
onMounted(() => {
  pagination.value.total = historyData.value.length
})
</script>

<style scoped lang="less">
.login-history {
  max-width: 1200px;
  margin: 0 auto;
}

.history-card {
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

// 筛选器区域
.filter-section {
  margin-bottom: var(--df-spacing-xl);
  padding: var(--df-spacing-lg);
  background: var(--df-primary-bg);
  border: 1px solid var(--df-text-disabled);
  border-radius: var(--df-radius-md);
}

// 统计信息区域
.stats-section {
  margin-bottom: var(--df-spacing-xl);
  padding: var(--df-spacing-lg);
  background: var(--df-primary-bg);
  border: 1px solid var(--df-text-disabled);
  border-radius: var(--df-radius-md);
  
  :deep(.ant-statistic) {
    .ant-statistic-title {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-sm);
      margin-bottom: var(--df-spacing-xs);
    }
    
    .ant-statistic-content {
      font-weight: 600;
      font-size: var(--df-font-size-xl);
    }
  }
}

// 表格样式
:deep(.ant-table) {
  background: transparent;
  
  .ant-table-thead > tr > th {
    background: var(--df-primary-bg);
    color: var(--df-text-primary);
    border-bottom-color: var(--df-text-disabled);
    font-weight: 600;
    
    &:hover {
      background: var(--df-primary-bg);
    }
  }
  
  .ant-table-tbody > tr > td {
    background: transparent;
    color: var(--df-text-primary);
    border-bottom-color: var(--df-text-disabled);
  }
  
  .ant-table-tbody > tr:hover > td {
    background: rgba(142, 93, 255, 0.05);
  }
  
  .ant-table-tbody > tr.ant-table-row-selected > td {
    background: rgba(142, 93, 255, 0.1);
  }
}

// 表格内容样式
.device-info {
  display: flex;
  align-items: center;
  gap: var(--df-spacing-sm);
  
  .device-icon {
    font-size: var(--df-font-size-lg);
    color: var(--df-accent-primary);
  }
  
  .device-details {
    .device-name {
      color: var(--df-text-primary);
      font-weight: 500;
      font-size: var(--df-font-size-sm);
    }
    
    .device-os {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-xs);
    }
  }
}

.location-info {
  display: flex;
  align-items: center;
  gap: var(--df-spacing-sm);
  
  .location-icon {
    color: var(--df-accent-primary);
    font-size: var(--df-font-size-base);
  }
  
  .location-city {
    color: var(--df-text-primary);
    font-weight: 500;
    font-size: var(--df-font-size-sm);
  }
  
  .location-ip {
    color: var(--df-text-secondary);
    font-size: var(--df-font-size-xs);
    font-family: 'JetBrains Mono', 'Consolas', monospace;
  }
}

.time-info {
  .time-date {
    color: var(--df-text-primary);
    font-size: var(--df-font-size-sm);
    font-weight: 500;
  }
  
  .time-relative {
    color: var(--df-text-secondary);
    font-size: var(--df-font-size-xs);
  }
}

// 位置详情弹窗
.location-details {
  .security-assessment {
    margin-top: var(--df-spacing-lg);
    padding-top: var(--df-spacing-lg);
    border-top: 1px solid var(--df-text-disabled);
    
    h4 {
      color: var(--df-text-primary);
      margin-bottom: var(--df-spacing-md);
      font-weight: 600;
    }
    
    h5 {
      color: var(--df-text-primary);
      margin: var(--df-spacing-md) 0 var(--df-spacing-sm) 0;
      font-weight: 600;
    }
    
    .risk-indicator {
      display: flex;
      align-items: center;
      gap: var(--df-spacing-sm);
      margin-bottom: var(--df-spacing-sm);
      
      .risk-label {
        color: var(--df-text-secondary);
        font-size: var(--df-font-size-sm);
        min-width: 80px;
      }
    }
    
    .risk-factors {
      ul {
        margin: 0;
        padding-left: var(--df-spacing-lg);
        color: var(--df-text-primary);
        
        li {
          margin-bottom: var(--df-spacing-xs);
          color: var(--df-accent-error);
        }
      }
    }
  }
}

// 全局组件样式
:deep(.ant-select) {
  .ant-select-selector {
    background: var(--df-primary-bg);
    border-color: var(--df-text-disabled);
    color: var(--df-text-primary);
    
    &:hover, &:focus {
      border-color: var(--df-accent-primary);
    }
    
    .ant-select-selection-placeholder {
      color: var(--df-text-secondary);
    }
  }
  
  &.ant-select-focused .ant-select-selector {
    border-color: var(--df-accent-primary);
    box-shadow: 0 0 0 2px rgba(142, 93, 255, 0.1);
  }
}

:deep(.ant-picker) {
  background: var(--df-primary-bg);
  border-color: var(--df-text-disabled);
  
  &:hover, &:focus {
    border-color: var(--df-accent-primary);
  }
  
  &.ant-picker-focused {
    border-color: var(--df-accent-primary);
    box-shadow: 0 0 0 2px rgba(142, 93, 255, 0.1);
  }
  
  .ant-picker-input > input {
    color: var(--df-text-primary);
    
    &::placeholder {
      color: var(--df-text-secondary);
    }
  }
  
  .ant-picker-separator {
    color: var(--df-text-secondary);
  }
}

:deep(.ant-btn) {
  border-color: var(--df-text-disabled);
  color: var(--df-text-primary);
  
  &:hover {
    border-color: var(--df-accent-primary);
    color: var(--df-accent-primary);
  }
  
  &.ant-btn-text {
    color: var(--df-text-secondary);
    
    &:hover {
      color: var(--df-accent-primary);
      background: rgba(142, 93, 255, 0.1);
    }
    
    &.ant-btn-dangerous {
      color: var(--df-accent-error);
      
      &:hover {
        color: var(--df-accent-error);
        background: rgba(239, 68, 68, 0.1);
      }
    }
  }
  
  .anticon {
    margin-right: var(--df-spacing-xs);
  }
}

:deep(.ant-tag) {
  border-radius: var(--df-radius-sm);
  font-size: var(--df-font-size-xs);
  font-weight: 500;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  
  &.ant-tag-success {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--df-accent-success);
    color: var(--df-accent-success);
  }
  
  &.ant-tag-error {
    background: rgba(239, 68, 68, 0.1);
    border-color: var(--df-accent-error);
    color: var(--df-accent-error);
  }
  
  &.ant-tag-warning {
    background: rgba(245, 158, 11, 0.1);
    border-color: #F59E0B;
    color: #F59E0B;
  }
  
  &.ant-tag-orange {
    background: rgba(251, 146, 60, 0.1);
    border-color: #FB923C;
    color: #FB923C;
  }
  
  &.ant-tag-green {
    background: rgba(16, 185, 129, 0.1);
    border-color: var(--df-accent-success);
    color: var(--df-accent-success);
  }
}

:deep(.ant-descriptions) {
  .ant-descriptions-item-label {
    color: var(--df-text-secondary);
    font-weight: 500;
  }
  
  .ant-descriptions-item-content {
    color: var(--df-text-primary);
  }
  
  &.ant-descriptions-bordered {
    .ant-descriptions-item-label {
      background: var(--df-primary-bg);
      border-color: var(--df-text-disabled);
    }
    
    .ant-descriptions-item-content {
      background: var(--df-secondary-bg);
      border-color: var(--df-text-disabled);
    }
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
}

:deep(.ant-pagination) {
  .ant-pagination-item {
    background: var(--df-primary-bg);
    border-color: var(--df-text-disabled);
    
    a {
      color: var(--df-text-primary);
    }
    
    &:hover {
      border-color: var(--df-accent-primary);
      
      a {
        color: var(--df-accent-primary);
      }
    }
    
    &.ant-pagination-item-active {
      background: var(--df-accent-primary);
      border-color: var(--df-accent-primary);
      
      a {
        color: white;
      }
    }
  }
  
  .ant-pagination-prev, .ant-pagination-next {
    .ant-pagination-item-link {
      background: var(--df-primary-bg);
      border-color: var(--df-text-disabled);
      color: var(--df-text-primary);
      
      &:hover {
        border-color: var(--df-accent-primary);
        color: var(--df-accent-primary);
      }
    }
  }
  
  .ant-pagination-options {
    .ant-select {
      .ant-select-selector {
        background: var(--df-primary-bg);
        border-color: var(--df-text-disabled);
        color: var(--df-text-primary);
      }
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .login-history {
    max-width: 100%;
    padding: 0 var(--df-spacing-md);
  }
}

@media (max-width: 768px) {
  .filter-section {
    .ant-row > .ant-col {
      margin-bottom: var(--df-spacing-sm);
    }
  }
  
  .stats-section {
    :deep(.ant-statistic) {
      text-align: center;
      margin-bottom: var(--df-spacing-md);
      
      .ant-statistic-content {
        font-size: var(--df-font-size-lg);
      }
    }
  }
  
  .device-info {
    flex-direction: column;
    align-items: flex-start;
    
    .device-details {
      width: 100%;
    }
  }
  
  .location-info {
    flex-direction: column;
    align-items: flex-start;
  }
  
  :deep(.ant-table) {
    .ant-table-tbody > tr > td {
      padding: var(--df-spacing-sm);
      font-size: var(--df-font-size-xs);
    }
  }
}

@media (max-width: 480px) {
  .history-card {
    :deep(.ant-card-body) {
      padding: var(--df-spacing-md);
    }
  }
  
  .filter-section,
  .stats-section {
    padding: var(--df-spacing-md);
  }
}
</style>