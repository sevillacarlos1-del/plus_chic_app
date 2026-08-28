from pathlib import Path
from PIL import Image
import streamlit as st

# 1. Ejecutar el parche PWA
try:
    from patch_index import patch_streamlit_index
    patch_streamlit_index()
except Exception:
    pass

# 2. Cargar ícono para la pestaña del navegador
ROOT_DIR = Path(__file__).parent.resolve()
icon_path = ROOT_DIR / "assets" / "icono-192.png"
page_icon_val = "✦"
if icon_path.exists():
    try:
        page_icon_val = Image.open(icon_path)
    except Exception:
        pass

st.set_page_config(
    page_title="+CHIC | Luxury Gifts · Sarasota, FL",
    page_icon=page_icon_val,
    layout="wide",
    initial_sidebar_state="collapsed",
)


"""
+CHIC — Boutique de Lujo | main.py
Versión final y corregida para Streamlit Cloud, Chrome Desktop, iOS y Android.
Arquitectura del proyecto:
  ├── main.py
  ├── static/
  │   ├── manifest.json
  │   ├── sw.js
  │   ├── icon-192.png
  │   └── icon-512.png
  └── assets/
      ├── css/
      │   └── styles.css
      └── images/
"""

import base64
import urllib.parse
from pathlib import Path
import streamlit as st

# ── Configuración de la página ────────────────────────────────────────────────
st.set_page_config(
    page_title="+CHIC | Luxury Gifts · Sarasota, FL",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="collapsed",
)
# ==============================================================================
# 1. RELOJ KEEP-ALIVE (PING RENDER)
# ==============================================================================
if st.query_params.get("ping") == "true":
    st.write("pong")
    st.stop()

# ── Rutas relativas seguras ───────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"
ASSETS_IMAGES = ASSETS / "images"
CSS_FILE = ASSETS / "css" / "styles.css"

if not CSS_FILE.exists():
    CSS_FILE = BASE_DIR / "css" / "luxury_style.css"

WHATSAPP_NUMBER = "19412989750"
WHATSAPP_BASE = f"https://wa.me/{WHATSAPP_NUMBER}"


# ── Caching & Performance Engine Blindado ─────────────────────────────────────
@st.cache_data(show_spinner=False)
def img_b64(filename: str) -> str:
    """Convierte una imagen local a Data-URI base64 con caché de Streamlit."""
    try:
        p = ASSETS_IMAGES / filename
        if not p.exists():
            p = ASSETS / filename
        
        if not p.exists() or not p.is_file():
            return ""

        suffix = p.suffix.lower()
        mime_map = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".svg": "image/svg+xml",
            ".gif": "image/gif",
            ".ico": "image/x-icon",
        }
        mime = mime_map.get(suffix, "image/jpeg")
        data = p.read_bytes()
        encoded = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{encoded}"
    except Exception:
        return ""


@st.cache_data(show_spinner=False)
def load_css_file(css_path_str: str) -> str:
    """Carga en caché el contenido del archivo CSS externo de forma segura."""
    try:
        p = Path(css_path_str)
        if p.exists() and p.is_file():
            return p.read_text(encoding="utf-8")
    except Exception:
        pass
    return ""


# ── Inyección Estabilizada de CSS + Metadatos PWA ────────────────────────────
def inject_pwa_and_css():
    st.markdown("""
<meta name="google" content="notranslate">
<meta name="theme-color" content="#8B0000">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="+CHIC">
<link rel="manifest" href="/app/static/manifest.json">
<link rel="icon" type="image/png" sizes="192x192" href="/app/static/icon-192.png">
<link rel="apple-touch-icon" sizes="192x192" href="/app/static/icon-192.png">
""", unsafe_allow_html=True)

    css_external = load_css_file(str(CSS_FILE))
    if css_external:
        st.markdown(f"<style>{css_external}</style>", unsafe_allow_html=True)

    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400..700;1,400..700&family=Montserrat:wght@300;400;500;600;700&display=swap');

:root { 
    --chic-white: #FFFFFF; 
    --chic-gold: #D4AF37; 
    --chic-gold-light: #FFE57F;
    --chic-gold-dark: #AA820A;
    --chic-red: #8B0000;
    --chic-dark: #1A1A1A;
    --chic-bg: #FAFAF8;
}

