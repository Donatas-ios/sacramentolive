"""
Shared California State Capitol SVG silhouette used across all page headers.
Black detailed silhouette designed to match the actual CA Capitol building:
  - Flagpole + finial
  - Tall hemispherical dome with drum colonnade
  - Triangular pediment
  - 8-column Corinthian portico
  - Main building body
  - Two symmetrical wings
  - Grand staircase
"""

CAPITOL_SVG = """\
<svg class="capitol-icon" viewBox="0 0 120 130" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-label="California State Capitol">

  <!-- ── Flagpole ── -->
  <rect x="59" y="0" width="2" height="10" fill="#1a1a1a"/>
  <polygon points="61,0 68,3 61,6" fill="#1a1a1a"/>

  <!-- ── Lantern ── -->
  <rect x="54.5" y="10" width="11" height="3" rx="0.5" fill="#1a1a1a"/>
  <rect x="56"   y="13" width="8"  height="5" rx="0.5" fill="#1a1a1a"/>

  <!-- ── Dome ── -->
  <!-- Outer dome shape: tall semi-ellipse -->
  <path d="M30,52 C30,28 45,16 60,15 C75,16 90,28 90,52 Z" fill="#1a1a1a"/>
  <!-- Dome ribs (light vertical cuts) -->
  <rect x="46" y="20" width="1.2" height="20" fill="white" opacity="0.18"/>
  <rect x="51" y="17" width="1.2" height="22" fill="white" opacity="0.18"/>
  <rect x="60" y="16" width="1.2" height="23" fill="white" opacity="0.18"/>
  <rect x="68" y="17" width="1.2" height="22" fill="white" opacity="0.18"/>
  <rect x="73" y="20" width="1.2" height="20" fill="white" opacity="0.18"/>
  <!-- Dome oculus ring -->
  <ellipse cx="60" cy="52" rx="30" ry="3" fill="#1a1a1a"/>

  <!-- ── Drum colonnade ── -->
  <rect x="36" y="49" width="48" height="9" fill="#1a1a1a"/>
  <!-- Drum columns (12 small bumps on drum) -->
  <rect x="37"   y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="41.5" y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="46"   y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="50.5" y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="55"   y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="59.5" y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="64"   y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="68.5" y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="73"   y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="77.5" y="46" width="2.2" height="5" fill="#1a1a1a"/>
  <rect x="82"   y="46" width="2.2" height="5" fill="#1a1a1a"/>

  <!-- ── Pediment ── -->
  <path d="M18,64 L60,56 L102,64 Z" fill="#1a1a1a"/>
  <!-- Pediment entablature -->
  <rect x="18" y="63" width="84" height="4" fill="#1a1a1a"/>

  <!-- ── Portico columns (8 columns) ── -->
  <rect x="22"   y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="28.5" y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="35"   y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="41.5" y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="75"   y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="81.5" y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="88"   y="67" width="3.5" height="22" fill="#1a1a1a"/>
  <rect x="94.5" y="67" width="3.5" height="22" fill="#1a1a1a"/>

  <!-- ── Main building body ── -->
  <rect x="14" y="67" width="92" height="28" fill="#1a1a1a"/>
  <!-- Central door -->
  <rect x="54" y="80" width="12" height="15" rx="1" fill="white" opacity="0.15"/>

  <!-- ── Wings ── -->
  <rect x="2"  y="76" width="14" height="19" fill="#1a1a1a"/>
  <rect x="104" y="76" width="14" height="19" fill="#1a1a1a"/>
  <!-- Wing windows -->
  <rect x="5"   y="80" width="4" height="6" rx="0.5" fill="white" opacity="0.15"/>
  <rect x="111" y="80" width="4" height="6" rx="0.5" fill="white" opacity="0.15"/>

  <!-- ── Grand staircase (4 steps) ── -->
  <rect x="18"  y="95"  width="84" height="4"  rx="0.5" fill="#1a1a1a"/>
  <rect x="12"  y="99"  width="96" height="4"  rx="0.5" fill="#1a1a1a"/>
  <rect x="6"   y="103" width="108" height="4" rx="0.5" fill="#1a1a1a"/>
  <rect x="0"   y="107" width="120" height="4" rx="0.5" fill="#1a1a1a"/>

</svg>"""
