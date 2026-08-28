import shutil
import pathlib
import streamlit

def patch_streamlit_index():
    root_dir = pathlib.Path(__file__).parent.resolve()
    assets_src = root_dir / "assets"
    
    # Directorio estático interno de Streamlit
    st_static_dir = pathlib.Path(streamlit.__file__).parent / "static"
    index_path = st_static_dir / "index.html"

    if not index_path.exists():
        return

    # 1. Copiar assets a la carpeta estática interna de Streamlit
    if assets_src.exists():
        dest_assets = st_static_dir / "assets"
        dest_assets.mkdir(parents=True, exist_ok=True)
        for item in assets_src.glob("*"):
            if item.is_file():
                shutil.copy2(item, dest_assets / item.name)
                shutil.copy2(item, st_static_dir / item.name)

    # 2. Inyectar tags en index.html raíz
    html_content = index_path.read_text(encoding="utf-8")
    manifest_tag = 'rel="manifest"'

    if manifest_tag not in html_content:
        pwa_head_tags = '''
    <!-- PWA Icons & Manifest Injected -->
    <link rel="manifest" href="/app/static/assets/manifest.json">
    <link rel="icon" type="image/png" sizes="192x192" href="/app/static/assets/icono-192.png">
    <link rel="apple-touch-icon" sizes="192x192" href="/app/static/assets/icono-192.png">
    <link rel="apple-touch-icon" sizes="512x512" href="/app/static/assets/icono-512.png">
    <meta name="theme-color" content="#1a1a1a">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent"></head>'''
        updated_content = html_content.replace("</head>", pwa_head_tags)
        index_path.write_text(updated_content, encoding="utf-8")

if __name__ == "__main__":
    patch_streamlit_index()