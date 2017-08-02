from setuptools import setup, find_packages

setup(name='indras_net',
    version='1.21',
    description='A framework for agent-based modeling in Python.',
    url='http://github.com/gcallah/indra',
    author='Gene Callahan and Nathan Conroy',
    author_email='gcallah@mac.com',
    license='GNU',
    zip_safe=False,
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*",
                                 "tests"]),
    install_requires=[
          "networkx",
          "numpy",
    ],
    test_suite="",
    entry_points={
        "console_scripts": ['indra = indra.__main__:main']
    },
)
