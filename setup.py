from setuptools import setup, find_packages
setup(
    name="rigger_plugin_framework",
    version="0.0.5",
    packages=find_packages(),
    # include_package_data=True,
    install_requires=["rigger_singleton"],
)