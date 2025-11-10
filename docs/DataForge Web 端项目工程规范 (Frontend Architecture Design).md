## DataForge Web 端项目工程规范 (Frontend Architecture Design)

本规范旨在为 DataForge Web 端项目提供一个清晰、可扩展、易于维护的架构蓝图，并指导开发团队遵循一致的编码实践和设计原则。我们将在 Vue 3 + TypeScript、Pinia、Axios 和 Ant Design Vue 的技术栈基础上，融合科技感·未来风的设计理念，打造高效、专业的用户体验。

### 1. 目录结构设计 (Folder Structure)

我们将采用一种结合了功能领域 (Feature-Sliced Design 思想) 和关注点分离的目录结构。这种结构能有效隔离不同模块的逻辑，提升代码可读性和可维护性。

```
├── public/                 # 静态资源，不会被打包处理
│   └── index.html
│   └── favicon.ico
│
├── src/                    # 源代码目录
│   ├── assets/             # 静态资源，会被打包处理
│   │   ├── fonts/          # 字体文件
│   │   ├── images/         # 图片文件 (logo, icon等)
│   │   └── styles/         # 全局或基础样式
│   │       ├── base.less          # 基础样式重置、通用变量
│   │       ├── theme.less         # Ant Design Vue 主题定制样式
│   │       └── utils.less         # 常用工具类样式
│   │
│   ├── components/         # 通用组件 (不耦合任何业务逻辑，可在多个模块中复用)
│   │   ├── common/         # 基础组件封装，如定制化的 AButton, AInput
│   │   ├── ui/             # 具备独立UI但无业务逻辑的组合组件 (如 LoadingSpinner)
│   │   └── layout/         # 通用布局组件 (如 BaseLayout, Header, Footer)
│   │
│   ├── composites/         # 复合组件 (具备一定业务上下文但仍可复用的组件，如 LoginForm, ProfileCard)
│   │   ├── auth/
│   │   │   ├── LoginForm.vue
│   │   │   └── RegisterForm.vue
│   │   ├── workbench/
│   │   │   ├── FieldCard.vue
│   │   │   └── FieldConfigPanel.vue
│   │   └── ...
│   │
│   ├── config/             # 项目配置
│   │   ├── index.ts        # 全局配置 (如 API_BASE_URL)
│   │   ├── constants.ts    # 全局常量
│   │   └── env.d.ts        # 环境变量声明
│   │
│   ├── directives/         # Vue 自定义指令
│   │   └── permission.ts
│   │
│   ├── plugins/            # Vue 插件 (如 Pinia, Router, AntD)
│   │   ├── ant-design-vue.ts  # Ant Design Vue 配置 (按需引入/全局注册)
│   │   ├── axios.ts           # Axios 实例及拦截器配置
│   │   ├── pinia.ts           # Pinia 实例创建及插件集成
│   │   └── router.ts          # Vue Router 实例创建
│   │   └── index.ts           # 统一导出插件
│   │
│   ├── router/             # 路由配置
│   │   ├── index.ts        # 路由入口文件
│   │   ├── guards.ts       # 路由守卫
│   │   └── routes.ts       # 路由定义 (可按模块拆分)
│   │
│   ├── services/           # 后端API服务请求
│   │   ├── modules/        # 按模块划分 API 请求函数
│   │   │   ├── auth.ts
│   │   │   ├── workbench.ts
│   │   │   └── ...
│   │   └── index.ts        # 统一导出 API 服务
│   │
│   ├── stores/             # Pinia 状态管理
│   │   ├── auth.ts         # 用户认证相关状态
│   │   ├── workbench.ts    # 工作台数据结构、字段配置状态
│   │   ├── templates.ts    # 模板管理相关状态
│   │   └── ...             # 其他模块状态
│   │   └── index.ts        # 统一导出所有 stores
│   │
│   ├── utils/              # 工具函数库
│   │   ├── helpers.ts      # 通用辅助函数 (日期格式化、字符串处理等)
│   │   ├── validators.ts   # 前端校验函数
│   │   ├── storage.ts      # LocalStorage/SessionStorage 封装
│   │   └── types.ts        # 全局 TypeScript 类型定义
│   │
│   ├── views/              # 页面级组件 (负责组合 composites 和 data fetching)
│   │   ├── auth/           # 用户认证模块
│   │   │   ├── RegisterPage.vue
│   │   │   └── LoginPage.vue
│   │   │   └── ResetPasswordPage.vue
│   │   ├── profile/        # 个人中心模块 (使用嵌套路由)
│   │   │   ├── ProfileLayout.vue
│   │   │   ├── ProfileDetails.vue
│   │   │   ├── AccountSecurity.vue
│   │   │   └── LoginHistory.vue
│   │   ├── workbench/      # 数据生成工作台模块
│   │   │   └── WorkbenchPage.vue
│   │   ├── templates/      # 模板管理模块
│   │   │   └── TemplatesPage.vue
│   │   ├── api/            # API 管理模块
│   │   │   └── ApiManagementPage.vue
│   │   └── NotFoundPage.vue # 404页面
│   │
│   ├── App.vue             # 根组件
│   └── main.ts             # 应用入口文件
│
├── .env.development        # 开发环境变量
├── .env.production         # 生产环境变量
├── .eslintrc.js            # ESLint 配置
├── .prettierrc.js          # Prettier 配置
├── tsconfig.json           # TypeScript 配置
├── vite.config.ts          # Vite 配置
├── package.json
└── README.md
```  

