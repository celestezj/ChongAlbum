#!/usr/bin/env python3
"""
Album HTML Builder
Reads album.json, generates grid + overlay HTML, and injects into template.

Usage:
    python build_album.py                          # defaults: album.json template.html index.html
    python build_album.py -j data.json -t tmpl.html -o out.html
"""

import json
import argparse
import os
import re


# ---- Deco symbols: semantic name → HTML entity ----
DECO_MAP = {
    "cross":    "&#10014;",
    "star":     "&#10032;",
    "arrow":    "&#10115;",
    "eight":    "&#10108;",
    "thirteen": "&#10153;",
}


# ---- Helpers ----

def cls(base, *modifiers):
    """Build class string: cls('box__text', 'bottom', 'right') → 'box__text box__text--bottom box__text--right'"""
    parts = [base]
    for m in modifiers:
        if m:
            parts.append(f"{base}--{m}")
    return " ".join(parts)


def title_modifiers(style_list):
    """Return title class modifiers list from style list."""
    if not style_list:
        return []
    return [s for s in style_list if s in ("straight", "bottom", "left")]


def text_modifiers(style_list):
    """Return text class modifiers from style list (positional ones)."""
    if not style_list:
        return []
    return [s for s in style_list if s in ("bottom", "topcloser", "bottomcloser", "right")]


def indent(text, level=3):
    """Indent HTML lines for pretty output."""
    pad = "  " * level
    return "\n".join(pad + line if line.strip() else line for line in text.split("\n"))


# ---- Renderers ----

def render_grid_item(item):
    """Render one <a class="grid__item"> for the grid."""
    item_id = item.get("id")
    title = item["title"]
    title_hover = item.get("title_hover", title)
    title_styles = title_modifiers(item.get("title_style", []))
    text_val = item["text"]
    text_styles = text_modifiers(item.get("text_style", []))
    text_rotation = item.get("text_rotation")
    text_reverse = item.get("text_reverse", False)
    deco = item.get("deco")
    deco_top = item.get("deco_top", False)
    quote = item.get("quote")
    img_url = item["img"]

    # --- title ---
    title_cls = cls("box__title", *title_styles)
    title_class_attr = f' class="{title_cls}"' if title_styles else ""

    # --- text ---
    text_cls = cls("box__text", *text_styles)
    text_class_attr = f' class="{text_cls}"' if text_styles else ""

    # text-inner modifiers
    inner_mods = []
    if text_rotation:
        inner_mods.append(text_rotation)
    if text_reverse:
        inner_mods.append("reverse")
    inner_cls = cls("box__text-inner", *inner_mods) if inner_mods else "box__text-inner"

    # --- deco ---
    deco_html = ""
    if deco:
        entity = DECO_MAP.get(deco, deco)
        deco_cls = "box__deco box__deco--top" if deco_top else "box__deco"
        deco_html = f'<div class="{deco_cls}">{entity}</div>'

    # --- quote (box__content) ---
    quote_html = f'<p class="box__content">{quote}</p>' if quote else ""

    return f"""<a class="grid__item" href="#preview-{item_id}">
  <div class="box">
    <div class="box__shadow"></div>
    <img class="box__img" src="{img_url}" alt="Some image" />
    <h3{title_class_attr}><span class="box__title-inner" data-hover="{title_hover}">{title}</span></h3>
    <h4{text_class_attr}><span class="{inner_cls}">{text_val}</span></h4>
    {deco_html}
    {quote_html}
  </div>
</a>"""


