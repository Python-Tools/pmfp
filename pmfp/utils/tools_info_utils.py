"""tools_info_utils

获取功能依赖工具信息的工具组
"""
import warnings
import json
from pathlib import Path
from typing import Optional
from pmfp.utils.fs_utils import init_pmfprc
from pmfp.utils.run_command_utils import run_command
from pmfp.const import (
    PMFP_CONFIG_PATH,
    GOLBAL_PYTHON,
    GOLBAL_CC
)


def get_global_python() -> str:
    """获取全局python."""
    init_pmfprc()
    with open(PMFP_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("python", GOLBAL_PYTHON)


def get_global_cc() -> str:
    """获取全局c编译器."""
    init_pmfprc()
    with open(PMFP_CONFIG_PATH, "r") as f:
        pmfprc = json.load(f)
        return pmfprc.get("cc", GOLBAL_CC)


def get_node_version() -> Optional[str]:
    """获取系统中node的版本."""
    p = run_command(
        "node -v"
    ).catch(
        lambda _: warnings.warn("系统中未找到node环境,如有需要请安装")
    ).then(
        lambda x: x[1:]
    )
    return p.get()


def get_golang_version() -> Optional[str]:
    """获取本地golang的版本."""
    p = run_command(
        "go version"
    ).catch(
        lambda _: warnings.warn("系统中未找到golang环境,如有需要请安装")
    ).then(
        lambda content: [i for i in content.split(" ") if "." in i][0][2:]
    )
    return p.get()


def get_protoc_version() -> Optional[str]:
    """获取本地protoc的版本."""
    p = run_command(
        "protoc --version"
    ).catch(
        lambda _: warnings.warn("系统中未找到protoc环境,如有需要请安装")
    ).then(
        lambda content: [i for i in content.split(" ") if "." in i][0]
    )
    return p.get()


def get_local_python(env_path: Path) -> str:
    """获取本地环境python解释器的地址.

    Args:
        env_path_str (Path): python本地环境目录.

    Returns:
        str: python位置字符串
    """
    python_path = env_path.joinpath("bin/python")
    if not python_path.exists():
        python_path = env_path.joinpath("Scripts/python")
        if not python_path.exists():
            python_path = env_path.joinpath("python")
            if not python_path.exists():
                warnings.warn("目录中未找到python环境.使用全局python")
                return get_global_python()
    return str(python_path)
