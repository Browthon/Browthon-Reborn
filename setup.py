from setuptools import setup, find_packages

import browthon

setup(
    name='Browthon-Reborn',
    version=browthon.__version__,
    description='A webbrowser made with Python and PySide2',
    url='https://github.com/Browthon/Browthon-Reborn',
    author='LavaPower',
    author_email='lavapower84@gmail.com',
    license='GNU GPLv3',
    packages=find_packages(),
    install_requires=[
        'PySide2'
    ],
    entry_points={
      'console_scripts':[
          'browthon = browthon.browthon_app:launch',
      ],
    },
    include_package_data=True,

    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Natural Language :: French',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP :: Browsers'
    ],
)