**组织原则:**

- **Feature-Sliced Design (FSCD) 理念:** 在 views、stores、services 等核心业务逻辑层，倾向于按照功能模块进行切片，实现模块内部的高内聚和模块间的低耦合。
    
- **关注点分离 (Separation of Concerns):** 严格区分 UI 组件、业务逻辑组件、状态管理、路由、API 请求和通用工具函数。
    
- **易于导航:** 目录结构清晰，开发人员可以快速定位到所需文件。
    

### 2. 组件化策略 (Component Strategy)

我们将基于 Ant Design Vue 构建，并遵循原子设计原则 (Atomic Design) 进行组件分层。

1. **Ant Design Vue 基础组件:** 作为项目的基础 UI 骨架，统一使用其提供的组件。
    
2. **原子组件 (Atoms) - 位于 src/components/common:**
    
    - **定义:** 对 Ant Design Vue 基础组件进行薄封装或样式定制，使其符合项目的“科技感·未来风”设计语言。例如，封装 a-button 以应用全局主题色和悬停效果。
        
    - **职责:** 最小功能单元，无业务逻辑。
        
    - **示例:** BaseButton.vue (封装 a-button 并应用 未来紫 主色)、StyledInput.vue (封装 a-input 并实现聚焦发光效果)。
        
3. **分子组件 (Molecules) - 位于 src/components/ui:**
    
    - **定义:** 由多个原子组件组合而成，实现特定 UI 功能但仍无业务逻辑的组件。
        
    - **职责:** 专注于 UI 组合和内部交互，通过 props 接收数据，通过 emit 派发事件。
        
    - **示例:** PasswordStrengthIndicator.vue (组合 a-progress 和 a-typography.Text 展示密码强度)。
        
4. **组织 (Organisms) - 位于 src/composites:**
    
    - **定义:** 具有特定业务上下文，由原子/分子组件以及少量业务逻辑组成的复杂组件。它们是页面或视图的关键组成部分。
        
    - **职责:** 协调内部组件，处理局部业务逻辑和状态，与 Pinia Store 或后端服务交互（通过 services 封装的 API）。
        
    - **示例:** LoginForm.vue (组合 StyledInput、BaseButton 等，处理登录表单的校验和提交)、FieldCard.vue (工作台中的字段展示卡片，包含字段名称编辑、删除按钮等)。
        
