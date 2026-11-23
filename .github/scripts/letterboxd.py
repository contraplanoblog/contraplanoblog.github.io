"""Busca o diário recente do Letterboxd (RSS público) e salva em _data/letterboxd.json.

Uso: python3 .github/scripts/letterboxd.py USUARIO _data/letterboxd.json
Se a busca falhar, o arquivo existente fica como está.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET

MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
NS = {"lb": "https://letterboxd.com"}
LIMITE = 8


def estrelas(nota):
    cheias = int(nota)
    meia = nota - cheias >= 0.5
    return "★" * cheias + ("½" if meia else "")


def main(usuario, destino):
    url = f"https://letterboxd.com/{usuario}/rss/"
    pedido = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (contraplano blog)"})
    with urllib.request.urlopen(pedido, timeout=30) as resposta:
        raiz = ET.fromstring(resposta.read())

    filmes = []
    for item in raiz.iter("item"):
        titulo = item.findtext("lb:filmTitle", namespaces=NS)
        if not titulo:  # listas e outros itens que não são filmes
            continue
        nota_txt = item.findtext("lb:memberRating", namespaces=NS)
        nota = float(nota_txt) if nota_txt else None
        data = item.findtext("lb:watchedDate", namespaces=NS) or ""
        data_curta = ""
        if len(data) == 10:
            ano, mes, dia = data.split("-")
            data_curta = f"{int(dia)} {MESES[int(mes) - 1]}"
        filmes.append({
            "titulo": titulo,
            "ano": item.findtext("lb:filmYear", namespaces=NS) or "",
            "nota": nota,
            "estrelas": estrelas(nota) if nota else "",
            "curtiu": (item.findtext("lb:memberLike", namespaces=NS) or "").lower() == "yes",
            "revisto": (item.findtext("lb:rewatch", namespaces=NS) or "").lower() == "yes",
            "data": data,
            "data_curta": data_curta,
            "link": item.findtext("link") or f"https://letterboxd.com/{usuario}/",
        })
        if len(filmes) >= LIMITE:
            break

    with open(destino, "w", encoding="utf-8") as arquivo:
        json.dump(filmes, arquivo, ensure_ascii=False, indent=2)
    print(f"{len(filmes)} filmes salvos em {destino}")


if __name__ == "__main__":
    try:
        main(sys.argv[1], sys.argv[2])
    except Exception as erro:  # não derruba a montagem do site
        print(f"Não foi possível atualizar o Letterboxd: {erro}")
