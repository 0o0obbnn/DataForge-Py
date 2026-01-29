<template>
  <div class="template-manager">
    <div class="template-header">
      <div class="header-content">
        <div class="header-left">
          <h1>模板管理</h1>
          <p>创建、管理和分享数据生成模板</p>
        </div>
        <div class="header-actions">
          <a-space>
            <a-button @click="showCreateModal = true">
              <template #icon><PlusOutlined /></template>
              创建模板
            </a-button>
            <a-upload
              :show-upload-list="false"
              :before-upload="handleImportTemplate"
              accept=".json"
            >
              <a-button>
                <template #icon><UploadOutlined /></template>
                导入模板
              </a-button>
            </a-upload>
            <a-button @click="refreshTemplates">
              <template #icon><ReloadOutlined /></template>
              刷新
            </a-button>
          </a-space>
        </div>
      </div>
    </div>

    <div class="template-content">
      <!-- 搜索和过滤 -->
      <div class="search-section">
        <div class="search-controls">
          <a-input-search
            v-model:value="searchQuery"
            placeholder="搜索模板名称、描述或标签..."
            style="width: 400px"
            @search="handleSearch"
            @change="handleSearch"
          />
          <a-select
            v-model:value="selectedCategory"
            placeholder="选择分类"
            style="width: 150px"
            @change="handleCategoryChange"
          >
            <a-select-option value="">全部分类</a-select-option>
            <a-select-option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }} ({{ category.templateCount }})
            </a-select-option>
          </a-select>
          <a-select
            v-model:value="sortBy"
            placeholder="排序方式"
            style="width: 150px"
            @change="handleSortChange"
          >
            <a-select-option value="updated">最近更新</a-select-option>
            <a-select-option value="created">创建时间</a-select-option>
            <a-select-option value="name">名称</a-select-option>
            <a-select-option value="usage">使用次数</a-select-option>
          </a-select>
        </div>
      </div>

      <!-- 模板列表 -->
      <div class="templates-section">
        <div v-if="loading" class="loading-state">
          <a-spin size="large" />
          <p>加载模板中...</p>
        </div>

        <div v-else-if="filteredTemplates.length === 0" class="empty-state">
          <div class="empty-content">
            <FileTextOutlined class="empty-icon" />
            <h3>暂无模板</h3>
            <p v-if="searchQuery">未找到匹配的模板，请尝试其他搜索条件</p>
            <p v-else>开始创建您的第一个数据生成模板</p>
            <a-button type="primary" @click="showCreateModal = true">
              创建模板
            </a-button>
          </div>
        </div>

        <div v-else class="templates-grid">
          <div
            v-for="template in paginatedTemplates"
            :key="template.id"
            class="template-card"
          >
            <div class="card-header">
              <div class="card-title">
                <h3>{{ template.name }}</h3>
                <a-tag :color="getCategoryColor(template.category)">
                  {{ getCategoryName(template.category) }}
                </a-tag>
              </div>
              <a-dropdown>
                <a-button type="text" size="small">
                  <MoreOutlined />
                </a-button>
                <template #overlay>
                  <a-menu @click="handleMenuClick($event, template)">
                    <a-menu-item key="use">
                      <PlayCircleOutlined />
                      使用模板
                    </a-menu-item>
                    <a-menu-item key="edit">
                      <EditOutlined />
                      编辑模板
                    </a-menu-item>
                    <a-menu-item key="duplicate">
                      <CopyOutlined />
                      复制模板
                    </a-menu-item>
                    <a-menu-item key="export">
                      <DownloadOutlined />
                      导出模板
                    </a-menu-item>
                    <a-menu-divider />
                    <a-menu-item key="delete" class="danger-item">
                      <DeleteOutlined />
                      删除模板
                    </a-menu-item>
                  </a-menu>
                </template>
              </a-dropdown>
            </div>

            <div class="card-content">
              <p class="template-description">{{ template.description }}</p>

              <div class="template-stats">
                <div class="stat-item">
                  <DatabaseOutlined />
                  <span>{{ template.fields.length }} 个字段</span>
                </div>
                <div class="stat-item">
                  <EyeOutlined />
                  <span>{{ template.statistics?.usageCount || 0 }} 次使用</span>
                </div>
                <div class="stat-item">
                  <ClockCircleOutlined />
                  <span>{{ formatDate(template.metadata.updatedAt) }}</span>
                </div>
              </div>

              <div v-if="template.metadata.tags.length > 0" class="template-tags">
                <a-tag
                  v-for="tag in template.metadata.tags.slice(0, 3)"
                  :key="tag"
                  size="small"
                >
                  {{ tag }}
                </a-tag>
                <a-tag v-if="template.metadata.tags.length > 3" size="small">
                  +{{ template.metadata.tags.length - 3 }}
                </a-tag>
              </div>
            </div>

            <div class="card-footer">
              <a-button
                type="primary"
                block
                @click="useTemplate(template)"
              >
                <PlayCircleOutlined />
                使用模板
              </a-button>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div v-if="filteredTemplates.length > pageSize" class="pagination-section">
          <a-pagination
            v-model:current="currentPage"
            :total="filteredTemplates.length"
            :page-size="pageSize"
            :show-size-changer="false"
            :show-quick-jumper="true"
            :show-total="(total, range) => `${range[0]}-${range[1]} / ${total} 个模板`"
          />
        </div>
      </div>
    </div>

    <!-- 创建/编辑模板弹窗 -->
    <a-modal
      v-model:open="showCreateModal"
      title="创建模板"
      width="600px"
      @ok="handleCreateTemplate"
      @cancel="resetCreateForm"
    >
      <a-form
        ref="createFormRef"
        :model="createForm"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
      >
        <a-form-item
          label="模板名称"
          name="name"
          :rules="[{ required: true, message: '请输入模板名称' }]"
        >
          <a-input v-model:value="createForm.name" placeholder="输入模板名称" />
        </a-form-item>

        <a-form-item
          label="模板描述"
          name="description"
          :rules="[{ required: true, message: '请输入模板描述' }]"
        >
          <a-textarea
            v-model:value="createForm.description"
            placeholder="描述模板的用途和特点"
            :rows="3"
          />
        </a-form-item>

        <a-form-item
          label="模板分类"
          name="category"
          :rules="[{ required: true, message: '请选择模板分类' }]"
        >
          <a-select v-model:value="createForm.category" placeholder="选择分类">
            <a-select-option
              v-for="category in categories"
              :key="category.id"
              :value="category.id"
            >
              {{ category.name }}
            </a-select-option>
          </a-select>
        </a-form-item>

        <a-form-item label="标签" name="tags">
          <a-select
            v-model:value="createForm.tags"
            mode="tags"
            placeholder="添加标签（回车添加）"
            :max-tag-count="5"
          />
        </a-form-item>

        <a-form-item label="公开模板" name="isPublic">
          <a-switch
            v-model:checked="createForm.isPublic"
            checked-children="公开"
            un-checked-children="私有"
          />
          <div class="form-help">公开的模板可以被其他用户发现和使用</div>
        </a-form-item>
      </a-form>
    </a-modal>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { message, Modal } from 'ant-design-vue'
