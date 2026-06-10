"""
Header icons used across all pages.

CAPITOL_SVG  — California State Capitol silhouette (left of title)
               Matches reference: smooth dome, drum colonnade, two portico
               tiers with white-gap columns, grand staircase. Black.

TREE_SVG     — Sacramento oak tree silhouette (right of title)
               Wide spreading canopy, trunk, ground shadow. Black.
"""

# ---------------------------------------------------------------------------
# Capitol building
# Column logic (white gaps in filled dark rectangles):
#   Drum   (w=72): 12 cols × 4px + 11 gaps × 2px = 48+22 = 70 ≈ 72  ✓
#   Upper  (w=76): 10 cols × 5.6px + 9 gaps × 2px = 56+18 = 74 ≈ 76 ✓
#   Lower  (w=80):  8 cols × 7px  + 7 gaps × 3px  = 56+21 = 77 ≈ 80 ✓
# ---------------------------------------------------------------------------
CAPITOL_SVG = """\
<svg class="capitol-icon" viewBox="0 0 100 115" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-label="California State Capitol">

  <!-- Finial / spire -->
  <rect x="48.5" y="0" width="3" height="8" rx="1" fill="#1a1a1a"/>
  <rect x="45.5" y="8" width="9" height="3.5" rx="0.5" fill="#1a1a1a"/>

  <!-- Dome — large smooth semi-ellipse, base at y=53 -->
  <path d="M16,53 A34,43 0 0,1 84,53 Z" fill="#1a1a1a"/>

  <!-- Dome base ring -->
  <rect x="14" y="51" width="72" height="4" fill="#1a1a1a"/>

  <!-- ── Drum colonnade (x 14–86, w=72, h=15) ── -->
  <rect x="14" y="55" width="72" height="15" fill="#1a1a1a"/>
  <!-- 11 white gaps → 12 dark columns, spacing=6 (4 col + 2 gap) -->
  <rect x="18" y="55" width="2" height="15" fill="white"/>
  <rect x="24" y="55" width="2" height="15" fill="white"/>
  <rect x="30" y="55" width="2" height="15" fill="white"/>
  <rect x="36" y="55" width="2" height="15" fill="white"/>
  <rect x="42" y="55" width="2" height="15" fill="white"/>
  <rect x="48" y="55" width="2" height="15" fill="white"/>
  <rect x="54" y="55" width="2" height="15" fill="white"/>
  <rect x="60" y="55" width="2" height="15" fill="white"/>
  <rect x="66" y="55" width="2" height="15" fill="white"/>
  <rect x="72" y="55" width="2" height="15" fill="white"/>
  <rect x="78" y="55" width="2" height="15" fill="white"/>

  <!-- Entablature below drum -->
  <rect x="12" y="70" width="76" height="4" fill="#1a1a1a"/>

  <!-- ── Upper portico (x 12–88, w=76, h=12) ── -->
  <rect x="12" y="74" width="76" height="12" fill="#1a1a1a"/>
  <!-- 9 white gaps → 10 dark columns, spacing=7.6 (5.6 col + 2 gap) -->
  <rect x="17.6" y="74" width="2" height="12" fill="white"/>
  <rect x="25.2" y="74" width="2" height="12" fill="white"/>
  <rect x="32.8" y="74" width="2" height="12" fill="white"/>
  <rect x="40.4" y="74" width="2" height="12" fill="white"/>
  <rect x="48.0" y="74" width="2" height="12" fill="white"/>
  <rect x="55.6" y="74" width="2" height="12" fill="white"/>
  <rect x="63.2" y="74" width="2" height="12" fill="white"/>
  <rect x="70.8" y="74" width="2" height="12" fill="white"/>
  <rect x="78.4" y="74" width="2" height="12" fill="white"/>

  <!-- Second entablature -->
  <rect x="10" y="86" width="80" height="4" fill="#1a1a1a"/>

  <!-- ── Lower portico (x 10–90, w=80, h=15) ── -->
  <rect x="10" y="90" width="80" height="15" fill="#1a1a1a"/>
  <!-- 7 white gaps → 8 dark columns, spacing=10 (7 col + 3 gap) -->
  <rect x="17" y="90" width="3" height="15" fill="white"/>
  <rect x="27" y="90" width="3" height="15" fill="white"/>
  <rect x="37" y="90" width="3" height="15" fill="white"/>
  <rect x="47" y="90" width="3" height="15" fill="white"/>
  <rect x="57" y="90" width="3" height="15" fill="white"/>
  <rect x="67" y="90" width="3" height="15" fill="white"/>
  <rect x="77" y="90" width="3" height="15" fill="white"/>

  <!-- Grand staircase (4 steps, each widens by 6) -->
  <rect x="14" y="105" width="72" height="3" fill="#1a1a1a"/>
  <rect x="8"  y="108" width="84" height="3" fill="#1a1a1a"/>
  <rect x="2"  y="111" width="96" height="3" fill="#1a1a1a"/>
  <rect x="0"  y="114" width="100" height="1" fill="#1a1a1a"/>

</svg>"""


# ---------------------------------------------------------------------------
# Oak tree — Sacramento is "City of Trees"; oak is the state tree symbol
# Spreading canopy + trunk + ground shadow
# ---------------------------------------------------------------------------
TREE_SVG = """\
<svg class="tree-icon" viewBox="0 0 120 105" fill="none"
     xmlns="http://www.w3.org/2000/svg" aria-label="Sacramento oak tree">

  <!-- Main canopy — wide spreading organic silhouette -->
  <path d="
    M 16,70
    C  5,62  1,48  7,36
    C  4,22 13,12 24,10
    C 28, 4 36, 2 42, 8
    C 44, 2 50, 0 56, 6
    C 60, 0 66, 2 70, 8
    C 76, 4 86,10 92,16
    C 100,18 107,30 105,44
    C 109,54 109,64 104,70
    Z"
    fill="#1a1a1a"/>

  <!-- Secondary canopy layer (lower overlap, adds visual depth) -->
  <path d="
    M 16,70
    C 20,64 14,58 18,52
    C 22,46 28,48 30,54
    C 34,50 38,46 44,50
    C 48,45 54,46 56,52
    C 60,46 66,46 70,52
    C 74,47 80,48 82,54
    C 86,50 92,52 96,58
    C 100,62 104,68 104,70
    Z"
    fill="#1a1a1a"/>

  <!-- Trunk — tapered, slightly irregular -->
  <path d="
    M 50,70
    C 48,78 45,90 43,103
    L 77,103
    C 75,90 72,78 70,70
    C 66,68 54,68 50,70
    Z"
    fill="#1a1a1a"/>

  <!-- A few visible branch silhouettes at canopy base -->
  <path d="M55,70 C50,66 40,64 28,66" stroke="#1a1a1a" stroke-width="3.5"
        stroke-linecap="round" fill="none"/>
  <path d="M65,70 C70,66 80,64 92,66" stroke="#1a1a1a" stroke-width="3.5"
        stroke-linecap="round" fill="none"/>
  <path d="M60,68 C60,62 58,56 56,50"  stroke="#1a1a1a" stroke-width="3"
        stroke-linecap="round" fill="none"/>

  <!-- Ground shadow -->
  <ellipse cx="60" cy="103" rx="38" ry="4" fill="#1a1a1a"/>

</svg>"""
