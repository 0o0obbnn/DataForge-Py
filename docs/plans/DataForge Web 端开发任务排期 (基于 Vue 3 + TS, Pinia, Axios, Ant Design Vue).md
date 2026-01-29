**总览:**
本排期分为三个主要阶段，每个阶段内包含多个任务，每个任务都是一个独立的、可由AI逐步实现的功能点。任务之间存在明确的依赖关系，AI应按照此顺序进行开发，并在每个任务完成后进行自我评估和集成测试。

---

#### **Phase 0: 核心框架与基础库集成**

**(目标: 建立基于 Vue 3 + TS 的项目基础，集成并配置 Vue Router, Pinia, Axios, Ant Design Vue 等核心库)**

- **Task 0.01 - 项目初始化与 Vue Router 配置 (TypeScript)**

    - **Feature:** 项目骨架与路由

    - **Component/Interaction:** Vue 3 + TypeScript 项目初始化，配置 Vue Router 实例。

    - **Description:** 使用 Vue CLI 或 Vite 初始化一个 Vue 3 + TypeScript 项目。配置 Vue Router，定义基础路由 (/register, /login, /profile, /workbench, /templates, /api)。创建基本的 App.vue 布局，预留 <router-view />。

    - **Dependencies:** None

- **Task 0.02 - Pinia 状态管理配置 (TypeScript)**

    - **Feature:** 全局状态管理

    - **Component/Interaction:** Pinia 存储库的配置。

    - **Description:** 在 Vue 应用中集成 Pinia。定义一个基础的 auth store，用于存储用户登录状态（isLoggedIn: boolean, userToken: string | null, userInfo: UserInfo | null）和相关 actions（如 login, logout）。定义 UserInfo 接口。

    - **Dependencies:** Task 0.01

- **Task 0.03 - Ant Design Vue (AntD) 集成与全局配置**

    - **Feature:** UI 组件库

    - **Component/Interaction:** Ant Design Vue 组件库的安装和按需引入/全局引入。

    - **Description:** 安装 ant-design-vue。配置 AntD 的按需加载或全局注册，确保其样式和组件能够在 Vue 应用中正常使用。测试导入并使用一个 AntD Button 组件。

    - **Dependencies:** Task 0.01

- **Task 0.04 - Axios HTTP 客户端配置 (TypeScript)**

    - **Feature:** 网络请求

    - **Component/Interaction:** Axios 实例的创建与配置。

    - **Description:** 创建一个 Axios 实例，配置 baseURL。实现请求拦截器，用于在请求头中添加用户认证 Token（从 Pinia auth store 获取）。实现响应拦截器，用于全局处理 API 错误（如 401 状态码时自动登出）和统一的错误消息提示（使用 AntD Message 或 Notification）。定义通用的 API 请求函数。

    - **Dependencies:** Task 0.01, Task 0.02, Task 0.03 (用于 AntD Message/Notification)


---

#### **Phase 1: 用户管理模块 (Authentication & Account)**

**(目标: 实现用户注册、登录、密码找回和个人资料管理的核心功能，全部使用 Ant Design Vue 组件和 Pinia/Axios)**

- **Task 1.01 - 注册页面基础布局 (AntD)**

    - **Feature:** 注册界面

    - **Component/Interaction:** a-form, a-tabs, a-tab-pane, 页面标题。

    - **Description:** 构建注册页面 (/register) 的整体布局，使用 a-tabs 和 a-tab-pane 实现“邮箱注册”、“手机号注册”Tab 切换。页面标题使用 AntD 的排版组件。

    - **Dependencies:** Task 0.01, Task 0.03

