"""
数据预加载模块
在应用启动时预加载常用数据以提高性能
"""
import threading
import time
from typing import List, Dict, Any
from .cache import add_preload_task, preload_data_async, get_data_file_path, get_cache_stats


class DataPreloadManager:
    """数据预加载管理器"""
    
    def __init__(self):
        self._preloaded = False
        self._preload_lock = threading.Lock()
        self._preload_thread = None
    
    def register_common_data_files(self):
        """注册常用的数据文件进行预加载"""
        # 中文数据文件
        add_preload_task(get_data_file_path('chinese/surnames.json'))
        add_preload_task(get_data_file_path('chinese/givennames.json'))
        add_preload_task(get_data_file_path('chinese/regions.json'))
    
    def start_preload(self) -> bool:
        """启动数据预加载"""
        with self._preload_lock:
            if self._preloaded or self._preload_thread is not None:
                return False
            
            # 注册常用数据文件
            self.register_common_data_files()
            
            # 启动异步预加载
            self._preload_thread = preload_data_async()
            return True
    
    def wait_for_preload(self, timeout: float = 10.0) -> bool:
        """等待预加载完成"""
        if self._preload_thread is None:
            return True
        
        try:
            self._preload_thread.join(timeout)
            if self._preload_thread.is_alive():
                return False  # 超时
            
            with self._preload_lock:
                self._preloaded = True
            return True
            
        except Exception:
            return False
    
    def is_preloaded(self) -> bool:
        """检查是否已预加载"""
        return self._preloaded
    
    def get_preload_stats(self) -> Dict[str, Any]:
        """获取预加载统计信息"""
        cache_stats = get_cache_stats()
        return {
            'is_preloaded': self._preloaded,
            'is_preloading': self._preload_thread is not None and self._preload_thread.is_alive(),
            'cache_stats': cache_stats
        }


# 全局预加载管理器实例
_preload_manager = DataPreloadManager()


def start_data_preload() -> bool:
    """启动数据预加载的便捷函数"""
    return _preload_manager.start_preload()


def wait_for_data_preload(timeout: float = 10.0) -> bool:
    """等待数据预加载完成的便捷函数"""
    return _preload_manager.wait_for_preload(timeout)


def is_data_preloaded() -> bool:
    """检查数据是否已预加载的便捷函数"""
    return _preload_manager.is_preloaded()


def get_preload_stats() -> Dict[str, Any]:
    """获取预加载统计信息的便捷函数"""
    return _preload_manager.get_preload_stats()


def enable_auto_preload():
    """启用自动预加载（在模块导入时执行）"""
    start_data_preload()


class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self._generation_times: List[float] = []
        self._cache_hits = 0
        self._cache_misses = 0
        self._lock = threading.Lock()
    
    def record_generation_time(self, generation_time: float):
        """记录数据生成时间"""
        with self._lock:
            self._generation_times.append(generation_time)
            # 只保留最近1000次记录
            if len(self._generation_times) > 1000:
                self._generation_times = self._generation_times[-1000:]
    
    def record_cache_hit(self):
        """记录缓存命中"""
        with self._lock:
            self._cache_hits += 1
    
    def record_cache_miss(self):
        """记录缓存未命中"""
        with self._lock:
            self._cache_misses += 1
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """获取性能统计信息"""
        with self._lock:
            if not self._generation_times:
                avg_time = 0
                min_time = 0
                max_time = 0
            else:
                avg_time = sum(self._generation_times) / len(self._generation_times)
                min_time = min(self._generation_times)
                max_time = max(self._generation_times)
            
            total_requests = self._cache_hits + self._cache_misses
            hit_rate = (self._cache_hits / total_requests * 100) if total_requests > 0 else 0
            
            return {
                'generation_count': len(self._generation_times),
                'avg_generation_time_ms': round(avg_time * 1000, 2),
                'min_generation_time_ms': round(min_time * 1000, 2),
                'max_generation_time_ms': round(max_time * 1000, 2),
                'cache_hits': self._cache_hits,
                'cache_misses': self._cache_misses,
                'cache_hit_rate_percent': round(hit_rate, 2)
            }
    
    def reset_stats(self):
        """重置统计信息"""
        with self._lock:
            self._generation_times.clear()
            self._cache_hits = 0
            self._cache_misses = 0


# 全局性能监控器实例
_performance_monitor = PerformanceMonitor()


def record_generation_time(generation_time: float):
    """记录数据生成时间的便捷函数"""
    _performance_monitor.record_generation_time(generation_time)


def record_cache_hit():
    """记录缓存命中的便捷函数"""
    _performance_monitor.record_cache_hit()


def record_cache_miss():
    """记录缓存未命中的便捷函数"""
    _performance_monitor.record_cache_miss()


def get_performance_stats() -> Dict[str, Any]:
    """获取性能统计信息的便捷函数"""
    return _performance_monitor.get_performance_stats()


def reset_performance_stats():
    """重置性能统计信息的便捷函数"""
    _performance_monitor.reset_stats()