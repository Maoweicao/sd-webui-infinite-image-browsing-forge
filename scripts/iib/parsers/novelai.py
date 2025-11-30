import os
import sys
import json

# 添加 iib 目录到 Python 路径
iib_dir = os.path.dirname(os.path.abspath(__file__))
if iib_dir not in sys.path:
    sys.path.insert(0, iib_dir)
from PIL import Image

from tool import (
    parse_generation_parameters,
    replace_punctuation
)
from parsers.model import ImageGenerationInfo, ImageGenerationParams


class NovelAIParser:
    def __init__(self):
        pass

    @classmethod
    def parse(clz, img, file_path):
        info = ""
        params = None
        if not clz.test(img, file_path):
            raise Exception("The input image does not match the current parser.")
        data = json.loads(img.info.get('Comment'))
        meta_kv = [f"""Steps: {data["steps"]}, Source Identifier: NovelAI"""]
        for key, value in data.items():
            if key not in ["prompt"]:
                value = replace_punctuation(str(value))
                meta_kv.append(f"{key}: {value}")
        meta = ', '.join(meta_kv)
        info = data["prompt"] + '\n' + meta

        params = parse_generation_parameters(info)

        return ImageGenerationInfo(
            info,
            ImageGenerationParams(
                meta=params["meta"]
                | {"final_width": img.size[0], "final_height": img.size[1]},
                pos_prompt=params["pos_prompt"],
            ),
        )

    @classmethod
    def test(clz, img: Image, file_path: str) -> bool:
        try:
            return img.info.get('Software') == 'NovelAI' and isinstance(img.info.get('Comment'), str)
        except Exception:
            return False
