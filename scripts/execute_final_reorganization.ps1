#!/usr/bin/env pwsh
<#
.SYNOPSIS
    DataForge 测试文件最终重组执行脚本
.DESCRIPTION
    一次性完成所有剩余测试文件的重组，避免文件冲突
#>

param(
    [switch]$Confirm = $false
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

Write-ColorOutput "🎯 DataForge 测试文件最终重组执行" "Magenta"
Write-ColorOutput "📍 当前目录: $(Get-Location)" "Gray"

# 检查剩余文件
$remainingFiles = Get-ChildItem -Path . -Name "test*.py"
Write-ColorOutput "📋 发现 $($remainingFiles.Count) 个待处理文件" "Cyan"

if ($remainingFiles.Count -eq 0) {
    Write-ColorOutput "✅ 没有需要处理的文件，重组已完成！" "Green"
    exit 0
}

# 显示文件列表
Write-ColorOutput "`n📄 待处理文件列表:" "Yellow"
$remainingFiles | ForEach-Object { Write-ColorOutput "   • $_" "Gray" }

# 定义移动操作
$moveOperations = @(
    # API测试
    @{ Source = "test_api_fixed.py"; Target = "tests/api/test_api_endpoints.py"; Category = "API" },
    @{ Source = "test_batch_generation.py"; Target = "tests/api/test_batch_api.py"; Category = "API" },
    @{ Source = "test_fastapi.py"; Target = "tests/api/test_fastapi_server.py"; Category = "API" },
    
    # 集成测试
    @{ Source = "test_basic_generators_comprehensive.py"; Target = "tests/integration/test_comprehensive_generators.py"; Category = "INTEGRATION" },
    @{ Source = "test_auth_generators.py"; Target = "tests/integration/test_auth_integration.py"; Category = "INTEGRATION" },
    @{ Source = "test_finance_generators.py"; Target = "tests/integration/test_finance_integration.py"; Category = "INTEGRATION" },
    @{ Source = "test_bankcard_generator.py"; Target = "tests/integration/test_bankcard_integration.py"; Category = "INTEGRATION" },
    @{ Source = "test_marital_final.py"; Target = "tests/integration/test_marital_complete.py"; Category = "INTEGRATION" },
    @{ Source = "test_marital_integration.py"; Target = "tests/integration/test_marital_full_integration.py"; Category = "INTEGRATION" },
    @{ Source = "test_context_aware.py"; Target = "tests/integration/test_context_integration.py"; Category = "INTEGRATION" },
    @{ Source = "test_relations.py"; Target = "tests/integration/test_data_relations.py"; Category = "INTEGRATION" },
    @{ Source = "test_template_management.py"; Target = "tests/integration/test_template_system.py"; Category = "INTEGRATION" },
    @{ Source = "test_export_functionality.py"; Target = "tests/integration/test_export_system.py"; Category = "INTEGRATION" },
    @{ Source = "test_new_generators.py"; Target = "tests/integration/test_extended_generators.py"; Category = "INTEGRATION" },
    
    # 性能测试
    @{ Source = "test_streaming_finance.py"; Target = "tests/performance/test_streaming_performance.py"; Category = "PERFORMANCE" }
)

# 显示移动计划
Write-ColorOutput "`n📋 移动计划:" "Blue"
$categoryStats = @{}
foreach ($op in $moveOperations) {
    if (Test-Path $op.Source) {
        Write-ColorOutput "   [$($op.Category)] $($op.Source) → $($op.Target)" "Cyan"
        $categoryStats[$op.Category] = ($categoryStats[$op.Category] ?? 0) + 1
    }
}

Write-ColorOutput "`n📊 分类统计:" "White"
foreach ($cat in $categoryStats.Keys) {
    Write-ColorOutput "   • $cat`: $($categoryStats[$cat]) 个文件" "Gray"
}

# 确认执行
if (-not $Confirm) {
    Write-ColorOutput "`n⚠️  这将移动 $($moveOperations.Count) 个文件。" "Yellow"
    $response = Read-Host "是否继续执行? (y/N)"
    if ($response -ne 'y' -and $response -ne 'Y') {
        Write-ColorOutput "❌ 用户取消操作" "Red"
        exit 1
    }
}

# 执行移动操作
Write-ColorOutput "`n🚀 开始执行移动操作..." "Green"
$successCount = 0
$errorCount = 0

foreach ($op in $moveOperations) {
    if (Test-Path $op.Source) {
        try {
            # 检查目标文件是否存在
            if (Test-Path $op.Target) {
                Write-ColorOutput "⚠️  目标文件已存在，将覆盖: $($op.Target)" "Yellow"
            }
            
            # 执行移动
            Move-Item $op.Source $op.Target -Force
            Write-ColorOutput "✅ [$($op.Category)] $($op.Source) → $($op.Target)" "Green"
            $successCount++
        }
        catch {
            Write-ColorOutput "❌ [$($op.Category)] 移动失败: $($op.Source) - $($_.Exception.Message)" "Red"
            $errorCount++
        }
    } else {
        Write-ColorOutput "⚠️  源文件不存在: $($op.Source)" "Yellow"
    }
}

# 最终检查
Write-ColorOutput "`n🔍 最终检查..." "Blue"
$finalRemaining = Get-ChildItem -Path . -Name "test*.py"

Write-ColorOutput "`n📊 执行结果:" "Cyan"
Write-ColorOutput "   • 成功移动: $successCount 个文件" "Green"
Write-ColorOutput "   • 移动失败: $errorCount 个文件" "Red"
Write-ColorOutput "   • 根目录剩余: $($finalRemaining.Count) 个测试文件" "Yellow"

if ($finalRemaining.Count -gt 0) {
    Write-ColorOutput "`n⚠️  根目录仍有测试文件:" "Yellow"
    $finalRemaining | ForEach-Object { Write-ColorOutput "   - $_" "Gray" }
}

# 生成最终统计
Write-ColorOutput "`n📈 tests目录最终统计:" "Blue"
$finalStats = @{}
$testDirs = @("unit", "integration", "api", "performance", "generators", "ui")

foreach ($dir in $testDirs) {
    $dirPath = "tests/$dir"
    if (Test-Path $dirPath) {
        if ($dir -eq "generators") {
            $count = (Get-ChildItem $dirPath -Recurse -Name "*.py").Count
        } elseif ($dir -eq "ui") {
            $count = (Get-ChildItem $dirPath -Name "*.ts").Count
        } else {
            $count = (Get-ChildItem $dirPath -Name "*.py" -ErrorAction SilentlyContinue).Count
        }
        $finalStats[$dir] = $count
        Write-ColorOutput "   • $dir`: $count 个文件" "Gray"
    }
}

$totalTestFiles = $finalStats.Values | Measure-Object -Sum | Select-Object -ExpandProperty Sum
Write-ColorOutput "   • 总计: $totalTestFiles 个测试文件" "White"

if ($finalRemaining.Count -eq 0 -and $errorCount -eq 0) {
    Write-ColorOutput "`n🎉 测试文件重组完全成功！" "Green"
    Write-ColorOutput "📋 所有测试文件已按功能分类重组到 tests/ 目录下" "Cyan"
    Write-ColorOutput "📄 详细信息请查看: final_reorganization_plan.md" "Blue"
} else {
    Write-ColorOutput "`n⚠️  重组部分完成，请检查剩余问题" "Yellow"
}

Write-ColorOutput "`n✨ 重组操作执行完毕！" "Magenta"