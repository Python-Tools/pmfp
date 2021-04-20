"""protocol.

用于定义模块支持的可以用于解析的json schema的模式.
"""
TEMPLATE_INFO_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "required": ["language"],
    "properties": {
        "language": {
            "type": "string",
            "description": "模板使用的编程语言",
            "enum": ["py", "go"]
        },
        "mini_language_version": {
            "type": "string",
            "description": "模板使用编程语言的最低版本"
        },
        "description": {
            "type": "string",
            "description": "模板的描述文件"
        },
        "author": {
            "type": "string",
            "description": "模板的作者"
        },
        "template_type": {
            "type": "string",
            "description": "模板的类型",
            "enum": ["server", "client", "GUI", "script", "cmd", "module"]
        },
        "env": {
            "type": "string",
            "description": "模板推荐的执行环境",
            "enum": ["venv", "conda", "gomod"]
        },
        "requires": {
            "type": "array",
            "title": "r",
            "description": "最小化执行的依赖",
            "items": {
                    "type": "string"
            }
        },
        "test_requires": {
            "type": "array",
            "title": "t",
            "description": "如果有测试部分测试需要的依赖",
            "items": {
                    "type": "string"
            }
        },
        "setup_requires": {
            "type": "array",
            "title": "s",
            "description": "如果有安装部分,安装时的依赖",
            "items": {
                    "type": "string"
            }
        },
        "extras_requires": {
            "type": "array",
            "title": "",
            "description": "扩展的依赖",
            "items": {
                    "type": "string"
            }
        },
        "command": {
            "description": "模板的操作命令,可以是形式为列表的字符串,会被解析为列表",
            "type": "string"
        }
    }
}


PMFP_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "cache_dir": {
            "type": "string",
            "description": "cache的缓存位置",
        },
        "default_template_host": {
            "type": "string",
            "description": "模板默认的维护地址",
            "default": "github.com"
        },
        "default_template_namespace": {
            "type": "string",
            "description": "模板默认的维护命名空间",
            "default": "Project-Manager-With-Git"
        },
        "template_config_name": {
            "type": "string",
            "description": "模板的配置文件名",
            "default": ".pmfp_template.json"
        },
        "python": {
            "type": "string",
            "description": "默认使用的python"
        },
        "cc": {
            "type": "string",
            "description": "默认使用的c语言编译器"
        },
        "cxx": {
            "type": "string",
            "description": "默认使用的c++语言编译器"
        }
    }
}