def render_about_item(about):
    """Render the special About grid item (no overlay, no image, clickable text)."""
    text_val = about["text"]
    text_styles = text_modifiers(about.get("text_style", []))
    text_rotation = about.get("text_rotation")
    text_reverse = about.get("text_reverse", False)
    link = about.get("link", "")
    content = about.get("content", "")

    text_cls = cls("box__text", *text_styles)
    text_class_attr = f' class="{text_cls}"' if text_styles else ""

    inner_mods = []
    if text_rotation:
        inner_mods.append(text_rotation)
    if text_reverse:
        inner_mods.append("reverse")
    inner_cls = cls("box__text-inner", *inner_mods) if inner_mods else "box__text-inner"

    onclick = f'onclick="window.open(\'{link}\')"' if link else ""
    onclick_attr = f" {onclick}" if onclick else ""

    return f"""<a class="grid__item grid__item--noclick" href="#">
  <div class="box">
    <div class="box__shadow"></div>
    <h4{text_class_attr}><span class="{inner_cls}"{onclick_attr}>{text_val}</span></h4>
    <p class="box__content">{content}</p>
  </div>
</a>"""


def render_overlay_item(item):
    """Render one <div class="overlay__item"> for the overlay section."""
    item_id = item.get("id")
    title = item["title"]
    text_val = item["text"]
    img_url = item["img"]
    overlay_content = item.get("overlay")

    # title modifiers
    title_styles = title_modifiers(item.get("title_style", []))
    title_cls = cls("box__title", *title_styles)
    title_attr = f' class="{title_cls}"' if title_styles else ""

    # text modifiers
    text_styles = text_modifiers(item.get("text_style", []))
    text_cls = cls("box__text", *text_styles)
    text_attr = f' class="{text_cls}"' if text_styles else ""

    inner_mods = []
    if item.get("text_rotation"):
        inner_mods.append(item["text_rotation"])
    inner_cls = cls("box__text-inner", *inner_mods) if inner_mods else "box__text-inner"

    # deco
    deco = item.get("deco")
    deco_top = item.get("deco_top", False)
    deco_html = ""
    if deco:
        entity = DECO_MAP.get(deco, deco)
        d_cls = "box__deco box__deco--top" if deco_top else "box__deco"
        deco_html = f'<div class="{d_cls}">{entity}</div>'

    # overlay content
    content_html = f'<p class="overlay__content">{overlay_content}</p>' if overlay_content else ""

    return f"""<div class="overlay__item" id="preview-{item_id}">
  <div class="box">
    <div class="box__shadow"></div>
    <img class="box__img box__img--original" src="{img_url}" alt="Some image" />
    <h3{title_attr}><span class="box__title-inner">{title}</span></h3>
    <h4{text_attr}><span class="{inner_cls}">{text_val}</span></h4>
    {deco_html}
  </div>
  {content_html}
</div>"""


def render_grid(albums, about):
    """Render the full <div class="grid"> content (items only, not the wrapper)."""
    items = [render_grid_item(a) for a in albums]
    items.append(render_about_item(about))
    return "\n".join(items)


def render_overlay(albums):
    """Render all overlay items (inside .overlay, between overlay__reveal and close button)."""
    return "\n".join(render_overlay_item(a) for a in albums)


# ---- Main ----

def main():
    parser = argparse.ArgumentParser(description="Build album HTML from JSON data.")
    parser.add_argument("-j", "--json", default="album.json", help="Input JSON file (default: album.json)")
    parser.add_argument("-t", "--template", default="template.html", help="Template HTML (default: template.html)")
    parser.add_argument("-o", "--output", default="index.html", help="Output HTML (default: index.html)")
    args = parser.parse_args()

    # Read data
    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    albums = data["albums"]
    about = data["about"]

    # Generate HTML
    grid_html = render_grid(albums, about)
    overlay_html = render_overlay(albums)

    # Read and patch template
    with open(args.template, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace("{{album_grid}}", grid_html)
    html = html.replace("{{album_overlay}}", overlay_html)

    # Write output
    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Done. Output written to {args.output}")
    print(f"  Grid items: {len(albums) + 1} ({len(albums)} photos + 1 about)")
    print(f"  Overlay items: {len(albums)}")


if __name__ == "__main__":
    main()
