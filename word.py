from math import ceil

from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

from Symbol import Symbol


class EGWord:
    def __init__(self, word: str, font_size: float):
        self.syms = [Symbol(sym, font_size) for sym in word] # кривая проверка входных данных
        self.word = word
        self.size = font_size
        self.gap = None

    def get_widths(self):
        word1 = self.word + '@'
        res = []
        for i in range(len(self.word)):
            sym = Symbol(word1[i], self.size)
            res.append((sym.get_width(), sym.get_height()))
            if word1[i + 1] != ' ':
                res.append((sym.get_gap(), 0))
        return res


    def get_binary_img(self):
        # определяем, есть ли буквы с "хвостиками": руцщфд, некоторые их элементы должны располагаться ниже основного текста
        img_ratio = max(sym.ratio for sym in self.syms)

        side_font = ImageFont.truetype('fonts/JetBrainsMonoNerdFont-Regular.ttf', 70)
        sym_font = ImageFont.truetype('fonts/gost_type_B.ttf', 1000)
        usual_small_letter_h = cnt_textbox_sizes('г', sym_font)[1]

        eg_imgs = [EGSymImg(Symbol(sym, self.size)) for sym in self.word]
        for img in eg_imgs:
            img.define_img()

        gapsize_text = f"{self.syms[0].get_gap()} мм"
        gapsize_text_w, gapsize_text_h = cnt_textbox_sizes(gapsize_text, side_font)

        # Считаем высоту с учетом того, что некоторые буквы выше (р, у, Д итп) и их нужно опустить, для этого к высоте прибавляем ratio_gap
        width, height = sum(map(lambda x: x.img.width, eg_imgs)), max(map(lambda x: x.img.height if x.sym.sym not in 'руцщДЦЩ' else usual_small_letter_h, eg_imgs)) + gapsize_text_h # если у буквы есть "хвост", то ее не берем в расчет высоты, она будет наравне со всеми остальными буквами
        ratio_gap = ceil(usual_small_letter_h * img_ratio)
        height += ratio_gap

        res_img = Image.new("1", (width, height), 1)

        gaptext_draw = ImageDraw.Draw(res_img)
        x_input_pos = 0
        for img in eg_imgs:
            if img.sym.ratio:
                res_img.paste(img.img, (x_input_pos, height - (img.img.height + (ratio_gap - ceil(usual_small_letter_h * img.sym.ratio)) + gapsize_text_h)))
            else:
                res_img.paste(img.img, (x_input_pos, height - (img.img.height + ratio_gap + gapsize_text_h)))
            if x_input_pos:
                gaptext_draw.text((x_input_pos - ceil(gapsize_text_w / 2), height), gapsize_text, fill=0, font=side_font, anchor='ms')
            x_input_pos += img.img.width

        buffer = BytesIO()
        res_img.save(buffer, "PNG")
        return buffer.getvalue()


class EGSymImg:
    def __init__(self, sym: Symbol):
        self.sym = sym
        self.img = None


    def define_img(self):

        side_font = ImageFont.truetype('fonts/JetBrainsMonoNerdFont-Regular.ttf', 70)
        sym_font = ImageFont.truetype('fonts/gost_type_B.ttf', 1000)
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