from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "data" / "images"
IMG.mkdir(parents=True, exist_ok=True)

def gen_png(path: Path, text: str, size=(512, 320)):
    im = Image.new("RGB", size, "white")
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 28)
    except Exception:
        font = ImageFont.load_default()
    tw, th = d.textbbox((0,0), text, font=font)[2:]
    d.rectangle((10, 10, size[0]-10, size[1]-10), outline="black", width=2)
    d.text(((size[0]-tw)//2, (size[1]-th)//2), text, fill="black", font=font)
    im.save(path)

if __name__ == "__main__":
    gen_png(IMG / "product.png", "Sample Product")
    gen_png(IMG / "logo.png", "Logo")
    print("Immagini generate in:", IMG)
