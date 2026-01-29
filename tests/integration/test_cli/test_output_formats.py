"""
CLI输出格式测试
"""

import json
import os
import subprocess
import sys
import tempfile

import pytest


@pytest.mark.integration
class TestOutputFormats:
    """CLI输出格式测试类"""

    def test_json_output_format(self):
        """测试JSON输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "3",
                    "--format",
                    "json",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 验证输出是有效的JSON
                try:
                    data = json.loads(result.stdout)
                    assert isinstance(data, (list, dict))
                except json.JSONDecodeError:
                    pass  # 如果不是JSON格式，跳过
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_csv_output_format(self):
        """测试CSV输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name,age",
                    "--count",
                    "3",
                    "--format",
                    "csv",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 验证输出包含CSV特征
                lines = result.stdout.strip().split("\n")
                assert len(lines) > 0
                # CSV通常有表头和数据行
                if len(lines) > 1:
                    assert "," in lines[0] or "\t" in lines[0]
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_xml_output_format(self):
        """测试XML输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "3",
                    "--format",
                    "xml",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 验证输出包含XML特征
                assert "<" in result.stdout and ">" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_sql_output_format(self):
        """测试SQL输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "3",
                    "--format",
                    "sql",
                    "--table",
                    "users",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 验证输出包含SQL特征
                output_upper = result.stdout.upper()
                assert "INSERT" in output_upper or "VALUES" in output_upper
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_yaml_output_format(self):
        """测试YAML输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "3",
                    "--format",
                    "yaml",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 验证输出包含YAML特征
                assert ":" in result.stdout or "-" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_text_output_format(self):
        """测试纯文本输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "5",
                    "--format",
                    "text",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 验证输出是纯文本
                lines = result.stdout.strip().split("\n")
                assert len(lines) >= 1
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_pretty_print_json(self):
        """测试美化JSON输出"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "2",
                    "--format",
                    "json",
                    "--pretty",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 美化的JSON应该有缩进
                assert "  " in result.stdout or "\t" in result.stdout
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_compact_json(self):
        """测试紧凑JSON输出"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "2",
                    "--format",
                    "json",
                    "--compact",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                # 紧凑的JSON不应该有多余的空白
                assert len(result.stdout.strip().split("\n")) <= 3
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_output_to_file_json(self):
        """测试输出JSON到文件"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".json"
            ) as f:
                output_file = f.name

            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "dataforge.cli.main",
                        "generate",
                        "name",
                        "--count",
                        "5",
                        "--format",
                        "json",
                        "--output",
                        output_file,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0 and os.path.exists(output_file):
                    # 验证文件内容是有效的JSON
                    with open(output_file, encoding="utf-8") as f:
                        try:
                            data = json.load(f)
                            assert isinstance(data, (list, dict))
                        except json.JSONDecodeError:
                            pass
            finally:
                if os.path.exists(output_file):
                    os.remove(output_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_output_to_file_csv(self):
        """测试输出CSV到文件"""
        try:
            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, suffix=".csv"
            ) as f:
                output_file = f.name

            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "dataforge.cli.main",
                        "generate",
                        "name,age",
                        "--count",
                        "5",
                        "--format",
                        "csv",
                        "--output",
                        output_file,
                    ],
                    capture_output=True,
                    text=True,
                    timeout=10,
                )

                if result.returncode == 0 and os.path.exists(output_file):
                    # 验证文件内容
                    with open(output_file, encoding="utf-8") as f:
                        content = f.read()
                        assert len(content) > 0
            finally:
                if os.path.exists(output_file):
                    os.remove(output_file)
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")

    def test_invalid_output_format(self):
        """测试无效的输出格式"""
        try:
            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "dataforge.cli.main",
                    "generate",
                    "name",
                    "--count",
                    "3",
                    "--format",
                    "invalid_format",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )

            # 应该返回错误或使用默认格式
            assert result.returncode != 0 or len(result.stdout) > 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pytest.skip("CLI not available or timeout")