html, body, .stApp {
    scroll-behavior: smooth !important;
}

.stApp {
    background-color: var(--chic-bg) !important;
    background-image:
        radial-gradient(at 0% 0%, rgba(212,175,55,0.06) 0, transparent 55%),
        radial-gradient(at 100% 100%, rgba(139,0,0,0.04) 0, transparent 55%);
    background-attachment: fixed;
    padding-bottom: 60px !important;
    font-family: 'Montserrat', sans-serif !important;
}

#MainMenu, header, footer { visibility: hidden !important; }
[data-testid="stDecoration"]  { display: none !important; }
[data-testid="stStatusWidget"]{ display: none !important; }

.block-container {
    padding-top: 0 !important;
    padding-bottom: 30px !important;
    padding-left: 12px !important;
    padding-right: 12px !important;
    max-width: 100% !important;
}
@media (min-width: 768px) {
    .block-container {
        padding-left: 32px !important;
        padding-right: 32px !important;
        max-width: 1200px !important;
        margin: 0 auto !important;
    }
}

[data-testid="stVerticalBlock"]   { gap: 0 !important; padding: 0 !important; }
[data-testid="column"]            { padding: 8px !important; background-color: transparent !important; }
[data-testid="stHorizontalBlock"] { gap: 16px !important; background-color: transparent !important; }

.product-card, .glass-card, .contact-img {
    background: #FFFFFF !important;
    border: 2px solid #D4AF37 !important;
    border-radius: 16px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 16px rgba(170, 130, 10, 0.12) !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease !important;
    box-sizing: border-box !important;
    display: flex !important;
    flex-direction: column !important;
    height: 100% !important; 
    margin-bottom: 20px !important;
}

.product-card:hover, .glass-card:hover, .contact-img:hover {
    box-shadow: 0 8px 24px rgba(170, 130, 10, 0.22) !important;
    border-color: #AA820A !important;
    transform: translateY(-3px);
}