- **Task 1.02 - 邮箱注册表单构建 (AntD)**

    - **Feature:** 注册界面

    - **Component/Interaction:** a-form-item, a-input, a-button, a-checkbox, a-progress (密码强度), a-space, router-link。

    - **Description:** 在邮箱注册 a-tab-pane 下构建表单 UI：

        - “邮箱地址”使用 a-input type="email"。

        - “获取验证码”按钮使用 a-button。

        - “邮箱验证码”使用 a-input。

        - “设置密码”、“确认密码”使用 a-input-password。

        - 密码强度指示器使用 a-progress 或自定义强度条。

        - “用户协议”复选框使用 a-checkbox。

        - “注册”按钮使用 a-button type="primary"。

        - “登录”链接使用 router-link。

    - **Dependencies:** Task 1.01

- **Task 1.03 - 邮箱注册表单前端校验与交互逻辑 (TS, Vue 3)**

    - **Feature:** 注册界面

    - **Component/Interaction:** a-form 的 rules 属性，v-model 绑定，a-button 的 loading 和 disabled 状态。

    - **Description:** 使用 Vue 3 的 reactive 或 ref 定义表单数据。为 a-form 配置 rules 属性，实现邮箱格式、密码强度、确认密码一致性等前端校验（基于 AntD 的校验机制）。实现“获取验证码”按钮的倒计时、启用/禁用逻辑。实现密码强度指示器根据输入实时更新。使用 a-checkbox 的 v-model 控制注册按钮的启用状态。

    - **Dependencies:** Task 1.02

- **Task 1.04 - 邮箱注册后端集成 (Axios, Pinia)**

    - **Feature:** 注册界面

    - **Component/Interaction:** a-button 的 @click 事件，调用 Axios 请求，更新 Pinia store，a-message 或 a-notification 提示。

    - **Description:**

        1. “获取验证码”按钮：点击时调用 Task 0.04 中配置的 Axios 实例，发送请求到后端 API 发送邮件验证码。处理成功/失败响应（使用 AntD Message/Notification）。

        2. “注册”按钮：点击时触发 a-form 的 validate 方法，校验通过后调用 Task 0.04 中配置的 Axios 实例，发送注册请求。处理成功后跳转到登录页 (router.push('/login')) 或直接登录并更新 Pinia auth store，失败则显示后端错误信息。

    - **Dependencies:** Task 1.03, Task 0.02, Task 0.04

- **Task 1.05 - 手机号注册表单构建与校验 (AntD, TS)**

    - **Feature:** 注册界面

    - **Component/Interaction:** a-input type="tel", a-button, a-form rules。

    - **Description:** 在手机号注册 a-tab-pane 下构建表单 UI 和前端校验逻辑。使用 a-input 实现手机号和短信验证码输入。复用密码设置、确认密码、协议勾选和注册按钮。

    - **Dependencies:** Task 1.01, Task 1.03 (复用校验), Task 1.02

- **Task 1.06 - 手机号注册后端集成 (Axios, Pinia)**

    - **Feature:** 注册界面

    - **Component/Interaction:** a-button 点击事件，Axios 请求。

    - **Description:**

        1. “获取验证码”按钮：点击时调用 Axios API 发送短信验证码。

        2. “注册”按钮：点击时调用 Axios API 完成手机号注册。

    - **Dependencies:** Task 1.05, Task 0.02, Task 0.04

- **Task 1.07 - 登录页面基础布局与表单构建 (AntD)**

    - **Feature:** 登录界面

    - **Component/Interaction:** a-tabs, a-form, a-input, a-input-password, a-checkbox, a-button, router-link, 页面标题。

    - **Description:** 构建登录页面 (/login) 布局。使用 a-tabs 实现登录方式切换。构建账号密码登录表单，使用 a-input (邮箱/手机号), a-input-password (密码), a-checkbox (记住我), a-button type="primary" (登录)。添加“忘记密码”和“立即注册” router-link。预留第三方登录区域。

    - **Dependencies:** Task 0.01, Task 0.03

- **Task 1.08 - 登录页面前端校验与后端集成 (Axios, Pinia)**

    - **Feature:** 登录界面

    - **Component/Interaction:** a-form rules, a-button loading & disabled 状态，Axios 请求，Pinia auth store 更新，router.push。

    - **Description:** 实现账号密码登录表单的前端非空校验。点击“登录”按钮时，调用 Axios API 进行认证。成功后更新 Pinia auth store 中的 isLoggedIn, userToken, userInfo，并重定向到首页 (router.push('/workbench'))。失败则显示错误提示。实现手机号验证码登录表单的校验和后端集成，类似注册流程。

    - **Dependencies:** Task 1.07, Task 0.02, Task 0.04

