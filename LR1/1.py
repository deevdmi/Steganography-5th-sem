import docx
import MTK2
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_COLOR_INDEX


doc = docx.Document('variant07.docx')


def run_get_spacing(run):
    rPr = run._r.get_or_add_rPr()
    spacings = rPr.xpath("./w:spacing")
    return spacings


def run_get_scale(run):
    rPr = run._r.get_or_add_rPr()
    scale = rPr.xpath("./w:w")
    return scale


def main():
    kod = ''
    for paragraph in doc.paragraphs:
        for run in paragraph.runs:
            font_color = run.font.color.rgb
            font_size = run.font.size
            font_highlight_color = run.font.highlight_color
            font_scale = run_get_scale(run)
            font_spacing = run_get_spacing(run)

            if (font_color != RGBColor(0, 0, 0) or
                    font_size.pt != 12.0 or
                    font_highlight_color != WD_COLOR_INDEX.WHITE or
                    font_spacing or font_scale):
                for i in range(len(run.text)):
                    kod += '1'
            else:
                for i in range(len(run.text)):
                    kod += '0'


    kod += "000"
    print(f'Посл-ть 0 и 1: {kod}')
    print(f'Длина посл-ти: {len(kod)}')
    print('MTK2:')

    normaltext = MTK2.MTK2_decode(kod)
    print(normaltext)
    normaltext = bytes.fromhex(hex(int(kod, 2))[2:]).decode(encoding="koi8_r")
    print(normaltext)
    normaltext = bytes.fromhex(hex(int(kod, 2))[2:]).decode(encoding="cp866")
    print(normaltext)
    normaltext = bytes.fromhex(hex(int(kod, 2))[2:]).decode(encoding="cp1251")
    print(normaltext)


if __name__ == '__main__':
    main()























