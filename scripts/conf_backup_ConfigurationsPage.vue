<template>
  <div class="configurations-page">
    <div class="page-header">
      <div class="header-content">
        <h1 class="page-title">配置管理</h1>
        <p class="page-description">管理您的数据生成配置</p>
      </div>
      <div class="header-actions">
        <a-button type="primary" @click="createConfiguration">
          <template #icon>
            <PlusOutlined />
          </template>
          新建配置
        </a-button>
      </div>
    </div>

    <div class="page-content">
      <!-- 搜索和筛选 -->
      <div class="filter-section">
        <div class="filter-left">
          <a-input-search
            v-model:value="searchKeyword"
            placeholder="搜索配置名称..."
            style="width: 300px"
            @search="handleSearch"
          />
        </div>
        <div class="filter-right">
          <a-select
            v-model:value="sortBy"
            placeholder="排序方式"
            style="width: 150px"
            @change="handleSort"
          >
            <a-select-option value="updatedAt">最近更新</a-select-option>
            <a-select-option value="createdAt">创建时间</a-select-option>
            <a-select-option value="name">名称</a-select-option>
          </a-select>
        </div>
      </div>

      <!-- 配置列表 -->
      <div class="configurations-grid">
        <div
          v-for="config in filteredConfigurations"
          :key="config.id"
          class="config-card"
          @click="editConfiguration(config.id)"
        >
          <div class="card-header">
            <h3 class="card-title">{{ config.name }}</h3>
            <a-dropdown @click.stop>
              <template #overlay>
                <a-menu>
                  <a-menu-item @click="editConfiguration(config.id)">
                    <EditOutlined />
                    编辑
                  </a-menu-item>
                  <a-menu-item @click="duplicateConfiguration(config.id)">
                    <CopyOutlined />
                    复制
                  </a-menu-item>
                  <a-menu-item @click="exportConfiguration(config.id)">
                    <DownloadOutlined />
                    导出
                  </a-menu-item>
                  <a-menu-divider />
                  <a-menu-item @click="deleteConfiguration(config.id)" danger>
                    <DeleteOutlined />
                    删除
                  </a-menu-item>
                </a-menu>
              </template>
              <a-button type="text" size="small">
                <MoreOutlined />
              </a-button>
            </a-dropdown>
          </div>
          
          <p class="card-description">
            {{ config.description || '暂无描述' }}
          </p>
          
          <div class="card-meta">
            <div class="meta-left">
              <span class="meta-item">
                <ClockCircleOutlined />
                {{ formatTime(config.updatedAt) }}
              </span>
              <span class="meta-item">
                <UserOutlined />
                {{ config.createdBy }}
              </span>
            </div>
            <div class="meta-right">
              <a-tag :color="getFormatColor(config.settings.outputFormat)">
                {{ config.settings.outputFormat.toUpperCase() }}
              </a-tag>
            </div>
          </div>
          
          <div class="card-actions">
            <a-button size="small" @click.stop="runConfiguration(config.id)">
              <template #icon>
                <PlayCircleOutlined />
              </template>
              运行
            </a-button>
            <a-button size="small" @click.stop="editConfiguration(config.id)">
              <template #icon>
                <EditOutlined />
              </template>
              编辑
            </a-button>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="filteredConfigurations.length === 0" class="empty-state">
        <a-empty description="暂无配置">
          <a-button type="primary" @click="createConfiguration">
            创建第一个配置
          </a-button>
        </a-empty>
      </div>

      <!-- 分页 -->
      <div v-if="filteredConfigurations.length > 0" class="pagination-section">
        <a-pagination
          v-model:current="currentPage"
          v-model:page-size="pageSize"
          :total="totalConfigurations"
          show-size-changer
          show-quick-jumper
          :show-total="(total: number, range: [number, number]) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { message, Modal } from 'ant-design-vue';
import { useConfigurationStore } from '@/stores/configuration';
import { ConfigurationService } from '@/services/configuration';
import dayjs from 'dayjs';
import {
  PlusOutlined,
  EditOutlined,
  CopyOutlined,
  DeleteOutlined,
  DownloadOutlined,
  MoreOutlined,
  ClockCircleOutlined,
  UserOutlined,
  PlayCircleOutlined
} from '@ant-design/icons-vue';

const router = useRouter();
const configStore = useConfigurationStore();