- **Task 1.09 - 密码找回页面 (AntD, Axios)**

    - **Feature:** 密码找回

    - **Component/Interaction:** a-form, a-input, a-input-password, a-button, a-message。

    - **Description:** 构建密码找回页面 (/reset-password) UI。实现“输入邮箱/手机号接收验证码”、“获取验证码”、“验证码输入”、“新密码设置”、“确认新密码”等表单项和按钮。集成 Axios API 进行验证码发送、验证和密码重置。

    - **Dependencies:** Task 0.01, Task 0.03, Task 0.04

- **Task 1.10 - 个人中心页面布局与导航 (AntD)**

    - **Feature:** 个人中心

    - **Component/Interaction:** a-layout, a-layout-sider, a-menu, a-menu-item, a-layout-content。

    - **Description:** 构建个人中心页面 (/profile) 的两栏布局。左侧使用 a-layout-sider 和 a-menu 实现导航菜单（“个人资料”、“账户安全”、“登录历史”）。右侧使用 a-layout-content 作为内容区域。

    - **Dependencies:** Task 0.01, Task 0.03

- **Task 1.11 - 个人资料管理 (UI & 交互) (AntD, Pinia)**

    - **Feature:** 个人资料

    - **Component/Interaction:** a-avatar, a-upload, a-input, a-button, a-typography.Text。

    - **Description:** 构建“个人资料”内容区 UI。头像显示使用 a-avatar，修改头像使用 a-upload 组件（仅 UI 层面，后端集成 Task 1.12）。昵称使用 a-input。邮箱/手机号使用 a-typography.Text 显示，并提供“更换/解绑” a-button link。使用 Pinia auth store 的 userInfo 绑定显示数据。

    - **Dependencies:** Task 1.10, Task 0.02, Task 0.03

- **Task 1.12 - 个人资料管理 (后端集成) (Axios, Pinia)**

    - **Feature:** 个人资料

    - **Component/Interaction:** a-upload 的 customRequest，a-button 的 @click 事件，Axios 请求，Pinia auth store 更新。

    - **Description:**

        1. “修改头像”：配置 a-upload 的 customRequest，手动调用 Axios API 上传图片。成功后更新 Pinia auth store 中的 userInfo.avatar。

        2. “保存”按钮：点击时调用 Axios API 提交昵称修改。成功后更新 Pinia auth store 中的 userInfo.nickname。

        3. 实现弹出对话框 (a-modal) 处理邮箱/手机号的绑定、更换、解绑流程及后端 Axios API 调用。

    - **Dependencies:** Task 1.11, Task 0.02, Task 0.04

- **Task 1.13 - 账户安全设置 (UI & 交互) (AntD)**

    - **Feature:** 账户安全

    - **Component/Interaction:** a-list, a-list-item, a-button, a-switch, a-modal。

    - **Description:** 构建“账户安全”内容区 UI。使用 a-list 展示“登录密码”、“两步验证”等条目。每个条目包含标题、描述和操作按钮 (a-button) 或开关 (a-switch)。点击“修改密码”按钮弹出 a-modal 对话框。

    - **Dependencies:** Task 1.10, Task 0.03

- **Task 1.14 - 账户安全设置 (后端集成) (Axios)**

    - **Feature:** 账户安全

    - **Component/Interaction:** a-modal 中表单的提交，a-switch 的 @change 事件。

    - **Description:** 集成 Axios API：修改密码、启用/禁用两步验证、两步验证的绑定/解绑/配置（如 TOTP 二维码生成和验证）。

    - **Dependencies:** Task 1.13, Task 0.04

