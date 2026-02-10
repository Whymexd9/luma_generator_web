import streamlit as st
import struct
from copy import deepcopy

def f2h(x):
    return struct.pack("<f", float(x)).hex()

def h2f(x):
    return struct.unpack("<f", bytes.fromhex(x))[0]

def norm(s):
    return "".join(c for c in s.lower() if c in "0123456789abcdef")

SHARP_ID14_ADDR = 0x110E63E
LUMA_ADDR = 0x110A2EE

SHARP_ID14_DEFAULT = norm(
    "0a490a140d000080401dc9763e3e250000803f2d0000803f"
    "0a140d0000803f1de3a51b3e250000803f2d0000803f"
    "0a140d3333f33f1d68916d3d250000803f2d0000803f"
    "12050d0000a040"
    "0a490a140d6666a6401d022b873d250000803f2d0000803f"
    "0a140d295c0f401dcdcccc3d250000803f2d0000803f"
    "0a140d48e10a401d5839343c250000803f2d0000803f"
    "12050d00002041"
    "0a490a140d9a99d1401d96430b3d250000803f2d0000803f"
    "0a140df6280c401dcdcc4c3e250000803f2d0000803f"
    "0a140d14aea73f1db81e053e250000803f2d0000803f"
    "12050d0000a041"
    "0a490a140df628cc401d6f12833c250000803f2d0000803f"
    "0a140d8fc225401dbc74933c250000803f2d0000803f"
    "0a140dd7a3903f1d0ad7a33c250000803f2d0000803f"
    "12050d00002042"
    "0a490a140d85ebb1401d6f12833c250000803f2d0000803f"
    "0a140d14ae17401dbc74933c250000803f2d0000803f"
    "0a140d000010401d0ad7a33c250000803f2d0000803f"
    "12050d0000a042000000000000000000"
)

def parse_id14(hexstr):
    h = hexstr
    p = 0
    out = []
    for _ in range(5):
        p = h.find("0a140d", p) + 6
        l1 = h2f(h[p:p+8]); p += 8
        p = h.find("1d", p) + 2
        l1a = h2f(h[p:p+8]); p += 8

        p = h.find("0a140d", p) + 6
        l2 = h2f(h[p:p+8]); p += 8
        p = h.find("1d", p) + 2
        l2a = h2f(h[p:p+8]); p += 8

        p = h.find("0a140d", p) + 6
        l3 = h2f(h[p:p+8]); p += 8
        p = h.find("1d", p) + 2
        l3a = h2f(h[p:p+8]); p += 8

        out.append([l1, l1a, l2, l2a, l3, l3a])
        p = h.find("12050d", p) + 6
    return out

def generate_id14(values):
    src = SHARP_ID14_DEFAULT
    out = []
    p = 0
    for i in range(5):
        for j in range(3):
            p = src.find("0a140d", p)
            out.append(src[p:p+6]); p += 6
            out.append(f2h(values[i][j*2]))
            p = src.find("1d", p)
            out.append("1d"); p += 2
            out.append(f2h(values[i][j*2+1]))
        end = src.find("12050d", p)
        out.append(src[p:end+6])
        p = end + 6
    out.append(src[p:])
    return "".join(out)

st.set_page_config(layout="wide")
st.title("Sharp Main ID14 + Luma Denoise")

if "vals" not in st.session_state:
    st.session_state.vals = parse_id14(SHARP_ID14_DEFAULT)

levels = ["Sharp very low", "Sharp low", "Sharp med", "Sharp high", "Sharp very high"]
vals = []

for i, name in enumerate(levels):
    with st.expander(name, True):
        c = st.columns(3)
        l1  = c[0].number_input("L1",  st.session_state.vals[i][0], format="%.4f")
        l1a = c[1].number_input("L1A", st.session_state.vals[i][1], format="%.4f")
        l2  = c[0].number_input("L2",  st.session_state.vals[i][2], format="%.4f")
        l2a = c[1].number_input("L2A", st.session_state.vals[i][3], format="%.4f")
        l3  = c[0].number_input("L3",  st.session_state.vals[i][4], format="%.4f")
        l3a = c[1].number_input("L3A", st.session_state.vals[i][5], format="%.4f")
        vals.append([l1, l1a, l2, l2a, l3, l3a])

if st.button("Generate Sharp ID14 HEX"):
    hexout = generate_id14(vals)
    st.code(hexout)
    st.text_input("Patch", f"0x{SHARP_ID14_ADDR:X}:{hexout}")
