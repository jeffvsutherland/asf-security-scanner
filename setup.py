"""
ASF Security Scanner Setup Configuration
"""
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="asf-security-scanner",
    version="2.0.0",
    author="Agent Saturday",
    author_email="asf@agentsaturday.dev",
    description="Intelligent security scanner for AI agent skills",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/agent-saturday/asf-security-scanner",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Security",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        # No external dependencies - uses standard library only
    ],
    entry_points={
        "console_scripts": [
            "asf-scanner=asf_skill_scanner_v2:main",
        ],
    },
    keywords="security scanner ai agent clawdbot skills",
    project_urls={
        "Bug Reports": "https://github.com/agent-saturday/asf-security-scanner/issues",
        "Source": "https://github.com/agent-saturday/asf-security-scanner",
        "Documentation": "https://github.com/agent-saturday/asf-security-scanner/tree/main/docs",
    },
)