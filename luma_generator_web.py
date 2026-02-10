import streamlit as st
import struct

def float_to_hex(f):
    return struct.pack("<f", float(f)).hex()

def hex_to_float(h):
    return struct.unpack("<f", bytes.fromhex(h))[0]

def clean_hex(s):
    return "".join(c for c in s.lower() if c in "0123456789abcdef")

SHARP_ID14_DEFAULT_HEX = clean_hex(
    "0a490a140d000080401dc9763e3e250000803f2d0000803f0a140d0000803f1de3a51b3e250000803f2d0000803f0a140d3333f33f1d68916d3d250000803f2d0000803f12050d0000a040"
    "0a490a140d6666a6401d022b873d250000803f2d0000803f0a140d295c0f401dcdcccc3d250000803f2d0000803f0a140d48e10a401d5839343c250000803f2d0000803f12050d00002041"
    "0a490a140d9a99d1401d96430b3d250000803f2d0000803f0a140df6280c401dcdcc4c3e250000803f2d0000803f0a140d14aea73f1db81e053e250000803f2d0000803f12050d0000a041"
    "0a490a140df628cc401d6f12833c250000803f2d0000803f0a140d8fc225401dbc74933c250000803f2d0000803f0a140dd7a3903f1d0ad7a33c250000803f2d0000803f12050d00002042"
    "0a490a140d85ebb1401d6f12833c250000803f2d0000803f0a140d14ae17401dbc74933c250000803f2d0000803f0a140d000010401d0ad7a33c250000803f2d0000803f12050d0000a042"
    "000000000000000000"
)

original_blocks = [SHARP_ID14_DEFAULT_HEX[i:i+240] for i in range(0, len(SHARP_ID14_DEFAULT_HEX), 240)]

default_values = [
    [4.0, 0.186, 1.0, 0.152, 1.9, 0.058],
    [5.2, 0.066, 2.24, 0.1, 2.17, 0.011],
    [6.55, 0.034, 2.19, 0.2, 1.31, 0.13],
    [6.38, 0.016, 2.59, 0.018, 1.13, 0.02],
    [5.56, 0.016, 2.37, 0.018, 2.25, 0.02],
]

def generate_id14(values):
    result = []
    for i in range(5):
        block = original_blocks[i]
        out = ""
        idx = 0
        for j in range(3):
            out += block[idx:idx+6]
            idx += 6
            out += float_to_hex(values[i][j*2])
            out += block[idx+8:idx+10]
            idx += 10
            out += float_to_hex(values[i][j*2+1])
            idx += 8
        out += block[idx:]
        result.append(out)
    return "".join(result)

def parse_id14(hex_str):
    s = clean_hex(hex_str)
    vals = []
    offset = 0
    for _ in range(5):
        offset += 6
        l1 = s[offset:offset+8]; offset += 8
        offset += 2
        l1a = s[offset:offset+8]; offset += 8
        offset += 24

        offset += 6
        l2 = s[offset:offset+8]; offset += 8
        offset += 2
        l2a = s[offset:offset+8]; offset += 8
        offset += 24

        offset += 6
        l3 = s[offset:offset+8]; offset += 8
        offset += 2
        l3a = s[offset:offset+8]; offset += 8
        offset += 42

        vals.append([hex_to_float(l1), hex_to_float(l1a), hex_to_float(l2), hex_to_float(l2a), hex_to_float(l3), hex_to_float(l3a)])
    return vals

st.set_page_config(layout="wide")
st.title("Sharp Main ID14")

if "vals" not in st.session_state:
    st.session_state.vals = [v[:] for v in default_values]

with st.expander("🔸Парсер Sharp Main ID14", expanded=False):
    hex_input = st.text_area("HEX для Sharp ID14:", value=SHARP_ID14_DEFAULT_HEX, height=200, key="hex_in")
    if st.button("🔍 Распарсить и заполнить поля", key="do_parse"):
        st.session_state.vals = parse_id14(hex_input)
        st.rerun()

inputs = []
for i in range(5):
    with st.expander(f"Sharp level {i}", True):
        c = st.columns(3)
        l1  = c[0].number_input("L1",  value=float(st.session_state.vals[i][0]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l1_{i}")
        l1a = c[1].number_input("L1A", value=float(st.session_state.vals[i][1]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l1a_{i}")
        l2  = c[0].number_input("L2",  value=float(st.session_state.vals[i][2]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l2_{i}")
        l2a = c[1].number_input("L2A", value=float(st.session_state.vals[i][3]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l2a_{i}")
        l3  = c[0].number_input("L3",  value=float(st.session_state.vals[i][4]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l3_{i}")
        l3a = c[1].number_input("L3A", value=float(st.session_state.vals[i][5]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l3a_{i}")
        inputs.append([l1, l1a, l2, l2a, l3, l3a])

if st.button("Generate HEX", key="gen"):
    st.code(generate_id14(inputs), language="text")
```0
