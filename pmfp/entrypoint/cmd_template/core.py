"""project命令的处理."""
from ..core import ppm, EntryPoint


ppm_template = EntryPoint("template")
ppm_template.__doc__ = """ppm template <subcmd>

    ppm template 的子命令有:

    module              项目模板管理工具
    component           组件模板管理工具
    """
ppm.regist_subcmd(ppm_template)
