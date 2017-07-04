from setuptools import setup, find_packages

setup(name='indras_net',
    version='1.0',
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
          "mkl",
          "numpy",
          "matplotlib",
          "cycler",
          "freetype",
          "icu",
          "libpng",
          "matplotlib",
          "pyqt",
          "python-dateutil",
          "pytz",
          "qt",
          "sip-4.19.3",
          "clint",
    ],
    test_suite="",
    entry_points={
        "console_scripts": ["bigbox = bigbox.__main__:main",
                            "schelling = schelling.__main__:main",
                            "models = models.__main__:main"
                           ]
    },
)


