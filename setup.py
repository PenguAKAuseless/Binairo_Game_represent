from setuptools import setup, find_packages

setup(
    name="Binairo_Game",  # Replace with your desired package name
    version="1.0.0",  # Increment as needed
    description="A Binairo game representation with Pygame",
    author="PenguAKAuseless",  # Replace with your name
    url="https://github.com/PenguAKAuseless/Binairo_Game_represent",  # Repository URL
    packages=find_packages(),  # Automatically find package directories
    install_requires=[
        "pygame>=2.0.0",  # Add dependencies here
    ],
    python_requires=">=3.7",  # Specify minimum Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update license as needed
        "Operating System :: OS Independent",
    ],
)