- **Task 1.15 - 登录历史记录 (UI & 交互 & 后端集成) (AntD)**

    - **Feature:** 登录历史

    - **Component/Interaction:** a-table, a-pagination, a-button (刷新)。

    - **Description:** 构建“登录历史”内容区 UI。使用 a-table 展示登录历史记录，配置分页 (a-pagination)。实现“刷新” a-button 点击重新加载数据。调用 Axios API 获取登录历史数据并渲染。

    - **Dependencies:** Task 1.10, Task 0.03, Task 0.04


---

#### **Phase 2: 数据生成工作台 (Core Functionality)**

**(目标: 实现可视化数据结构构建、参数配置、数据预览与批量生成下载，全部使用 Ant Design Vue 组件和 Pinia/Axios)**

- **Task 2.01 - 工作台基础布局与顶部全局操作 (AntD)**

    - **Feature:** 工作台

    - **Component/Interaction:** a-layout, a-layout-sider, a-layout-content, a-layout-footer, a-input (任务名称，可编辑)。

    - **Description:** 构建工作台页面 (/workbench) 的 a-layout 结构，实现三栏布局。任务名称使用可编辑的 a-input 组件（前端状态管理）。

    - **Dependencies:** Task 0.01, Task 0.03

- **Task 2.02 - 左侧字段库面板 (AntD)**

    - **Feature:** 字段库

    - **Component/Interaction:** a-input-search, a-collapse, a-collapse-panel, 自定义可拖拽 div。

    - **Description:** 构建左侧字段库面板 UI。使用 a-input-search 实现搜索功能。分类列表使用 a-collapse 和 a-collapse-panel 实现可折叠手风琴效果。每个数据类型项使用自定义 div 实现拖拽功能，显示图标和文本。

    - **Dependencies:** Task 2.01, Task 0.03

- **Task 2.03 - 中间数据结构画布 (AntD)**

    - **Feature:** 数据结构画布

    - **Component/Interaction:** 自定义可放置区域 (@dragover, @drop), 自定义字段卡片组件 (FieldCard.vue)。

    - **Description:** 构建中间画布区域 UI。实现拖拽放置逻辑。当字段从左侧拖入时，在画布上生成一个 FieldCard.vue 组件实例。FieldCard 内部包含 a-input (字段名，可编辑), a-button (删除按钮), a-icon (类型图标、关联标识)。实现字段卡片的选中（高亮）、删除、名称编辑（前端状态）。

    - **Dependencies:** Task 2.01, Task 2.02 (拖拽源), Task 0.03

- **Task 2.04 - 右侧字段配置面板基础框架 (AntD)**

    - **Feature:** 字段配置

    - **Component/Interaction:** a-form, a-input (字段名，只读), a-typography.Text (数据类型)。

    - **Description:** 构建右侧字段配置面板 UI。当选中画布中字段时，显示该字段的名称 (a-input) 和数据类型 (a-typography.Text)。

    - **Dependencies:** Task 2.01, Task 2.03 (选中事件)

- **Task 2.05 - 通用字段配置项组件化 (AntD, TS)**

    - **Feature:** 字段配置

    - **Component/Interaction:** 封装 AntD Form.Item 嵌套 a-input-number, a-range-picker, a-select, a-switch, a-upload 等组件。

    - **Description:** 抽象并实现一套通用的、可动态加载和渲染的配置项 Vue 组件。例如 NumberRangeInput.vue, DateRangePicker.vue, ToggleSwitch.vue, FileUpload.vue 等，它们内部使用 AntD 组件并封装了 v-model 绑定和 props 配置。定义 TypeScript 接口来规范这些配置项的类型。

    - **Dependencies:** Task 2.04, Task 0.03

- **Task 2.06 - 字段配置面板 - 基础配置与生成规则 (AntD, Pinia)**

    - **Feature:** 字段配置

    - **Component/Interaction:** a-collapse, a-collapse-panel, a-form-item 结合 Task 2.05 的通用组件。

    - **Description:** 根据选中字段的数据类型，动态加载并渲染 Task 2.05 中实现的对应配置项。使用 Pinia store 管理当前工作台的数据结构和字段配置，实现配置项与字段数据模型的双向绑定。

    - **Dependencies:** Task 2.05, Task 0.02 (Pinia Store)