const searchKeyword = ref('');
const sortBy = ref('updatedAt');
const currentPage = ref(1);
const pageSize = ref(12);

const filteredConfigurations = computed(() => {
  let configs = [...configStore.configurations];
  
  // 搜索过滤
  if (searchKeyword.value) {
    configs = configs.filter(config =>
      config.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
      (config.description && config.description.toLowerCase().includes(searchKeyword.value.toLowerCase()))
    );
  }
  
  // 排序
  configs.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name);
      case 'createdAt':
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
      case 'updatedAt':
      default:
        return new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime();
    }
  });
  
  // 分页
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return configs.slice(start, end);
});

const totalConfigurations = computed(() => configStore.configurations.length);

onMounted(async () => {
  await loadConfigurations();
});

const loadConfigurations = async () => {
  try {
    const response = await ConfigurationService.getConfigurations(currentPage.value, pageSize.value);
    // 将API数据同步到store
    configStore.configurations = response.configurations;
  } catch (_error) {
  void _error
>>>>>>> keep
     
    console.error('Failed to load configurations:', _error);
    message.error('加载配置列表失败');
  }
};

const createConfiguration = () => {
  router.push('/studio');
};

const editConfiguration = (id: string) => {
  router.push(`/studio/${id}`);
};

const duplicateConfiguration = async (id: string) => {
  try {
    const original = configStore.configurations.find(c => c.id === id);
    if (original) {
      const duplicatedConfig = await ConfigurationService.duplicateConfiguration(
        id, 
        `${original.name} (副本)`
      );
      configStore.configurations.push(duplicatedConfig);
      message.success('配置复制成功');
    }
  } catch (_error) {
     
    console.error('Duplicate configuration error:', _error);
    message.error('复制配置失败');
  }
};

const exportConfiguration = async (id: string) => {
  try {
    const config = configStore.configurations.find(c => c.id === id);
    if (config) {
      const dataStr = JSON.stringify(config, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `${config.name}.json`;
      link.click();
      URL.revokeObjectURL(url);
      message.success('配置导出成功');
    }
  } catch (_error) {
    message.error('导出失败');
  }
};

const deleteConfiguration = (id: string) => {
  const config = configStore.configurations.find(c => c.id === id);
  if (!config) return;
  
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除配置 "${config.name}" 吗？此操作不可恢复。`,
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    async onOk() {
      try {
        await ConfigurationService.deleteConfiguration(id);
        configStore.deleteConfiguration(id);
        message.success('配置删除成功');
      } catch (_error) {
         
        console.error('Delete configuration error:', _error);
        message.error('删除配置失败');
      }
    }
  });
};

const runConfiguration = async (id: string) => {
  try {
    message.info('正在启动生成任务...');
    // TODO: 实现运行逻辑
    router.push(`/studio/${id}`);
  } catch (_error) {
    message.error('启动失败');
  }
};

const handleSearch = () => {
  currentPage.value = 1;
};

const handleSort = () => {
  currentPage.value = 1;
};

const formatTime = (date: Date) => {
  return dayjs(date).format('YYYY-MM-DD HH:mm');
};

const getFormatColor = (format: string) => {
  const colors: Record<string, string> = {
    json: 'blue',
    csv: 'green',
    sql: 'orange'
  };
  return colors[format] || 'default';
};
</script>

<style scoped>
.configurations-page {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.page-title {
  font-size: 28px;
  font-weight: 600;
  margin: 0 0 8px 0;
  color: #1f2937;
}

.page-description {
  color: #6b7280;
  margin: 0;
}

.filter-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  border: 1px solid #f0f0f0;
}

.configurations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.config-card {
  background: white;
  border: 1px solid #f0f0f0;
  border-radius: 8px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.config-card:hover {
  border-color: #1677ff;
  box-shadow: 0 4px 12px rgba(22, 119, 255, 0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #1f2937;
  flex: 1;
  margin-right: 12px;
}

.card-description {
  color: #6b7280;
  margin: 0 0 16px 0;
  font-size: 14px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 12px;
  color: #6b7280;
}

.meta-left {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.pagination-section {
  display: flex;
  justify-content: center;
  padding: 20px;
}

@media (max-width: 768px) {
  .configurations-grid {
    grid-template-columns: 1fr;
  }
  
  .filter-section {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    align-items: stretch;
  }
}
</style>
