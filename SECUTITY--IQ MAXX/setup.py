from setuptools import setup, find_packages

setup(
    name="iqmaxx",
    version="2.5.0",
    description="IQ MAXX (by dk) - Advanced Cross-Platform Wi-Fi Auditing, Security Assessment & Password Access Suite",
    long_description=open("README.md", encoding="utf-8").read() if open("README.md", encoding="utf-8") else "",
    long_description_content_type="text/markdown",
    author="dk",
    packages=find_packages(),
    py_modules=["iqmaxx"],
    entry_points={
        "console_scripts": [
            "iqmaxx = iqmaxx:main",
            "iq-maxx = iqmaxx:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Security",
        "Topic :: System :: Networking",
    ],
    python_requires=">=3.7",
)
