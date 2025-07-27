"""
数据缓存管理器
提供高效的数据文件加载和缓存机制
"""
import json
import os
import threading
import time
from typing import Dict, Any, Optional, Callable
from functools import lru_cache
import weakref


class DataCache:
    """数据缓存管理器"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not self._initialized:
            self._cache: Dict[str, Any] = {}
            self._cache_times: Dict[str, float] = {}
            self._access_times: Dict[str, float] = {}
            self._file_mtimes: Dict[str, float] = {}
            self._lock = threading.RLock()
            self._max_cache_size = 100  # 最大缓存条目数
            self._cache_ttl = 3600  # 缓存生存时间（秒）
            self._initialized = True
    
    def get_data(self, file_path: str, loader_func: Optional[Callable] = None) -> Any:
        """
        获取缓存数据，如果不存在则加载
        
        Args:
            file_path: 数据文件路径
            loader_func: 自定义加载函数，默认为JSON加载
            
        Returns:
            加载的数据
        """
        with self._lock:
            # 标准化路径
            abs_path = os.path.abspath(file_path)
            
            # 检查文件是否存在
            if not os.path.exists(abs_path):
                raise FileNotFoundError(f"数据文件不存在: {abs_path}")
            
            # 获取文件修改时间
            current_mtime = os.path.getmtime(abs_path)
            
            # 检查缓存是否有效
            if self._is_cache_valid(abs_path, current_mtime):
                self._access_times[abs_path] = time.time()
                return self._cache[abs_path]
            
            # 加载数据
            if loader_func is None:
                loader_func = self._default_json_loader
            
            try:
                data = loader_func(abs_path)
                
                # 缓存数据
                self._store_in_cache(abs_path, data, current_mtime)
                
                return data
                
            except Exception as e:
                raise RuntimeError(f"加载数据文件失败 {abs_path}: {str(e)}")
    
    def _is_cache_valid(self, file_path: str, current_mtime: float) -> bool:
        """检查缓存是否有效"""
        if file_path not in self._cache:
            return False
        
        # 检查文件是否被修改
        if self._file_mtimes.get(file_path, 0) != current_mtime:
            return False
        
        # 检查缓存是否过期
        cache_time = self._cache_times.get(file_path, 0)
        if time.time() - cache_time > self._cache_ttl:
            return False
        
        return True
    
    def _store_in_cache(self, file_path: str, data: Any, mtime: float):
        """存储数据到缓存"""
        # 清理过期缓存
        self._cleanup_expired_cache()
        
        # 如果缓存已满，清理最少使用的项
        if len(self._cache) >= self._max_cache_size:
            self._cleanup_lru_cache()
        
        # 存储数据
        current_time = time.time()
        self._cache[file_path] = data
        self._cache_times[file_path] = current_time
        self._access_times[file_path] = current_time
        self._file_mtimes[file_path] = mtime
    
    def _cleanup_expired_cache(self):
        """清理过期的缓存项"""
        current_time = time.time()
        expired_keys = []
        
        for file_path, cache_time in self._cache_times.items():
            if current_time - cache_time > self._cache_ttl:
                expired_keys.append(file_path)
        
        for key in expired_keys:
            self._remove_cache_entry(key)
    
    def _cleanup_lru_cache(self):
        """清理最少使用的缓存项"""
        if not self._access_times:
            return
        
        # 找到最少使用的项
        lru_key = min(self._access_times.items(), key=lambda x: x[1])[0]
        self._remove_cache_entry(lru_key)
    
    def _remove_cache_entry(self, key: str):
        """移除缓存条目"""
        self._cache.pop(key, None)
        self._cache_times.pop(key, None)
        self._access_times.pop(key, None)
        self._file_mtimes.pop(key, None)
    
    def _default_json_loader(self, file_path: str) -> Any:
        """默认JSON加载器"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def invalidate(self, file_path: str = None):
        """
        使缓存失效
        
        Args:
            file_path: 特定文件路径，如果为None则清空所有缓存
        """
        with self._lock:
            if file_path is None:
                self._cache.clear()
                self._cache_times.clear()
                self._access_times.clear()
                self._file_mtimes.clear()
            else:
                abs_path = os.path.abspath(file_path)
                self._remove_cache_entry(abs_path)
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """获取缓存统计信息"""
        with self._lock:
            return {
                'cache_size': len(self._cache),
                'max_cache_size': self._max_cache_size,
                'cache_ttl': self._cache_ttl,
                'cached_files': list(self._cache.keys())
            }


# 全局缓存实例
_data_cache = DataCache()


def get_cached_data(file_path: str, loader_func: Optional[Callable] = None) -> Any:
    """
    获取缓存数据的便捷函数
    
    Args:
        file_path: 数据文件路径
        loader_func: 自定义加载函数
        
    Returns:
        加载的数据
    """
    return _data_cache.get_data(file_path, loader_func)


def invalidate_cache(file_path: str = None):
    """
    使缓存失效的便捷函数
    
    Args:
        file_path: 特定文件路径，如果为None则清空所有缓存
    """
    _data_cache.invalidate(file_path)


def get_cache_stats() -> Dict[str, Any]:
    """获取缓存统计信息的便捷函数"""
    return _data_cache.get_cache_stats()


@lru_cache(maxsize=32)
def get_data_file_path(relative_path: str) -> str:
    """
    获取数据文件的绝对路径（带缓存）
    
    Args:
        relative_path: 相对于dataforge包的路径
        
    Returns:
        绝对路径
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base_dir, 'data', relative_path)


class LazyDataLoader:
    """惰性数据加载器"""
    
    def __init__(self, file_path: str, loader_func: Optional[Callable] = None):
        self.file_path = file_path
        self.loader_func = loader_func
        self._data = None
        self._loaded = False
        self._lock = threading.Lock()
    
    @property
    def data(self) -> Any:
        """获取数据（惰性加载）"""
        if not self._loaded:
            with self._lock:
                if not self._loaded:
                    self._data = get_cached_data(self.file_path, self.loader_func)
                    self._loaded = True
        return self._data
    
    def reload(self):
        """重新加载数据"""
        with self._lock:
            invalidate_cache(self.file_path)
            self._loaded = False
            self._data = None


class DataPreloader:
    """数据预加载器"""
    
    def __init__(self):
        self._preload_tasks = []
    
    def add_preload_task(self, file_path: str, loader_func: Optional[Callable] = None):
        """添加预加载任务"""
        self._preload_tasks.append((file_path, loader_func))
    
    def preload_all(self):
        """执行所有预加载任务"""
        for file_path, loader_func in self._preload_tasks:
            try:
                get_cached_data(file_path, loader_func)
            except Exception as e:
                print(f"预加载失败 {file_path}: {e}")
    
    def preload_async(self):
        """异步执行预加载"""
        import threading
        
        def preload_worker():
            self.preload_all()
        
        thread = threading.Thread(target=preload_worker, daemon=True)
        thread.start()
        return thread


# 全局预加载器实例
_preloader = DataPreloader()


def add_preload_task(file_path: str, loader_func: Optional[Callable] = None):
    """添加预加载任务的便捷函数"""
    _preloader.add_preload_task(file_path, loader_func)


def preload_data():
    """执行数据预加载的便捷函数"""
    _preloader.preload_all()


def preload_data_async():
    """异步执行数据预加载的便捷函数"""
    return _preloader.preload_async()