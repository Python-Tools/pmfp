"""编译protobuf的schema为不同语言的代码."""
import subprocess
from typing import Dict, Any
import chardet
from pmfp.const import PROJECT_HOME


def build_pb_go(name: str, dir_: str, to: str, grpc: bool) -> None:
    if grpc:
        command = f"protoc -I {dir_} {dir_}/{name} --go_out=plugins=grpc:{to}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译grpc的protobuf项目<{name}>为go语言模块完成!")
        else:
            print(f"编译grpc的protobuf项目{name}为go语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        command = f"protoc -I={dir_} --go_out={to} {dir_}/{name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译protobuf项目<{name}>为go语言模块完成!")
        else:
            print(f"编译protobuf项目{name}为go语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))


def find_pypackage(final_path, packs):
    has_init = False
    for i in final_path.iterdir():
        if i.name == "__init__.py":
            has_init = True
    if not has_init:
        return
    else:
        lates_p = final_path.name
        packs.append(lates_p)
        find_pypackage(final_path.parent, packs)


def find_pypackage_string(to_path: str) -> str:
    packs = []
    final_path = PROJECT_HOME.joinpath(to_path)
    find_pypackage(final_path, packs)
    packs = ".".join(reversed(packs))
    return packs


def build_pb_py(name: str, dir_: str, to: str, grpc: bool) -> None:
    if grpc:
        command = f"python -m grpc_tools.protoc -I{dir_} --python_out={to} \
                    --grpc_python_out={to} {name}"
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
            for line in lines:
                if f"import {n}_pb2 as {n}__pb2" in line:
                    t = f"import {packstr}.{n}_pb2 as {n}__pb2\n"
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


def build_pb_js(name: str, dir_: str, to: str, grpc: bool) -> None:
    if grpc:
        command = f"python -m grpc_tools.protoc -I{dir_} --js_out={to} \
                    --grpc_js_out={to} {name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译grpc的protobuf项目<{name}>为js模块完成!")
        else:
            print(f"编译grpc的protobuf项目{name}为js模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))
    else:
        command = f"protoc -I={dir_} --js_out={to} {dir_}/{name}"
        res = subprocess.run(command, capture_output=True, shell=True)
        if res.returncode == 0:
            print(f"编译protobuf项目<{name}>为js语言模块完成!")
        else:
            print(f"编译protobuf项目{name}为js语言模块失败!")
            encoding = chardet.detect(res.stderr).get("encoding")
            print(res.stderr.decode(encoding))


def build_pb(kwargs: Dict[str, Any]) -> None:
    """编译protobuf的schema为不同语言的代码.

    Args:
        kwargs (Dict[str, Any]): 编译的配置信息字典.
    """
    name = kwargs.get("name")
    dir_ = kwargs.get("dir")
    to = kwargs.get("to")
    language = kwargs.get("language")
    grpc = kwargs.get("grpc")
    if not PROJECT_HOME.joinpath(to).is_dir():
        PROJECT_HOME.joinpath(to).mkdir()

    if language in ("go", "Go", "golang", "Golang"):
        build_pb_go(name, dir_, to, grpc)
    elif language in ("python", "py", "Python", "PY"):
        build_pb_py(name, dir_, to, grpc)
    elif language in ("js", "javascript", "JS", "Javascript"):
        build_pb_js(name, dir_, to, grpc)
