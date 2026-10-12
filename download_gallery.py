import urllib.request
import urllib.parse
import re
import os

page_url = "https://lechvizit.com.ua/%D0%A4%D0%BE%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B-%D0%BD%D0%B0%D1%80%D0%BA%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B3%D0%BE-%D0%A6%D0%B5%D0%BD%D1%82%D1%80%D0%B0-%D0%9C-Visit/foto-narkologicheskogo-centra-m-visit.html"
headers = {"User-Agent": "Mozilla/5.0"}
req = urllib.request.Request(page_url, headers=headers)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
except Exception as e:
    print(f"Error fetching page: {e}")
    html = ""

# Шукаємо всі посилання на картинки
raw_imgs = re.findall(r'src=["\']([^"\']*images/stories/[^"\']+)["\']', html)
print(f"Знайдено картинок у галереї: {len(raw_imgs)}")

target_names = [
    "gallery-vhod.jpg",
    "gallery-resepshn.jpg",
    "doktor-tarasov-portret.jpg",
    "licenziya-moz.png",
    "kabinet-lazeroterapii.jpg",
    "kabinet-konsultacii.jpg",
    "doktor-tarasov-priyom.jpg",
    "lazer-apparat.jpg"
]

os.makedirs("images", exist_ok=True)

for idx, src in enumerate(raw_imgs):
    encoded_path = urllib.parse.quote(src, safe=":/%")
    full_url = urllib.parse.urljoin("https://lechvizit.com.ua/", encoded_path)
    save_as = target_names[idx] if idx < len(target_names) else f"gallery-extra-{idx}.jpg"
    out_path = os.path.join("images", save_as)
    
    try:
        img_req = urllib.request.Request(full_url, headers=headers)
        with urllib.request.urlopen(img_req, timeout=10) as img_resp:
            data = img_resp.read()
            with open(out_path, "wb") as f:
                f.write(data)
            print(f"OK ({len(data)} bytes): {out_path} <- {src}")
    except Exception as e:
        print(f"ERR: {full_url} -> {e}")
