import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wandering-in-gpt",
    version="0.0.1",
    author="Mingli Yuan",
    author_email="mingli.yuan@gmail.com",
    description="Wandering in GPT is a role-play game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mountain/wandering-in-gpt",
    project_urls={
        'Documentation': 'https://github.com/mountain/wandering-in-gpt',
        'Source': 'https://github.com/mountain/wandering-in-gpt',
        'Tracker': 'https://github.com/mountain/wandering-in-gpt/issues',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'requests',
        'termcolor',
    ],
    scripts=['wig'],
)

