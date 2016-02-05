from setuptools import setup, find_packages

setup(
    name="yom",
    version="0.0.1",
    author="Yury Krapivko",
    author_email="hackprime@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    url="https://github.com/hackprime/yom",
    license="LICENSE.txt",
    description=("Useful command line utility "
                 "to manage your Yandex OAuth2 applications"),
    # long_description=open("README.txt").read(),
    entry_points={
        'console_scripts': ['yom = yom.cli:main'],
    },
    install_requires=[
        "grab==0.6.30",
        "humanfriendly==1.43.1",
    ],
    setup_requires=['pytest-runner'],
    tests_require=[
        "pytest",
        "mock",
    ],

)