.btn-gold {
    background: linear-gradient(135deg, #FFE57F 0%, #D4AF37 50%, #AA820A 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #AA820A !important;
    padding: 12px 20px !important;
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.76rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-radius: 30px !important;
    cursor: pointer !important;
    display: inline-flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
    width: 100% !important;
    transition: opacity 0.2s ease, box-shadow 0.2s ease !important;
    box-shadow: 0 4px 10px rgba(170, 130, 10, 0.15) !important;
    margin-top: auto !important; 
    margin-bottom: 6px;
}

.btn-gold:hover {
    box-shadow: 0 6px 16px rgba(212, 175, 55, 0.4) !important;
    opacity: 0.95;
}

.product-price-bottom {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    color: #000000 !important;
    margin-top: auto !important; 
    margin-bottom: 10px !important;
    text-align: center !important;
    letter-spacing: 0.05em !important;
}

.product-info { 
    padding: 14px 16px 16px 16px !important;
    text-align: center !important; 
    background: #FFFFFF !important; 
    display: flex !important;
    flex-direction: column !important;
    flex-grow: 1 !important; 
}
.product-name { 
    font-family: 'Playfair Display', serif !important; 
    font-size: 1.08rem !important; 
    font-weight: 600 !important; 
    color: #1A1A1A !important; 
    margin-top: 0px !important;
    margin-bottom: 4px !important;
}
.product-caption { 
    font-family: 'Montserrat', sans-serif !important; 
    font-size: 0.75rem !important; 
    color: #6B6B6B !important; 
    line-height: 1.35 !important; 
    margin-bottom: 12px !important;
}

.ornament, p.ornament, span.ornament, a.ornament { 
    font-family: 'Montserrat', sans-serif !important; 
    font-size: 0.68rem !important; 
    letter-spacing: 0.25em !important; 
    color: #D4AF37 !important; 
    text-transform: uppercase !important;
    text-decoration: none !important;
    font-weight: 600 !important;
}

.divider-gold {
    height: 3px;
    background: linear-gradient(90deg, transparent, #D4AF37, transparent);
    max-width: 220px;
    margin: 32px auto;
}

.stTabs [data-baseweb="tab-list"] {
    background: #FFFFFF !important;
    border-bottom: 2px solid #D4AF37 !important;
    padding: 0 12px !important;
    position: sticky !important; 
    top: 0 !important; 
    z-index: 999 !important;
    overflow-x: auto !important;
    gap: 0 !important;
    box-shadow: 0 2px 10px rgba(170, 130, 10, 0.08) !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Montserrat', sans-serif !important;
    font-size: 0.74rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #1A1A1A !important;
    padding: 16px 20px !important;
    border: none !important;
    background: transparent !important;
    white-space: nowrap !important;
    opacity: 1 !important;
}

.stTabs [aria-selected="true"] {
    color: #8B0000 !important;
    border-bottom: 3px solid #8B0000 !important;
    opacity: 1 !important;
    font-weight: 700 !important;
}

.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { 
    display: none !important; 
}

.essence-grid {
    display: grid !important;
    grid-template-columns: 1fr !important;
    gap: 20px !important;
    padding: 10px 4px !important;
}
@media (min-width: 640px) { 
    .essence-grid { grid-template-columns: repeat(3, 1fr) !important; } 
}
</style>
""", unsafe_allow_html=True)

    st.markdown("""
<div id="pwa-install-banner" style="display:none; position:fixed; bottom:20px; right:20px; z-index:999999; background:#FFFFFF; border:2px solid #D4AF37; border-radius:16px; padding:16px 20px; box-shadow:0 10px 30px rgba(139,0,0,0.2); max-width:320px; font-family:'Montserrat',sans-serif;">
  <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:8px;">
    <span style="font-family:'Playfair Display',serif; font-size:1rem; font-weight:700; color:#8B0000;">+CHIC App</span>
    <button onclick="dismissPWAInstall()" style="background:none; border:none; color:#999; font-size:1.1rem; cursor:pointer; padding:0 4px;">✕</button>
  </div>
  <p style="font-size:0.75rem; color:#555; margin:0 0 12px 0; line-height:1.4;">Instala nuestra boutique en tu pantalla de inicio.</p>
  <button id="pwa-install-btn" onclick="installPWAApp()" class="btn-gold" style="margin:0 !important; width:100% !important;">
    ✦ Instalar App +CHIC
  </button>
</div>

<script>
  (function() {
    const topWin = window.top || window;
    
    if (topWin.__chic_pwa_initialized) {
      if (topWin.__deferredPrompt) {
        const banner = document.getElementById('pwa-install-banner');
        if (banner && !sessionStorage.getItem('pwa_dismissed')) {
          banner.style.display = 'block';
        }
      }
      return;
    }
    topWin.__chic_pwa_initialized = true;

    topWin.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      topWin.__deferredPrompt = e;
      const banner = document.getElementById('pwa-install-banner');
      if (banner && !sessionStorage.getItem('pwa_dismissed')) {
        banner.style.display = 'block';
      }
    });

    window.installPWAApp = function() {
      const promptEvent = topWin.__deferredPrompt;
      if (promptEvent) {
        promptEvent.prompt();
        promptEvent.userChoice.then(() => {
          topWin.__deferredPrompt = null;
          window.dismissPWAInstall();
        });
      }
    };

    window.dismissPWAInstall = function() {
      const banner = document.getElementById('pwa-install-banner');
      if (banner) banner.style.display = 'none';
      sessionStorage.setItem('pwa_dismissed', 'true');
    };

    if ('serviceWorker' in navigator) {
      window.addEventListener('load', function() {
        navigator.serviceWorker.register('/app/static/sw.js')
          .catch(function() {
            navigator.serviceWorker.register('/static/sw.js').catch(function() {});
          });
      });
    }
  })();
