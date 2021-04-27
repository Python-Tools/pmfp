import json
from pathlib import Path
from typing import Optional, List, Tuple, Dict, Any
from pmfp.utils.fs_utils import get_abs_path
from pmfp.utils.remote_cache_utils import SourcePack
from pmfp.utils.tools_info_utils import get_cache_dir, get_config_info
from pmfp.entrypoint.env_.new import new_env
from pmfp.entrypoint.requires.install import install_requires
from pmfp.entrypoint.project.info import InfoBase
from pmfp.entrypoint.project.add import _add_component, make_template_kv, to_target_source, sourcepack_check_and_cached
from .core import project_new


def check_and_cached(cached_sourcepack: List[str], template_string: str, cache_dir: Path) -> Tuple[SourcePack, Path]:
    """检查组件的模板库是否有缓存,没有的话进行缓存.

    `latest`标签的模板库都会进行缓存更新.

    Args:
        template_string (str): 模板仓库字符串
        cache_dir (Path): 缓存根目录

    Raises:
        AttributeError: 组件缓存位置不是目录
        e: 其他执行中的异常

    Return:
        ComponentTemplate: 组件对象
    """
    source_pack = SourcePack.from_sourcepack_string(template_string)
    sourcepackdir = sourcepack_check_and_cached(cached_sourcepack, source_pack, cache_dir)
    return source_pack, sourcepackdir


def check_source(pmfpconf: Dict[str, Any], env: str, sourcepackdir: Path, template_string: str, language: Optional[str] = None) -> Dict[str, Any]:
    """校验组件所在模板库的信息,通过的话返回模板库信息"""
    if not language:
        if env in ("venv", "conda"):
            language = "py"
        elif env == "gomod":
            language = "go"
        elif env == "cmake":
            language = "CXX"
        else:
            raise AttributeError(f"env {env} not support")
    with open(sourcepackdir.joinpath(pmfpconf["template_config_name"]), encoding="utf-8") as f:
        sourcepack_config = json.load(f)
    sourcepack_language = sourcepack_config["language"]
    if sourcepack_language != language:
        raise AttributeError(f"组件{template_string}语言{sourcepack_language}与项目语言{language}不匹配")
    sourcepack_env = sourcepack_config.get("env")
    if sourcepack_env and sourcepack_env != env:
        raise AttributeError(f"组件{template_string}执行环境{sourcepack_env}与项目执行环境{env}不匹配")
    return sourcepack_config


@project_new.as_main
def new_project(env: str, *,
                language: Optional[str] = None,
                project_name: Optional[str] = None,
                version: Optional[str] = None,
                author: Optional[str] = None,
                author_email: Optional[str] = None,
                description: Optional[str] = None,
                keywords: Optional[List[str]] = None,
                requires: Optional[List[str]] = None,
                template_string: Optional[str] = None,
                with_test: bool = False,
                install: bool = False,
                kv: Optional[List[str]] = None,
                install_env_args: Optional[List[str]] = None,
                cwd: str = ".") -> None:

    if not template_string:
        print("开始构造指定的执行环境")
        new_env(env=env,
                language=language,
                project_name=project_name,
                version=version,
                author=author,
                author_email=author_email,
                description=description,
                keywords=keywords,
                cwd=cwd)

    else:
        # 开始根据模板构造项目组件
        pmfpconf = get_config_info()
        cache_dir = get_cache_dir()
        cwdp = get_abs_path(cwd)
        cached_sourcepacks: List[str] = []
        source_pack, sourcepackdir = check_and_cached(cached_sourcepacks, template_string, cache_dir)
        sourcepack_config = check_source(
            pmfpconf=pmfpconf,
            language=language,
            env=env,
            sourcepackdir=sourcepackdir,
            template_string=template_string
        )
        print("开始构造指定的执行环境")
        new_env(env=env,
                language=language,
                project_name=project_name,
                version=version,
                author=author,
                author_email=author_email,
                description=description,
                keywords=keywords,
                requires=sourcepack_config.get("requires"),
                test_requires=sourcepack_config.get("test_requires"),
                setup_requires=sourcepack_config.get("setup_requires"),
                cwd=cwd)

        projectinfo = InfoBase()
        projectinfo([])
        projectconfig = projectinfo.config
        components = sourcepack_config.get("components")
        if components:
            print("开始构造组件")
            for component_name, component_info in components.items():
                component_string = f"{template_string}//{component_name}"
                _add_component(
                    cached_sourcepacks=cached_sourcepacks,
                    projectconfig=projectconfig,
                    pmfpconf=pmfpconf,
                    cache_dir=cache_dir,
                    component_string=component_string,
                    cwdp=cwdp, kv=kv)
            print("组件构造结束")
        if with_test:
            sourcepack_test_config = sourcepack_config.get("test")
            if not sourcepack_test_config:
                print("模板没有提供测试资源")
            else:
                print("开始构造测试模板")
                target_source = sourcepack_test_config["source"]
                if "//" in target_source:
                    _add_component(
                        cached_sourcepacks=cached_sourcepacks,
                        projectconfig=projectconfig,
                        pmfpconf=pmfpconf,
                        cache_dir=cache_dir,
                        component_string=target_source,
                        cwdp=cwdp,
                        kv=kv,
                        save=False)
                else:
                    tempkv = make_template_kv(
                        sourcepack_config=sourcepack_config,
                        projectconfig=projectconfig,
                        kv=kv)
                    located_path_str = to_target_source(projectconfig=projectconfig,
                                                        target_component_info=sourcepack_test_config,
                                                        cwdp=cwdp,
                                                        sourcepackdir=sourcepackdir,
                                                        target_source=target_source,
                                                        tempkv=tempkv)

        if install:
            install_requires(env=env,
                             test=with_test,
                             requires=sourcepack_config.get("requires"),
                             test_requires=sourcepack_config.get("test_requires"),
                             env_args=install_env_args,
                             cwd=cwd)
