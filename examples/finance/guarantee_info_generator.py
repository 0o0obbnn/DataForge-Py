"""
担保信息文件生成器 (421GUARINFO.txt)

根据《互联网金融信息共享平台数据采集标准》生成担保信息文件。
文件包含三个信息段：
1. 人员标识信息段
2. 业务标识信息段
3. 担保信息段
"""

import os
import secrets
import sys
from datetime import date, datetime, timedelta
from typing import Optional

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from dataforge import GeneratorConfig, default_factory


def generate_id_number_by_type(id_type: str) -> str:
    """
    根据证件类型代码生成对应的证件号码

    Args:
        id_type: 证件类型代码

    Returns:
        生成的证件号码
    """
    # 证件类型代码到生成器的映射
    id_type_to_generator = {
        "0": ("idcard", {}),  # 身份证
        "1": ("household_register", {}),  # 户口簿
        "2": ("passport", {}),  # 护照
        "3": ("officer_card", {}),  # 军官证
        "4": ("soldier_card", {}),  # 士兵证
        "5": ("hk_mo_tw_id", {"type": "hk_mc"}),  # 港澳居民来往内地通行证
        "6": ("hk_mo_tw_id", {"type": "tw_mc"}),  # 台湾同胞来往内地通行证
        "7": ("temporary_idcard", {}),  # 临时身份证
        "8": ("foreigner_residence", {}),  # 外国人居留证
        "9": ("police_officer_card", {}),  # 警官证
        "A": ("hong_kong_id", {}),  # 香港身份证
        "B": ("macau_id", {}),  # 澳门身份证
        "C": ("taiwan_id", {}),  # 台湾身份证
        "D": ("wujing_card", {}),  # 武警官兵证
        "Y": ("foreign_permanent_residence", {}),  # 外国人永久居留身份证
        "Z": ("foreign_passport", {}),  # 外国护照
    }

    # 如果是已知类型，使用对应的生成器
    if id_type in id_type_to_generator:
        generator_name, parameters = id_type_to_generator[id_type]
        config = GeneratorConfig(
            generator_type=generator_name,
            parameters=parameters
        )
        generator = default_factory.create_generator(config)
        id_number = generator.generate_single()

        # 如果是身份证，确保最后一位是大写X
        if id_type == "0" and id_number and id_number[-1] == "x":
            id_number = id_number[:-1] + "X"

        return id_number
    else:
        # 其他证件类型（X-其他证件），生成18位随机字符
        return "".join(secrets.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(18))


