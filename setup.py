from setuptools import setup

packages = []
with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()


setup(
    name="AWS Serverless FastAPI 🚀",
    version="0.0.1",
    description="AWS Serverless FastAPI 🚀",
    author="Marius Engen",
    author_email="mariuengen@gmail.com",
    license="MIT",
    include_package_data=True,
    install_requires=requirements,
    packages=packages,
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
    ],
)