- **Task 2.07 - 字段配置面板 - 数据关联逻辑 (UI) (AntD, Vue 3)**

    - **Feature:** 字段关联

    - **Component/Interaction:** a-select, a-textarea, SVG/Canvas 连线。

    - **Description:** 构建“数据关联”配置 UI。使用 a-select 实现“关联到字段”下拉框，动态加载画布中其他字段。使用 a-textarea 作为“关联规则”输入框。实现当选择关联字段时，在画布上绘制可视化连线（使用 Vue 3 的 <Teleport> 或自定义 SVG/Canvas 组件）。

    - **Dependencies:** Task 2.06, Task 0.03

- **Task 2.08 - 字段配置面板 - 数据关联逻辑 (AI辅助建议)**

    - **Feature:** 字段关联 (AI增强)

    - **Component/Interaction:** a-textarea 的 autocomplete 或自定义建议弹出层。

    - **Description:** 为“关联规则” a-textarea 实现 AI 辅助功能：根据当前字段和关联字段的类型，实时提供语法提示或常用规则模板建议。这可能需要一个本地的 Vue Composition API hook 或一个调用后端微服务的逻辑来获取建议。

    - **Dependencies:** Task 2.07

- **Task 2.09 - 字段配置面板 - 高级选项 (AntD)**

    - **Feature:** 字段配置

    - **Component/Interaction:** a-input-number, a-select。

    - **Description:** 构建“高级选项”配置 UI。使用 a-input-number 实现“空值生成频率”，a-select 实现“边界值策略”。

    - **Dependencies:** Task 2.06

- **Task 2.10 - 底部控制台与全局配置 (AntD, Pinia)**

    - **Feature:** 全局配置

    - **Component/Interaction:** a-input-number, a-select, a-button, a-form-item。

    - **Description:** 构建底部控制台 UI。使用 a-input-number (“生成数量”), a-select (“输出格式”), a-button (预览数据、重置画布、保存为模板、生成并下载) 实现所有输入和按钮。实现“输出格式”下拉选择改变时，动态显示/隐藏对应的格式特定配置项（如 CSV 分隔符 a-input）。实现按钮的启用/禁用状态逻辑 (依赖 Pinia store 中的画布状态和校验结果)。

    - **Dependencies:** Task 2.01, Task 2.03, Task 0.02, Task 0.03

- **Task 2.11 - 数据预览模态框 (AntD)**

    - **Feature:** 数据预览

    - **Component/Interaction:** a-modal, a-typography.Title, a-typography.Paragraph, a-table, a-card (校验结果)。

    - **Description:** 实现数据预览模态框 (a-modal)。根据输出格式在内容显示区渲染数据 (JSON/XML/SQL 使用代码高亮库或 a-typography.Text 加 <code> 标签，CSV 使用 a-table)。在校验结果区显示后端返回的校验信息。

    - **Dependencies:** Task 2.10 ("预览数据"按钮), Task 0.03, (Code Highlighter Library)

- **Task 2.12 - 数据预览后端集成 (Axios)**

    - **Feature:** 数据预览

    - **Component/Interaction:** a-button 的 @click 事件，Axios 请求。

    - **Description:** 当“预览数据”按钮点击时，收集当前画布上所有字段的配置，调用 Axios API 请求少量预览数据。将后端返回的数据和校验结果填充到 Task 2.11 的模态框中。显示 a-spin (加载状态) 和 a-message (提示信息)。

    - **Dependencies:** Task 2.11, Task 0.04, Task 0.03

