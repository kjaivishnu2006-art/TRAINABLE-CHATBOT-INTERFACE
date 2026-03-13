"""Setup configuration for Trainable ChatBot Builder."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8")

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = requirements_file.read_text(encoding="utf-8").strip().split("\n")

setup(
    name="trainable-chatbot-builder",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="No-code platform for training and deploying chatbots in MIT App Inventor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/trainable-chatbot",
    project_urls={
        "Bug Tracker": "https://github.com/your-org/trainable-chatbot/issues",
        "Documentation": "https://trainable-chatbot.readthedocs.io",
        "Source Code": "https://github.com/your-org/trainable-chatbot",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.2.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "sphinx>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "chatbot-builder=src.chatbot_builder.main:main",
        ],
    },
    keywords="chatbot machine-learning education mit-app-inventor gsoc",
    include_package_data=True,
)
