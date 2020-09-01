"""version命令的处理."""
import argparse
from .core import ppm
from typing import Sequence
from pmfp import VERSION

@ppm.regist_subcmd
def version(argv:Sequence[str])->None:
    """ppm version

    获取pmfp工具的版本
    """
    cmd_version()

def cmd_version()->None:
    """打印工具的版本."""
    print(VERSION)