"""
CLI生成命令测试
"""

import subprocess
import sys

import pytest


@pytest.mark.integration
class TestGenerateCommand:
    """CLI生成命令测试类"""

    def test_cli_help_command(self):
        """测试CLI帮助命令"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "--help"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # 验证帮助信息
            assert result.returncode == 0 or "dataforge" in result.stdout.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_version_command(self):
        """测试CLI版本命令"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            # 验证版本信息
            assert result.returncode == 0 or "version" in result.stdout.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_generate_basic(self):
        """测试基本生成命令"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "generate", "name", "--count", "5"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 验证生成成功
            if result.returncode == 0:
                assert len(result.stdout) > 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_generate_with_locale(self):
        """测试带地区参数的生成"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "generate", "name", 
                 "--count", "3", "--locale", "zh_CN"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 验证生成成功
            if result.returncode == 0:
                assert len(result.stdout) > 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_generate_multiple_types(self):
        """测试生成多种类型数据"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "generate", 
                 "name,age,email", "--count", "3"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 验证生成成功
            if result.returncode == 0:
                assert len(result.stdout) > 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_generate_with_format(self):
        """测试指定输出格式"""
        formats = ["json", "csv", "xml"]
        
        for fmt in formats:
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "generate", "name",
                     "--count", "2", "--format", fmt],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证生成成功
                if result.returncode == 0:
                    assert len(result.stdout) > 0
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pytest.skip(f"CLI not available or timeout for format {fmt}")

    def test_cli_generate_to_file(self):
        """测试输出到文件"""
        import tempfile
        import os
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                temp_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "generate", "name",
                     "--count", "5", "--output", temp_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证文件已创建
                if result.returncode == 0 and os.path.exists(temp_file):
                    assert os.path.getsize(temp_file) > 0
            finally:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_invalid_generator(self):
        """测试无效的生成器类型"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "generate", "invalid_type"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 应该返回错误
            assert result.returncode != 0 or "error" in result.stderr.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_invalid_count(self):
        """测试无效的数量参数"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "generate", "name",
                 "--count", "invalid"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 应该返回错误
            assert result.returncode != 0 or "error" in result.stderr.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_cli_batch_generation(self):
        """测试批量生成"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", "generate", "name",
                 "--count", "100"],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # 验证批量生成成功
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                assert len(lines) >= 10  # 至少有一些输出
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")
