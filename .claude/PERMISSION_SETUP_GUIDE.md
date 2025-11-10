# Claude Code 权限配置完整指南

## 📌 快速配置（推荐）

### Windows 用户设置路径
```
%APPDATA%\Code\User\settings.json
或
C:\Users\{YourUsername}\AppData\Roaming\Code\User\settings.json
```

### 配置步骤

1. **打开 VS Code 设置**
   - 按 `Ctrl + ,` 打开设置
   - 点击右上角 "打开设置 (JSON)" 图标

2. **添加以下配置**（复制粘贴到 settings.json）：

```jsonc
{
  // ========================================
  // Claude Code 自动批准工具
  // ========================================
  "claude-code.autoApprovedTools": [
    // MCP 服务器
    "mcp__serena__*",
    "mcp__sequential-thinking__*",
    "mcp__context7__*",
    "mcp__playwright__*",
    "mcp__chrome-devtools__*",
    "mcp__magic__*",
    "mcp__tavily__*",

    // Python 开发
    "Bash(python:*)",
    "Bash(pip:*)",
    "Bash(pytest:*)",
    "Bash(black:*)",
    "Bash(isort:*)",
    "Bash(ruff:*)",
    "Bash(mypy:*)",

    // Git 操作（安全命令）
    "Bash(git status:*)",
    "Bash(git branch:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git pull:*)",

    // Node.js
    "Bash(npm:*)",
    "Bash(node:*)",
    "Bash(npx:*)",

    // Maven
    "Bash(mvn:*)",

    // 文件操作（只读）
    "Bash(ls:*)",
    "Bash(cat:*)",
    "Bash(grep:*)",
    "Bash(find:*)",

    // PowerShell（只读命令）
    "Bash(powershell -Command 'Get-*:*)",
    "Bash(powershell -Command 'Test-Path:*)",

    // DataForge 特定
    "Bash(dataforge:*)",
    "Bash(uvicorn:*)"
  ],

  // ========================================
  // 需要确认的危险操作
  // ========================================
  "claude-code.requireConfirmation": [
    "Bash(rm:*)",
    "Bash(del:*)",
    "Bash(git push:*)",
    "Bash(pip uninstall:*)",
    "Bash(npm uninstall:*)"
  ]
}
```

3. **保存并重新加载 VS Code**
   - 按 `Ctrl + Shift + P`
   - 输入 "Reload Window"
   - 按回车

---

## 🔧 详细权限说明

### ✅ 自动批准的命令（无需确认）

#### 1. **文件操作（项目内）**
```bash
mkdir new_folder          # 创建目录
mv file.txt backup.txt    # 移动/重命名文件
cp file.txt copy.txt      # 复制文件
touch new_file.txt        # 创建空文件
move file.txt backup.txt  # Windows 移动
copy file.txt copy.txt    # Windows 复制
rename old.txt new.txt    # Windows 重命名
```

#### 2. **Python 开发**
```bash
python --version           # 查看版本
python -m pytest          # 运行测试
pip install package       # 安装包
pip list                  # 列出包
black .                   # 格式化代码
isort .                   # 排序导入
ruff check .              # 代码检查
mypy .                    # 类型检查
```

#### 3. **Git 操作**
```bash
git status                # 查看状态
git branch               # 查看分支
git log                  # 查看历史
git diff                 # 查看差异
git add .                # 添加文件
git commit -m "msg"      # 提交更改
git checkout -b new      # 创建分支
git pull                 # 拉取更新
```

#### 4. **Node.js / npm**
```bash
npm --version            # 查看版本
npm install package      # 安装包
npm run build           # 运行构建
npm test                # 运行测试
npx command             # 执行命令
```

#### 5. **Maven**
```bash
mvn --version           # 查看版本
mvn clean              # 清理
mvn compile            # 编译
mvn test               # 测试
mvn package            # 打包
```

#### 6. **PowerShell**
```powershell
powershell -Command "Get-Command git"      # 查找命令
powershell -Command "Get-Process"          # 查看进程
powershell -Command "Test-Path file.txt"   # 测试路径
```

