import os
from setuptools import setup, find_packages

def read_file(filename):

    basepath = os.path.dirname(__file__)
    filepath = os.path.join(basepath, filename)

    if os.path.exists(filepath):
        return open(filepath).read()
    else:
        return ''


setup(
    name = 'ghs_armcc_error_analyzer',
    version = '0.0.1',
    description = "Analyzer for GHS ARM C Compiler's error messages",
    long_description = read_file('README.rst'),
    packages = find_packages(),
    include_package_data = True,
    install_requires = [
        'jinja2',
    ],
    entry_points = """
        [console_scripts]
        ghs_armcc_error_analyzer = ghs_armcc_error_analyzer.ghs_armcc_error_analyzer:main
    """,
    author = 'Katsuki Kobayashi',
    author_email = 'rare@tirasweel.org',
    url = 'https://github.com/rarewin/ghs-armcc-error-analyzer',
    license = 'BSD 2-Clause License',
)
