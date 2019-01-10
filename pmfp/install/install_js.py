import subprocess
import json
from typing import (
    Dict,
    Any,
    Optional
)
from pmfp.const import (
    JS_ENV_PATH,
    PMFPRC_PATH
)


def install_one(config: Dict[str, Any], package: str, dev: bool = False):
    if not JS_ENV_PATH.is_file():
        p_language = config["project-language"]
        print(f"{p_language}项目需要先有一个package.json配置文件")
    print(f"安装依赖{package}")
    if dev is False:
        command = f"npm install {package} --save"
        subprocess.check_call(command, shell=True)
        requirement = list(set(config["requirement"]))
        requirement.append(package)
        config["requirement"] = requirement
    else:
        command = f"npm install {package} --save-dev"
        subprocess.check_call(command, shell=True)
        requirement = list(set(config["requirement-dev"]))
        requirement.append(package)
        config["requirement-dev"] = requirement
    with open(str(PMFPRC_PATH), "w",encoding="utf-8") as f:
        json.dump(config, f)
    print(f"安装依赖{package}成功")


def install(config: Dict[str, Any], package: Optional[str] = None, dev: bool = False):
    """node 安装一条依赖."""
    if not JS_ENV_PATH.is_file():
        p_language = config["project-language"]
        print(f"{p_language}项目需要先有一个package.json配置文件")
    if package is None:
        print("安装全部依赖")
        if dev is False:
            for i in config.get("requirement"):
                install_one(config, i)
        else:
            for i in config.get("requirement-dev"):
                install_one(config, i)
        print("安装全部依赖成功")
    else:
        install_one(config, package, dev)

    return True
