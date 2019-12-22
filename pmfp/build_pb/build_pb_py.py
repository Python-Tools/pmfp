"""编译python语言模块."""
import subprocess
import chardet
from pmfp.const import PROJECT_HOME
from .utils import (
    find_pypackage_string,
    find_py_grpc_pb2_import_string
)


def build_pb_py(name: str, dir_: str, to: str, grpc: bool) -> None:
    """编译python语言模块.

    Args:
        name (str): 要编译的pb文件
        dir_ (str): 要编译的pb文件所在文件夹
        to (str): 将模块文件编译到目标位置
        grpc (bool): 编译grpc
    """
    if grpc:
        command = f"python -m grpc_tools.protoc -I{dir_} \
            --python_out={to} --grpc_python_out={to} {name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode != 0:
            print(f"编译grpc的protobuf项目{name}为python模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
        else:
            to_path = PROJECT_HOME.joinpath(to)
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
            print(f"编译grpc的protobuf项目<{name}>为python模块完成!")

    else:
        command = f"protoc -I={dir_} --python_out={to} {dir_}/{name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译protobuf项目<{name}>为python语言模块完成!")
        else:
            print(f"编译protobuf项目{name}为python语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))