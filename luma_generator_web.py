import streamlit as st
import struct
from copy import deepcopy

def float_to_hex(f):
    return struct.pack("<f", float(f)).hex()

def hex_to_float(h):
    return struct.unpack("<f", bytes.fromhex(h))[0]

def clean_hex(s):
    return "".join(c for c in s.lower() if c in "0123456789abcdef")

original_sharp_hex_lines2 = [
    "000080401dc9763e3e",
    "250000803f2d0000803f0a140d",
    "0000803f1de3a51b3e",
    "250000803f2d0000803f0a140d",
    "3333f33f1d68916d3d",
    "250000803f2d0000803f12050d0000a0400a490a140d",
    "0000a0400a490a140d6666a6401d022b873d",
    "250000803f2d0000803f0a140d",
    "295c0f401dcdcccc3d",
    "250000803f2d0000803f0a140d",
    "48e10a401d5839343c",
    "250000803f2d0000803f12050d000020410a490a140d",
    "000020410a490a140d9a99d1401d96430b3d",
    "250000803f2d0000803f0a140d",
    "f6280c401dcdcc4c3e",
    "250000803f2d0000803f0a140d",
    "14aea73f1db81e053e",
    "250000803f2d0000803f12050d0000a0410a490a140d",
    "0000a0410a490a140df628cc401d6f12833c",
    "250000803f2d0000803f0a140d",
    "8fc225401dbc74933c",
    "250000803f2d0000803f0a140d",
    "d7a3903f1d0ad7a33c",
    "250000803f2d0000803f12050d000020420a490a140d",
    "000020420a490a140d85ebb1401d6f12833c",
    "250000803f2d0000803f0a140d",
    "14ae17401dbc74933c",
    "250000803f2d0000803f0a140d",
    "000010401d0ad7a33c",
    "250000803f2d0000803f12050d0000a042000000000000000000",
]

sharp_slices_id14 = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
}

all_sharp_levels2 = [
    {"name": "Sharp very low",  "default": [4.0, 0.186, 1.0, 0.1520, 1.9, 0.058]},
    {"name": "Sharp low",       "default": [5.2, 0.066, 2.24, 0.1, 2.17, 0.011]},
    {"name": "Sharp med",       "default": [6.55, 0.034, 2.19, 0.2, 1.31, 0.13]},
    {"name": "Sharp high",      "default": [6.38, 0.016, 2.59, 0.018, 1.13, 0.02]},
    {"name": "Sharp very high", "default": [5.56, 0.016, 2.37, 0.018, 2.25, 0.02]},
]

SHARP_ID14_DEFAULT_HEX = clean_hex(
    "0a490a140d000080401dc9763e3e250000803f2d0000803f0a140d0000803f1de3a51b3e250000803f2d0000803f0a140d3333f33f1d68916d3d250000803f2d0000803f12050d0000a0400a490a140d6666a6401d022b873d250000803f2d0000803f0a140d295c0f401dcdcccc3d250000803f2d0000803f0a140d48e10a401d5839343c250000803f2d0000803f12050d000020410a490a140d9a99d1401d96430b3d250000803f2d0000803f0a140df6280c401dcdcc4c3e250000803f2d0000803f0a140d14aea73f1db81e053e250000803f2d0000803f12050d0000a0410a490a140df628cc401d6f12833c250000803f2d0000803f0a140d8fc225401dbc74933c250000803f2d0000803f0a140dd7a3903f1d0ad7a33c250000803f2d0000803f12050d000020420a490a140d85ebb1401d6f12833c250000803f2d0000803f0a140d14ae17401dbc74933c250000803f2d0000803f0a140d000010401d0ad7a33c250000803f2d0000803f12050d0000a042000000000000000000"
)

def generate_sharp_hex_id14(values_list, level_names, level_slices):
    lines = []
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]
        modified_block = deepcopy(original_sharp_hex_lines2[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"
        lines.extend(modified_block)
    return "".join(lines)

st.set_page_config(page_title="HEX Sharp ID14 Generator", layout="wide")
st.title("🔧 Sharp Main ID14 HEX Code Generator")

sharp_inputs2 = []
for idx, level in enumerate(all_sharp_levels2):
    with st.expander(level["name"], expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=st.session_state.get(f"2sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"2sharp_l1_{idx}")
        l1a = cols[1].number_input("L1A", value=st.session_state.get(f"2sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"2sharp_l1a_{idx}")
        l2 = cols[0].number_input("L2", value=st.session_state.get(f"2sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"2sharp_l2_{idx}")
        l2a = cols[1].number_input("L2A", value=st.session_state.get(f"2sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"2sharp_l2a_{idx}")
        l3 = cols[0].number_input("L3", value=st.session_state.get(f"2sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"2sharp_l3_{idx}")
        l3a = cols[1].number_input("L3A", value=st.session_state.get(f"2sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"2sharp_l3a_{idx}")
        sharp_inputs2.append([l1, l1a, l2, l2a, l3, l3a])

if st.button("🚀 Сгенерировать Sharp HEX ID14", key="gen_id14"):
    full_hex = generate_sharp_hex_id14(sharp_inputs2, all_sharp_levels2, sharp_slices_id14)
    st.code(full_hex, language="text")

with st.expander("🔸Парсер Sharp Main ID14", expanded=False):
    hex_input_main2 = st.text_area("HEX для Main Sharp ID14:", value=SHARP_ID14_DEFAULT_HEX, height=200, key="main_parser_input2")
    if st.button("🔍 Распарсить Main Sharp HEX ID14", key="parse_id14"):
        s = clean_hex(hex_input_main2)
        offset = 0
        results = []
        for _ in range(5):
            l1 = s[offset:offset+8]; offset += 8 + 2
            l1a = s[offset:offset+8]; offset += 8 + 26
            l2 = s[offset:offset+8]; offset += 8 + 2
            l2a = s[offset:offset+8]; offset += 8 + 26
            l3 = s[offset:offset+8]; offset += 8 + 2
            l3a = s[offset:offset+8]; offset += 8 + 44
            results.append([l1, l1a, l2, l2a, l3, l3a])

        for idx, (l1, l1a, l2, l2a, l3, l3a) in enumerate(results):
            st.session_state[f"2sharp_l1_{idx}_temp"] = float(round(hex_to_float(l1), 6))
            st.session_state[f"2sharp_l1a_{idx}_temp"] = float(round(hex_to_float(l1a), 6))
            st.session_state[f"2sharp_l2_{idx}_temp"] = float(round(hex_to_float(l2), 6))
            st.session_state[f"2sharp_l2a_{idx}_temp"] = float(round(hex_to_float(l2a), 6))
            st.session_state[f"2sharp_l3_{idx}_temp"] = float(round(hex_to_float(l3), 6))
            st.session_state[f"2sharp_l3a_{idx}_temp"] = float(round(hex_to_float(l3a), 6))

        st.success("✅ Поля Main Sharp ID14 обновлены")
        st.rerun()
```0
