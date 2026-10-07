"""Generate high-resolution Brand Radar macOS AppIcon.icns using native macOS qlmanage, sips, and iconutil."""
import os
import shutil
import subprocess
from pathlib import Path

SVG_CONTENT = """<svg width="1024" height="1024" viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- Background Gradient -->
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#0a0f1d"/>
      <stop offset="50%" stop-color="#0f172a"/>
      <stop offset="100%" stop-color="#1e1e38"/>
    </linearGradient>

    <!-- Radar Sweep Gradient (Intelligence Heat & Tech) -->
    <linearGradient id="sweepGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.5"/>
      <stop offset="50%" stop-color="#818cf8" stop-opacity="0.2"/>
      <stop offset="100%" stop-color="#c084fc" stop-opacity="0"/>
    </linearGradient>

    <!-- Glowing filters -->
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="8" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <radialGradient id="centerGlow" cx="50%" cy="50%" r="50%">
      <stop offset="0%" stop-color="#38bdf8" stop-opacity="0.9"/>
      <stop offset="50%" stop-color="#6366f1" stop-opacity="0.4"/>
      <stop offset="100%" stop-color="#6366f1" stop-opacity="0"/>
    </radialGradient>

    <!-- Clip squircle -->
    <clipPath id="squircleClip">
      <rect width="1024" height="1024" rx="224" ry="224"/>
    </clipPath>
  </defs>

  <!-- Base Squircle -->
  <rect width="1024" height="1024" rx="224" ry="224" fill="url(#bgGrad)"/>
  <rect width="1020" height="1020" x="2" y="2" rx="222" ry="222" fill="none" stroke="#6366f1" stroke-width="4" stroke-opacity="0.5"/>

  <!-- Content clipped to squircle -->
  <g clip-path="url(#squircleClip)">
    <!-- Tech Grid Background -->
    <path d="M 112 512 L 912 512 M 512 112 L 512 912" stroke="#2e3856" stroke-width="2" stroke-opacity="0.7"/>
    <path d="M 230 230 L 794 794 M 230 794 L 794 230" stroke="#2e3856" stroke-width="1.5" stroke-dasharray="8 8" stroke-opacity="0.4"/>

    <!-- Concentric Radar Rings -->
    <circle cx="512" cy="512" r="390" fill="none" stroke="#374151" stroke-width="3" stroke-opacity="0.6"/>
    <circle cx="512" cy="512" r="310" fill="none" stroke="#4338ca" stroke-width="3.5" stroke-opacity="0.6"/>
    <circle cx="512" cy="512" r="220" fill="none" stroke="#4f46e5" stroke-width="4" stroke-opacity="0.8"/>
    <circle cx="512" cy="512" r="130" fill="none" stroke="#6366f1" stroke-width="4.5"/>
    <circle cx="512" cy="512" r="50" fill="none" stroke="#818cf8" stroke-width="3.5"/>

    <!-- Distance Ticks -->
    <circle cx="512" cy="512" r="350" fill="none" stroke="#312e81" stroke-width="1.5" stroke-dasharray="4 16" stroke-opacity="0.7"/>

    <!-- Radar Sweep Beam (Pie sector) -->
    <path d="M 512 512 L 770 210 A 390 390 0 0 1 890 410 Z" fill="url(#sweepGrad)"/>
    <!-- Leading Beam Edge -->
    <line x1="512" y1="512" x2="890" y2="410" stroke="#38bdf8" stroke-width="4.5" filter="url(#glow)"/>

    <!-- Ambient Center Radar Halo -->
    <circle cx="512" cy="512" r="90" fill="url(#centerGlow)"/>
    <circle cx="512" cy="512" r="14" fill="#38bdf8" filter="url(#glow)"/>
    <circle cx="512" cy="512" r="6" fill="#ffffff"/>

    <!-- 4 BRAND INTELLIGENCE NODES (Airfryer Champions) -->
    <!-- 1. SHARKNINJA (Amber/Orange - Top Right: Leader in DualZone & Spend) -->
    <circle cx="690" cy="320" r="24" fill="#f59e0b" fill-opacity="0.3"/>
    <circle cx="690" cy="320" r="14" fill="#fbbf24"/>
    <circle cx="690" cy="320" r="6" fill="#fff"/>
    <text x="718" y="318" fill="#fef3c7" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="22" font-weight="900">NINJA</text>
    <text x="718" y="338" fill="#fde68a" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="13" font-weight="600">DualZone · #1 Spend</text>

    <!-- 2. COSORI (Emerald/Mint - Top Left: Community & Influencer Powerhouse) -->
    <circle cx="340" cy="320" r="24" fill="#10b981" fill-opacity="0.3"/>
    <circle cx="340" cy="320" r="14" fill="#34d399"/>
    <circle cx="340" cy="320" r="6" fill="#fff"/>
    <text x="210" y="318" fill="#d1fae5" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="22" font-weight="900">COSORI</text>
    <text x="190" y="338" fill="#a7f3d0" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="13" font-weight="600">TurboBlaze · Creator #1</text>

    <!-- 3. PHILIPS (Royal Blue - Bottom Left: Premium Pioneer & Airfryer Category Creator) -->
    <circle cx="350" cy="670" r="24" fill="#3b82f6" fill-opacity="0.3"/>
    <circle cx="350" cy="670" r="14" fill="#60a5fa"/>
    <circle cx="350" cy="670" r="6" fill="#fff"/>
    <text x="210" y="668" fill="#dbeafe" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="22" font-weight="900">PHILIPS</text>
    <text x="205" y="688" fill="#bfdbfe" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="13" font-weight="600">Airfryer XXL · SEM Brand</text>

    <!-- 4. TEFAL (Crimson Red - Bottom Right: Groupe SEB Heritage & Dual Easy Fry) -->
    <circle cx="680" cy="670" r="24" fill="#ef4444" fill-opacity="0.3"/>
    <circle cx="680" cy="670" r="14" fill="#f87171"/>
    <circle cx="680" cy="670" r="6" fill="#fff"/>
    <text x="714" y="668" fill="#fee2e2" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="22" font-weight="900">TEFAL</text>
    <text x="714" y="688" fill="#fecaca" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="13" font-weight="600">Dual Easy · Retail #1</text>

    <!-- Typography -->
    <text x="512" y="190" text-anchor="middle" fill="#60a5fa" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="28" font-weight="900" letter-spacing="10">BRAND RADAR</text>
    <text x="512" y="855" text-anchor="middle" fill="#94a3b8" font-family="-apple-system, Helvetica, Arial, sans-serif" font-size="18" font-weight="700" letter-spacing="7">GERMAN AIRFRYER INTEL</text>

    <!-- Subtle Glass Sheen on Top -->
    <path d="M 0 0 L 1024 0 L 1024 380 Q 512 480 0 380 Z" fill="#ffffff" fill-opacity="0.04"/>
  </g>
</svg>"""

