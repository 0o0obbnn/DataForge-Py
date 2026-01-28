from datetime import datetime, timedelta, timezone
from typing import Any

# 忽略mypy对缺少类型存根的警告
try:
    from jose import jwt  # type: ignore
except ImportError:
    jwt = None

try:
    from passlib.context import CryptContext  # type: ignore
except ImportError:
    CryptContext = None

from dataforge.config.settings import get_settings

# 加密算法
ALGORITHM = "HS256"
# 访问令牌过期时间（分钟）
ACCESS_TOKEN_EXPIRE_MINUTES = 30
# 用于签发JWT的密钥
SECRET_KEY = get_settings().jwt_secret_key

# 确保CryptContext存在后再初始化
pwd_context = (
    CryptContext(schemes=["bcrypt"], deprecated="auto") if CryptContext else None
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    if not pwd_context:
        raise ImportError("passlib.context.CryptContext 未安装")
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """生成密码哈希"""
    if not pwd_context:
        raise ImportError("passlib.context.CryptContext 未安装")
    return pwd_context.hash(password)


def create_access_token(
    data: dict[str, Any], expires_delta: timedelta | None = None
) -> str:
    """创建访问令牌"""
    if not jwt:
        raise ImportError("jose 未安装")
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