import {
  PlusOutlined, UploadOutlined, ReloadOutlined, MoreOutlined,
  EditOutlined, CopyOutlined, DownloadOutlined, DeleteOutlined,
  PlayCircleOutlined, FileTextOutlined, DatabaseOutlined,
  EyeOutlined, ClockCircleOutlined
} from '@ant-design/icons-vue'
import { useWorkbenchStore } from '@/stores/workbench'
import { TemplateService } from '@/services/template'
import type { GenerationTemplate, TemplateCategory } from '@/services/template'
import dayjs from 'dayjs'

const router = useRouter()
const workbenchStore = useWorkbenchStore()

// 响应式数据
const loading = ref(false)
const templates = ref<GenerationTemplate[]>([])
const categories = ref<TemplateCategory[]>([])
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('updated')
const currentPage = ref(1)
const pageSize = ref(12)

// 弹窗状态
const showCreateModal = ref(false)
const createFormRef = ref()
const createForm = ref({
  name: '',
  description: '',
  category: '',
  tags: [] as string[],
  isPublic: false
})

// 计算属性
const filteredTemplates = computed(() => {
  let result = templates.value

  // 应用搜索过滤
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(template =>
      template.name.toLowerCase().includes(query) ||
      template.description.toLowerCase().includes(query) ||
      template.metadata.tags.some(tag => tag.toLowerCase().includes(query))
    )
  }

  // 应用分类过滤
  if (selectedCategory.value) {
    result = result.filter(template => template.category === selectedCategory.value)
  }

  // 应用排序
  result.sort((a, b) => {
    switch (sortBy.value) {
      case 'created':
        return new Date(b.metadata.createdAt).getTime() - new Date(a.metadata.createdAt).getTime()
      case 'updated':
        return new Date(b.metadata.updatedAt).getTime() - new Date(a.metadata.updatedAt).getTime()
      case 'name':
        return a.name.localeCompare(b.name)
      case 'usage':
        return (b.statistics?.usageCount || 0) - (a.statistics?.usageCount || 0)
      default:
        return 0
    }
  })

  return result
})

