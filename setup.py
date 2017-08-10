from setuptools import setup, find_packages

setup(name='indras_net',
    version='2.0.4',
    description='A framework for agent-based modeling in Python.',
    url='https://github.com/gcallah/indras_net.git',
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
    classifiers=[
            # How mature is this project? Common values are
            #   3 - Alpha
            #   4 - Beta
            #   5 - Production/Stable
            'Development Status :: 4 - Beta',

            # Indicate who your project is intended for
            'Intended Audience :: Developers',

            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
    ],
)
