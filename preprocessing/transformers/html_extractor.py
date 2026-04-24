from bs4 import BeautifulSoup, Tag, Comment
import re

FUNCTIONAL_TAGS = {
    "h1", "h2", "h3", "h4", "h5", "h6",
    "form",
    "input", "textarea", "select", "option",
    "button",
    "label",
    "table", "thead", "tbody", "tr", "th", "td",
    "a"
}

REMOVE_TAGS = {
    "script", "style", "noscript",
    "header", "footer", "nav",
    "svg", "img", "picture", "video", "audio",
    "iframe", "canvas", "figure", "figcaption", 
    "br", "i", 
}

# Solo attributi funzionali per tag
KEEP_ATTRS = {
    "a":        {"href", "aria-label"},
    "form":     {"action", "method"},
    "input":    {"type", "name", "value", "placeholder", "required", "disabled", "checked"},
    "textarea": {"name", "placeholder", "required"},
    "select":   {"name", "required", "multiple"},
    "option":   {"value", "selected"},
    "button":   {"type", "name", "disabled"},
    "label":    {"for"},
    "th":       set(),
    "td":       set(),
    "tr":       set(),
    "table":    set(),
    "thead":    set(),
    "tbody":    set(),
} 

MAX_ROWS = 10 

def _clean_attrs(tag: Tag) -> None:
    """Rimuove attributi non funzionali da un tag."""
    allowed = KEEP_ATTRS.get(tag.name, set())
    for attr in [k for k in list(tag.attrs) if k not in allowed]:
        del tag.attrs[attr]


def _collapse_whitespace(text: str) -> str:
    """Collassa whitespace multipli in uno spazio singolo."""
    return re.sub(r'\s+', ' ', text).strip()


def _is_empty(tag: Tag) -> bool:
    """Restituisce True se il tag non ha contenuto utile."""
    # Input e select sono sempre utili anche senza testo
    if tag.name in {"input", "select", "textarea"}:
        return False
    text = tag.get_text(strip=True)
    return not text


def html_extractor(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")

    # Rimuovi commenti HTML
    for comment in soup.find_all(string=lambda s: isinstance(s, Comment)):
        comment.extract()

    root = soup.find("main") or soup.find("body")
    if root is None:
        return ""

    #Rimuovi tag rumorosi
    for tag in root.find_all(REMOVE_TAGS): 
        tag.decompose()

    #limita righe tabelle
    for table in root.find_all("table"):
      if table.find_parent("table"):
          continue #ignoro tabelle annidate

      body = table.find("tbody") or table
      rows = body.find_all("tr")

      for r in rows[MAX_ROWS:]:
        r.decompose()    

    #rimuovi span mantenendo testo per funzionalità semantica 
    for tag in root.find_all("span"): 
        tag.unwrap()     

    # Rimuovi div e span completamente vuoti
    for tag in root.find_all(["div"]):
        if _is_empty(tag):
            tag.unwrap()  # unwrap invece di decompose: preserva i figli utili

    extracted = []

    def traverse(node):
        for child in list(node.children):
            if not isinstance(child, Tag):
                continue

            if child.name in FUNCTIONAL_TAGS:

                # Salta se vuoto (eccetto input/select/textarea)
                if _is_empty(child):
                    continue

                # Salta <a> senza testo né aria-label
                if child.name == "a":
                    text = _collapse_whitespace(child.get_text())
                    aria = child.get("aria-label", "").strip()
                    if not text and not aria:
                        continue

                # Pulisci attributi su tutto il sottoalbero
                for descendant in child.find_all(True):
                    _clean_attrs(descendant)
                    # Collassa whitespace nei testi interni
                    for string in descendant.strings:
                        if string.strip():
                            string.replace_with(_collapse_whitespace(str(string)))

                _clean_attrs(child)

                extracted.append(str(child))

            else:
                traverse(child)

    traverse(root)
    return "\n".join(extracted) 