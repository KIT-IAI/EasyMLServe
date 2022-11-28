import setuptools


with open('requirements.txt', 'r') as f:
    requirements = f.read().split('\n')
    f.close()


setuptools.setup(
    name='easymlserve',
    version='0.1',
    packages=setuptools.find_packages(),

    install_requires=requirements,
    extras_require={
        'dev': [
            'pytest'
        ]
    },
    author='Oliver Neumann',
    author_email='oliver.neumann@kit.edu',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Libraries',
        'Natural Language :: English',
        'Operating System :: OS Independent',
    ],
    description='Deploy machine learning pipelines easily in a RESTful way.',
    keywords='rest restful machine-learning',
)