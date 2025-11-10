{
  "// ===================================": "",
  "// Claude Code 权限配置": "",
  "// ===================================": "",

  "claude-code.autoApprovedTools": [
    "// ============ MCP 工具 ============",
    "mcp__serena__*",
    "mcp__sequential-thinking__*",
    "mcp__context7__*",
    "mcp__playwright__*",

    "// ============ 文件操作 ============",
    "Bash(mkdir:*)",
    "Bash(mv:*)",
    "Bash(cp:*)",
    "Bash(touch:*)",
    "Bash(move:*)",
    "Bash(copy:*)",
    "Bash(rename:*)",

    "// ============ Python 开发 ============",
    "Bash(python --version:*)",
    "Bash(python -m:*)",
    "Bash(python *.py:*)",
    "Bash(pip --version:*)",
    "Bash(pip list:*)",
    "Bash(pip show:*)",
    "Bash(pip install:*)",
    "Bash(pytest:*)",
    "Bash(black:*)",
    "Bash(isort:*)",
    "Bash(ruff:*)",
    "Bash(mypy:*)",

    "// ============ Git 操作 ============",
    "Bash(git status:*)",
    "Bash(git branch:*)",
    "Bash(git log:*)",
    "Bash(git diff:*)",
    "Bash(git show:*)",
    "Bash(git add:*)",
    "Bash(git commit:*)",
    "Bash(git checkout:*)",
    "Bash(git pull:*)",
    "Bash(git fetch:*)",

    "// ============ Node.js ============",
    "Bash(node --version:*)",
    "Bash(npm --version:*)",
    "Bash(npm list:*)",
    "Bash(npm install:*)",
    "Bash(npm run:*)",
    "Bash(npm test:*)",
    "Bash(npx:*)",

    "// ============ Maven ============",
    "Bash(mvn --version:*)",
    "Bash(mvn clean:*)",
    "Bash(mvn compile:*)",
    "Bash(mvn test:*)",
    "Bash(mvn package:*)",

    "// ============ 文件操作（只读）============",
    "Bash(ls:*)",
    "Bash(dir:*)",
    "Bash(cat:*)",
    "Bash(type:*)",
    "Bash(head:*)",
    "Bash(tail:*)",
    "Bash(find:*)",
    "Bash(grep:*)",
    "Bash(pwd:*)",
    "Bash(echo:*)",
    "Bash(which:*)",
    "Bash(where:*)",

    "// ============ PowerShell ============",
    "Bash(powershell -Command 'Get-Command:*)",
    "Bash(powershell -Command 'Get-Process:*)",
    "Bash(powershell -Command 'Test-Path:*)",

    "// ============ DataForge CLI ============",
    "Bash(dataforge:*)",
    "Bash(uvicorn:*)"
  ],

  "claude-code.requireConfirmation": [
    "// ============ 危险操作 ============",
    "Bash(rm:*)",
    "Bash(del:*)",
    "Bash(git push:*)",
    "Bash(git push --force:*)",
    "Bash(git reset --hard:*)",
    "Bash(git clean:*)",
    "Bash(pip uninstall:*)",
    "Bash(npm uninstall:*)",
    "Bash(powershell -Command 'Remove-Item:*)"
  ],

  "// ===================================": "",
  "// 其他 Claude Code 设置": "",
  "// ===================================": "",

  "claude-code.enableMCP": true,
  "claude-code.maxTokens": 200000,
  "claude-code.model": "claude-sonnet-4-5",

  "// ===================================": "",
  "// Python 项目设置": "",
  "// ===================================": "",

  "python.defaultInterpreterPath": "D:\\python\\python.exe",
  "python.testing.pytestEnabled": true,
  "python.linting.enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,

  "// ===================================": "",
  "// 文件关联": "",
  "// ===================================": "",

  "files.associations": {
    "*.yaml": "yaml",
    "*.yml": "yaml",
    ".claude/**": "markdown",
    "CLAUDE.md": "markdown"
  }
}