5. **页面模板 (Templates) - 位于 src/views/layout 或各模块 views/xxx/Layout.vue:**
    
    - **定义:** 定义页面整体结构和布局，将组织和其他组件进行编排，不包含具体内容。
        
    - **职责:** 提供一致的页面框架，如侧边栏导航、顶部标题栏、内容区域等。
        
    - **示例:** ProfileLayout.vue (定义个人中心的左右两栏布局)。
        
6. **页面 (Pages) - 位于 src/views 各模块下:**
    
    - **定义:** 页面是特定的路由视图，负责编排页面模板和组织，进行数据获取 (Data Fetching)，并将数据传递给子组件。
        
    - **职责:** 作为业务逻辑的入口，通常会通过 Pinia Store 或直接调用 services 来获取和管理页面所需数据。
        
    - **示例:** RegisterPage.vue (组合 RegisterForm 和其他 UI 元素，处理整个注册流程的页面视图)。
        

**组件设计规范:**

- **单一职责原则:** 每个组件只做一件事，并把它做好。
    
- **Props Down, Events Up (P.D.E.U.):** 父组件通过 Props 向子组件传递数据，子组件通过 Events (emit) 向父组件通知事件。
    
- **TypeScript 强类型:** 所有组件的 props、emits 都应使用 TypeScript 进行严格类型定义。
    
- **命名规范:**
    
    - 文件命名: 遵循 PascalCase (如 LoginForm.vue)。
        
    - 组件内部变量/函数: 遵循 camelCase。
        
    - Props 命名: 遵循 camelCase (如 userName)。
        
- **样式范围:** 优先使用 <style scoped> 限制组件样式，避免全局污染。对于需要穿透 Ant Design Vue 组件的样式，使用 Less/Sass 的深度选择器 (::v-deep 或 >>>)。
    
- **可访问性 (Accessibility):** 遵循 WCAG 标准，确保组件具有正确的 ARIA 属性和键盘导航能力。
    

### 3. 状态管理方案 (State Management)

我们将使用 Pinia 作为核心状态管理库，并结合其模块化和 TypeScript 友好性进行设计。

1. **Pinia Store 划分:**
    
    - **全局 Store (src/stores/auth.ts):** 存储与用户认证相关的全局状态，如 isLoggedIn (boolean), userToken (string | null), userInfo (UserInfo 接口定义)。包含 login, logout 等 actions。
        
    - **模块级 Store (src/stores/workbench.ts, src/stores/templates.ts, src/stores/api.ts 等):**
        
        - 每个主要的业务模块拥有独立的 Pinia Store，管理该模块特有的复杂状态。
            
        - **workbench.ts:** 管理数据生成工作台的画布数据结构（字段列表、每个字段的详细配置、字段间的关联关系）、当前任务名称、生成数量、输出格式等。
            
        - **templates.ts:** 管理模板列表数据、模板筛选/排序条件、当前编辑的模板 ID 等。
            
        - **api.ts:** 管理 API Key 列表、API 调用统计数据、日志等。
            
    - **好处:** 避免单个巨型 Store，使得状态管理更加清晰，模块间解耦，易于扩展和维护。
        
2. **数据流向:**
    
    - **组件 -> Actions:** 组件通过调用 Store 中的 actions 来修改状态。Actions 可以包含异步操作（如 API 请求）。
        
    - **Actions -> Mutations (Implicit in Pinia):** Pinia 允许直接在 actions 中修改 state，无需显式定义 mutations。这简化了流程。
        
    - **State -> Getters:** 组件通过 getters 派生状态，避免直接访问 state，提高复用性。
        
    - **State -> 组件:** 组件通过 storeToRefs 或直接访问 Store 实例来响应状态变化。
        
3. **持久化:**
    
    - 对于需要跨会话或刷新页面保持的状态（如 userToken, isLoggedIn, rememberMe 状态），我们将集成 pinia-plugin-persistedstate 插件，将其存储在 LocalStorage 或 SessionStorage 中。
        
    - **auth.ts:** userToken, isLoggedIn 应当持久化。
        
