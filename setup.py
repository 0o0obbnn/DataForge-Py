from setuptools import setup, find_packages
import os

# 读取README文件
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "DataForge - 高效、灵活的测试数据生成工具"

# 读取requirements文件
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="dataforge",
    version="1.0.0",
    author="DataForge Team",
    author_email="contact@dataforge.org",
    description="高效、灵活的测试数据生成工具，专注于中国本土化数据生成",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dataforge/dataforge",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'dataforge': [
            'data/chinese/*.json',
            'data/international/*.json',
            'config/templates/*.yaml',
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.10',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.910',
        ],
        'docs': [
            'mkdocs>=1.4',
            'mkdocs-material>=8.0',
        ],
    },
    entry_points={
        'console_scripts': [
            'dataforge=dataforge.cli.main:main',
            'df=dataforge.cli.main:main',  # 简化命令
        ],
    },
    keywords="test data generation mock faker chinese localization",
    project_urls={
        "Bug Reports": "https://github.com/dataforge/dataforge/issues",
        "Source": "https://github.com/dataforge/dataforge",
        "Documentation": "https://dataforge.readthedocs.io/",
    },
)