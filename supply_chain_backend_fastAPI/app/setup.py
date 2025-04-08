from setuptools import setup, find_packages

setup(
    name="supply_chain_backend_fastAPI",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-jose",
        "passlib",
        "python-dotenv",
        # Add other dependencies...
    ],
)