- **Task 2.13 - 生成与下载后端集成 (Axios)**

    - **Feature:** 批量生成与下载

    - **Component/Interaction:** a-button 的 @click 事件，Axios 请求，下载文件处理。

    - **Description:** 当“生成并下载”按钮点击时，收集所有配置，调用 Axios API 启动批量数据生成任务。前端显示 a-progress 或 a-spin (加载状态)。任务完成后，接收后端提供的文件下载流或下载链接，并使用 window.URL.createObjectURL 触发文件下载。

    - **Dependencies:** Task 2.10, Task 0.04, Task 0.03


---

#### **Phase 3: 模板与 API 管理模块 (Advanced Features)**

**(目标: 实现模板的保存、管理、共享、版本控制和API调用集成，全部使用 Ant Design Vue 组件和 Pinia/Axios)**

- **Task 3.01 - 模板管理页面基础布局 (AntD)**

    - **Feature:** 模板列表

    - **Component/Interaction:** a-layout, a-page-header, a-input-search, a-select, a-button。

    - **Description:** 构建模板管理页面 (/templates) 的整体布局。使用 a-page-header 作为页面头部。使用 a-input-search 实现搜索功能，a-select 实现筛选下拉菜单。a-button 实现“新建模板”功能。

    - **Dependencies:** Task 0.01, Task 0.03

- **Task 3.02 - 模板列表表格/卡片展示 (AntD)**

    - **Feature:** 模板列表

    - **Component/Interaction:** a-table, a-pagination, a-button, a-tooltip。

    - **Description:** 实现模板列表的 UI 展示。使用 a-table 显示模板信息，每行包含模板名称 (router-link), 创建者、时间、描述。操作列包含“编辑”, “复制”, “删除”, “分享”, “获取API”等 a-button link。使用 a-tooltip 为按钮提供提示。底部使用 a-pagination 实现分页。

    - **Dependencies:** Task 3.01, Task 0.03

- **Task 3.03 - 模板列表后端集成 (Axios)**

    - **Feature:** 模板列表

    - **Component/Interaction:** a-input-search 的 v-model 和 @search 事件，a-select 的 v-model 和 @change 事件，a-pagination 的 @change 事件。

    - **Description:** 调用 Axios API 获取模板列表数据，根据搜索、筛选和分页条件请求数据并渲染到 Task 3.02 的 a-table 中。

    - **Dependencies:** Task 3.02, Task 0.04

- **Task 3.04 - “保存模板”对话框 (AntD)**

    - **Feature:** 模板保存

    - **Component/Interaction:** a-modal, a-form, a-input, a-textarea, a-checkbox, a-button。

    - **Description:** 实现“保存模板” a-modal 对话框。包含 a-input (模板名称), a-textarea (模板描述), a-textarea (版本备注), a-checkbox (保存为新版本) 和 a-button (保存/覆盖, 取消)。实现表单校验。

    - **Dependencies:** Task 2.10 ("保存为模板"按钮), Task 0.03

- **Task 3.05 - “保存模板”后端集成 (Axios)**

    - **Feature:** 模板保存

    - **Component/Interaction:** a-modal 中 a-button 的 @click 事件，Axios 请求。

    - **Description:** 当“保存/覆盖”按钮点击时，收集对话框中的信息，调用 Axios API 进行模板的保存或更新。处理成功/失败响应，并刷新模板列表（Task 3.03）。

    - **Dependencies:** Task 3.04, Task 3.03, Task 0.04

- **Task 3.06 - “分享模板”对话框 (AntD)**

    - **Feature:** 模板共享

    - **Component/Interaction:** a-modal, a-radio-group, a-radio, a-select (多选，用户/组选择器), a-button。

    - **Description:** 实现“分享模板” a-modal 对话框。包含 a-radio-group (分享范围, 权限), a-select mode="multiple" (用户/组选择器，动态显示)。

    - **Dependencies:** Task 3.02 ("分享"按钮), Task 0.03

- **Task 3.07 - “分享模板”后端集成 (Axios)**

    - **Feature:** 模板共享

    - **Component/Interaction:** a-button 的 @click 事件，Axios 请求。

    - **Description:** 当“确认分享”按钮点击时，调用 Axios API 进行模板分享，处理响应。

    - **Dependencies:** Task 3.06, Task 0.04

