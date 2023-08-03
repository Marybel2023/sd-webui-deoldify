'''
Author: SpenserCai
Date: 2023-07-28 14:41:28
version: 
LastEditors: SpenserCai
LastEditTime: 2023-08-03 15:11:07
Description: file content
'''
# DeOldify UI & Processing
from modules import scripts_postprocessing
import gradio as gr

from modules.ui_components import FormRow

from deoldify.device_id import DeviceId
from PIL import Image

from deoldify.visualize import *

import warnings
warnings.filterwarnings("ignore", category=UserWarning, message=".*?Your .*? set is empty.*?")
warnings.filterwarnings("ignore", category=UserWarning, message="The parameter 'pretrained' is deprecated since 0.13 and may be removed in the future, please use 'weights' instead.")
warnings.filterwarnings("ignore", category=FutureWarning, message="Arguments other than a weight enum or `None`.*?")

class ScriptPostprocessingUpscale(scripts_postprocessing.ScriptPostprocessing):
    name = "Deoldify"
    order = 20999
    model = None

    def ui(self):
        with FormRow():
            is_enabled = gr.Checkbox(label="启用")
            is_enabled.value = False
            render_factor = gr.Slider(minimum=1, maximum=50, step=1, label="渲染因子")
            render_factor.value = 35
            # 一个名为artistic的复选框，初始值是False
            artistic = gr.Checkbox(label="艺术化")
            artistic.value = False

        return {
            "is_enabled": is_enabled,
            "render_factor": render_factor,
            "artistic": artistic,
        }
    
    def process_image(self, image, render_factor, artistic):
        vis = get_image_colorizer(root_folder=Path("models"),render_factor=render_factor, artistic=artistic)
        outImg = vis.get_transformed_image_from_image(image, render_factor=render_factor)
        return outImg

    def process(self, pp: scripts_postprocessing.PostprocessedImage, is_enabled, render_factor, artistic):
        if not is_enabled or is_enabled is False:
            return
        
        print(type(pp.image))

        pp.image = self.process_image(pp.image, render_factor, artistic)
        pp.info["deoldify"] = f"render_factor={render_factor}, artistic={artistic}"