</script>
""", unsafe_allow_html=True)


inject_pwa_and_css()

# ── Catálogo de Productos ─────────────────────────────────────────────────────
CATALOG = [
    {
        "file":    "regalo1.jpg",
        "name":    "Gift Set Elite",
        "caption": "Premium hand-curated gift box. Perfect for celebrating unique moments.",
        "price":   "", 
        "msg":     "Hi! I'm interested in the Gift Set Elite. Is it available?",
    },                                                                           
    {
        "file":    "regalo2_nuevo.jpg",
        "name":    "Golden Arrangement",
        "caption": "Floral arrangement with gold metallic finishes. Elegance for any occasion.",
        "price":   "38.00 USD",
        "msg":     "Hi! I'm interested in the Golden Arrangement ($38). Can we coordinate delivery?",
    },
    {
        "file":    "regalo3_nuevo.jpg",
        "name":    "Crimson Basket",
        "caption": "Exclusive selection in deep red tones. The gift that never goes unnoticed.",
        "price":   "27.00 USD",
        "msg":     "Hi! I'd like the Crimson Basket ($27). Is it available?",
    },
    {
        "file":    "regalo4_nuevo.jpg",
        "name":    "Box Serenity",
        "caption": "Wellness gift box with luxury body and mind products.",
        "price":   "30.00 USD",
        "msg":     "Hi! I'm interested in the Box Serenity ($30). How can I order it?",
    },
    {
        "file":    "regalo5_nuevo.jpg",
        "name":    "Luxury Bloom",
        "caption": "Artistic bouquet with premium decorative elements. A one-of-a-kind design.",
        "price":   "45.00 USD",
        "msg":     "Hi! I'd love the Luxury Bloom ($45). Can you give me more details?",
    },
    {
        "file":    "regalo6_nuevo.jpg",
        "name":    "Signature Set",
        "caption": "Our flagship box with the +CHIC seal. For those who demand the very best.",
        "price":   "15.00 USD",
        "msg":     "Hi! I want the Signature Set ($15). That's exactly what I'm looking for!",
    },
    {
        "file":    "regalo7_nuevo.jpg",
        "name":    "Romantic Edition",
        "caption": "Special couples set with curated details and impeccable presentation.",
        "price":   "30.00 USD",
        "msg":     "Hi! I love the Romantic Edition ($30). Is it available?",
    },
    {
        "file":    "regalo8_nuevo.jpg",
        "name":    "Mini Luxe Pack",
        "caption": "Compact version of our star set. Big visual impact in a refined small presentation.",
        "price":   "15.00 USD",
        "msg":     "Hi! I'd like the Mini Luxe Pack ($15). Can you help me place the order?",
    },
    {
        "file":    "regalo9_nuevo.jpg",
        "name":    "Grand Prestige",
        "caption": "Our most exclusive piece. Limited-edition handcrafted packaging, truly one of a kind.",
        "price":   "27.00 USD",
        "msg":     "Hi! I'm interested in the Grand Prestige ($27). Is it available?",
    },
]


# ── Helper: Botón WhatsApp ────────────────────────────────────────────────────
def wa_button(msg: str, label: str = "✦ Order via WhatsApp") -> str:
    url = f"{WHATSAPP_BASE}?text={urllib.parse.quote(msg)}"
    return (
        f'<a href="{url}" target="_blank" rel="noopener noreferrer" style="text-decoration:none;display:block;width:100%;">'
        f'<button class="btn-gold">'
        f'<svg width="16" height="16" fill="currentColor" viewBox="0 0 24 24" style="vertical-align:middle;">'
        f'<path d="M12.031 21c-1.603 0-3.14-.407-4.498-1.182l-.322-.184-3.344.877.893-3.26-.202-.32A8.932 8.932 0 013.06 12.03C3.06 7.086 7.085 3.06 12.031 3.06c4.945 0 8.97 4.025 8.97 8.97 0 4.945-4.025 8.97-8.97 8.97zm4.83-6.338c-.264-.132-1.563-.771-1.805-.859-.242-.088-.418-.132-.594.132s-.682.859-.836 1.035c-.154.176-.308.198-.572.066-.264-.132-1.114-.41-2.122-1.308-.784-.699-1.313-1.562-1.467-1.826-.154-.264-.016-.407.116-.539.119-.118.264-.308.396-.462.132-.154.176-.264.264-.44.088-.176.044-.33-.022-.462-.066-.132-.594-1.43-.814-1.958-.214-.514-.432-.443-.594-.451l-.506-.009a.97.97 0 00-.704.33c-.242.264-.924.903-.924 2.201s.946 2.553 1.078 2.729c.132.176 1.861 2.84 4.509 3.982.63.272 1.122.434 1.506.556.633.201 1.209.173 1.664.105.507-.075 1.563-.639 1.783-1.257.22-.617.22-1.146.154-1.257-.066-.11-.242-.176-.506-.308z"/>'
        f'</svg>'
        f'<span style="vertical-align:middle;margin-left:4px;">{label}</span>'
        f'</button>'
        f'</a>'
    )


# ── Render Tarjeta de Producto ────────────────────────────────────────────────
def render_product_card(product: dict) -> str:
    src = img_b64(product["file"])
    wa_html = wa_button(product["msg"])
    price_val = product.get('price', '').strip()
    price_html = f'<div class="product-price-bottom">{price_val}</div>' if price_val else ''

    img_html = (
        f'<img src="{src}" alt="{product["name"]}" loading="lazy"'
        f' style="width:100%;height:100%;object-fit:cover;display:block;margin:0;padding:0;">'
        if src else
        f'<div style="display:flex;align-items:center;justify-content:center;'
        f'height:200px;background:#F5F0E8;color:#D4AF37;font-size:0.8rem;">'
        f'📷 {product["file"]}</div>'
    )
    return f"""
