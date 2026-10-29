from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
W, H = 1280, 720


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def gradient() -> Image.Image:
    img = Image.new("RGB", (W, H), "#101218")
    px = img.load()
    for y in range(H):
        for x in range(W):
            r = int(12 + 16 * x / W + 16 * y / H)
            g = int(18 + 34 * x / W)
            b = int(28 + 80 * y / H)
            px[x, y] = (r, g, b)
    return img


def rounded(draw: ImageDraw.ImageDraw, xy, radius, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def title(draw, text, subtitle):
    draw.text((70, 56), text, fill="#f8fafc", font=font(56, True))
    draw.text((74, 128), subtitle, fill="#9fb2ca", font=font(25))


def save_intro():
    img = gradient()
    d = ImageDraw.Draw(img)
    title(d, "DESIGN SERVER: ACCESS LOCKED", "Командный квест для IT-аудитории")
    for i, label in enumerate(["PIXEL", "BINARY", "GRID", "FINAL"]):
        x = 100 + i * 285
        rounded(d, (x, 260, x + 210, 455), 18, "#171d27", "#2d3b50", 2)
        d.text((x + 38, 300), f"0{i + 1}", fill="#55d6be", font=font(36, True))
        d.text((x + 34, 360), label, fill="#f8fafc", font=font(30, True))
    d.line((110, 570, 1170, 570), fill="#55d6be", width=3)
    d.text((110, 598), "Соберите ключ. Последний символ приведет к цифре в аудитории.", fill="#d7e1ee", font=font(26))
    img.save(ASSETS / "intro.png")


def save_pixel():
    img = gradient()
    d = ImageDraw.Draw(img)
    title(d, "01 / PIXEL MAP", "Узнайте две английские буквы по светлым пикселям.")
    grid = [
        "#...#.#...#",
        "#...#.#...#",
        "#...#..#.#.",
        "#...#...#..",
        "#...#..#.#.",
        "#...#.#...#",
        ".###..#...#",
    ]
    cell, ox, oy = 54, 340, 210
    for y, row in enumerate(grid):
        for x, ch in enumerate(row):
            fill = "#55d6be" if ch == "#" else "#1c2430"
            rounded(d, (ox + x * cell, oy + y * cell, ox + x * cell + 42, oy + y * cell + 42), 8, fill)
    d.text((340, 625), "Выберите ответ: UX / UI / IT", fill="#dbeafe", font=font(30, True))
    img.save(ASSETS / "stage_1_pixel.png")


def save_binary():
    img = gradient()
    d = ImageDraw.Draw(img)
    title(d, "02 / BINARY COLOR", "Переведите двоичный цвет в слово.")
    code = "01001111 01001110 01000101"
    d.text((155, 260), code, fill="#f8fafc", font=font(54, True))
    for i, color in enumerate(["#ff4d6d", "#55d6be", "#f7d154"]):
        rounded(d, (210 + i * 300, 420, 420 + i * 300, 535), 14, color)
    d.text((210, 595), "Подсказка внутри IT: 8 бит = 1 символ ASCII.", fill="#dbeafe", font=font(28))
    img.save(ASSETS / "stage_2_binary.png")


def save_grid():
    img = gradient()
    d = ImageDraw.Draw(img)
    title(d, "03 / INTERFACE GRID", "Кнопка спрятана в координате: ряд F, колонка 1.")
    letters = ["A", "B", "C", "D", "E", "F"]
    ox, oy, cell = 360, 170, 86
    for y in range(6):
        d.text((ox - 65, oy + y * cell + 24), letters[y], fill="#9fb2ca", font=font(28, True))
        for x in range(6):
            fill = "#1c2430"
            if y == 5 and x == 0:
                fill = "#55d6be"
            rounded(d, (ox + x * cell, oy + y * cell, ox + x * cell + 64, oy + y * cell + 64), 10, fill, "#2d3b50")
            if y == 0:
                d.text((ox + x * cell + 20, oy - 48), str(x + 1), fill="#9fb2ca", font=font(28, True))
    d.text((250, 645), "Ответ отправьте как координату кнопки, без пробелов.", fill="#dbeafe", font=font(27))
    img.save(ASSETS / "stage_3_grid.png")


def save_final():
    img = gradient()
    d = ImageDraw.Draw(img)
    title(d, "04 / FINAL KEY", "UX + ONE + F1 = найдите общий хвост.")
    d.text((160, 255), "UX", fill="#55d6be", font=font(78, True))
    d.text((395, 255), "ONE", fill="#f7d154", font=font(78, True))
    d.text((725, 255), "F1", fill="#ff4d6d", font=font(78, True))
    d.line((140, 390, 1110, 390), fill="#2d3b50", width=4)
    d.text((155, 455), "В финале нужна не буква, а цифра. Она уже видна в последнем фрагменте.", fill="#f8fafc", font=font(34, True))
    img.save(ASSETS / "stage_4_final.png")


def main():
    ASSETS.mkdir(exist_ok=True)
    save_logic_cards()
    print(f"Generated assets in {ASSETS}")


def save_logic_cards():
    from quest import QUEST
    cards = [("intro.png", "КОМНАТА ЛОГИКИ", "11 заданий для вашей команды", ["ВНИМАНИЕ", "ЗАКОНОМЕРНОСТИ", "ЛОГИКА", "ФИНАЛЬНАЯ ЦИФРА"])]
    cards.extend((item["image"], f"{index + 1:02d} / {item['title'].upper()}",
                  f"Задание {index + 1} из {len(QUEST)}", item["lines"])
                 for index, item in QUEST.items())
    old_cards = [
        ("intro.png", "КОМНАТА ЛОГИКИ", "Четыре испытания. Один ключ.", ["01   Закономерность", "02   Очередь", "03   Правда и ложь", "04   Финальный замок"]),
        ("stage_1_pixel.png", "01 / СЛОМАННЫЙ РЯД", "Найдите пропущенное число", ["2     3     5     ?     12     17", "Первый шаг: +1. Следующий: +2.", "Каждый шаг на один больше."]),
        ("stage_2_binary.png", "02 / ОЧЕРЕДЬ", "Четыре человека. Четыре места.", ["АНЯ     БОРЯ     ВИКА     ГЛЕБ", "Боря сразу за Аней.", "Между Аней и Глебом два человека.", "Вика перед Глебом. Где стоит Вика?"]),
        ("stage_3_grid.png", "03 / ТРИ ЯЩИКА", "Только одна надпись правдива", ["КРАСНЫЙ: ключ здесь", "СИНИЙ: ключ не здесь", "ЗЕЛЁНЫЙ: ключ не в красном", "В каком ящике спрятан ключ?"]),
        ("stage_4_final.png", "04 / ФИНАЛЬНЫЙ ЗАМОК", "Все фрагменты собраны", ["8          3          4", "ПЕРВЫЙ − ВТОРОЙ − ТРЕТИЙ", "Введите цифру, которая откроет дверь."]),
    ]
    for filename, heading, subtitle, lines in cards:
        img = gradient()
        d = ImageDraw.Draw(img)
        title(d, heading, subtitle)
        colors = ["#55d6be", "#f7d154", "#ff8195", "#f8fafc"]
        for i, line in enumerate(lines):
            size = 42 if i == 0 else 32
            face = font(size, True)
            while d.textbbox((0, 0), line, font=face)[2] > W - 160:
                size -= 1
                face = font(size, True)
            d.text((80, 235 + i * 85), line, fill=colors[i], font=face)
        d.line((80, 630, 1200, 630), fill="#55d6be", width=3)
        d.text((80, 650), "КОМАНДНЫЙ КВЕСТ / IT + DESIGN", fill="#9fb2ca", font=font(22))
        img.save(ASSETS / filename)


if __name__ == "__main__":
    main()
