import streamlit as st
import struct
from copy import deepcopy
import numpy as np

def float_to_hex(f):
    return struct.pack('<f', float(f)).hex()

def hex_to_float(h):
    return struct.unpack('<f', bytes.fromhex(h))[0]

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

all_sharp_levels2 = [
    {"name": "Sharp very low",  "default": [4.0, 0.186, 1.0, 0.1520, 1.9, 0.058]},
    {"name": "Sharp low",       "default": [5.2, 0.066, 2.24, 0.1, 2.17, 0.011]},
    {"name": "Sharp med",       "default": [6.55, 0.034, 2.19, 0.2, 1.31, 0.13]},
    {"name": "Sharp high",      "default": [6.38, 0.016, 2.59, 0.018, 1.13, 0.02]},
    {"name": "Sharp very high", "default": [5.56, 0.016, 2.37, 0.018, 2.25, 0.02]},
]

LUMA_DEFAULT_HEX = clean_hex(
    "00000a610a0f0dcdccac3f15cdcccc3d1dae50223f0a0f0dc3f5a83f15cdcccc3d1d95806d3e0a0f0d6666863f15cdcc4c3d1d09997a3e0a0f0d9a99593f15cdcc4c3d1d0e06743e0a0a0dcdcc4c3f1d68ceb13e12050d0000a0401dcdcccc3f250000003f0a610a0f0d0000c03f15cdcccc3d1d65a5113f0a0f0dc3f5a83f15cdcccc3d1d5a469a3e0a0f0dcdcc4c3f159a99993d1d6616913e0a0f0d9a99193f150000803d1df20bbf3e0a0a0d3333333f1dffe6ed3e12050d000020411dcdcccc3f250000003f0a610a0f0d1f856b3f15cdcccc3d1d14fa003f0a0f0d6666863f15cdcccc3d1d49ccbd3e0a0f0d7b142e3f15cdcccc3d1d37e0a43e0a0f0d8fc2f53e159a99993d1d7b0a023f0a0a0d295c0f3f1dd1ff143f12050d0000a0411dcdcccc3f250000003f0a610a0f0d9a99993f159a99193e1d1093243f0a0f0d9a99593f15cdcccc3d1dd08a203f0a0f0dec51b83e15cdcccc3d1d54eef13e0a0f0dcdcccc3e15cdcccc3d1d93d7b93e0a0a0d295c8f3e1daf3c9f3d12050d000020421dcdcccc3f250000003f0a610a0f0d0000803f159a99193e1d1093243f0a0f0d3333733f15cdcccc3d1dd08a203f0a0f0dec51b83e15cdcccc3d1d54eef13e0a0f0dcdcccc3e15cdcccc3d1d93d7b93e0a0a0d295c8f3e1daf3c9f3d12050d0000a0421dcdcccc3f250000003f00"
)

bayer_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.050, 0.244724, 0.80, 0.050, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",      "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",      "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",     "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high","default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]},
]

def generate_bayer_hex(values_list):
    tails = [
        "12050d0000a0401dcdcccc3f250000003f0a610a0f0d",
        "12050d000020411dcdcccc3f250000003f0a610a0f0d",
        "12050d0000a0411dcdcccc3f250000003f0a610a0f0d",
        "12050d000020421dcdcccc3f250000003f0a610a0f0d",
        "12050d0000a0421dcdcccc3f250000003f00",
    ]
    lines = []
    for i, v in enumerate(values_list):
        l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a = v
        level_hex = (
            f"{f2h(l1)}15{f2h(l1a)}1d{f2h(l1b)}0a0f0d"
            f"{f2h(l2)}15{f2h(l2a)}1d{f2h(l2b)}0a0f0d"
            f"{f2h(l3)}15{f2h(l3a)}1d{f2h(l3b)}0a0f0d"
            f"{f2h(l4)}15{f2h(l4a)}1d{f2h(l4b)}0a0a0d"
            f"{f2h(l5)}1d{f2h(l5a)}"
            f"{tails[i]}"
        )
        lines.append(level_hex)
    return "".join(lines)

def parse_bayer_hex(hex_str):
    h = clean_hex(hex_str)
    p = 0
    out = []
    for _ in range(5):
        l1 = h2f(h[p:p+8]); p += 8
        p += 2
        l1a = h2f(h[p:p+8]); p += 8
        p += 2
        l1b = h2f(h[p:p+8]); p += 8
        p += 6
        l2 = h2f(h[p:p+8]); p += 8
        p += 2
        l2a = h2f(h[p:p+8]); p += 8
        p += 2
        l2b = h2f(h[p:p+8]); p += 8
        p += 6
        l3 = h2f(h[p:p+8]); p += 8
        p += 2
        l3a = h2f(h[p:p+8]); p += 8
        p += 2
        l3b = h2f(h[p:p+8]); p += 8
        p += 6
        l4 = h2f(h[p:p+8]); p += 8
        p += 2
        l4a = h2f(h[p:p+8]); p += 8
        p += 2
        l4b = h2f(h[p:p+8]); p += 8
        p += 6
        l5 = h2f(h[p:p+8]); p += 8
        p += 2
        l5a = h2f(h[p:p+8]); p += 8
        p += 44
        out.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])
    return out

st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab2, tab6 = st.tabs(["🔍 Sharp Main ID14", "🌪️ Luma Denoise"])

with tab2:
    st.markdown("### 🔧 Sharp Main ID14")

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
        st.code(SHARP_ID14_DEFAULT_HEX, language="text")

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