4. **TypeScript 支持:**
    
    - 所有 Store 的 state、getters、actions 的参数和返回值都将使用 TypeScript 进行严格类型定义，确保类型安全和开发时的智能提示。
        
    - 定义全局 UserInfo 等接口，统一数据模型。
        

### 4. 路由设计 (Routing)

我们将使用 Vue Router 4 (与 Vue 3 兼容) 来管理应用的导航。

1. **路由定义 (src/router/routes.ts):**
    
    - **基础路由:** 定义 /register, /login, /profile, /workbench, /templates, /api 等一级路由。
        
    - **嵌套路由:** profile 页面将使用嵌套路由实现左侧导航的子页面切换 (/profile/details, /profile/security, /profile/history)。
    ```
{
  path: '/profile',
  name: 'Profile',
  component: () => import('@/views/profile/ProfileLayout.vue'),
  meta: { requiresAuth: true },
  children: [
    {
      path: 'details',
      name: 'ProfileDetails',
      component: () => import('@/views/profile/ProfileDetails.vue'),
      meta: { title: '个人资料' }
    },
    {
      path: 'security',
      name: 'AccountSecurity',
      component: () => import('@/views/profile/AccountSecurity.vue'),
      meta: { title: '账户安全' }
    },
    {
      path: 'history',
      name: 'LoginHistory',
      component: () => import('@/views/profile/LoginHistory.vue'),
      meta: { title: '登录历史' }
    },
    {
      path: '', // 默认子路由
      redirect: { name: 'ProfileDetails' }
    }
  ]
},
```
    - **动态路由:** /workbench/:templateId? 用于加载特定模板或创建新任务。
        
    - **路由懒加载:** 所有页面组件都将使用动态导入 (() => import(...)) 实现路由懒加载，优化首屏加载性能。
        
3. **路由守卫 (src/router/guards.ts):**
    
    - **全局前置守卫 (router.beforeEach):**
        
        - **认证检查:** 检查 Pinia auth store 中的 userToken 或 isLoggedIn 状态。
            
            - 如果用户未登录且访问需要认证的页面 (meta.requiresAuth: true)，则重定向到 /login。
                
            - 如果用户已登录且访问 /login 或 /register 页面，则重定向到 /workbench (首页)。
                
        - **权限控制 (未来扩展):** 可根据后端返回的用户角色信息，在路由的 meta 字段中定义所需权限，并在守卫中进行检查。
            
    - **页面标题更新:** 在路由守卫中根据路由 meta.title 更新页面标题 (document.title)。
        
4. **导航逻辑:**
    
    - 在组件内部，使用 useRouter 或 useRoute 组合式 API 进行编程式导航 (router.push, router.replace)。
        

### 5. 测试策略 (Testing Strategy)

我们将采用多层次的测试策略，确保代码质量和应用稳定性。

1. **单元测试 (Unit Tests):**
    
    - **范围:** 针对独立的函数、工具类 (src/utils)、Pinia Store (src/stores) 和没有复杂 DOM 交互的 Vue 组件 (src/components/common, src/components/ui)。
        
    - **工具:** Vitest (作为测试运行器) + @vue/test-utils (Vue 组件测试工具)。
        
    - **覆盖率:** 目标代码覆盖率 (如 80%)，通过 c8 (Vite 集成的覆盖率工具) 进行统计和报告。
        
    - **实践:**
        
        - 每个 Store 或 Utility 文件都有对应的 .spec.ts 文件。
            
        - Vue 组件测试注重组件的 Props、Events、Slot 渲染和内部方法的调用。
            
2. **集成测试 (Integration Tests):**
    
    - **范围:** 验证多个组件、Pinia Store 和 API 服务的组合交互是否按预期工作，例如登录流程、字段拖拽到画布、数据预览功能。
        
    - **工具:** Vitest 结合模拟 API 请求 (msw 或 vitest.mock)。
        
    - **实践:** 模拟后端 API 响应，测试组件与 Pinia Store 之间的状态更新和数据流转。
        