def generate_common_fields() -> dict:
    """
    生成所有类型共用的字段（业务标识信息段和担保信息段）
    
    Returns:
        包含共用字段的字典
    """
    record = {}

    # ========== 业务标识信息段 ==========
    # 4108: 业务发生机构（社会信用代码或组织机构代码，18位）
    # 固定值：097967874（组织机构代码）
    record["4108"] = "097967874"

    # 4109: 担保合同编号（64位，公司内部唯一标识）
    # 生成格式：GT + 日期(YYYYMMDD) + 随机字符
    contract_date = datetime.now().strftime("%Y%m%d")
    random_suffix = "".join(secrets.choice("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(20))
    record["4109"] = f"GT{contract_date}{random_suffix}"[:64]

    # ========== 担保信息段 ==========
    # 4110: 担保业务种类
    # 11-保证；12-抵押；13-质押；14-留置；15-定金；99-其他
    record["4110"] = secrets.choice(["11", "12", "13", "14", "15", "99"])

    # 4111: 担保类型
    # 1-融资担保；2-非融资担保
    record["4111"] = secrets.choice(["1", "2"])

    # 4112: 担保起始日期 (YYYYMMDD格式)
    # 生成过去1年到未来1年之间的日期
    start_date = date.today() - timedelta(days=secrets.randbelow(365))
    record["4112"] = start_date.strftime("%Y%m%d")

    # 4113: 担保到期日期 (YYYYMMDD格式)
    # 担保到期日期应该在起始日期之后，最多5年
    days_duration = secrets.randbelow(1825) + 30  # 30天到5年
    end_date = start_date + timedelta(days=days_duration)
    record["4113"] = end_date.strftime("%Y%m%d")

    # 4114: 担保金额（正整数，单位：元，10位数字）
    # 生成10万到9999999999元之间的金额
    amount = secrets.randbelow(9999900000) + 100000
    record["4114"] = str(amount)

    return record


def generate_enterprise_record() -> dict:
    """
    生成企业或其他组织类型的担保信息记录
    
    Returns:
        企业类型的担保信息记录字典
    """
    record = {}

    # ========== 人员标识信息段 ==========
    # 4101: 被担保人类型
    record["4101"] = "1"  # 企业或其他组织

    # 4102: 被担保人名称（企业名称）
    company_config = GeneratorConfig(
        generator_type="company_name",
        parameters={"type": "ANY", "prefix_region": True}
    )
    record["4102"] = default_factory.create_generator(company_config).generate_single()

    # 4103: 被担保人证件类型
    # 企业证件类型：a-组织机构代码；b-社会信用代码
    record["4103"] = secrets.choice(["a", "b"])

    # 4104: 被担保人证件号码
    if record["4103"] == "a":  # 组织机构代码
        org_code_config = GeneratorConfig(
            generator_type="chinese_organization_code",
            parameters={"valid": True}
        )
        org_code = default_factory.create_generator(org_code_config).generate_single()
        # 移除连字符，只保留9位代码
        record["4104"] = org_code.replace("-", "")[:9]
    else:  # 社会信用代码
        uscc_config = GeneratorConfig(
            generator_type="uscc",
            parameters={"valid": True}
        )
        record["4104"] = default_factory.create_generator(uscc_config).generate_single()[:18]

    # 4105-4107: 企业法人信息（企业类型必填）
    # 4105: 企业法人姓名
    name_config = GeneratorConfig(
        generator_type="name",
        parameters={}
    )
    record["4105"] = default_factory.create_generator(name_config).generate_single()

    # 4106: 企业法人证件类型
    # 自然人证件类型：0-身份证；1-户口簿；2-护照；3-军官证；4-士兵证；D-武警官兵证；
    # 5-港澳居民来往内地通行证；6-台湾同胞来往内地通行证；7-临时身份证；
    # 8-外国人居留证；9-警官证；A-香港身份证；B-澳门身份证；C-台湾身份证；
    # Y-外国人永久居留身份证；Z-外国护照；X-其他证件
    # 企业法人通常使用身份证，但也可以使用其他证件类型
    # 优先使用身份证（0），偶尔使用其他类型
    if secrets.randbelow(10) < 8:  # 80%概率使用身份证
        record["4106"] = "0"
    else:
        record["4106"] = secrets.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "Y", "Z", "X"])

    # 4107: 企业法人证件号码
    record["4107"] = generate_id_number_by_type(record["4106"])

    # 合并共用字段
    record.update(generate_common_fields())

    return record


def generate_individual_record() -> dict:
    """
    生成自然人类型的担保信息记录
    
    Returns:
        自然人类型的担保信息记录字典
    """
    record = {}

    # ========== 人员标识信息段 ==========
    # 4101: 被担保人类型
    record["4101"] = "2"  # 自然人

    # 4102: 被担保人名称（自然人姓名）
    name_config = GeneratorConfig(
        generator_type="name",
        parameters={}
    )
    record["4102"] = default_factory.create_generator(name_config).generate_single()

    # 4103: 被担保人证件类型
    # 自然人证件类型：0-身份证；1-户口簿；2-护照；3-军官证；4-士兵证；D-武警官兵证；
    # 5-港澳居民来往内地通行证；6-台湾同胞来往内地通行证；7-临时身份证；
    # 8-外国人居留证；9-警官证；A-香港身份证；B-澳门身份证；C-台湾身份证；
    # Y-外国人永久居留身份证；Z-外国护照；X-其他证件
    # 优先使用身份证（0），偶尔使用其他类型
    if secrets.randbelow(10) < 7:  # 70%概率使用身份证
        record["4103"] = "0"
    else:
        record["4103"] = secrets.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "Y", "Z", "X"])

    # 4104: 被担保人证件号码
    record["4104"] = generate_id_number_by_type(record["4103"])

    # 4105-4107: 企业法人信息（自然人类型为空）
    record["4105"] = ""  # 企业法人姓名
    record["4106"] = ""  # 企业法人证件类型
    record["4107"] = ""  # 企业法人证件号码

    # 合并共用字段
    record.update(generate_common_fields())

    return record


