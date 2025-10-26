from setuptools import setup, find_packages

setup(
    name="visionflow",
    version="0.1.0",
    description="VISIONFLOW - Professional image editor with optical integrity preservation",
    author="VisionFlow Team",
    packages=find_packages(),
    install_requires=[
        "Pillow>=10.0.0",
        "numpy>=1.24.0",
        "scipy>=1.11.0",
    ],
    entry_points={
        'console_scripts': [
            'visionflow=visionflow.cli:main',
        ],
    },
    python_requires='>=3.8',
)
