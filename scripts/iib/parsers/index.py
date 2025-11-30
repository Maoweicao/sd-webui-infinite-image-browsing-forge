import sys
import os

# 添加 iib 目录到 Python 路径
iib_dir = os.path.dirname(os.path.abspath(__file__))
if iib_dir not in sys.path:
    sys.path.insert(0, iib_dir)
from parsers.comfyui import ComfyUIParser
from parsers.sd_webui import SdWebUIParser
from parsers.fooocus import FooocusParser
from parsers.novelai import NovelAIParser
from parsers.model import ImageGenerationInfo
from parsers.stable_swarm_ui import StableSwarmUIParser
from parsers.invoke_ai import InvokeAIParser
from parsers.sd_webui_stealth import SdWebUIStealthParser
from logger import logger
from PIL import Image
from plugin import plugin_insts
import traceback


def parse_image_info(image_path: str) -> ImageGenerationInfo:
    enable_stealth_parser = os.getenv('IIB_ENABLE_SD_WEBUI_STEALTH_PARSER', 'false').lower() == 'true'
    parsers = plugin_insts + [
        ComfyUIParser,
        FooocusParser,
        NovelAIParser,
        InvokeAIParser,
        StableSwarmUIParser,
    ]
    
    if enable_stealth_parser:
        parsers.append(SdWebUIStealthParser)
    
    parsers.append(SdWebUIParser)
    with Image.open(image_path) as img:
        for parser in parsers:
            if parser.test(img, image_path):
                try:
                    return parser.parse(img, image_path)
                except Exception as e:
                    logger.error(e, stack_info=True)
                    print(e)
                    print(traceback.format_exc())
                    return ImageGenerationInfo()
        raise Exception("matched parser is not found")