<div class="product-card">
  <div style="position:relative;overflow:hidden;aspect-ratio:4/3;">
    {img_html}
  </div>
  <div class="product-info">
    <p class="product-name">{product['name']}</p>
    <p class="product-caption">{product['caption']}</p>
    {price_html}
    {wa_html}
  </div>
</div>"""


# ── Render Catálogo ───────────────────────────────────────────────────────────
def render_catalog():
    st.markdown("""
<div style="text-align:center;padding:36px 0 20px;">
  <p class="ornament">✦ EXCLUSIVE COLLECTION ✦</p>
  <h2 style="font-family:'Playfair Display',serif;font-size:clamp(1.6rem,5vw,2.4rem);color:#1A1A1A;margin:10px 0 8px;">Our Catalog</h2>
  <p style="font-family:Montserrat,sans-serif;font-size:0.85rem;color:#6B6B6B;">
    Every piece, a story. Every gift, a +CHIC experience.
  </p>
</div>
<div class="divider-gold"></div>
""", unsafe_allow_html=True)

    cols = st.columns(3)
    for i, p in enumerate(CATALOG):
        with cols[i % 3]:
            st.markdown(render_product_card(p), unsafe_allow_html=True)


# ── Tab: INICIO ───────────────────────────────────────────────────────────────
def render_inicio():
    st.markdown("""
<section style="text-align:center;padding:40px 16px 20px;">
  <p class="ornament">✦ LUXURY BOUTIQUE ✦</p>
  <h1 style="font-family:'Playfair Display',serif;font-size:clamp(2.5rem,6vw,4rem);color:#8B0000;margin:12px 0 16px;font-weight:700;">+CHIC</h1>
  <p style="font-family:'Montserrat',sans-serif;font-size:0.95rem;color:#6B6B6B;margin:0 auto 20px;">
    Luxury gifts for unforgettable moments.
  </p>