with tab6:
    st.markdown("### 🌪️ Luma Denoise")

    if "luma_defaults_loaded" not in st.session_state:
        parsed = parse_bayer_hex(LUMA_DEFAULT_HEX)
        for idx in range(5):
            st.session_state[f"bayer_l1_{idx}_temp"] = float(round(parsed[idx][0], 6))
            st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(parsed[idx][1], 6))
            st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(parsed[idx][2], 6))
            st.session_state[f"bayer_l2_{idx}_temp"] = float(round(parsed[idx][3], 6))
            st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(parsed[idx][4], 6))
            st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(parsed[idx][5], 6))
            st.session_state[f"bayer_l3_{idx}_temp"] = float(round(parsed[idx][6], 6))
            st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(parsed[idx][7], 6))
            st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(parsed[idx][8], 6))
            st.session_state[f"bayer_l4_{idx}_temp"] = float(round(parsed[idx][9], 6))
            st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(parsed[idx][10], 6))
            st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(parsed[idx][11], 6))
            st.session_state[f"bayer_l5_{idx}_temp"] = float(round(parsed[idx][12], 6))
            st.session_state[f"bayer_l5a_{idx}_temp"] = float(round(parsed[idx][13], 6))
        st.session_state.luma_defaults_loaded = True

    bayer_inputs = []
    for idx, level in enumerate(bayer_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)

            l1 = cols[0].number_input("L1", value=st.session_state.get(f"bayer_l1_{idx}_temp", level["default"][0]), format="%.6f", key=f"bayer_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"bayer_l1a_{idx}_temp", level["default"][1]), format="%.6f", key=f"bayer_l1a_{idx}")
            l1b = cols[2].number_input("L1B", value=st.session_state.get(f"bayer_l1b_{idx}_temp", level["default"][2]), format="%.6f", key=f"bayer_l1b_{idx}")

            l2 = cols[0].number_input("L2", value=st.session_state.get(f"bayer_l2_{idx}_temp", level["default"][3]), format="%.6f", key=f"bayer_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"bayer_l2a_{idx}_temp", level["default"][4]), format="%.6f", key=f"bayer_l2a_{idx}")
            l2b = cols[2].number_input("L2B", value=st.session_state.get(f"bayer_l2b_{idx}_temp", level["default"][5]), format="%.6f", key=f"bayer_l2b_{idx}")

            l3 = cols[0].number_input("L3", value=st.session_state.get(f"bayer_l3_{idx}_temp", level["default"][6]), format="%.6f", key=f"bayer_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"bayer_l3a_{idx}_temp", level["default"][7]), format="%.6f", key=f"bayer_l3a_{idx}")
            l3b = cols[2].number_input("L3B", value=st.session_state.get(f"bayer_l3b_{idx}_temp", level["default"][8]), format="%.6f", key=f"bayer_l3b_{idx}")

            l4 = cols[0].number_input("L4", value=st.session_state.get(f"bayer_l4_{idx}_temp", level["default"][9]), format="%.6f", key=f"bayer_l4_{idx}")
            l4a = cols[1].number_input("L4A", value=st.session_state.get(f"bayer_l4a_{idx}_temp", level["default"][10]), format="%.6f", key=f"bayer_l4a_{idx}")
            l4b = cols[2].number_input("L4B", value=st.session_state.get(f"bayer_l4b_{idx}_temp", level["default"][11]), format="%.6f", key=f"bayer_l4b_{idx}")

            l5 = cols[0].number_input("L5", value=st.session_state.get(f"bayer_l5_{idx}_temp", level["default"][12]), format="%.6f", key=f"bayer_l5_{idx}")
            l5a = cols[1].number_input("L5A", value=st.session_state.get(f"bayer_l5a_{idx}_temp", level["default"][13]), format="%.6f", key=f"bayer_l5a_{idx}")

            bayer_inputs.append([l1, l1a, l1b, l2, l2a, l2b, l3, l3a, l3b, l4, l4a, l4b, l5, l5a])

    if st.button("🚀 Сгенерировать HEX (Luma Denoise)", key="gen_luma"):
        full_hex = generate_bayer_hex(bayer_inputs)
        st.code(full_hex, language="text")

    with st.expander("Парсер для Luma Denoise", expanded=False):
        hex_input_bayer = st.text_area("Вставь HEX-строку сюда:", value=LUMA_DEFAULT_HEX, height=200, key="bayer_parser_input_inside")
        if st.button("🔍 Распарсить HEX (Luma автозаполнение)", key="parse_luma"):
            parsed = parse_bayer_hex(hex_input_bayer)
            for idx in range(5):
                st.session_state[f"bayer_l1_{idx}_temp"] = float(round(parsed[idx][0], 6))
                st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(parsed[idx][1], 6))
                st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(parsed[idx][2], 6))
                st.session_state[f"bayer_l2_{idx}_temp"] = float(round(parsed[idx][3], 6))
                st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(parsed[idx][4], 6))
                st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(parsed[idx][5], 6))
                st.session_state[f"bayer_l3_{idx}_temp"] = float(round(parsed[idx][6], 6))
                st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(parsed[idx][7], 6))
                st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(parsed[idx][8], 6))
                st.session_state[f"bayer_l4_{idx}_temp"] = float(round(parsed[idx][9], 6))
                st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(parsed[idx][10], 6))
                st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(parsed[idx][11], 6))
                st.session_state[f"bayer_l5_{idx}_temp"] = float(round(parsed[idx][12], 6))
                st.session_state[f"bayer_l5a_{idx}_temp"] = float(round(parsed[idx][13], 6))
            st.success("✅ Поля Luma Denoise обновлены")
            st.rerun()
```0
