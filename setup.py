from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pomodoro-raccoon",
    version="0.1.3",
    author="Nick Witmar",
    author_email="nickwitmar@gmail.com",
    description="Ein simpler Pomodoro-Timer mit ASCII-Waschbär-Animation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/event173/pomodoro-racoon",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Office/Business :: Scheduling",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pomodoro-raccoon=pomodoro_raccoon:run",
        ],
    },
    keywords="pomodoro timer productivity ascii animation raccoon",
    project_urls={
        "Bug Reports": "https://github.com/event173/pomodoro-racoon/issues",
        "Source": "https://github.com/event173/pomodoro-racoon",
    },
)