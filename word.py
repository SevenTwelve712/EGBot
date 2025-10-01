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
        imgs = [EGSymImg(Symbol(sym, self.size)).get_img() for sym in self.word]

        width, height = sum(map(lambda x: x.width, imgs)), max(map(lambda x: x.height, imgs))
        res_img = Image.new("1", (width, height), 1)

        x_input_pos = 0
        for img in imgs:
            res_img.paste(img, (x_input_pos, height - img.height))
            x_input_pos += img.width

        buffer = BytesIO()
        res_img.save(buffer, "PNG")
        return buffer.getvalue()


class EGSymImg:
    def __init__(self, sym: Symbol):
        self.sym = sym
        self.img_path = f"sym_imgs/{sym.sym}.png"

    def get_img(self) -> Image:

        side_font = ImageFont.truetype('fonts/JetBrainsMonoNerdFont-Regular.ttf', 70)
        sym_font = ImageFont.truetype('fonts/gost_type_B.ttf', 1000)
        gap = 30

        # Создаем временное изображение для подсчета размеров текста
        tmp_img = Image.new("RGB", (1, 1))
        draw = ImageDraw.Draw(tmp_img)

        # Создаем textbox для подсчета размера текста
        upper_box = draw.textbbox((0, 0), f"{self.sym.size} мм", side_font)
        side_box = draw.textbbox((0, 0), f"{self.sym.size} мм", side_font)
        sym_box = draw.textbbox((0, 0), str(self.sym.sym), sym_font)

        # Считаем размеры текста
        count_box_wh = lambda box: (box[2] - box[0], box[3] - box[1])
        upper_box_w, upper_box_h = count_box_wh(upper_box)
        sym_box_w, sym_box_h = count_box_wh(sym_box)
        side_box_w, side_box_h = count_box_wh(side_box)
        side_box_rotated_w, side_box_rotated_h = side_box_h, side_box_w

        # Считаем размеры нашего изображения
        width, height = max(sym_box_w, upper_box_w) + side_box_rotated_w, max(sym_box_h + upper_box_h + gap, side_box_rotated_h)

        # Рисуем изображения
        side_img = Image.new("1", (width, side_box_h + gap), 1) # side_img имеет ширину не side_box_w, а width, так как иначе оно не будет центрироваться в исходном изображении
        side_img_draw = ImageDraw.Draw(side_img)
        side_img_draw.text((width // 2, gap // 2), f"{self.sym.get_height()} мм", fill=0, font=side_font, anchor='mt')
        side_img = side_img.rotate(90, expand=True)

        res_img = Image.new("1", (int(width), int(height)), 1)

        if self.sym.get_height():
            res_img.paste(side_img, (0, 0))

        draw = ImageDraw.Draw(res_img)

        draw.text((width // 2,  gap // 2), f"{self.sym.get_width()} мм", fill=0, font=side_font, anchor='mt')
        draw.text((side_box_rotated_w, gap + upper_box_h), str(self.sym.sym), fill=0, font=sym_font, anchor='lt')

        return res_img