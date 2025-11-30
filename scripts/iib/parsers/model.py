from tool import os
import sys
import omit

# 添加 iib 目录到 Python 路径
iib_dir = os.path.dirname(os.path.abspath(__file__))
if iib_dir not in sys.path:
    sys.path.insert(0, iib_dir)


class ImageGenerationParams:
    def __init__(self, meta: dict = {}, pos_prompt: list = [], extra: dict = {}) -> None:
        self.meta = meta
        self.pos_prompt = pos_prompt
        self.extra = omit(extra, ["meta", "pos_prompt"])


class ImageGenerationInfo:
    def __init__(
        self,
        raw_info: str = "",
        params: ImageGenerationParams = ImageGenerationParams(),
    ):
        self.raw_info = raw_info
        self.params = params
