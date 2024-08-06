from setuptools import setup, find_packages

setup(
    name="qubitcooling",
    version="0.777",
    author="GiulianoWasHere",
    short_description="QuL is a python package to generate, analyze and test quantum circuits for various computational cooling protocols.",
    long_description="QuL is a python package to generate, analyze and test quantum circuits for various computational cooling protocols.",
    install_requires=['qiskit', 'scipy','numpy'],
    keywords=['python', 'quantum', 'cooling', 'qubit', 'quantumcomputing'],
    project_urls={
        'Source': "https://github.com/GiulianoWasHere/QuL",
    },
)