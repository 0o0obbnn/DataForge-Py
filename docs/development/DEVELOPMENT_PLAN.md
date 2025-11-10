# DataForge 未实现功能开发计划

## 📋 项目概述

基于DataForge.md需求文档与已实现生成器的对比分析，制定系统性开发计划，确保所有数据类型完整实现。

## 🎯 开发优先级矩阵

### 🔴 P0 - 核心功能缺失（立即开发）
| 数据类型 | 状态 | 开发复杂度 | 业务价值 | 预计工时 |
|---------|------|------------|----------|----------|
| **时间戳/日期时间** | 未实现 | 低 | 极高 | 4小时 |
| **IPv4/IPv6地址** | 未实现 | 中 | 极高 | 6小时 |
| **完整URL生成器** | 未实现 | 中 | 极高 | 6小时 |
| **域名生成器** | 未实现 | 低 | 高 | 3小时 |

### 🟡 P1 - 重要功能补充（1周内完成）
| 数据类型 | 状态 | 开发复杂度 | 业务价值 | 预计工时 |
|---------|------|------------|----------|----------|
| **JSON/XML/YAML生成器** | 未实现 | 高 | 极高 | 12小时 |
| **职业/职位信息** | 未实现 | 低 | 高 | 3小时 |
| **学历/教育水平** | 未实现 | 低 | 高 | 2小时 |
| **业务单据号** | 未实现 | 中 | 高 | 4小时 |
| **产品编码** | 未实现 | 中 | 高 | 4小时 |

### 🟢 P2 - 扩展功能增强（2周内完成）
| 数据类型 | 状态 | 开发复杂度 | 业务价值 | 预计工时 |
|---------|------|------------|----------|----------|
| **星座/民族/血型** | 未实现 | 低 | 中 | 6小时 |
| **婚姻状况** | 未实现 | 低 | 中 | 1小时 |
| **护照/签证/驾驶证号** | 未实现 | 中 | 中 | 8小时 |
| **优惠券/促销码** | 未实现 | 低 | 中 | 4小时 |
| **物流单号** | 未实现 | 中 | 中 | 4小时 |

### 🔵 P3 - 专项测试工具（专项需求）
| 数据类型 | 状态 | 开发复杂度 | 业务价值 | 预计工时 |
|---------|------|------------|----------|----------|
| **安全注入payload** | 未实现 | 高 | 中 | 10小时 |
| **媒体文件模拟** | 未实现 | 中 | 低 | 8小时 |
| **用户行为数据** | 未实现 | 高 | 中 | 12小时 |
| **交易日历** | 未实现 | 高 | 低 | 8小时 |

## 🛠️ 技术实现规范

### 代码标准
- **严格遵循ruff规范**
- **类型注解完整**（使用Python 3.9+语法）
- **完整的docstring**
- **单元测试覆盖率≥90%**
- **性能基准测试**

### 目录结构规范
```
dataforge/generators/
├── [category]/           # 功能分类目录
│   ├── __init__.py
│   ├── [generator].py    # 具体生成器实现
│   └── test_[generator].py # 单元测试
└── shared/              # 共享工具和基类
```

## 📅 分阶段开发路线图

### Phase 1: 核心功能补齐（Week 1-2）
**目标**: 解决P0级缺失功能

#### Week 1: 时间+网络基础
- **Day 1-2**: 时间戳/日期时间生成器
  - `datetime/timestamp.py`
  - `datetime/date_range.py`
  - 支持格式化和时区处理

- **Day 3-4**: IPv4/IPv6地址生成器
  - `network/ip_address.py`
  - 支持公网/私网/CIDR范围
  - 包含中国IP段数据库

- **Day 5-6**: 域名生成器
  - `network/domain.py`
  - 支持自定义TLD和二级域名规则
  - 集成常见域名黑名单

#### Week 2: URL+结构化数据
- **Day 1-2**: 完整URL生成器
  - `network/url_generator.py`
  - 支持HTTP/HTTPS/FTP协议
  - 参数化路径和查询字符串

- **Day 3-5**: JSON生成器
  - `structured/json_generator.py`
  - 支持JSON Schema
  - 递归嵌套结构

- **Day 6**: XML/YAML基础实现
  - `structured/xml_generator.py`
  - `structured/yaml_generator.py`

### Phase 2: 业务数据扩展（Week 3-4）
**目标**: 完善个人信息和业务数据

#### Week 3: 个人信息增强
- **Day 1**: 职业/职位生成器
  - `basic/occupation.py`
  - 基于中国职业分类大典

- **Day 2**: 学历生成器
  - `basic/education.py`
  - 支持国内外学历体系

- **Day 3**: 星座/民族/血型
  - `basic/extended_profile.py`
  - 支持地域分布权重

- **Day 4-5**: 婚姻状况
  - `basic/marital_status.py`
  - 年龄关联规则

#### Week 4: 业务标识符
- **Day 1-2**: 业务单据号
  - `identifier/document_number.py`
  - 支持多种业务场景
  - 可配置前缀和校验位

