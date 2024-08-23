from setuptools import setup, find_packages

setup(
    name="J_Core",
    author="jswa",
    description="Private Python library to create and maintain business object endpoints.",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent"
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content"
    ],
    python_requires='>=3.12',
    setup_requires=['setuptools-git-versioning'],
    version_config={
        "dirty_template": "{tag}",
    },
    install_requires=[
        'psycopg2-binary==2.9.9',
        'Flask==3.0.2',
        'SQLAlchemy==2.0.28'
    ]
)
