# coding: utf-8
from setuptools import setup, find_packages

setup(
    name="webpage-saliency-map",
    version='1.1',
    description='ウェブページの顕著性マップ生成',
    author='Yuya Inagaki',
    author_email='yuya.ina56@gmail.com',
    url='https://github.com/yuya-inagaki/web-saliency-map',
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      webpage_saliency_map = webpage_saliency_map.cli:execute
    """,
)