</section>
""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1.2, 1.6, 1.2])
    with c2:
        st.markdown(wa_button(
            "Hi! I'd love to learn more about +CHIC gifts.",
            "✦ Contact Us"
        ), unsafe_allow_html=True)

    st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)

    st.markdown("""
<div style="text-align:center;padding:32px 0 20px;">
  <p class="ornament">✦ OUR ESSENCE ✦</p>
  <h2 style="font-family:'Playfair Display',serif;font-size:clamp(1.6rem,5vw,2.4rem);color:#1A1A1A;margin:10px 0 8px;">The +CHIC Experience</h2>
  <p style="font-family:Montserrat,sans-serif;font-size:0.85rem;color:#6B6B6B;max-width:600px;margin:0 auto;line-height:1.6;">
    We believe gifting is an art. Every detail is carefully designed to convey elegance, exclusivity, and love.
  </p>
</div>
""", unsafe_allow_html=True)

    essence = [
        ("inicio1.jpg", "Exclusive Identity", "Distinctive design, high visual impact, and elegance."), 
        ("inicio2.jpg", "Impeccable Presentation", "Luxury boxes, silk ribbons, and a flawless finish."),
        ("inicio3.jpg", "Unique Moments", "We don't just deliver gifts, we deliver emotions.")
    ]

    cards = ""
    for img, title, desc in essence:
        src = img_b64(img)
        
        if img == "inicio1.jpg":
            if src:
                img_tag = (
                    f'<div style="position:relative;overflow:hidden;aspect-ratio:4/3;background:#FFFFFF;display:flex;align-items:center;justify-content:center;padding:12px;">'
                    f'<img src="{src}" alt="{title}" style="width:100%;height:100%;object-fit:contain;display:block;margin:0;">'
                    f'</div>'
                )
            else:
                img_tag = (
                    f'<div style="position:relative;overflow:hidden;aspect-ratio:4/3;background:#F5F0E8;display:flex;align-items:center;justify-content:center;color:#D4AF37;font-size:0.8rem;">'
                    f'📷 {img}</div>'
                )
        else:
            if src:
                img_tag = (
                    f'<div style="position:relative;overflow:hidden;aspect-ratio:4/3;">'
                    f'<img src="{src}" alt="{title}" style="width:100%;height:100%;display:block;margin:0;object-fit:cover;">'
                    f'</div>'
                )
            else:
                img_tag = (
                    f'<div style="position:relative;overflow:hidden;aspect-ratio:4/3;background:#F5F0E8;display:flex;align-items:center;justify-content:center;color:#D4AF37;font-size:0.8rem;">'
                    f'📷 {img}</div>'
                )
        
        cards += f"""
<div class="glass-card">
  {img_tag}
  <div class="product-info">
    <p class="product-name">{title}</p>
    <p class="product-caption">{desc}</p>
  </div>
</div>"""
            
    st.markdown(f'<div class="essence-grid">{cards}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider-gold"></div>', unsafe_allow_html=True)
    st.markdown("""
<div class="glass-card" style="text-align:center;padding:40px 24px;max-width:640px;margin:0 auto 40px;">
  <p class="ornament">✦ READY TO IMPRESS? ✦</p>
  <h2 style="font-family:'Playfair Display',serif;font-size:1.8rem;color:#1A1A1A;margin:12px 0 10px;">
    Create a moment<br>no one will forget
  </h2>
  <p style="font-family:Montserrat,sans-serif;font-size:0.85rem;color:#6B6B6B;margin-bottom:0;">
    Explore our exclusive catalog or contact us for a personalized service.
  </p>
</div>
""", unsafe_allow_html=True)


# ── Tab: CONTACTO (HTML Limpio y Directo) ─────────────────────────────────────
def render_contacto():
    st.markdown("""
<div style="text-align:center;padding:40px 24px 28px;">
  <p class="ornament">✦ WE'RE HERE FOR YOU ✦</p>
  <h2 style="font-family:'Playfair Display',serif;font-size:2.2rem;color:#1A1A1A;margin:10px 0 8px;">
    Contact &amp; Orders
  </h2>
  <p style="font-family:Montserrat,sans-serif;font-size:0.88rem;color:#6B6B6B;max-width:500px;margin:0 auto;">
    Our concierge team is ready to guide you through every detail of your perfect gift.
  </p>
</div>
<div class="divider-gold"></div>
""", unsafe_allow_html=True)

    col_imgs, col_info = st.columns([1, 1], gap="large")

    with col_imgs:
        for img in ["contacto1.jpg", "contacto2.jpg", "contacto3.jpg"]:
            src = img_b64(img)
            img_html = (
                f'<div class="contact-img" style="aspect-ratio:4/3;margin-bottom:16px;overflow:hidden;">'
                f'<img src="{src}" alt="+CHIC" style="width:100%;height:100%;display:block;margin:0;object-fit:cover;">'
                f'</div>'
                if src else
                f'<div class="contact-img" style="aspect-ratio:4/3;margin-bottom:16px;display:flex;align-items:center;justify-content:center;background:#F5F0E8;color:#D4AF37;font-size:0.8rem;">'
                f'📷 {img}</div>'
            )
            st.markdown(img_html, unsafe_allow_html=True)

    with col_info:
        btn_order = wa_button(
            "Hi! I'd like to place a custom order with +CHIC. Can you assist me?",
            "✦ Place Order via WhatsApp"
        )
        btn_query = wa_button(
            "Hi! I have a question about +CHIC gifts in Sarasota.",
            "💬 General Inquiry"
        )

        contact_card_html = f"""
<div class="glass-card" style="padding:24px; height:100%;">
  <p class="ornament" style="margin-bottom:12px;">✦ +CHIC L.L.C.</p>
  <h3 style="font-family:'Playfair Display',serif;font-size:1.5rem;color:#8B0000;margin-bottom:16px;">Luxury Boutique</h3>
  <p style="font-family:Montserrat,sans-serif;font-size:0.85rem;color:#6B6B6B;line-height:1.7;margin-bottom:24px;">
    Specialists in personalized luxury gifts. Every box is a work of art curated with meticulous attention to detail.
  </p>

  <div style="margin-bottom:16px;">
    <p style="font-family:Montserrat,sans-serif;font-size:0.72rem;letter-spacing:0.18em;color:#D4AF37;text-transform:uppercase;margin-bottom:4px;">Direct WhatsApp</p>
    <p style="font-family:Montserrat,sans-serif;font-size:0.9rem;color:#1A1A1A;font-weight:600;">+1 (941) 298-9750</p>
  </div>

  <div style="margin-bottom:16px;">
    <p style="font-family:Montserrat,sans-serif;font-size:0.72rem;letter-spacing:0.18em;color:#D4AF37;text-transform:uppercase;margin-bottom:4px;">Instagram</p>
    <p style="font-family:Montserrat,sans-serif;font-size:0.9rem;color:#1A1A1A;font-weight:600;">@chic.fl</p>
  </div>

  <div style="display:flex;flex-direction:column;gap:12px;margin-top:24px;margin-bottom:16px;">
    {btn_order}
    {btn_query}
  </div>

  <div style="margin-top:28px;padding:16px;background:rgba(212,175,55,0.07);border-left:3px solid #D4AF37;border-radius:8px;">
    <p style="font-family:Montserrat,sans-serif;font-size:0.78rem;color:#6B6B6B;line-height:1.6;font-style:italic;margin:0;">
      "We don't send packages — we deliver stories with the +Chic seal."
    </p>
  </div>
</div>"""
        st.markdown(contact_card_html, unsafe_allow_html=True)


