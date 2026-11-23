"""Ilustrações em retícula do Contraplano (duas tintas: a cor do texto + vermelho).

Uso: python3 tools/halftone.py CENA COR saida.svg
CENA: fjord | piano     COR: rosa | azul | amarelo | menta | laranja | lilas
"""
import math
import sys

INKS = {"rosa": "#ee5fae", "azul": "#2f6fd6", "amarelo": "#efb000", "menta": "#12a36b", "laranja": "#ff6a2b", "lilas": "#9467d6"}
RED = "#e4252f"
W = H = 600


def lighten(hexcolor, k):
    r, g, b = (int(hexcolor[i:i + 2], 16) for i in (1, 3, 5))
    return "#%02x%02x%02x" % tuple(round(c + (255 - c) * k) for c in (r, g, b))


def poly(x, y, pts):
    inside, j = False, len(pts) - 1
    for i in range(len(pts)):
        xi, yi = pts[i]; xj, yj = pts[j]
        if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def rect(x, y, x0, y0, x1, y1): return x0 <= x <= x1 and y0 <= y <= y1
def circ(x, y, cx, cy, r): return math.hypot(x - cx, y - cy) <= r


def heart_F(x, y, cx, cy, s):
    u = (x - cx) / s; v = -(y - cy) / s + 0.25
    return (u * u + v * v - 1) ** 3 - u * u * v ** 3


def heart_path(cx, cy, s):
    return (f"M{cx:.1f},{cy + 0.95*s:.1f} C{cx - 1.35*s:.1f},{cy + 0.05*s:.1f} {cx - 1.05*s:.1f},{cy - 1.05*s:.1f} {cx:.1f},{cy - 0.45*s:.1f} "
            f"C{cx + 1.05*s:.1f},{cy - 1.05*s:.1f} {cx + 1.35*s:.1f},{cy + 0.05*s:.1f} {cx:.1f},{cy + 0.95*s:.1f}Z")


# ---------- cenas ----------
class Fjord:
    label = "Ilustração em retícula de montanhas sobre um fiorde, com uma casinha vermelha de janela em forma de coração"
    M1 = [(-20, 400), (190, 110), (390, 400)]
    M2 = [(200, 400), (420, 160), (640, 400)]
    HOUSE = [(452, 352), (500, 318), (548, 352), (548, 398), (452, 398)]
    HEARTS = [(500, 372, 9)]

    def mountain(self, x, y): return poly(x, y, self.M1) or poly(x, y, self.M2)

    def inside(self, x, y):
        return self.mountain(x, y) or (y >= 405 and y <= 590 and 0 <= x <= 600) or circ(x, y, 470, 95, 48) or poly(x, y, self.HOUSE)

    def ink(self, x, y):
        if poly(x, y, self.HOUSE) or circ(x, y, 470, 95, 48): return 0
        if y >= 405:  # água: listras de reflexo
            band = 0.5 + 0.5 * math.sin(y * 0.42)
            refl = 0.42 if self.mountain(x, 805 - y) else 0.1
            return (refl * (0.35 + 0.65 * band)) * (1 - (y - 405) / 230)
        snow = 0.0
        for (px, py), base in ((self.M1[1], 0), (self.M2[1], 0)):
            if y < py + 70 and abs(x - px) < (y - py) * 0.75 + 6: snow = 1
        d = 0.25 + 0.55 * (y - 110) / 290
        if x < 190 and poly(x, y, self.M1) and not poly(x, y, self.M2): d += 0.12  # encosta à sombra
        return d * (0.35 if snow else 1)

    def red(self, x, y):
        if poly(x, y, self.HOUSE): return 0.95
        if circ(x, y, 470, 95, 48): return 0.18 + 0.5 * (math.hypot(x - 470, y - 95) / 48) ** 2
        if 405 <= y <= 412: return 0.5
        if y > 405 and poly(x, y - 2 * (y - 405) + 0, self.HOUSE): return 0.45  # reflexo da casa
        return 0.0


