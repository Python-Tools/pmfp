"""ppm proto命令的处理."""
from schema_entry import EntryPoint
from ..core import ppm


class Grpc(EntryPoint):
    """protobuf和grpc相关的工具."""


grpc = ppm.regist_sub(Grpc)
