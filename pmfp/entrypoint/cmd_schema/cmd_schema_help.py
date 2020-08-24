"""ppm proto help命令的处理."""
import argparse
from .core import ppm_schema
from typing import Sequence


@ppm_schema.regist_subcmd
def help(argv:Sequence[str]):
    """ppm schema help <subcommand>
ppm schema工具的子命令有:

    new                 创建一个json schema的模式文件
    check               检查一个json文件是否满足指定的json schema的模式
    """
    parser = argparse.ArgumentParser(
        prog='ppm schema help',
        description='查看子命令的帮助说明',
        usage= ppm_schema.subcmds.get("help").__doc__
    )
    parser.add_argument('subcmd', type=str,
                        default=list(ppm_schema.subcmds.keys()), help="支持的子命令")
    parser.set_defaults(func=cmd_help)
    args = parser.parse_args(argv)
    args.func(args)

def cmd_help(args:argparse.Namespace):
    print(ppm_schema.subcmds.get(args.subcmd).__doc__)