const paginatedTemplates = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredTemplates.value.slice(start, end)
})

// 方法
const loadTemplates = () => {
  loading.value = true
  try {
    templates.value = TemplateService.getAllTemplates()
    categories.value = TemplateService.getTemplateCategories()
  } catch (error) {
    message.error('加载模板失败')
    console.error('加载模板失败:', error)
  } finally {
    loading.value = false
  }
}

const refreshTemplates = () => {
  loadTemplates()
  message.success('模板列表已刷新')
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleCategoryChange = () => {
  currentPage.value = 1
}

const handleSortChange = () => {
  currentPage.value = 1
}

const handleMenuClick = ({ key }: { key: string }, template: GenerationTemplate) => {
  switch (key) {
    case 'use':
      useTemplate(template)
      break
    case 'edit':
      editTemplate(template)
      break
    case 'duplicate':
      duplicateTemplate(template)
      break
    case 'export':
      exportTemplate(template)
      break
    case 'delete':
      deleteTemplate(template)
      break
  }
}

const useTemplate = (template: GenerationTemplate) => {
  // 增加使用次数
  TemplateService.incrementUsageCount(template.id)

  // 加载模板到工作台
  workbenchStore.loadTemplate(template)

  // 跳转到工作台
  router.push('/workbench')
  message.success(`已加载模板: ${template.name}`)
}

const editTemplate = (template: GenerationTemplate) => {
  // 跳转到工作台编辑模式
  router.push(`/workbench/edit/${template.id}`)
}

const duplicateTemplate = (template: GenerationTemplate) => {
  const duplicated = TemplateService.duplicateTemplate(template.id)
  if (duplicated) {
    loadTemplates()
  }
}

const exportTemplate = (template: GenerationTemplate) => {
  TemplateService.exportTemplate(template.id)
}

const deleteTemplate = (template: GenerationTemplate) => {
  Modal.confirm({
    title: '确认删除',
    content: `确定要删除模板 "${template.name}" 吗？此操作不可撤销。`,
    okText: '删除',
    okType: 'danger',
    cancelText: '取消',
    onOk() {
      const success = TemplateService.deleteTemplate(template.id)
      if (success) {
        loadTemplates()
      }
    }
  })
}

const handleImportTemplate = async (file: File) => {
  const imported = await TemplateService.importTemplate(file)
  if (imported) {
    loadTemplates()
  }
  return false // 阻止自动上传
}

const handleCreateTemplate = async () => {
  try {
    await createFormRef.value.validate()

    // 从当前工作台状态创建模板
    if (!workbenchStore.hasFields) {
      message.warning('请先在工作台中配置字段，然后再创建模板')
      return
    }

    const template = TemplateService.saveTemplate({
      name: createForm.value.name,
      description: createForm.value.description,
      category: createForm.value.category,
      fields: workbenchStore.fields,
      generationConfig: workbenchStore.generationConfig
    })

    // 更新模板元数据
    TemplateService.updateTemplate(template.id, {
      metadata: {
        ...template.metadata,
        tags: createForm.value.tags,
        isPublic: createForm.value.isPublic
      }
    })

    loadTemplates()
    resetCreateForm()
    showCreateModal.value = false
  } catch (error) {
    console.error('创建模板失败:', error)
  }
}

const resetCreateForm = () => {
  createForm.value = {
    name: '',
    description: '',
    category: '',
    tags: [],
    isPublic: false
  }
  createFormRef.value?.resetFields()
}

const getCategoryName = (categoryId: string) => {
  const category = categories.value.find(c => c.id === categoryId)
  return category?.name || '未知分类'
}

const getCategoryColor = (categoryId: string) => {
  const colors: Record<string, string> = {
    user_data: 'blue',
    business_data: 'green',
    financial_data: 'orange',
    testing_data: 'purple',
    demo_data: 'cyan'
  }
  return colors[categoryId] || 'default'
}

const formatDate = (dateString: string) => {
  return dayjs(dateString).format('YYYY-MM-DD')
}

// 组件挂载
onMounted(() => {
  loadTemplates()
})
</script>

<script>
export default {
  name: 'TemplateManager'
}
</script>

<style scoped lang="less">
.template-manager {
  min-height: 100vh;
  background: var(--df-primary-bg);
}

.template-header {
  background: var(--df-secondary-bg);
  border-bottom: 1px solid var(--df-text-disabled);
  padding: var(--df-spacing-lg);

  .header-content {
    max-width: 1200px;
    margin: 0 auto;
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-left {
      h1 {
        color: var(--df-text-primary);
        font-size: var(--df-font-size-xxl);
        margin: 0;
      }

      p {
        color: var(--df-text-secondary);
        margin: var(--df-spacing-xs) 0 0 0;
      }
    }
  }
}

.template-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--df-spacing-lg);
}