#### 7. **文件操作（只读）**
```bash
ls / dir                # 列出文件
cat / type              # 读取文件
grep / findstr          # 搜索文本
find / where            # 查找文件
pwd                     # 当前目录
```

---

### ⚠️ 需要确认的命令

这些命令会弹出确认对话框：

```bash
rm file.txt             # 删除文件
del file.txt            # Windows 删除
git push                # 推送到远程
git push --force        # 强制推送
git reset --hard        # 硬重置
pip uninstall package   # 卸载包
npm uninstall package   # 卸载 npm 包
```

---

### 🚫 禁止命令

以下命令我不会执行：

```bash
rm -rf /                # 危险的系统删除
format C:               # 格式化磁盘
shutdown                # 关闭系统
del /f /s /q C:\*      # 危险的批量删除
```

---

## 🎯 DataForge 项目特定权限

### CLI 命令
```bash
# 自动批准
dataforge generate idcard --count 10
dataforge generate --config config.yaml
dataforge --help

# 需要确认
dataforge generate idcard --count 1000000  # 大量数据生成
```

### API 服务
```bash
# 自动批准
uvicorn dataforge.api.main:app --reload
python -m dataforge.api.main

# 需要确认
uvicorn dataforge.api.main:app --host 0.0.0.0  # 公开访问
```

### 测试执行
```bash
# 自动批准
pytest tests/
pytest tests/ -m unit
pytest tests/ --cov=dataforge

# 需要确认
pytest tests/ --cov-report=html && rm -rf htmlcov  # 包含删除操作
```

---

## 📝 自定义配置

### 添加新的自动批准命令

在 `settings.json` 中添加：

```jsonc
"claude-code.autoApprovedTools": [
  // 现有配置...

  // 添加自定义命令
  "Bash(your-custom-command:*)",
  "Bash(docker:*)",           // Docker 命令
  "Bash(kubectl:*)",          // Kubernetes 命令
  "Bash(terraform:*)"         // Terraform 命令
]
```

### 添加需要确认的命令

```jsonc
"claude-code.requireConfirmation": [
  // 现有配置...

  // 添加自定义危险命令
  "Bash(docker system prune:*)",
  "Bash(kubectl delete:*)"
]
```

---

## 🔍 验证配置

运行以下命令测试配置是否生效：

```bash
# 应该自动执行
python --version
git status
npm --version

# 应该需要确认
git push
rm test.txt
```

---

## ⚡ 性能优化建议

1. **批量操作使用通配符**
   ```jsonc
   "Bash(pytest:*)"  // 匹配所有 pytest 命令
   ```

2. **MCP 工具全部批准**
   ```jsonc
   "mcp__*"  // 批准所有 MCP 工具
   ```

3. **项目特定工具**
   ```jsonc
   "Bash(dataforge:*)",
   "Bash(uvicorn:*)"
   ```

---

## 🆘 常见问题

### Q: 配置后不生效？
A: 重新加载 VS Code 窗口（Ctrl+Shift+P → "Reload Window"）

### Q: 某些命令仍然需要确认？
A: 检查命令格式是否与配置匹配，注意通配符使用

### Q: 如何临时禁用自动批准？
A: 在命令前添加 `--interactive` 标志（如果工具支持）

### Q: 如何查看当前配置？
A: 打开 VS Code 设置（Ctrl+,）搜索 "claude-code"

---

## 📚 参考资料

- [Claude Code 官方文档](https://docs.claude.com/claude-code)
- [VS Code 设置指南](https://code.visualstudio.com/docs/getstarted/settings)
- [CLAUDE.md 项目配置](../CLAUDE.md)

---

## ✅ 配置完成检查清单

- [ ] 打开 VS Code 设置 JSON
- [ ] 复制粘贴权限配置
- [ ] 保存 settings.json
- [ ] 重新加载 VS Code 窗口
- [ ] 测试 `python --version`（应自动执行）
- [ ] 测试 `git status`（应自动执行）
- [ ] 测试 `git push`（应需要确认）
- [ ] 验证 MCP 工具可用

配置完成后，您可以享受更流畅的开发体验！🎉