def build_icns(out_icns: Path, out_png: Path):
    temp_dir = Path("data/_icon_build")
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir(parents=True)
    iconset = temp_dir / "radar.iconset"
    iconset.mkdir()

    svg_file = temp_dir / "icon.svg"
    svg_file.write_text(SVG_CONTENT, encoding="utf-8")

    # 1. Render 1024x1024 PNG using macOS qlmanage
    subprocess.run(["qlmanage", "-t", "-s", "1024", "-o", str(temp_dir), str(svg_file)],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    rendered_png = temp_dir / "icon.svg.png"
    if not rendered_png.exists():
        raise FileNotFoundError(f"QuickLook thumbnail failed to produce {rendered_png}")

    png_1024 = temp_dir / "icon_1024.png"
    # Ensure exact 1024x1024 via sips
    subprocess.run(["sips", "-z", "1024", "1024", str(rendered_png), "--out", str(png_1024)],
                   check=True, stdout=subprocess.DEVNULL)

    # Copy out high-res 1024 PNG
    out_png.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(png_1024, out_png)

    # 2. Downscale into standard macOS iconset sizes using sips
    sizes = [
        ("icon_16x16.png", 16),
        ("icon_16x16@2x.png", 32),
        ("icon_32x32.png", 32),
        ("icon_32x32@2x.png", 64),
        ("icon_128x128.png", 128),
        ("icon_128x128@2x.png", 256),
        ("icon_256x256.png", 256),
        ("icon_256x256@2x.png", 512),
        ("icon_512x512.png", 512),
        ("icon_512x512@2x.png", 1024),
    ]

    for name, sz in sizes:
        dst = iconset / name
        subprocess.run(["sips", "-z", str(sz), str(sz), str(png_1024), "--out", str(dst)],
                       check=True, stdout=subprocess.DEVNULL)

    # 3. Compile icns via iconutil
    out_icns.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["iconutil", "-c", "icns", str(iconset), "-o", str(out_icns)], check=True)
    shutil.rmtree(temp_dir)
    print(f"Generated {out_icns} ({out_icns.stat().st_size} bytes)")
    print(f"Generated {out_png} ({out_png.stat().st_size} bytes)")

if __name__ == "__main__":
    out_icns = Path("assets/AppIcon.icns")
    out_png = Path("assets/icon.png")
    build_icns(out_icns, out_png)
