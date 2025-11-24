"""
DataForge 数据预加载模块
提供数据预加载和智能缓存管理功能
"""

import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Optional

from .cache import get_cached_data, get_data_file_path

# 配置日志
logger = logging.getLogger(__name__)


class DataPreloader:
    """智能数据预加载器"""

    def __init__(self, max_workers: int = 4):
        """
        初始化预加载器

        Args:
            max_workers: 最大工作线程数
        """
        self.max_workers = max_workers
        self._preload_configs: list[dict[str, Any]] = []
        self._loading_status: dict[str, str] = {}  # pending, loading, completed, failed
        self._loading_lock = threading.RLock()
        self._completion_callbacks: dict[str, list[Callable]] = {}

    def register_data_source(
        self,
        name: str,
        file_path: str,
        loader_func: Optional[Callable] = None,
        priority: int = 0,
        auto_reload: bool = False,
        dependencies: Optional[list[str]] = None,
    ) -> None:
        """
        注册数据源

        Args:
            name: 数据源名称
            file_path: 文件路径（相对路径）
            loader_func: 自定义加载函数
            priority: 优先级（数字越大优先级越高）
            auto_reload: 是否自动重载
            dependencies: 依赖的其他数据源
        """
        config = {
            "name": name,
            "file_path": get_data_file_path(file_path),
            "loader_func": loader_func,
            "priority": priority,
            "auto_reload": auto_reload,
            "dependencies": dependencies or [],
        }

        with self._loading_lock:
            # 检查是否已存在
            existing_idx = None
            for i, existing in enumerate(self._preload_configs):
                if existing["name"] == name:
                    existing_idx = i
                    break

            if existing_idx is not None:
                self._preload_configs[existing_idx] = config
                logger.info(f"更新数据源配置: {name}")
            else:
                self._preload_configs.append(config)
                logger.info(f"注册数据源: {name}")

            # 按优先级排序
            self._preload_configs.sort(key=lambda x: x["priority"], reverse=True)

            # 初始化状态
            self._loading_status[name] = "pending"
            self._completion_callbacks[name] = []

    def add_completion_callback(
        self, name: str, callback: Callable[[str, bool, Any], None]
    ) -> None:
        """
        添加加载完成回调

        Args:
            name: 数据源名称
            callback: 回调函数，参数为 (name, success, data/error)
        """
        with self._loading_lock:
            if name not in self._completion_callbacks:
                self._completion_callbacks[name] = []
            self._completion_callbacks[name].append(callback)

    def preload_all(self, timeout: Optional[float] = None) -> dict[str, Any]:
        """
        同步预加载所有注册的数据源

        Args:
            timeout: 超时时间（秒）

        Returns:
            加载结果统计
        """
        start_time = time.time()

        # 解析依赖关系并确定加载顺序
        load_order = self._resolve_dependencies()

        results = {
            "total": len(load_order),
            "success": 0,
            "failed": 0,
            "errors": [],
            "loaded_data": {},
            "loading_time": 0,
        }

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # 分批处理有依赖关系的数据源
            current_batch = []
            completed_sources = set()

            for source_name in load_order:
                config = self._get_config_by_name(source_name)
                if not config:
                    continue

                # 检查依赖是否已完成
                dependencies_ready = all(
                    dep in completed_sources for dep in config["dependencies"]
                )

                if dependencies_ready:
                    current_batch.append(config)
                else:
                    # 如果当前批次不为空，先处理当前批次
                    if current_batch:
                        self._process_batch(
                            executor, current_batch, results, completed_sources, timeout
                        )
                        current_batch = []

                    # 等待依赖完成后再加载当前项
                    current_batch.append(config)

            # 处理最后一批
            if current_batch:
                self._process_batch(
                    executor, current_batch, results, completed_sources, timeout
                )

        results["loading_time"] = time.time() - start_time
        logger.info(
            f"预加载完成: {results['success']}/{results['total']} 成功, 耗时 {results['loading_time']:.2f}s"
        )

        return results

    def preload_async(self) -> threading.Thread:
        """
        异步预加载所有数据源

        Returns:
            预加载线程
        """

        def preload_worker():
            try:
                self.preload_all()
            except Exception as e:
                logger.error(f"异步预加载失败: {e}")

        thread = threading.Thread(
            target=preload_worker, daemon=True, name="DataPreloader"
        )
        thread.start()
        return thread

    def preload_single(self, name: str, force_reload: bool = False) -> bool:
        """
        预加载单个数据源

        Args:
            name: 数据源名称
            force_reload: 是否强制重新加载

        Returns:
            是否加载成功
        """
        config = self._get_config_by_name(name)
        if not config:
            logger.error(f"数据源不存在: {name}")
            return False

        # 检查当前状态
        with self._loading_lock:
            current_status = self._loading_status.get(name, "pending")
            if current_status == "loading":
                logger.warning(f"数据源正在加载中: {name}")
                return False
            elif current_status == "completed" and not force_reload:
                logger.info(f"数据源已加载: {name}")
                return True

            self._loading_status[name] = "loading"

        try:
            # 加载数据
            data = get_cached_data(config["file_path"], config["loader_func"])

            with self._loading_lock:
                self._loading_status[name] = "completed"

            # 执行回调
            self._execute_callbacks(name, True, data)

            logger.info(f"数据源加载成功: {name}")
            return True

        except Exception as e:
            with self._loading_lock:
                self._loading_status[name] = "failed"

            # 执行回调
            self._execute_callbacks(name, False, e)

            logger.error(f"数据源加载失败 {name}: {e}")
            return False

    def get_loading_status(self, name: Optional[str] = None) -> dict[str, str]:
        """
        获取加载状态

        Args:
            name: 数据源名称，如果为None则返回所有状态

        Returns:
            状态信息
        """
        with self._loading_lock:
            if name:
                return {name: self._loading_status.get(name, "unknown")}
            else:
                return self._loading_status.copy()

    def _get_config_by_name(self, name: str) -> Optional[dict[str, Any]]:
        """根据名称获取配置"""
        for config in self._preload_configs:
            if config["name"] == name:
                return config
        return None

    def _resolve_dependencies(self) -> list[str]:
        """解析依赖关系，返回加载顺序"""
        # 使用拓扑排序解决依赖关系
        in_degree = {}
        graph = {}

        # 初始化
        for config in self._preload_configs:
            name = config["name"]
            in_degree[name] = 0
            graph[name] = []

        # 构建依赖图
        for config in self._preload_configs:
            name = config["name"]
            for dep in config["dependencies"]:
                if dep in graph:
                    graph[dep].append(name)
                    in_degree[name] += 1
                else:
                    logger.warning(f"依赖的数据源不存在: {dep} (被 {name} 依赖)")

        # 拓扑排序
        result = []
        queue = [name for name, degree in in_degree.items() if degree == 0]

        while queue:
            current = queue.pop(0)
            result.append(current)

            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # 检查是否有循环依赖
        if len(result) != len(self._preload_configs):
            remaining = [name for name in in_degree if name not in result]
            logger.error(f"检测到循环依赖: {remaining}")
            # 将剩余的项添加到结果末尾
            result.extend(remaining)

        return result

    def _process_batch(
        self,
        executor: ThreadPoolExecutor,
        batch: list[dict],
        results: dict,
        completed_sources: set,
        timeout: Optional[float],
    ):
        """处理一批加载任务"""
        futures = {}

        for config in batch:
            future = executor.submit(self._load_single_source, config)
            futures[future] = config["name"]

        # 等待完成
        for future in as_completed(futures, timeout=timeout):
            source_name = futures[future]
            try:
                success, data_or_error = future.result()
                if success:
                    results["success"] += 1
                    results["loaded_data"][source_name] = data_or_error
                    completed_sources.add(source_name)
                else:
                    results["failed"] += 1
                    results["errors"].append(f"{source_name}: {data_or_error}")
            except Exception as e:
                results["failed"] += 1
                results["errors"].append(f"{source_name}: {e}")
                logger.error(f"批处理加载失败 {source_name}: {e}")

    def _load_single_source(self, config: dict[str, Any]) -> tuple[bool, Any]:
        """加载单个数据源"""
        name = config["name"]

        with self._loading_lock:
            self._loading_status[name] = "loading"

        try:
            data = get_cached_data(config["file_path"], config["loader_func"])

            with self._loading_lock:
                self._loading_status[name] = "completed"

            # 执行回调
            self._execute_callbacks(name, True, data)

            return True, data

        except Exception as e:
            with self._loading_lock:
                self._loading_status[name] = "failed"

            # 执行回调
            self._execute_callbacks(name, False, e)

            return False, e

    def _execute_callbacks(self, name: str, success: bool, data_or_error: Any):
        """执行完成回调"""
        callbacks = self._completion_callbacks.get(name, [])
        for callback in callbacks:
            try:
                callback(name, success, data_or_error)
            except Exception as e:
                logger.error(f"回调执行失败 {name}: {e}")


