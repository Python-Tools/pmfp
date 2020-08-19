"""编译python语言模块."""
import subprocess
import chardet
from pathlib import Path
from typing import List, Optional,NoReturn,Dict

def _find_pypackage(final_path: Path, packs: List[Optional[str]]):
    has_init = False
    for i in final_path.iterdir():
        if i.name == "__init__.py":
            has_init = True
    if not has_init:
        return
    else:
        lates_p = final_path.name
        packs.append(lates_p)
        _find_pypackage(final_path.parent, packs)


def find_pypackage_string(to_path: str) -> str:
    """find_pypackage_string.

    Args:
        to_path (str): 目标地址
    Returns:
        str: package地址

    """
    packs = []
    tp = Path(to_path)
    if tp.is_absolute():
        final_path = tp
    else:
        final_path = Path(".").absolute().joinpath(to_path)
    _find_pypackage(final_path, packs)
    packs = ".".join(reversed(packs))
    return packs


def find_py_grpc_pb2_import_string(n: str)->str:
    """python的grpc模块as的内容."""
    org = f"{n}_pb2"
    return "__".join(org.split("_"))

def _build_pb_py(files: List[str], includes: List[str], to: str, **kwargs: Dict[str, str]) -> NoReturn:
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    task = "protobuf"
    command = f"protoc  {includes_str} {flag_str} --python_out={to} {target_str}"
    print(f"编译命令:{command}")
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"编译{task}项目{name}为python语言模块失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        print(f"编译{task}项目{name}为python语言模块完成!")

def _build_grpc_py(files: List[str], includes: List[str], to: str, **kwargs: Dict[str, str])->NoReturn:
    includes_str = " ".join([f"-I {include}" for include in includes])
    target_str = " ".join(files)
    flag_str = ""
    if kwargs:
        flag_str += " ".join([f"{k}={v}" for k, v in kwargs.items()])
    task = "grpc"
    command = f"python -m grpc_tools.protoc {includes_str} {flag_str} --python_out={to} --grpc_python_out={to} {target_str}"
    print(f"编译命令:{command}")
    res = subprocess.run(command, capture_output=True, shell=True)
    if res.returncode != 0:
        print(f"编译{task}项目{target_str}为python语言模块失败!")
        encoding = chardet.detect(res.stderr).get("encoding")
        print(res.stderr.decode(encoding))
    else:
        to_path = PROJECT_HOME.joinpath(to)
        tp = Path(to)
        if tp.is_absolute():
            to_path = tp
        else:
            to_path = Path(".").absolute().joinpath(to)

        n = name.split(".")[0]
        to_path.joinpath("__init__.py").open("w").write(
            f"""from .{n}_pb2 import *
from .{n}_pb2_grpc import *"""
        )
        grpc_file = to_path.joinpath(f"{n}_pb2_grpc.py")
        with open(str(grpc_file), "r") as f:
            lines = f.readlines()
        new_lines = []
        packstr = find_pypackage_string(to)
        print(to)
        print(packstr)
        as_package = find_py_grpc_pb2_import_string(n)
        for line in lines:
            if f"import {n}_pb2 as {as_package}" in line:
                t = f"import {packstr}.{n}_pb2 as {as_package}\n"
                new_lines.append(t)
            else:
                new_lines.append(line)
        with open(str(grpc_file), "w") as f:
            f.writelines(new_lines)
        print(f"编译{task}项目{target_str}为python语言模块完成!")


def build_pb_py(files: List[str], includes: List[str], to: str,grpc:bool, **kwargs: Dict[str, str]) -> NoReturn:
    """编译python语言模块.

    Args:
        files (List[str]): 待编译的protobuffer文件
        includes (List[str]): 待编译的protobuffer文件所在的文件夹
        to (str): 编译成的模块文件放到的路径
        grpc (bool): 是否编译为grpc

    """
    if grpc:
        _build_grpc_py(files, includes, to, **kwargs)

    else:
        _build_pb_py(files, includes, to, **kwargs)