import os
import sys
from PIL import Image

# 添加 iib 目录到 Python 路径
iib_dir = os.path.dirname(os.path.abspath(__file__))
if iib_dir not in sys.path:
    sys.path.insert(0, iib_dir)

from tool import (
    parse_generation_parameters,
    read_sd_webui_gen_info_from_image,
)
from parsers.model import ImageGenerationInfo, ImageGenerationParams


class SdWebUIParser:
    def __init__(self):
        pass

    @classmethod
    def parse(clz, img: Image, file_path):
        if not clz.test(img, file_path):
            raise Exception("The input image does not match the current parser.")
        info = read_sd_webui_gen_info_from_image(img, file_path)
        width, height = img.size
        if not info:
            return ImageGenerationInfo(
                params=ImageGenerationParams(
                    meta={"final_width": width, "final_height": height}
                )
            )
        info += ", Source Identifier: Stable Diffusion web UI"
        params = parse_generation_parameters(info)
        return ImageGenerationInfo(
            info,
            ImageGenerationParams(
                meta=params["meta"] | {"final_width": width, "final_height": height},
                pos_prompt=params["pos_prompt"],
                extra=params,
            ),
        )

    @classmethod
    def test(clz, img: Image, file_path: str):
        try:
            return True
        except Exception as e:
            return False