# 全局预加载器实例
default_preloader = DataPreloader()


def register_data_source(
    name: str,
    file_path: str,
    loader_func: Optional[Callable] = None,
    priority: int = 0,
    auto_reload: bool = False,
    dependencies: Optional[list[str]] = None,
) -> None:
    """注册数据源的便捷函数"""
    default_preloader.register_data_source(
        name=name,
        file_path=file_path,
        loader_func=loader_func,
        priority=priority,
        auto_reload=auto_reload,
        dependencies=dependencies,
    )


def preload_data() -> dict[str, Any]:
    """预加载所有数据的便捷函数"""
    return default_preloader.preload_all()


def preload_data_async() -> threading.Thread:
    """异步预加载数据的便捷函数"""
    return default_preloader.preload_async()


# 注册核心数据源
def setup_core_data_sources():
    """设置核心数据源"""
    # 姓名数据
    register_data_source(
        name="chinese_surnames", file_path="chinese/surnames.json", priority=10
    )

    register_data_source(
        name="chinese_givennames", file_path="chinese/givennames.json", priority=10
    )

    # 地区数据
    register_data_source(
        name="chinese_regions", file_path="chinese/regions.json", priority=8
    )


def start_data_preload() -> threading.Thread:
    """启动数据预加载的便捷函数

    Returns:
        预加载线程
    """
    return preload_data_async()