- **Day 3-4**: 产品编码
  - `identifier/product_code.py`
  - SKU/ISBN/UPC支持
  - 行业分类码

- **Day 5**: 优惠券/促销码
  - `identifier/coupon_code.py`
  - 防冲突算法

### Phase 3: 证件和物流（Week 5-6）
**目标**: 证件和物流相关数据

#### Week 5: 证件号码
- **Day 1-2**: 护照号生成器
  - `identifier/passport.py`
  - 多国家格式支持

- **Day 3**: 签证号生成器
  - `identifier/visa.py`
  - 申根/美签/日签格式

- **Day 4-5**: 驾驶证号
  - `identifier/driver_license.py`
  - 各省市格式差异

#### Week 6: 物流系统
- **Day 1-2**: 物流单号
  - `identifier/tracking_number.py`
  - 主流快递公司规则

- **Day 3-4**: 运单号
  - `identifier/waybill.py`
  - 国际运单格式

### Phase 4: 专项测试工具（Week 7-8）
**目标**: 安全测试和高级功能

#### Week 7: 安全测试
- **Day 1-3**: SQL注入payload生成器
  - `security/sql_injection.py`
  - 多数据库类型支持
  - 绕过技术模拟

- **Day 4-5**: XSS攻击脚本
  - `security/xss_payload.py`
  - DOM/反射/存储型

#### Week 8: 媒体和行为
- **Day 1-2**: 媒体文件模拟
  - `media/file_simulator.py`
  - 图片/视频/文档头

- **Day 3-5**: 用户行为数据
  - `behavior/user_actions.py`
  - 点击流/搜索/购物车

## 🔧 技术实现细节

### 时间生成器设计
```python
# dataforge/generators/datetime/timestamp.py
from datetime import datetime, timezone
from typing import Optional

class TimestampGenerator(BaseGenerator):
    """高精度时间戳生成器"""
    
    def generate(self, 
                start_date: Optional[str] = None,
                end_date: Optional[str] = None,
                timezone_str: str = "UTC",
                format_type: str = "iso") -> str:
        """生成时间戳"""
        pass
```

### IP地址生成器设计
```python
# dataforge/generators/network/ip_address.py
import ipaddress
from typing import Literal

class IPAddressGenerator(BaseGenerator):
    """IPv4/IPv6地址生成器"""
    
    def generate(self,
                version: Literal[4, 6] = 4,
                ip_type: Literal["public", "private", "any"] = "any",
                cidr: Optional[str] = None) -> str:
        """生成IP地址"""
        pass
```

### JSON生成器设计
```python
# dataforge/generators/structured/json_generator.py
import json
from typing import Dict, Any, Optional

class JSONGenerator(BaseGenerator):
    """JSON数据结构生成器"""
    
    def generate(self,
                schema: Optional[Dict[str, Any]] = None,
                depth: int = 3,
                array_size: tuple = (1, 5)) -> Dict[str, Any]:
        """生成JSON对象"""
        pass
```

## 📊 测试策略

### 单元测试模板
```python
# tests/generators/test_timestamp.py
import pytest
from datetime import datetime
from dataforge.generators.datetime.timestamp import TimestampGenerator

class TestTimestampGenerator:
    def test_basic_generation(self):
        gen = TimestampGenerator()
        result = gen.generate()
        assert isinstance(result, str)
        
    def test_timezone_handling(self):
        gen = TimestampGenerator()
        result = gen.generate(timezone_str="Asia/Shanghai")
        # 验证时区处理
```

### 性能测试基准
- **生成速度**: ≥1000条/秒
- **内存使用**: ≤100MB/万条数据
- **并发安全**: 支持多线程并发调用

## 🎯 验收标准

### 功能验收
- [ ] 所有P0功能完整实现
- [ ] CLI参数支持完整
- [ ] 上下文关联正确
- [ ] 错误处理完善

### 质量验收
- [ ] 单元测试覆盖率≥90%
- [ ] ruff检查0错误
- [ ] 性能基准达标
- [ ] 文档完整

### 集成验收
- [ ] 与现有系统无缝集成
- [ ] 向后兼容性保持
- [ ] API接口一致性

## 📈 风险管控

### 技术风险
- **JSON Schema复杂性**: 采用渐进式实现
- **性能瓶颈**: 提前基准测试和优化
- **时区处理**: 使用标准库pytz

### 进度风险
- **需求变更**: 每周同步评审
- **技术难点**: 预留20%缓冲时间
- **依赖项**: 提前识别第三方库依赖

## 📞 沟通机制

### 周报制度
- **每周五**: 进度同步会议
- **关键节点**: 里程碑评审
- **问题升级**: 24小时内响应机制

### 文档更新
- **实时更新**: 开发计划动态调整
- **版本控制**: Git管理变更历史
- **知识沉淀**: 技术决策记录

---

**制定日期**: 2024年12月19日  
**版本**: v1.0  
**状态**: 待评审  
**下次评审**: 2024年12月26日