.search-section {
  margin-bottom: var(--df-spacing-lg);

  .search-controls {
    display: flex;
    gap: var(--df-spacing-md);
    align-items: center;
    flex-wrap: wrap;
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--df-spacing-xxl);

  p {
    color: var(--df-text-secondary);
    margin-top: var(--df-spacing-md);
  }
}

.empty-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 400px;

  .empty-content {
    text-align: center;

    .empty-icon {
      font-size: 64px;
      color: var(--df-text-disabled);
      margin-bottom: var(--df-spacing-lg);
    }

    h3 {
      color: var(--df-text-primary);
      margin-bottom: var(--df-spacing-md);
    }

    p {
      color: var(--df-text-secondary);
      margin-bottom: var(--df-spacing-lg);
    }
  }
}

.templates-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: var(--df-spacing-lg);
  margin-bottom: var(--df-spacing-lg);
}

.template-card {
  background: var(--df-secondary-bg);
  border: 1px solid var(--df-text-disabled);
  border-radius: var(--df-radius-lg);
  padding: var(--df-spacing-lg);
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--df-accent-primary);
    box-shadow: 0 4px 12px rgba(139, 92, 246, 0.15);
    transform: translateY(-2px);
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: var(--df-spacing-md);

    .card-title {
      flex: 1;

      h3 {
        color: var(--df-text-primary);
        font-size: var(--df-font-size-lg);
        margin: 0 0 var(--df-spacing-xs) 0;
      }
    }
  }

  .card-content {
    margin-bottom: var(--df-spacing-lg);

    .template-description {
      color: var(--df-text-secondary);
      font-size: var(--df-font-size-sm);
      line-height: 1.5;
      margin-bottom: var(--df-spacing-md);
    }

    .template-stats {
      display: flex;
      flex-direction: column;
      gap: var(--df-spacing-xs);
      margin-bottom: var(--df-spacing-md);

      .stat-item {
        display: flex;
        align-items: center;
        gap: var(--df-spacing-xs);
        color: var(--df-text-secondary);
        font-size: var(--df-font-size-sm);
      }
    }

    .template-tags {
      display: flex;
      flex-wrap: wrap;
      gap: var(--df-spacing-xs);
    }
  }
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: var(--df-spacing-lg);
}

.form-help {
  color: var(--df-text-secondary);
  font-size: var(--df-font-size-sm);
  margin-top: var(--df-spacing-xs);
}

.danger-item {
  color: var(--df-error-color) !important;
}

// 响应式设计
@media (max-width: 768px) {
  .template-header {
    .header-content {
      flex-direction: column;
      gap: var(--df-spacing-md);
      align-items: flex-start;
    }
  }

  .search-controls {
    flex-direction: column;
    align-items: stretch !important;

    > * {
      width: 100% !important;
    }
  }

  .templates-grid {
    grid-template-columns: 1fr;
  }
}
</style>
