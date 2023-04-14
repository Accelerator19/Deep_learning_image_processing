import io
import base64
import random
from PIL import Image
from PIL import ImageEnhance


def pic_onekey(image_buffer, rotate, zoom, cut, flip, color):
    # 使用PIL库打开图像
    image = Image.open(io.BytesIO(image_buffer))
    if rotate == "True":
        # 随机旋转0-360度
        angle = random.randint(0, 360)
        image = image.rotate(angle)

    if zoom == "True":
        # 随机缩放
        width, height = image.size
        scale_factor = random.uniform(0.5, 2.0)
        new_width = int(width * scale_factor)
        new_height = int(height * scale_factor)
        image = image.resize((new_width, new_height))

    if cut == "True":
        # 随机裁剪
        width, height = image.size
        crop_width = random.randint(int(0.5 * width), int(0.8 * width))  # 裁剪后的宽度随机在原始图像宽度的一半到0.8倍之间
        crop_height = random.randint(int(0.5 * height), int(0.8 * height))  # 裁剪后的高度随机在原始图像高度的一半到0.8倍之间
        left = random.randint(0, width - crop_width)
        top = random.randint(0, height - crop_height)
        right = left + crop_width
        bottom = top + crop_height
        image = image.crop((left, top, right, bottom))

    if flip == "True":
        # 随机水平或垂直翻转
        if random.random() < 0.5:
            # 水平翻转
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        else:
            # 垂直翻转
            image = image.transpose(Image.FLIP_TOP_BOTTOM)

    if color == "True":
        # 随机颜色变换
        brightness_factor = random.uniform(0.7, 1.3)  # 亮度调整因子
        color_factor = random.uniform(0.7, 1.3)  # 色调调整因子
        contrast_factor = random.uniform(0.7, 1.3)  # 对比度调整因子
        image_enhancer = ImageEnhance.Brightness(image)
        image = image_enhancer.enhance(brightness_factor)
        image_enhancer = ImageEnhance.Color(image)
        image = image_enhancer.enhance(color_factor)
        image_enhancer = ImageEnhance.Contrast(image)
        image = image_enhancer.enhance(contrast_factor)

    # 将处理后的图像转换为Base64编码的字符串
    output_buffer = io.BytesIO()
    image.save(output_buffer, format='JPEG')
    output_data = output_buffer.getvalue()
    base64_str = base64.b64encode(output_data).decode('utf-8')
    return base64.b64decode(base64_str)