3. **端到端测试 (End-to-End Tests - E2E):**
    
    - **范围:** 模拟真实用户在浏览器中的操作路径，验证整个应用从头到尾的关键业务流程。
        
    - **工具:** Cypress 或 Playwright。
        
    - **实践:** 重点覆盖用户注册、登录、工作台数据生成并下载、模板保存/加载、API Key 管理等核心功能。确保 UI 元素的可交互性和整体流程的正确性。
        
4. **Linting 和 Prettier:**
    
    - **工具:** ESLint (结合 @typescript-eslint/parser 和 eslint-plugin-vue) + Prettier。
        
    - **职责:** 强制执行编码规范和风格，在代码提交前自动格式化代码，减少代码审查中的风格问题。
        
    - **配置:** 配置 husky 和 lint-staged 在 git commit 前自动运行 Linting 和 Prettier。
        

### 6. 构建与部署 (Build & Deployment)

我们将利用 Vite 的高性能构建能力，并结合 CI/CD 流程实现自动化部署。

1. **构建工具:**
    
    - **Vite:** 作为开发和构建工具，充分利用其快速冷启动、按需编译和 Rollup 打包优化等特性。
        
    - **TypeScript:** 通过 Vite 内置的 esbuild 或 Vue-tsc 进行类型检查。
        
2. **环境变量管理:**
    
    - 使用 .env 文件 (例如 .env.development, .env.production) 定义不同环境的变量。
        
    - 通过 import.meta.env 在代码中访问这些变量 (如 import.meta.env.VITE_API_BASE_URL)。
        
    - 敏感信息（如 API Key）应仅用于后端或通过安全的 CI/CD 变量传递，避免前端硬编码。
        
3. **性能优化:**
    
    - **代码分割 (Code Splitting):** 结合 Vue Router 的懒加载，按需加载路由对应的组件和模块。
        
    - **资源压缩:** Vite 会自动对 JS、CSS、HTML 进行压缩。
        
    - **图片优化:** 使用 vite-plugin-imagemin 或其他工具压缩图片。
        
    - **CDN (Content Delivery Network):** 生产环境可将静态资源部署到 CDN，加速全球访问。
        
    - **Gzip/Brotli 压缩:** 服务器端开启 HTTP 响应的 Gzip 或 Brotli 压缩。
        
    - **Tree Shaking:** Vite (Rollup) 会自动进行 Tree Shaking，移除未使用的代码。
        
    - **Ant Design Vue 按需引入:** 确保 Ant Design Vue 按照文档说明进行按需引入，减少最终包体积。
        
4. **CI/CD (Continuous Integration / Continuous Deployment):**
    
    - **工具:** 建议使用 GitHub Actions, GitLab CI/CD 或 Jenkins 等 CI/CD 工具。
        
    - **流程:**
        
        1. **代码提交 (Push):** 开发者将代码推送到版本控制系统 (如 Git)。
            
        2. **持续集成 (CI):**
            
            - **Linting & Formatting:** 运行 ESLint 和 Prettier 检查代码规范。
                
            - **Unit Tests & Integration Tests:** 运行所有单元测试和集成测试。
                
            - **Build:** 使用 Vite 构建生产环境代码。
                
            - **Artifacts:** 将构建产物（如 dist 目录）保存为 CI/CD Artifacts。
                
        3. **持续部署 (CD):**
            
            - **部署到开发/测试环境:** 代码合并到 develop 或 test 分支后，自动部署到开发/测试服务器。
                
            - **部署到生产环境:** 代码合并到 main 或 master 分支后，需要人工审批或定时触发，部署到生产服务器。
                
    - **回滚策略:** 确保部署系统支持快速回滚到上一个稳定版本。
        
5. **错误监控与日志:**
    
    - 集成 Sentry, Bugsnag 等前端错误监控服务，实时捕获并上报生产环境的运行时错误。
        
    - 统一的日志输出规范，使用 console.warn, console.error 等，并考虑在生产环境禁用 console.log。