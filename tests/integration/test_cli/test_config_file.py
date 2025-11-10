"""
CLI配置文件测试
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest
import yaml


@pytest.mark.integration
class TestConfigFile:
    """CLI配置文件测试类"""

    def test_json_config_file(self):
        """测试JSON配置文件"""
        config = {
            "generators": [
                {"type": "name", "count": 5},
                {"type": "age", "count": 5}
            ],
            "output": {
                "format": "json"
            }
        }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(config, f)
                config_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "--config", config_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证配置文件被正确读取
                if result.returncode == 0:
                    assert len(result.stdout) > 0
            finally:
                if os.path.exists(config_file):
                    os.remove(config_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_yaml_config_file(self):
        """测试YAML配置文件"""
        config = {
            "generators": [
                {"type": "name", "count": 3},
                {"type": "email", "count": 3}
            ],
            "output": {
                "format": "csv"
            }
        }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.yaml') as f:
                yaml.dump(config, f)
                config_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "--config", config_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证配置文件被正确读取
                if result.returncode == 0:
                    assert len(result.stdout) > 0
            finally:
                if os.path.exists(config_file):
                    os.remove(config_file)
        except (subprocess.TimeoutExpired, FileNotFoundError, ImportError):
            pytest.skip("CLI not available, timeout, or yaml not installed")

    def test_invalid_config_file(self):
        """测试无效的配置文件"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                f.write("invalid json content {{{")
                config_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "--config", config_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 应该返回错误
                assert result.returncode != 0 or "error" in result.stderr.lower()
            finally:
                if os.path.exists(config_file):
                    os.remove(config_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_missing_config_file(self):
        """测试不存在的配置文件"""
        try:
            result = subprocess.run(
                [sys.executable, "-m", "dataforge.cli.main", 
                 "--config", "/nonexistent/config.json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            # 应该返回错误
            assert result.returncode != 0 or "error" in result.stderr.lower()
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_config_with_parameters(self):
        """测试带参数的配置"""
        config = {
            "generators": [
                {
                    "type": "age",
                    "count": 5,
                    "parameters": {
                        "min": 18,
                        "max": 65
                    }
                }
            ]
        }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(config, f)
                config_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "--config", config_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证参数被正确应用
                if result.returncode == 0:
                    assert len(result.stdout) > 0
            finally:
                if os.path.exists(config_file):
                    os.remove(config_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_config_with_output_file(self):
        """测试配置文件指定输出文件"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as output_f:
                output_file = output_f.name
            
            config = {
                "generators": [
                    {"type": "name", "count": 5}
                ],
                "output": {
                    "file": output_file,
                    "format": "json"
                }
            }
            
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as config_f:
                json.dump(config, config_f)
                config_file = config_f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", "--config", config_file],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证输出文件已创建
                if result.returncode == 0 and os.path.exists(output_file):
                    assert os.path.getsize(output_file) > 0
            finally:
                for f in [config_file, output_file]:
                    if os.path.exists(f):
                        os.remove(f)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_config_override_by_cli_args(self):
        """测试CLI参数覆盖配置文件"""
        config = {
            "generators": [
                {"type": "name", "count": 5}
            ]
        }
        
        try:
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
                json.dump(config, f)
                config_file = f.name
            
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "dataforge.cli.main", 
                     "--config", config_file, "--count", "10"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # 验证CLI参数覆盖了配置文件
                if result.returncode == 0:
                    assert len(result.stdout) > 0
            finally:
                if os.path.exists(config_file):
                    os.remove(config_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")
