#!/usr/bin/env python
"""PMFP.

一个项目管理脚手架.
"""


import sys
from typing import List
from colorama import init

from gevent import monkey
monkey.patch_all()
init()
from .entrypoint import ppm


def main(argv: List[str] = sys.argv[1:]) -> None:
    """服务启动入口.

    设置覆盖顺序`环境变量>命令行参数`>`'-c'指定的配置文件`>`项目启动位置的配置文件`>默认配置.
    """
    ppm(argv)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))