from PIL import ImageFont, ImageDraw, Image

from conf import Conf
from model.symbol import Symbol


class EGSymImg:
    def __init__(self, sym: Symbol):
        self.sym = sym
        self.img = None


    def define_img(self):

        side_font = ImageFont.truetype(f'{Conf.project_path}/fonts/JetBrainsMonoNerdFont-Regular.ttf', 70)
        sym_font = ImageFont.truetype(f'{Conf.project_path}/fonts/gost_type_B.ttf', 1000)
        gap = 30

        # Считаем размеры текста
        upper_box_w, upper_box_h = cnt_textbox_sizes(f"{self.sym.get_width()} мм", side_font)
        sym_box_w, sym_box_h = cnt_textbox_sizes(self.sym.sym, sym_font)
        side_box_w, side_box_h = cnt_textbox_sizes(f"{self.sym.get_height()} мм", side_font)
        side_box_rotated_w, side_box_rotated_h = side_box_h, side_box_w

        # Считаем размеры нашего изображения
        width, height = max(sym_box_w, upper_box_w) + side_box_rotated_w, max(sym_box_h + upper_box_h + gap, side_box_rotated_h)

        # Рисуем изображения
        side_img = Image.new("1", (int(width), int(side_box_h + gap)), 1) # side_img имеет ширину не side_box_w, а width, так как иначе оно не будет центрироваться в исходном изображении
        # Рисуем боковую надпись
        side_img_draw = ImageDraw.Draw(side_img)
        side_img_draw.text((width // 2, gap // 2), f"{self.sym.get_height()} мм", fill=0, font=side_font, anchor='mt')
        side_img = side_img.rotate(90, expand=True)

        res_img = Image.new("1", (int(width), int(height)), 1)

        if self.sym.get_height(): # если ненулевая высота, то выводим боковую надпись на картинку
            res_img.paste(side_img, (0, 0))

        draw = ImageDraw.Draw(res_img)

        draw.text((width // 2,  gap // 2), f"{self.sym.get_width()} мм", fill=0, font=side_font, anchor='mt')
        draw.text((side_box_rotated_w, gap + upper_box_h), str(self.sym.sym), fill=0, font=sym_font, anchor='lt')

        self.img = res_img


def cnt_textbox_sizes(text, font: ImageFont) -> tuple[float, float]:
    tmp_img = Image.new("1", (1, 1))
    draw = ImageDraw.Draw(tmp_img)

    textbox = draw.textbbox((0, 0), text, font)
    return textbox[2] - textbox[0], textbox[3] - textbox[1]