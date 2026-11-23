"""Gera as imagens de prévia (1200x630) que aparecem quando um link do blog é compartilhado.

Uso: python3 tools/compartilhar.py   (lê _posts/ e _config.yml, grava em assets/compartilhar/)
Precisa do Playwright com um Chrome disponível.
"""
import html
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

RAIZ = pathlib.Path(__file__).resolve().parent.parent
SAIDA = RAIZ / "assets" / "compartilhar"
CHROME = sys.argv[1] if len(sys.argv) > 1 else "/usr/bin/google-chrome"
GRAO = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='240'%3E%3Cfilter id='n'%3E"
        "%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='3' stitchTiles='stitch'/%3E%3CfeColorMatrix "
        "values='0 0 0 0 .42 0 0 0 0 .36 0 0 0 0 .3 0 0 0 .1 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E")


def campo(texto, nome):
    m = re.search(rf'^{nome}:\s*"?(.*?)"?\s*$', texto, re.M)
    return m.group(1) if m else ""


def cartao(esquerda, imagem, larg_img):
    return f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Shippori+Mincho:wght@500;600&family=Poppins:wght@500;700&display=swap">
<style>
body{{margin:0;width:1200px;height:630px;background:#f2eee8 url("{GRAO}");color:#e4252f;font-family:Poppins,sans-serif;overflow:hidden}}
.c{{position:relative;height:630px;padding:56px 64px;box-sizing:border-box;display:flex;flex-direction:column;justify-content:space-between}}
.k{{font:500 24px Poppins}} .f{{font:600 120px/1 'Shippori Mincho';margin:10px 0 0;max-width:720px}}
.f.long{{font-size:84px}} .t{{text-wrap:balance;font:500 40px/1.2 'Shippori Mincho';max-width:640px;margin-top:22px}}
.m b{{display:block;font:700 46px/1 Poppins}} .m span{{font:500 22px Poppins}}
.dots{{position:absolute;left:64px;right:64px;bottom:150px;height:6px;background:radial-gradient(circle at 3px 3px,#e4252f 1.6px,transparent 2.1px) 0 0/9px 6px repeat-x}}
img{{position:absolute;right:40px;top:40px;width:{larg_img}px;mix-blend-mode:multiply}}
</style></head><body><div class="c"><img src="{imagem}"><div>{esquerda}</div>
<div class="m"><span>Críticas &amp; resenhas · contraplanoblog.github.io</span><b>CONTRAPLANO</b></div><div class="dots"></div></div></body></html>"""


def main():
    SAIDA.mkdir(parents=True, exist_ok=True)
    config = (RAIZ / "_config.yml").read_text()
    trabalhos = [("contraplano", cartao(f'<div class="t" style="font-size:54px;max-width:700px;margin:0">{html.escape(campo(config, "tagline"))}</div>',
                                         (RAIZ / "assets/camera.svg").as_uri(), 420))]
    for post in sorted((RAIZ / "_posts").glob("*.md")):
        texto = post.read_text()
        slug = post.stem[11:]
        ilus = campo(texto, "ilustracao")
        imagem = (RAIZ / ilus.lstrip("/")).as_uri() if ilus else (RAIZ / "assets/camera.svg").as_uri()
        filme = html.escape(campo(texto, "filme"))
        esquerda = (f'<div class="k">Crítica · {html.escape(campo(texto, "ano"))}</div>'
                    f'<div class="f{" long" if len(filme) > 10 else ""}">{filme}</div>'
                    f'<div class="t">{html.escape(campo(texto, "title"))}</div>')
        trabalhos.append((slug, cartao(esquerda, imagem, 470)))

    with sync_playwright() as p:
        navegador = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--allow-file-access-from-files"])
        pagina = navegador.new_page(viewport={"width": 1200, "height": 630})
        for nome, doc in trabalhos:
            arquivo = SAIDA / f"_tmp_{nome}.html"
            arquivo.write_text(doc)
            pagina.goto(arquivo.as_uri())
            pagina.wait_for_timeout(1500)
            pagina.screenshot(path=str(SAIDA / f"{nome}.png"))
            arquivo.unlink()
            print("ok", nome)
        navegador.close()


if __name__ == "__main__":
    main()
