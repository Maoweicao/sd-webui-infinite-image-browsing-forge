from PIL import os
import sys
import Image

# 添加 iib 目录到 Python 路径
iib_dir = os.path.dirname(os.path.abspath(__file__))
if iib_dir not in sys.path:
    sys.path.insert(0, iib_dir)

from tool import (
    comfyui_exif_data_to_str,
    is_img_created_by_comfyui,
    is_img_created_by_comfyui_with_webui_gen_info,
    get_comfyui_exif_data,
    parse_generation_parameters,
    read_sd_webui_gen_info_from_image,
)
from parsers.model import os
import sys
import ImageGenerationInfo, ImageGenerationParams
from logger import logger


class ComfyUIParser:
    def __init__(self):
        pass

    @classmethod
    def parse(clz, img, file_path):
        info = ""
        params = None
        if not clz.test(img, file_path):
            raise Exception("The input image does not match the current parser.")
        width, height = img.size
        try:
            if is_img_created_by_comfyui_with_webui_gen_info(img):
                info = read_sd_webui_gen_info_from_image(img, file_path)
                info += ", Source Identifier: ComfyUI"
                params = parse_generation_parameters(info)
            else:
                params = get_comfyui_exif_data(img)
                info = comfyui_exif_data_to_str(params)
        except Exception as e:
            logger.error("parse comfyui image failed. prompt:")
            logger.error(img.info.get("prompt"))
            return ImageGenerationInfo(
                params=ImageGenerationParams(
                    meta={"final_width": width, "final_height": height}
                )
            )
        return ImageGenerationInfo(
            info,
            ImageGenerationParams(
                meta=params["meta"] | {"final_width": width, "final_height": height},
                pos_prompt=params["pos_prompt"],
                extra=params,
            ),
        )

    @classmethod
    def test(clz, img: Image, file_path: str) -> bool:
        try:
            return is_img_created_by_comfyui(
                img
            ) or is_img_created_by_comfyui_with_webui_gen_info(img)
        except Exception:
            return False