- **Task 3.08 - 模板版本历史对话框 (AntD)**

    - **Feature:** 模板版本管理

    - **Component/Interaction:** a-modal, a-table, a-button。

    - **Description:** 实现“模板版本历史” a-modal 对话框。构建 a-table 显示版本列表，操作列包含“预览”和“回溯到此版本” a-button link。

    - **Dependencies:** Task 3.02 (模板操作), Task 0.03

- **Task 3.09 - 模板版本历史后端集成与回溯 (Axios)**

    - **Feature:** 模板版本管理

    - **Component/Interaction:** 对话框初始化加载，a-button @click 事件，Axios 请求。

    - **Description:** 调用 Axios API 获取指定模板的版本历史。当点击“预览”按钮时，调用后端获取该版本模板配置，并在只读 a-modal 中展示。当点击“回溯到此版本”按钮时，调用 Axios API 将模板回溯到指定版本，成功后刷新模板列表并提示。

    - **Dependencies:** Task 3.08, Task 0.04

- **Task 3.10 - API 管理页面基础布局与 API Key 列表 (AntD)**

    - **Feature:** API Key 管理

    - **Component/Interaction:** a-tabs, a-tab-pane, a-button, a-table, a-switch。

    - **Description:** 构建 API 管理页面 (/api) 布局。使用 a-tabs 实现 Tab 切换。构建“我的API Key”区域 UI，包含“生成新的 API Key” a-button 和 a-table (显示 API Key、状态切换 a-switch 等)。

    - **Dependencies:** Task 0.01, Task 0.03

- **Task 3.11 - API Key 管理后端集成 (Axios)**

    - **Feature:** API Key 管理

    - **Component/Interaction:** a-button @click 事件，a-switch @change 事件，a-modal (确认删除/轮换)。

    - **Description:** 调用 Axios API：初始化加载 API Key 列表，生成新的 API Key，启用/禁用 API Key，删除 API Key，轮换 API Key。

    - **Dependencies:** Task 3.10, Task 0.04

- **Task 3.12 - API 调用统计页面 (AntD, Chart Library)**

    - **Feature:** API 调用统计

    - **Component/Interaction:** a-select, 图表组件 (vue-chartjs/echarts), a-input-search, a-table, a-pagination。

    - **Description:** 构建“API 调用统计”区域 UI。使用 a-select 实现时间范围选择。集成图表库绘制调用次数、成功率、响应时间图表。构建调用日志 a-table 和 a-pagination。

    - **Dependencies:** Task 3.10, Task 0.03, Task 0.04, (Chart Library)

- **Task 3.13 - API 调用统计后端集成 (Axios)**

    - **Feature:** API 调用统计

    - **Component/Interaction:** a-select @change 事件，a-input-search @search 事件。

    - **Description:** 调用 Axios API 获取 API 调用统计数据和详细日志。根据前端的筛选条件请求数据并更新图表和日志表格。

    - **Dependencies:** Task 3.12, Task 0.04

- **Task 3.14 - “模板API调用指南”对话框 (AntD)**

    - **Feature:** 模板 API 调用

    - **Component/Interaction:** a-modal, a-typography.Text, a-button, a-tabs, a-tab-pane, 代码高亮组件。

    - **Description:** 实现“模板API调用指南” a-modal 对话框。动态显示 API 信息（URL、方法、认证）。使用代码高亮组件展示请求/响应参数示例和编程语言代码片段 (a-tabs 切换 Python, Java, Curl)。提供所有“复制”按钮。

    - **Dependencies:** Task 3.02 ("获取API"按钮), Task 0.03, (Code Highlighter Library)

- **Task 3.15 - “模板API调用指南”后端集成 (Axios)**

    - **Feature:** 模板 API 调用

    - **Component/Interaction:** a-modal 初始化加载。

    - **Description:** 当对话框显示时，调用 Axios API 获取指定模板的 API 调用详细信息、参数示例和代码片段。

    - **Dependencies:** Task 3.14, Task 0.04