# ── FOOTER ────────────────────────────────────────────────────────────────────
def render_footer():
    st.markdown("""
<div class="divider-gold" style="max-width:100%; margin:32px 0 0 0;"></div>
<footer style="text-align:center;padding:24px 24px 40px;">
  <p style="font-family:'Playfair Display',serif;font-size:1.6rem;font-weight:700;letter-spacing:0.2em;color:#8B0000;margin-bottom:8px;">
    +CHIC
  </p>
  <p class="ornament" style="margin-bottom:12px;">© 2026 +CHIC L.L.C. · Luxury Gifts · Sarasota, FL</p>
  <div style="display:flex;gap:20px;justify-content:center;">
    <a href="https://instagram.com/chic.fl" target="_blank" rel="noopener noreferrer" style="font-family:Montserrat,sans-serif;font-size:0.75rem;color:#6B6B6B;text-decoration:none;">
      Instagram
    </a>
    <span style="color:#D4AF37;">·</span>
    <a href="https://wa.me/19412989750" target="_blank" rel="noopener noreferrer" style="font-family:Montserrat,sans-serif;font-size:0.75rem;color:#6B6B6B;text-decoration:none;">
      WhatsApp
    </a>
  </div>
</footer>
""", unsafe_allow_html=True)


# ── NAVEGACIÓN PRINCIPAL ──────────────────────────────────────────────────────
tab_inicio, tab_catalogo, tab_contacto = st.tabs(["✦ INICIO", "✦ CATALOG", "✦ CONTACT"])

with tab_inicio:
    render_inicio()

with tab_catalogo:
    render_catalog()

with tab_contacto:
    render_contacto()

render_footer()
# ==============================================================================
# NOTA INFORMATIVA DE INSTALACIÓN PWA
# ==============================================================================
st.markdown("---")
st.markdown("### 📲 **Instala la App en tu Móvil**")
st.info(
    "**¿Quieres tener esta App en tu pantalla de inicio?**\n\n"
    "• **Android (Chrome):** Toca los 3 puntos arriba a la derecha y selecciona **'Agregar a la pantalla principal'** o **'Instalar aplicación'**.\n\n"
    "• **iPhone (Safari):** Toca el botón **Compartir** (el cuadro con la flecha hacia arriba) y selecciona **'Agregar al inicio'**."
)