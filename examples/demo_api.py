#!/usr/bin/env python3
"""
DataForge API客户端演示
演示如何使用API生成数据
"""

import time
from typing import Any

import requests


class DataForgeAPIClient:
    """DataForge API客户端"""

    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()

    def health_check(self) -> dict[str, Any]:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

    def list_generators(self) -> dict[str, Any]:
        """获取生成器列表"""
        response = self.session.get(f"{self.base_url}/generators")
        response.raise_for_status()
        return response.json()

    def get_generator_info(self, generator_name: str) -> dict[str, Any]:
        """获取生成器详细信息"""
        response = self.session.get(f"{self.base_url}/generators/{generator_name}")
        response.raise_for_status()
        return response.json()

    def generate_data(
        self, generator_name: str, count: int = 1, parameters: dict[str, Any] = None
    ) -> dict[str, Any]:
        """生成数据"""
        payload = {
            "generator_type": generator_name,
            "count": count,
            "parameters": parameters or {},
            "validate": True,
            "output_format": "json",
        }

        response = self.session.post(
            f"{self.base_url}/generate/{generator_name}", json=payload
        )
        response.raise_for_status()
        return response.json()

    def generate_batch_data(
        self, generators_config: list, count: int = 1
    ) -> dict[str, Any]:
        """批量生成关联数据"""
        payload = {
            "generators": generators_config,
            "count": count,
            "output_format": "json",
        }

        response = self.session.post(f"{self.base_url}/batch/generate", json=payload)
        response.raise_for_status()
        return response.json()

    def generate_async(
        self, generator_name: str, count: int, parameters: dict[str, Any] = None
    ) -> dict[str, Any]:
        """异步生成数据"""
        payload = {
            "generator_type": generator_name,
            "count": count,
            "parameters": parameters or {},
            "validate": True,
            "output_format": "json",
        }

        response = self.session.post(
            f"{self.base_url}/generate/async/{generator_name}", json=payload
        )
        response.raise_for_status()
        return response.json()

    def get_task_status(self, task_id: str) -> dict[str, Any]:
        """获取任务状态"""
        response = self.session.get(f"{self.base_url}/tasks/{task_id}")
        response.raise_for_status()
        return response.json()

    def wait_for_task(self, task_id: str, timeout: int = 60) -> dict[str, Any]:
        """等待任务完成"""
        start_time = time.time()

        while time.time() - start_time < timeout:
            task_status = self.get_task_status(task_id)

            if task_status["status"] in ["completed", "failed"]:
                return task_status

            print(f"任务进度: {task_status.get('progress', 0):.1f}%")
            time.sleep(1)

        raise TimeoutError(f"任务 {task_id} 在 {timeout} 秒内未完成")


def demo_api_basic_usage():
    """演示API基本用法"""
    print("=== DataForge API 基本用法演示 ===")

    client = DataForgeAPIClient()

    try:
        # 1. 健康检查
        print("1. 健康检查:")
        health = client.health_check()
        print(f"   状态: {health['status']}")
        print(f"   生成器数量: {health['generators_count']}")
        print()

        # 2. 获取生成器列表
        print("2. 可用生成器 (前10个):")
        generators = client.list_generators()
        for i, gen in enumerate(generators[:10]):
            print(f"   {i + 1}. {gen['name']} - {gen['type']}")
        print(f"   ... 总共 {len(generators)} 个生成器")
        print()

        # 3. 生成单个数据
        print("3. 生成身份证号:")
        result = client.generate_data(
            generator_name="idcard",
            count=3,
            parameters={"region": "110000", "gender": "MALE"},
        )
        print(f"   生成数量: {result['count']}")
        for item in result["data"][:3]:
            print(f"   - {item['idcard']}")
        print()

        # 4. 生成关联数据
        print("4. 生成关联数据 (姓名+邮箱+手机):")
        batch_config = [
            {"generator_type": "name", "parameters": {"gender": "FEMALE"}},
            {"generator_type": "email", "parameters": {"type": "COMMON"}},
            {"generator_type": "phone", "parameters": {"operator": "MOBILE"}},
        ]

        batch_result = client.generate_batch_data(batch_config, count=2)
        print(f"   生成数量: {batch_result['count']}")
        for i, record in enumerate(batch_result["data"]):
            print(
                f"   用户{i + 1}: {record['name']} | {record['email']} | {record['phone']}"
            )
        print()

        # 5. 异步生成大量数据
        print("5. 异步生成大量数据:")
        async_task = client.generate_async(
            generator_name="uuid", count=1000, parameters={"version": 4}
        )

        print(f"   任务ID: {async_task['task_id']}")
        print(f"   状态: {async_task['status']}")

        # 等待任务完成
        print("   等待任务完成...")
        final_result = client.wait_for_task(async_task["task_id"])

        if final_result["status"] == "completed":
            data_count = len(final_result["result"]["data"])
            print(f"   ✅ 任务完成，生成了 {data_count} 条UUID")
            print(
                f"   前3个: {[item['uuid'] for item in final_result['result']['data'][:3]]}"
            )
        else:
            print(f"   ❌ 任务失败: {final_result.get('error', 'Unknown error')}")

        print("\n🎉 API演示完成！")

    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务")
        print("请确保API服务正在运行: python start_api.py")
    except Exception as e:
        print(f"❌ API调用出错: {e}")


def demo_api_advanced_usage():
    """演示API高级用法"""
    print("\n=== DataForge API 高级用法演示 ===")

    client = DataForgeAPIClient()

    try:
        # 1. 获取特定生成器信息
        print("1. 生成器详细信息:")
        info = client.get_generator_info("email")
        print(f"   名称: {info['name']}")
        print(f"   类型: {info['type']}")
        print(f"   参数: {', '.join(info['parameters'])}")
        print(f"   示例参数: {info['example_parameters']}")
        print()

        # 2. 多种数据类型生成
        print("2. 多种数据类型生成:")
        data_types = ["integer", "string", "boolean", "uuid", "date"]

        for data_type in data_types:
            result = client.generate_data(data_type, count=1)
            sample_data = result["data"][0][data_type]
            print(f"   {data_type}: {sample_data}")
        print()

        # 3. 复杂参数配置
        print("3. 复杂参数配置:")

        # 生成中文格式的性别
        result = client.generate_data(
            "gender", count=5, parameters={"format": "CHINESE", "type": "BINARY"}
        )
        genders = [item["gender"] for item in result["data"]]
        print(f"   中文性别: {', '.join(genders)}")

        # 生成指定范围的整数
        result = client.generate_data(
            "integer",
            count=5,
            parameters={"min": 100, "max": 200, "distribution": "NORMAL"},
        )
        numbers = [item["integer"] for item in result["data"]]
        print(f"   正态分布整数: {numbers}")

        # 生成IPv6地址
        result = client.generate_data(
            "ip_address", count=3, parameters={"version": 6, "type": "PUBLIC"}
        )
        ipv6_addresses = [item["ip_address"] for item in result["data"]]
        print(f"   IPv6地址: {ipv6_addresses}")
        print()

    except Exception as e:
        print(f"❌ 高级演示出错: {e}")


def main():
    """主演示函数"""
    print("DataForge API 客户端演示")
    print("=" * 50)

    # 检查API服务是否运行
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API服务运行正常")
        else:
            print("⚠️ API服务响应异常")
            return
    except requests.exceptions.RequestException:
        print("❌ API服务未运行")
        print("请先启动API服务: python start_api.py")
        return

    # 运行演示
    demo_api_basic_usage()
    demo_api_advanced_usage()


if __name__ == "__main__":
    main()
