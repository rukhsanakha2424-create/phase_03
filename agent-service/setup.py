"""Setup configuration for agent service package."""
from setuptools import setup, find_packages

setup(
    name="agent-service",
    version="0.1.0",
    description="Natural language interpreter for todo commands using OpenAI Agents SDK",
    author="Taskie Team",
    author_email="team@taskie.local",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "openai>=1.0.0",
        "pydantic>=2.0.0",
        "httpx>=0.24.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "mypy>=1.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
