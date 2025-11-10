#!/usr/bin/env pwsh
<#
.SYNOPSIS
    处理剩余的测试文件 - 避免文件名冲突
.DESCRIPTION
    将根目录下剩余的测试文件移动到合适的位置，处理文件名冲突
#>

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

Write-ColorOutput "🔧 处理剩余的测试文件..." "Magenta"

# 获取剩余的测试文件
$remainingFiles = Get-ChildItem -Path . -Name "test*.py"
Write-ColorOutput "📋 发现 $($remainingFiles.Count) 个剩余测试文件" "Cyan"

# 定义文件分类和处理策略
$fileHandling = @{
    # API测试
    "test_api_fixed.py" = @{
        "category" = "api"
        "newname" = "test_api_endpoints.py"
        "action" = "rename_move"
    }
    "test_batch_generation.py" = @{
        "category" = "api" 
        "newname" = "test_batch_api.py"
        "action" = "rename_move"
    }
    "test_fastapi.py" = @{
        "category" = "api"
        "newname" = "test_fastapi_server.py" 
        "action" = "rename_move"
    }
    
    # 集成测试
    "test_basic_generators_comprehensive.py" = @{
        "category" = "integration"
        "newname" = "test_comprehensive_generators.py"
        "action" = "rename_move"
    }
    "test_new_generators.py" = @{
        "category" = "integration"
        "newname" = "test_extended_generators.py"
        "action" = "check_existing"
    }
    "test_finance_generators.py" = @{
        "category" = "integration"
        "newname" = "test_finance_integration.py"
        "action" = "rename_move"
    }
    "test_auth_generators.py" = @{
        "category" = "integration"
        "newname" = "test_auth_integration.py"
        "action" = "rename_move"
    }
    "test_marital_final.py" = @{
        "category" = "integration"
        "newname" = "test_marital_complete.py"
        "action" = "rename_move"
    }
    "test_marital_integration.py" = @{
        "category" = "integration"
        "newname" = "test_marital_full_integration.py"
        "action" = "rename_move"
    }
    "test_bankcard_generator.py" = @{
        "category" = "integration"
        "newname" = "test_bankcard_integration.py"
        "action" = "rename_move"
    }
    "test_context_aware.py" = @{
        "category" = "integration"
        "newname" = "test_context_integration.py"
        "action" = "rename_move"
    }
    "test_relations.py" = @{
        "category" = "integration"
        "newname" = "test_data_relations.py"
        "action" = "rename_move"
    }
    "test_template_management.py" = @{
        "category" = "integration"
        "newname" = "test_template_system.py"
        "action" = "rename_move"
    }
    "test_export_functionality.py" = @{
        "category" = "integration"
        "newname" = "test_export_system.py"
        "action" = "rename_move"
    }
    
    # 性能测试
    "test_streaming_finance.py" = @{
        "category" = "performance"
        "newname" = "test_streaming_performance.py"
        "action" = "rename_move"
    }
}

# 处理每个文件
foreach ($file in $remainingFiles) {
    if ($fileHandling.ContainsKey($file)) {
        $config = $fileHandling[$file]
        $targetDir = "tests/$($config.category)/"
        $targetPath = "$targetDir$($config.newname)"
        
        Write-ColorOutput "📁 处理: $file -> $($config.category)/$($config.newname)" "Yellow"
        
        # 检查目标文件是否已存在
        if (Test-Path $targetPath) {
            Write-ColorOutput "⚠️  目标文件已存在: $targetPath" "Red"
            
            # 比较文件大小和修改时间
            $sourceInfo = Get-Item $file
            $targetInfo = Get-Item $targetPath
            
            Write-ColorOutput "   源文件: $($sourceInfo.Length) bytes, 修改时间: $($sourceInfo.LastWriteTime)" "Gray"
            Write-ColorOutput "   目标文件: $($targetInfo.Length) bytes, 修改时间: $($targetInfo.LastWriteTime)" "Gray"
            
            if ($sourceInfo.LastWriteTime -gt $targetInfo.LastWriteTime) {
                Write-ColorOutput "   源文件更新，覆盖目标文件" "Green"
                Move-Item $file $targetPath -Force
            } else {
                Write-ColorOutput "   目标文件更新，删除源文件" "Blue"
                Remove-Item $file -Force
            }
        } else {
            # 直接移动并重命名
            Move-Item $file $targetPath
            Write-ColorOutput "✅ 已移动: $file -> $targetPath" "Green"
        }
    } else {
        Write-ColorOutput "❓ 未知文件: $file (跳过)" "Yellow"
    }
}

Write-ColorOutput "`n🎉 剩余文件处理完成!" "Green"

# 最终统计
Write-ColorOutput "`n📊 最终统计:" "Cyan"
$finalStats = @{
    "unit" = (Get-ChildItem "tests/unit/" -Name "*.py").Count
    "integration" = (Get-ChildItem "tests/integration/" -Name "*.py").Count  
    "api" = (Get-ChildItem "tests/api/" -Name "*.py").Count
    "performance" = (Get-ChildItem "tests/performance/" -Name "*.py").Count
    "generators" = (Get-ChildItem "tests/generators/" -Recurse -Name "*.py").Count
    "ui" = (Get-ChildItem "tests/ui/" -Name "*.ts").Count
}

foreach ($category in $finalStats.Keys) {
    Write-ColorOutput "   • $category`: $($finalStats[$category]) 个文件" "Gray"
}

$totalTests = $finalStats.Values | Measure-Object -Sum | Select-Object -ExpandProperty Sum
Write-ColorOutput "   • 总计: $totalTests 个测试文件" "White"

# 检查根目录是否还有测试文件
$remainingRoot = Get-ChildItem -Path . -Name "test*.py"
if ($remainingRoot.Count -eq 0) {
    Write-ColorOutput "`n✅ 根目录已清理完毕，所有测试文件已重组!" "Green"
} else {
    Write-ColorOutput "`n⚠️  根目录仍有 $($remainingRoot.Count) 个测试文件:" "Yellow"
    $remainingRoot | ForEach-Object { Write-ColorOutput "   - $_" "Gray" }
}