class Symbol:

    # Размеры идут в списке для шрифтов в таком порядке: 1.8, 2.5, 3.5, 5, 7, 10, 14, 20,
    # то есть font_sizes['023456789'][1] будет шириной для цифр 023456789 в шрифте 2.5
    font_sizes = {
        'size': [1.8, 2.5, 3.5, 5, 7, 10, 14, 20],
        'lowercase_height': [1.3, 1.8, 2.5, 3.5, 5, 7, 10, 14],
        'ГЕЗС': [0.9, 1.25, 1.75, 2.5, 3.5, 5, 7, 10],
        'БВИЙКЛНОПРТУЦЧЬЯ': [1.1, 1.5, 2.1, 3, 4.2, 6, 8.4, 12],
        'АДМХЫЮ': [1.3, 1.8, 2.5, 3.5, 5, 7, 10, 14],
        'ЖФЩШЪ': [1.4, 2, 2.8, 4, 5.6, 8, 12, 16],
        '1': [0.5, 0.75, 1, 1.5, 2, 3, 4.2, 6],
        '023456789': [0.9, 1.25, 1.75, 2.5, 3.5, 5, 7, 10],
        ' ': [1.1, 1.5, 2.1, 3, 4.2, 6, 8.4, 12],
        'gap': [0.35, 0.5, 0.7, 1, 1.4, 2, 2.8, 4],
        'с': [0.8, 1, 1.4, 2, 2.8, 4, 5.6, 8],
        'абвгдеийклнопрухцчьэя': [0.9, 1.25, 1.75, 2.5, 3.5, 5, 7, 10],
        'мъыю': [1.1, 1.5, 2.1, 3, 4.2, 6, 8.4, 12],
        'жтфшщ': [1.3, 1.8, 2.5, 3.5, 5, 7, 10, 14]
    }

    def __init__(self, sym: str, size: float):
        # Проверка входных дынных
        if size not in self.font_sizes['size']:
            raise ValueError(f'Size {size} not exists in font sizes table')
        if all(sym not in key for key in self.font_sizes.keys()):
            raise ValueError(f'Sym {sym} not exists in font sizes table')

        self.size = size
        self.sym = sym
        self.index = self.font_sizes['size'].index(size) # индекс символа в списке размеров


    def get_width(self):
        for key in self.font_sizes.keys():
            if self.sym in key:
                return self.font_sizes[key][self.index]

    def get_height(self):
        if self.sym == ' ':
            return 0 # нулевая высота у пробела
        if 48 <= ord(self.sym) <= 57 or 1040 <= ord(self.sym) <= 1071: # заглавные буквыы и цифры
            return self.font_sizes['size'][self.index]
        else:
            return self.font_sizes['lowercase_height'][self.index]

    def get_gap(self):
        return self.font_sizes['gap'][self.index]