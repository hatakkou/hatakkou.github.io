# reference.pdf から図の領域を PNG として抜き出すスクリプト
# 使い方: python -X utf8 extract_figures.py  (images/ に fig01..fig19.png を出力)
import os
import pymupdf

PDF = "reference.pdf"
OUT = "images"
ZOOM = 3.0  # 216 dpi 相当

# (図番号, ページindex, x0, y0, x1, y1)  PDF上のpt座標
FIGURES = [
    ("fig01", 3, 135, 444, 470, 780),
    ("fig02", 4, 342, 88, 568, 241),
    ("fig03", 4, 344, 262, 560, 437),
    ("fig04", 4, 48, 526, 341, 742),
    ("fig05", 4, 340, 560, 551, 742),
    ("fig06", 6, 124, 138, 461, 357),
    ("fig07", 6, 52, 562, 544, 746),
    ("fig08", 7, 44, 383, 552, 643),
    ("fig09", 8, 368, 52, 573, 402),
    ("fig10", 8, 302, 450, 544, 604),
    ("fig11", 10, 75, 103, 520, 283),
    ("fig12", 11, 110, 100, 486, 370),
    ("fig13", 12, 46, 493, 542, 663),
    ("fig14", 13, 330, 352, 562, 571),
    ("fig15", 14, 311, 98, 575, 266),
    ("fig16", 15, 60, 448, 526, 640),
    ("fig17", 16, 61, 136, 544, 277),
    ("fig18", 17, 315, 406, 541, 610),
    ("fig19", 18, 86, 548, 470, 718),
]

# 画像に写り込む図内キャプション等を白で消す領域 (図番号 -> [(x0,y0,x1,y1), ...])
WHITEOUT = {
    "fig01": [(225, 763, 373, 779)],
    "fig09": [(342, 368, 575, 403)],
    "fig16": [(166, 614, 423, 631)],
    "fig17": [(339, 250, 516, 267)],
}

CAPTIONS = {
    "fig01": "図1", "fig02": "図2", "fig03": "図3", "fig04": "図4", "fig05": "図5",
    "fig06": "図6", "fig07": "図7", "fig08": "図8", "fig09": "図9", "fig10": "図10",
    "fig11": "図11", "fig12": "図12", "fig13": "図13", "fig14": "図14", "fig15": "図15",
    "fig16": "図16", "fig17": "図17", "fig18": "図18", "fig19": "図19",
}


def main():
    doc = pymupdf.open(PDF)
    os.makedirs(OUT, exist_ok=True)
    mat = pymupdf.Matrix(ZOOM, ZOOM)
    for name, pno, x0, y0, x1, y1 in FIGURES:
        page = doc[pno]
        for wx0, wy0, wx1, wy1 in WHITEOUT.get(name, []):
            page.draw_rect(pymupdf.Rect(wx0, wy0, wx1, wy1), color=None, fill=(1, 1, 1))
        clip = pymupdf.Rect(x0, y0, x1, y1)
        pix = page.get_pixmap(matrix=mat, clip=clip, alpha=False)
        path = os.path.join(OUT, f"{name}.png")
        pix.save(path)
        print(f"{path}  {pix.width}x{pix.height}")


if __name__ == "__main__":
    main()
