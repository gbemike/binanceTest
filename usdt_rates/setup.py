from setuptools import find_packages, setup

setup(
    name="usdt_rates",
    packages=find_packages(exclude=["usdt_rates_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