def get_preload_stats() -> dict[str, Any]:
    """获取预加载状态统计

    Returns:
        预加载统计信息，包含:
        - is_preloaded: 是否已预加载完成
        - is_preloading: 是否正在预加载
        - status: 各数据源状态
    """
    status = default_preloader.get_loading_status()

    # 检查是否所有数据源都加载完成
    is_preloaded = (
        all(s in ("success", "skipped") for s in status.values()) if status else False
    )
    is_preloading = any(s == "loading" for s in status.values())

    return {
        "is_preloaded": is_preloaded,
        "is_preloading": is_preloading,
        "status": status,
    }


def wait_for_data_preload(timeout: float = 30.0) -> bool:
    """等待数据预加载完成

    Args:
        timeout: 超时时间（秒）

    Returns:
        是否在超时前完成预加载
    """
    import time

    start_time = time.time()

    while time.time() - start_time < timeout:
        stats = get_preload_stats()
        if stats["is_preloaded"]:
            return True
        if not stats["is_preloading"]:
            # 没有正在加载的，说明已完成或失败
            return stats["is_preloaded"]
        time.sleep(0.1)

    return False


def get_performance_stats() -> dict[str, Any]:
    """获取性能统计信息

    Returns:
        性能统计信息（当前为空实现）
    """
    return {"preload_time": 0.0, "cache_hits": 0, "cache_misses": 0}


# 在模块加载时自动注册核心数据源
setup_core_data_sources()