class Piano:
    label = "Ilustração em retícula de um piano de cauda com a tampa aberta e um coração recortado nela"
    LID = [(150, 252), (440, 100), (520, 252)]
    HEARTS = [(398, 192, 18)]

    def inside(self, x, y):
        return (poly(x, y, self.LID) or rect(x, y, 100, 252, 500, 332) or circ(x, y, 492, 292, 40)
                or rect(x, y, 58, 262, 132, 300) or rect(x, y, 122, 332, 142, 455) or rect(x, y, 466, 332, 486, 455)
                or rect(x, y, 298, 332, 316, 440) or rect(x, y, 284, 440, 330, 468)
                or rect(x, y, 12, 384, 92, 398) or rect(x, y, 18, 398, 28, 470) or rect(x, y, 76, 398, 86, 470)
                or (abs(y - 486) < 16 and abs(x - 300) < 250 and ((x - 300) / 250) ** 2 + ((y - 486) / 16) ** 2 <= 1))

    def ink(self, x, y):
        if abs(y - 486) < 16 and not rect(x, y, 18, 398, 86, 470): return 0.0
        if rect(x, y, 58, 262, 132, 300): return 0.0
        if poly(x, y, self.LID): return 0.30 + 0.45 * (y - 100) / 152
        return 0.55 + 0.3 * (y - 252) / 220

    def red(self, x, y):
        if abs(y - 486) < 16 and abs(x - 300) < 250: return 0.35 * (1 - abs(x - 300) / 250)
        if rect(x, y, 58, 262, 132, 300): return 0.9 if int((x - 58) / 7) % 2 == 0 else 0.0  # teclas
        if abs((x - 400) - (y - 252) * (30 / -112)) < 3 and 140 <= y <= 252: return 0.9  # haste da tampa
        if rect(x, y, 100, 252, 500, 262): return 0.55
        return 0.0


SCENES = {"fjord": Fjord, "piano": Piano}


def edge(scene, x, y, rad=10):
    out = sum(1 for k in range(12) if not scene.inside(x + rad * math.cos(k * math.pi / 6), y + rad * math.sin(k * math.pi / 6)))
    return out / 12


def grid(spacing, angle):
    ca, sa = math.cos(angle), math.sin(angle)
    n = int(W * 1.6 / spacing)
    for i in range(-n, n):
        for j in range(-n, n):
            u, v = i * spacing, j * spacing
            x = W / 2 + u * ca - v * sa; y = H / 2 + u * sa + v * ca
            if 0 <= x <= W and 0 <= y <= H: yield x, y


def in_heart(scene, x, y): return any(heart_F(x, y, cx, cy, s) <= 0 for cx, cy, s in scene.HEARTS)


def glow(scene, x, y):
    g = 0
    for cx, cy, s in scene.HEARTS:
        F = heart_F(x, y, cx, cy, s)
        if F > 0: g = max(g, math.exp(-F * 2.5))
    return g


def dots(scene, spacing, angle, fn):
    out = []
    for x, y in grid(spacing, angle):
        if not scene.inside(x, y) or in_heart(scene, x, y): continue
        d = max(0.0, min(1.0, fn(x, y)))
        r = spacing / 2 * math.sqrt(d) * 1.08
        if r >= 0.55: out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}"/>')
    return out


def main(name, cor, path):
    scene = SCENES[name]()
    ink = INKS[cor]
    a = dots(scene, 7.5, math.radians(15), lambda x, y: scene.ink(x, y) + 0.3 * edge(scene, x, y) * (scene.ink(x, y) > 0))
    b = dots(scene, 7.5, math.radians(45), lambda x, y: scene.red(x, y) + 0.9 * glow(scene, x, y))
    hearts = "".join(heart_path(cx, cy + 2, s * 0.95) for cx, cy, s in scene.HEARTS)
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{scene.label}">
<defs><filter id="g-{name}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
<linearGradient id="k-{name}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{lighten(ink, .35)}"/><stop offset="1" stop-color="{ink}"/></linearGradient></defs>
<g fill="url(#k-{name})" style="mix-blend-mode:multiply">{"".join(a)}</g>
<g fill="{RED}" style="mix-blend-mode:multiply" transform="translate(2 1.5)">{"".join(b)}</g>
<path d="{hearts}" fill="{RED}" opacity=".7" filter="url(#g-{name})"/>
<path d="{hearts}" fill="#fff"/>
</svg>'''
    open(path, "w").write(svg)
    print(name, len(a), len(b), len(svg))


if __name__ == "__main__":
    main(*sys.argv[1:4])
