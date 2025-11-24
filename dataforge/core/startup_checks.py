"""应用启动时的安全检查

在应用启动时验证关键安全配置，防止不安全的配置进入生产环境
"""

import logging
import os

logger = logging.getLogger(__name__)


def check_security_configuration() -> tuple[bool, list[str]]:
    """检查安全配置

    Returns:
        Tuple[bool, List[str]]: (是否通过检查, 警告/错误列表)
    """
    issues = []
    is_dev = os.getenv("DEVELOPMENT", "false").lower() == "true"

    # 检查JWT密钥
    jwt_key = os.getenv("JWT_SECRET_KEY")
    if not jwt_key:
        if is_dev:
            issues.append("⚠️  WARNING: Using insecure development JWT key")
        else:
            issues.append("❌ ERROR: JWT_SECRET_KEY not set in production")
            return False, issues
    elif len(jwt_key) < 32:
        issues.append("⚠️  WARNING: JWT_SECRET_KEY is too short (< 32 characters)")

    # 检查是否使用了不安全的默认密钥
    if jwt_key and "insecure" in jwt_key.lower():
        issues.append("⚠️  WARNING: JWT_SECRET_KEY appears to be an insecure default")

    # 检查CORS配置
    cors_origins = os.getenv("ALLOWED_ORIGINS")
    if not cors_origins:
        if not is_dev:
            issues.append("❌ ERROR: ALLOWED_ORIGINS not set in production")
            return False, issues
    elif "*" in cors_origins and not is_dev:
        issues.append("❌ ERROR: CORS allows all origins (*) in production")
    else:
        # 如果设置了CORS，验证格式
        origins_list = [
            origin.strip() for origin in cors_origins.split(",") if origin.strip()
        ]
        for origin in origins_list:
            if not origin.startswith(("http://", "https://")):
                issues.append(
                    f"⚠️  WARNING: CORS origin '{origin}' should start with http:// or https://"
                )

    # 检查Redis配置（如果使用）
    redis_host = os.getenv("REDIS_HOST")
    if redis_host and redis_host not in ["localhost", "127.0.0.1"] and not is_dev:
        # 确保使用密码
        redis_password = os.getenv("REDIS_PASSWORD")
        if not redis_password:
            issues.append("⚠️  WARNING: Redis password not set for remote host")

    return len([i for i in issues if i.startswith("❌")]) == 0, issues


def perform_startup_checks() -> None:
    """执行启动检查

    Raises:
        RuntimeError: 当安全检查失败时抛出
    """
    logger.info("Performing startup security checks...")

    passed, issues = check_security_configuration()

    for issue in issues:
        if issue.startswith("❌"):
            logger.error(issue)
        else:
            logger.warning(issue)

    if not passed:
        logger.error("Security checks failed! Application will not start.")
        raise RuntimeError("Security configuration is invalid for production use")

    if issues:
        logger.warning(f"Security checks passed with {len(issues)} warnings")
    else:
        logger.info("✅ All security checks passed")
