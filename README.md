# Biology Bilingual Website (Flask)

A compact, bilingual (English + Kurdish/Sorani) biology website that reuses your uploaded **Biology guide** template.  
- Framework: Flask (Python)
- Bilingual routing: `/en/...` and `/ckb/...`
- Pages: Home, Chapters, Full Guide (your uploaded HTML with language-aware tweaks)
- Styling: minimal Tailwind-like aesthetic via custom CSS.

## Run locally
```bash
pip install flask
python app.py
```
Open: http://localhost:5000/ (redirects to `/en`)

## Project structure
```
bio_site/
├─ app.py
├─ templates/
│  ├─ base.html
│  ├─ index.html
│  ├─ chapters.html
│  └─ guide.html   # based on your uploaded Biology guide
└─ static/
   ├─ css/site.css
   ├─ js/site.js
   └─ images/
```

> Tip: Put histology/embryology images into `static/images` and reference them where needed.
