"""
交易日历数据更新器

通过API接口自动更新节假日数据到配置文件

支持的数据源：
- timor.tech 免费节假日API（推荐）
- 国务院公告数据（需爬虫）
- 自定义API数据源
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

try:
    import yaml

    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class TradingCalendarUpdater:
    """交易日历数据更新器

    功能：
    - 从API获取最新节假日数据
    - 自动更新配置文件
    - 数据验证和错误处理
    - 更新日志记录

    使用示例：
        >>> updater = TradingCalendarUpdater()
        >>> updater.update(year=2026)
        >>> updater.update_multiple_years([2024, 2025, 2026])
    """

    # API数据源配置
    API_SOURCES = {
        "timor": {
            "name": "Timor 节假日API",
            "url": "http://timor.tech/api/holiday/year/{year}",
            "free": True,
            "reliable": True,
        },
        "gov": {
            "name": "国务院公告",
            "url": "http://www.gov.cn/zhengce/content/index.htm",
            "free": True,
            "reliable": True,
        },
    }

    def __init__(self, config_file: Path | None = None):
        """初始化更新器

        Args:
            config_file: 配置文件路径，默认为项目配置目录
        """
        if not REQUESTS_AVAILABLE:
            raise ImportError("需要安装 requests 库: pip install requests")

        if config_file is None:
            # 默认配置文件路径
            current_file = Path(__file__)
            project_root = current_file.parent.parent.parent
            config_file = project_root / "config" / "trading_calendar.yaml"

        self.config_file = config_file
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

    def _fetch_from_timor(self, year: int) -> dict[str, Any]:
        """从 Timor API 获取节假日数据

        Args:
            year: 年份

        Returns:
            节假日数据字典
        """
        url = self.API_SOURCES["timor"]["url"].format(year=year)

        try:
            # 添加User-Agent避免被ban
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get("code") != 0:
                raise ValueError(f"API返回错误: {data.get('message')}")

            return data.get("holiday", {})  # type: ignore

        except Exception as e:
            print(f"错误: 从Timor API获取数据失败: {e}")
            return {}

    def _parse_timor_data(
        self, raw_data: dict[str, Any], year: int
    ) -> tuple[list[dict], list[str]]:
        """解析Timor API返回的数据

        Args:
            raw_data: API原始数据
            year: 年份

        Returns:
            (节假日列表, 调休工作日列表)
        """
        holidays = []
        adjusted_working_days = []

        for date_str, info in raw_data.items():
            # 补全年份（API返回的是MM-DD格式）
            if len(date_str) == 5:  # MM-DD
                full_date = f"{year}-{date_str}"
            else:
                full_date = date_str

            # 节假日
            if info.get("holiday", False):
                holidays.append(
                    {"date": full_date, "name": info.get("name", ""), "type": "LEGAL"}
                )

            # 调休工作日（周末补班）
            if info.get("wage", 1) == 3:  # wage=3 表示需要补班
                adjusted_working_days.append(full_date)

        return holidays, adjusted_working_days

    def update_year(
        self, year: int, source: str = "timor", dry_run: bool = False
    ) -> bool:
        """更新指定年份的节假日数据

        Args:
            year: 年份
            source: 数据源 ('timor', 'gov')
            dry_run: 是否为演练模式（不实际写入文件）

        Returns:
            是否更新成功
        """
        print(f"\n📅 正在更新 {year} 年节假日数据...")
        print(f"   数据源: {self.API_SOURCES.get(source, {}).get('name', source)}")

        # 获取数据
        if source == "timor":
            raw_data = self._fetch_from_timor(year)
            if not raw_data:
                print("❌ 获取数据失败")
                return False

            holidays, working_days = self._parse_timor_data(raw_data, year)
        else:
            print(f"❌ 暂不支持数据源: {source}")
            return False

        print(
            f"   ✅ 获取到 {len(holidays)} 个节假日, {len(working_days)} 个调休工作日"
        )

        # 读取现有配置
        config = self._load_config()

        # 更新数据
        if "holidays" not in config:
            config["holidays"] = {}
        config["holidays"][year] = holidays

        if "adjusted_working_days" not in config:
            config["adjusted_working_days"] = {}
        config["adjusted_working_days"][year] = working_days

        # 更新元数据
        config["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 更新日志
        if "update_log" not in config:
            config["update_log"] = []

        config["update_log"].insert(
            0,
            {
                "version": config.get("version", "1.0"),
                "date": datetime.now().strftime("%Y-%m-%d"),
                "changes": [
                    f"更新{year}年节假日数据（{len(holidays)}个节假日）",
                    f"更新{year}年调休工作日（{len(working_days)}个）",
                    f"数据源: {self.API_SOURCES.get(source, {}).get('name', source)}",
                ],
            },
        )

        # 保持最多10条更新日志
        config["update_log"] = config["update_log"][:10]

        if dry_run:
            print("   🔍 演练模式：不写入文件")
            print("   📝 将要写入的数据预览:")
            print(f"      - 节假日: {holidays[:3]}...")
            print(f"      - 调休工作日: {working_days[:3]}...")
            return True

        # 写入配置文件
        try:
            self._save_config(config)
            print(f"   ✅ 配置文件已更新: {self.config_file}")
            return True

        except Exception as e:
            print(f"   ❌ 写入配置文件失败: {e}")
            return False

    def update_multiple_years(
        self, years: list[int], source: str = "timor", dry_run: bool = False
    ) -> dict[int, bool]:
        """批量更新多个年份的数据

        Args:
            years: 年份列表
            source: 数据源
            dry_run: 是否为演练模式

        Returns:
            更新结果字典 {年份: 是否成功}
        """
        print(f"\n🚀 批量更新节假日数据: {years}")

        results = {}
        for year in years:
            results[year] = self.update_year(year, source, dry_run)

        # 统计结果
        success_count = sum(1 for v in results.values() if v)
        print(f"\n📊 更新完成: 成功 {success_count}/{len(years)}")

        return results

    def _load_config(self) -> dict[str, Any]:
        """加载现有配置文件

        Returns:
            配置字典
        """
        if not self.config_file.exists():
            return {
                "version": "2025.1",
                "description": "中国A股交易日历配置文件",
                "holidays": {},
                "adjusted_working_days": {},
                "metadata": {"source": "Timor API", "update_frequency": "yearly"},
            }

        try:
            with open(self.config_file, encoding="utf-8") as f:
                if YAML_AVAILABLE:
                    import yaml  # type: ignore

                    return yaml.safe_load(f) or {}  # type: ignore
                else:
                    return json.load(f)
        except Exception as e:
            print(f"警告: 加载配置文件失败: {e}")
            return {}

    def _save_config(self, config: dict[str, Any]) -> None:
        """保存配置到文件

        Args:
            config: 配置字典
        """
        with open(self.config_file, "w", encoding="utf-8") as f:
            if YAML_AVAILABLE:
                import yaml  # type: ignore

                yaml.dump(
                    config,
                    f,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                )
            else:
                json.dump(config, f, ensure_ascii=False, indent=2)

    def preview_update(self, year: int, source: str = "timor") -> None:
        """预览更新（不实际写入文件）

        Args:
            year: 年份
            source: 数据源
        """
        self.update_year(year, source, dry_run=True)


def main():
    """命令行入口"""
    import argparse

    parser = argparse.ArgumentParser(description="更新交易日历数据")
    parser.add_argument(
        "years", nargs="+", type=int, help="要更新的年份（可以指定多个）"
    )
    parser.add_argument(
        "--source",
        default="timor",
        choices=["timor", "gov"],
        help="数据源（默认: timor）",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="演练模式（不实际写入文件）"
    )
    parser.add_argument("--config", type=Path, help="配置文件路径（可选）")

    args = parser.parse_args()

    # 创建更新器
    updater = TradingCalendarUpdater(config_file=args.config)

    # 执行更新
    if len(args.years) == 1:
        updater.update_year(args.years[0], args.source, args.dry_run)
    else:
        updater.update_multiple_years(args.years, args.source, args.dry_run)


if __name__ == "__main__":
    main()
