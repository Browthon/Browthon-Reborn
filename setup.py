from setuptools import setup, find_packages

print(find_packages())

setup(name='Browthon Reborn',
    version='0.1.0',
    description='A webbrowser made with Python and PyQt',
    url='https://github.com/Browthon/Browthon-Reborn',
    author='KavaPower',
    author_email='lavapower84@gmail.com',
    license='GNU GPLv3',
    packages=find_packages(),
    install_requires=[
        'PyQt5'
    ],
    entry_points={
        'console_scripts':[
            'browthon = browthon.browthon_app:launch',
        ],
    }, 
    include_package_data=True,

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
    ],
)
