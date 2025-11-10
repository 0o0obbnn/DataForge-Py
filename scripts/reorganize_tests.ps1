#!/usr/bin/env pwsh
<#
.SYNOPSIS
    DataForge 测试文件重组脚本
.DESCRIPTION
    将根目录下散落的测试文件按功能分类重组到 tests 目录下
.AUTHOR
    CodeBuddy - 资深前端架构师
#>

param(
    [switch]$DryRun = $false,
    [switch]$Backup = $true
)

# 设置错误处理
$ErrorActionPreference = "Stop"

# 颜色输出函数
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# 创建目录函数
function New-DirectoryIfNotExists {
    param([string]$Path)
    if (-not (Test-Path $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-ColorOutput "✅ 创建目录: $Path" "Green"
    }
}

# 移动文件函数
function Move-TestFile {
    param(
        [string]$Source,
        [string]$Destination,
        [string]$Category
    )
    
    if (Test-Path $Source) {
        if ($DryRun) {
            Write-ColorOutput "🔍 [DRY RUN] 将移动: $Source -> $Destination" "Yellow"
        } else {
            try {
                Move-Item $Source $Destination -Force
                Write-ColorOutput "📁 [$Category] 已移动: $(Split-Path $Source -Leaf) -> $Destination" "Cyan"
            } catch {
                Write-ColorOutput "❌ 移动失败: $Source - $($_.Exception.Message)" "Red"
            }
        }
    } else {
        Write-ColorOutput "⚠️  文件不存在: $Source" "Yellow"
    }
}

Write-ColorOutput "🚀 开始 DataForge 测试文件重组..." "Magenta"
Write-ColorOutput "📍 当前目录: $(Get-Location)" "Gray"

# 1. 创建备份（如果启用）
if ($Backup -and -not $DryRun) {
    $backupDir = "backup_tests_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-DirectoryIfNotExists $backupDir
    
    Write-ColorOutput "💾 创建备份..." "Blue"
    Get-ChildItem -Name "test*" | ForEach-Object {
        Copy-Item $_ "$backupDir/" -Recurse -Force
    }
    Write-ColorOutput "✅ 备份完成: $backupDir" "Green"
}

# 2. 创建新的测试目录结构
Write-ColorOutput "📂 创建测试目录结构..." "Blue"

$testDirs = @(
    "tests/unit",
    "tests/integration", 
    "tests/api",
    "tests/fixtures",
    "tests/data",
    "tests/performance",
    "tests/security"
)

foreach ($dir in $testDirs) {
    New-DirectoryIfNotExists $dir
}

# 3. 定义文件分类映射
$fileMapping = @{
    # 单元测试
    "unit" = @(
        "test_phone_type_safe.py",
        "test_email.py", 
        "test_validation.py",
        "test_marital_simple.py",
        "test_marital_simple_fixed.py",
        "test_marital_status_simple.py",
        "test_phone_simple.py",
        "test_phone.py",
        "test_xml_simple.py",
        "test_simple_batch.py"
    )
    
    # 集成测试
    "integration" = @(
        "test_basic_generators_comprehensive.py",
        "test_new_generators.py",
        "test_finance_generators.py",
        "test_auth_generators.py",
        "test_marital_final.py",
        "test_marital_integration.py",
        "test_bankcard_generator.py",
        "test_context_aware.py",
        "test_relations.py",
        "test_template_management.py",
        "test_export_functionality.py"
    )
    
    # API测试
    "api" = @(
        "test_api_fixed.py",
        "test_batch_generation.py", 
        "test_fastapi.py"
    )
    
    # 性能测试
    "performance" = @(
        "test_streaming_finance.py"
    )
}

# 4. 执行文件移动
Write-ColorOutput "📦 开始移动测试文件..." "Blue"

foreach ($category in $fileMapping.Keys) {
    Write-ColorOutput "📋 处理 $category 类别测试..." "Cyan"
    
    foreach ($file in $fileMapping[$category]) {
        $destination = "tests/$category/"
        Move-TestFile $file $destination $category
    }
}

# 5. 移动测试数据文件
Write-ColorOutput "📋 处理测试数据文件..." "Cyan"

$dataFiles = @(
    "test_export_*.csv",
    "test_export_*.json", 
    "test_export_*.xml",
    "test_export_*.sql"
)

foreach ($pattern in $dataFiles) {
    Get-ChildItem -Name $pattern -ErrorAction SilentlyContinue | ForEach-Object {
        Move-TestFile $_ "tests/data/" "DATA"
    }
}

# 6. 移动测试固定数据
Write-ColorOutput "📋 处理测试固定数据..." "Cyan"

$fixtureFiles = @(
    "test_api_request.json",
    "test_frontend_api.html",
    "test_frontend_download.html"
)

foreach ($file in $fixtureFiles) {
    Move-TestFile $file "tests/fixtures/" "FIXTURE"
}

# 7. 生成重组报告
Write-ColorOutput "📊 生成重组报告..." "Blue"

$reportPath = "test_reorganization_report.md"
$report = @"
# DataForge 测试文件重组报告

**执行时间:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
**执行模式:** $(if ($DryRun) { "预览模式 (Dry Run)" } else { "实际执行" })

## 重组结构

``````
tests/
├── unit/                    # 单元测试 ($(($fileMapping.unit).Count) 个文件)
├── integration/             # 集成测试 ($(($fileMapping.integration).Count) 个文件)  
├── api/                     # API测试 ($(($fileMapping.api).Count) 个文件)
├── performance/             # 性能测试 ($(($fileMapping.performance).Count) 个文件)
├── generators/              # 生成器专项测试 (现有)
├── ui/                      # UI测试 (现有)
├── fixtures/                # 测试固定数据
└── data/                    # 测试输出数据
``````

## 文件分类详情

### 单元测试 (tests/unit/)
$(($fileMapping.unit | ForEach-Object { "- $_" }) -join "`n")

### 集成测试 (tests/integration/)  
$(($fileMapping.integration | ForEach-Object { "- $_" }) -join "`n")

### API测试 (tests/api/)
$(($fileMapping.api | ForEach-Object { "- $_" }) -join "`n")

### 性能测试 (tests/performance/)
$(($fileMapping.performance | ForEach-Object { "- $_" }) -join "`n")

## 后续步骤

1. **更新导入路径:** 检查并修复测试文件中的相对导入
2. **更新配置:** 修改 pytest.ini 或 pyproject.toml 中的测试路径
3. **验证测试:** 运行 ``pytest tests/`` 确保所有测试正常
4. **更新CI/CD:** 修改持续集成配置中的测试路径
5. **更新文档:** 修改 README 中的测试说明

## 推荐的测试命令

``````bash
# 运行所有测试
pytest tests/

# 按类别运行测试
pytest tests/unit/          # 单元测试
pytest tests/integration/   # 集成测试  
pytest tests/api/           # API测试
pytest tests/performance/   # 性能测试

# 并行执行测试
pytest tests/ -n auto
``````
"@

if (-not $DryRun) {
    $report | Out-File -FilePath $reportPath -Encoding UTF8
    Write-ColorOutput "📄 报告已生成: $reportPath" "Green"
}

# 8. 完成总结
Write-ColorOutput "`n🎉 测试文件重组完成!" "Green"
Write-ColorOutput "📈 重组统计:" "White"
Write-ColorOutput "   • 单元测试: $(($fileMapping.unit).Count) 个文件" "Gray"
Write-ColorOutput "   • 集成测试: $(($fileMapping.integration).Count) 个文件" "Gray" 
Write-ColorOutput "   • API测试: $(($fileMapping.api).Count) 个文件" "Gray"
Write-ColorOutput "   • 性能测试: $(($fileMapping.performance).Count) 个文件" "Gray"

if ($DryRun) {
    Write-ColorOutput "`n💡 这是预览模式，没有实际移动文件。" "Yellow"
    Write-ColorOutput "   要执行实际重组，请运行: .\reorganize_tests.ps1" "Yellow"
} else {
    Write-ColorOutput "`n✅ 所有文件已成功重组到 tests/ 目录下" "Green"
    Write-ColorOutput "📋 请查看重组报告: $reportPath" "Cyan"
}