def generate_guarantee_info_record(
    guarantor_type: Optional[int] = None,
    count: int = 1,
) -> list[dict]:
    """
    生成担保信息记录
    
    根据被担保人类型的不同，调用相应的生成函数：
    - 类型1（企业或其他组织）：使用 generate_enterprise_record()
    - 类型2（自然人）：使用 generate_individual_record()
    
    Args:
        guarantor_type: 被担保人类型 (1-企业或其他组织；2-自然人)，None表示随机
        count: 生成记录数量
    
    Returns:
        担保信息记录列表
    """
    records = []

    for _ in range(count):
        # 随机选择被担保人类型（如果未指定）
        if guarantor_type is None:
            current_type = secrets.choice([1, 2])
        else:
            current_type = guarantor_type

        # 根据被担保人类型调用相应的生成函数
        if current_type == 1:
            # 企业或其他组织
            record = generate_enterprise_record()
        else:
            # 自然人
            record = generate_individual_record()

        records.append(record)

    return records


def format_guarantee_record(record: dict) -> str:
    """
    格式化担保信息记录为CSV格式
    
    根据规范：
    - 数据项间逗号分隔
    - 数据项为空的，不用空格填充，但要保留逗号位置
    - 记录之间用回车换行符（"\r\n"）分隔
    
    Args:
        record: 担保信息记录字典
    
    Returns:
        格式化后的记录字符串
    """
    # 按照标识符顺序排列字段
    field_order = [
        "4101", "4102", "4103", "4104", "4105", "4106", "4107",  # 人员标识信息段
        "4108", "4109",  # 业务标识信息段
        "4110", "4111", "4112", "4113", "4114",  # 担保信息段
    ]

    fields = []
    for field_id in field_order:
        value = record.get(field_id, "")
        # 如果值为空，保留空字符串（不填充空格）
        fields.append(str(value) if value else "")

    return ",".join(fields)


def generate_guarantee_info_file(
    output_file: str = "421GUARINFO.txt",
    count: int = 10,
    guarantor_type: Optional[int] = None,
) -> None:
    """
    生成担保信息文件
    
    Args:
        output_file: 输出文件名
        count: 生成记录数量
        guarantor_type: 被担保人类型 (1-企业或其他组织；2-自然人)，None表示随机
    """
    print(f"正在生成担保信息文件: {output_file}")
    print(f"记录数量: {count}")

    # 生成记录
    records = generate_guarantee_info_record(guarantor_type=guarantor_type, count=count)

    # 写入文件（使用UTF-8编码，记录之间用\r\n分隔）
    with open(output_file, "w", encoding="UTF-8", newline="") as f:
        for i, record in enumerate(records, 1):
            formatted_record = format_guarantee_record(record)
            f.write(formatted_record)
            if i < len(records):
                f.write("\r\n")

    print(f"✓ 文件生成成功: {output_file}")
    print(f"✓ 共生成 {len(records)} 条记录")

    # 打印前3条记录作为示例
    print("\n前3条记录示例:")
    for i, record in enumerate(records[:3], 1):
        print(f"\n记录 {i}:")
        print(f"  被担保人类型: {record['4101']} ({'企业' if record['4101'] == '1' else '自然人'})")
        print(f"  被担保人名称: {record['4102']}")
        print(f"  被担保人证件类型: {record['4103']}")
        print(f"  被担保人证件号码: {record['4104']}")
        if record['4101'] == '1':
            print(f"  企业法人姓名: {record['4105']}")
            print(f"  企业法人证件类型: {record['4106']}")
            print(f"  企业法人证件号码: {record['4107']}")
        print(f"  业务发生机构: {record['4108']}")
        print(f"  担保合同编号: {record['4109']}")
        print(f"  担保业务种类: {record['4110']}")
        print(f"  担保类型: {record['4111']} ({'融资担保' if record['4111'] == '1' else '非融资担保'})")
        print(f"  担保起始日期: {record['4112']}")
        print(f"  担保到期日期: {record['4113']}")
        print(f"  担保金额: {record['4114']} 元")


if __name__ == "__main__":
    # 生成示例文件
    print("=" * 60)
    print("担保信息文件生成器 (421GUARINFO.txt)")
    print("=" * 60)

    # 生成10条随机记录（包含企业和自然人）
    generate_guarantee_info_file(
        output_file="421GUARINFO.txt",
        count=60,
        guarantor_type=None,  # 随机
    )

    print("\n" + "=" * 60)
    print("生成完成！")
    print("=" * 60)

