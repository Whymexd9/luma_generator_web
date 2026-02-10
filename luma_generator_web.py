import streamlit as st
import struct
from copy import deepcopy

def float_to_hex(f):
    return struct.pack("<f", float(f)).hex()

def hex_to_float(h):
    return struct.unpack("<f", bytes.fromhex(h))[0]

def norm_hex(s: str) -> str:
    return "".join(c for c in s.lower().strip() if c in "0123456789abcdef")

SHARP_MAIN_ID14_ADDR = 0x110E63E
SHARP_MAIN_ID14_DEFAULT_HEX = norm_hex(
    "0a490a140d000080401dc9763e3e250000803f2d0000803f0a140d0000803f1de3a51b3e250000803f2d0000803f0a140d3333f33f1d68916d3d250000803f2d0000803f12050d0000a0400a490a140d6666a6401d022b873d250000803f2d0000803f0a140d295c0f401dcdcccc3d250000803f2d0000803f0a140d48e10a401d5839343c250000803f2d0000803f12050d000020410a490a140d9a99d1401d96430b3d250000803f2d0000803f0a140df6280c401dcdcc4c3e250000803f2d0000803f0a140d14aea73f1db81e053e250000803f2d0000803f12050d0000a0410a490a140df628cc401d6f12833c250000803f2d0000803f0a140d8fc225401dbc74933c250000803f2d0000803f0a140dd7a3903f1d0ad7a33c250000803f2d0000803f12050d000020420a490a140d85ebb1401d6f12833c250000803f2d0000803f0a140d14ae17401dbc74933c250000803f2d0000803f0a140d000010401d0ad7a33c250000803f2d0000803f12050d0000a042000000000000000000"
)

LUMA_DENOISE_ADDR = 0x110A2EE
LUMA_DENOISE_DEFAULT_HEX = norm_hex(
    "00000a610a0f0dcdccac3f15cdcccc3d1dae50223f0a0f0dc3f5a83f15cdcccc3d1d95806d3e0a0f0d6666863f15cdcc4c3d1d09997a3e0a0f0d9a99593f15cdcc4c3d1d0e06743e0a0a0dcdcc4c3f1d68ceb13e12050d0000a0401dcdcccc3f250000003f0a610a0f0d0000c03f15cdcccc3d1d65a5113f0a0f0dc3f5a83f15cdcccc3d1d5a469a3e0a0f0dcdcc4c3f159a99993d1d6616913e0a0f0d9a99193f150000803d1df20bbf3e0a0a0d3333333f1dffe6ed3e12050d000020411dcdcccc3f250000003f0a610a0f0d1f856b3f15cdcccc3d1d14fa003f0a0f0d6666863f15cdcccc3d1d49ccbd3e0a0f0d7b142e3f15cdcccc3d1d37e0a43e0a0f0d8fc2f53e159a99993d1d7b0a023f0a0a0d295c0f3f1dd1ff143f12050d0000a0411dcdcccc3f250000003f0a610a0f0d9a99993f159a99193e1d1093243f0a0f0d9a99593f15cdcccc3d1dd08a203f0a0f0dec51b83e15cdcccc3d1d54eef13e0a0f0dcdcccc3e15cdcccc3d1d93d7b93e0a0a0d295c8f3e1daf3c9f3d12050d000020421dcdcccc3f250000003f0a610a0f0d0000803f159a99193e1d1093243f0a0f0d3333733f15cdcccc3d1dd08a203f0a0f0dec51b83e15cdcccc3d1d54eef13e0a0f0dcdcccc3e15cdcccc3d1d93d7b93e0a0a0d295c8f3e1daf3c9f3d12050d0000a0421dcdcccc3f250000003f00"
)

levels_sharp = ["Sharp very low", "Sharp low", "Sharp med", "Sharp high", "Sharp very high"]

original_sharp_hex_lines = [
    "0a490a140d000080401dc9763e3e",
    "250000803f2d0000803f0a140d",
    "0000803f1de3a51b3e250000803f2d0000803f0a140d3333f33f1d68916d3d",
    "250000803f2d0000803f12050d",
    "3333f33f1d68916d3d",
    "250000803f2d0000803f12050d",
    "0000a0400a490a140d6666a6401d022b873d",
    "250000803f2d0000803f0a140d",
    "295c0f401dcdcccc3d",
    "250000803f2d0000803f0a140d",
    "48e10a401d5839343c",
    "250000803f2d0000803f12050d",
    "000020410a490a140d9a99d1401d96430b3d",
    "250000803f2d0000803f0a140d",
    "f6280c401dcdcc4c3e",
    "250000803f2d0000803f0a140d",
    "14aea73f1db81e053e",
    "250000803f2d0000803f12050d",
    "0000a0410a490a140df628cc401d6f12833c",
    "250000803f2d0000803f0a140d",
    "8fc225401dbc74933c",
    "250000803f2d0000803f0a140d",
    "d7a3903f1d0ad7a33c",
    "250000803f2d0000803f12050d",
    "000020420a490a140d85ebb1401d6f12833c",
    "250000803f2d0000803f0a140d",
    "14ae17401dbc74933c",
    "250000803f2d0000803f0a140d",
    "000010401d0ad7a33c",
    "250000803f2d0000803f12050d0000a042000000000000000000",
]

sharp_slices = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30),
}

def parse_sharp_id14(hexstr):
    h = norm_hex(hexstr)
    out = []
    p = 0
    for _ in range(5):
        p = h.find("0a140d", p) + 6
        l1 = hex_to_float(h[p:p+8]); p += 8
        p = h.find("1d", p) + 2
        l1a = hex_to_float(h[p:p+8]); p += 8

        p = h.find("0a140d", p) + 6
        l2 = hex_to_float(h[p:p+8]); p += 8
        p = h.find("1d", p) + 2
        l2a = hex_to_float(h[p:p+8]); p += 8

        p = h.find("0a140d", p) + 6
        l3 = hex_to_float(h[p:p+8]); p += 8
        p = h.find("1d", p) + 2
        l3a = hex_to_float(h[p:p+8]); p += 8

        out.append([l1, l1a, l2, l2a, l3, l3a])
        p = h.find("12050d", p) + 6
    return out

def generate_sharp_id14(vals):
    lines = []
    for i, name in enumerate(levels_sharp):
        start, end = sharp_slices[name]
        block = deepcopy(original_sharp_hex_lines[start:end])
        block[0] = f"0a490a140d{float_to_hex(vals[i][0])}1d{float_to_hex(vals[i][1])}"
        block[2] = f"{float_to_hex(vals[i][2])}1d{float_to_hex(vals[i][3])}{block[2][18:]}"
        block[4] = f"{float_to_hex(vals[i][4])}1d{float_to_hex(vals[i][5])}{block[4][18:]}"
        lines.extend(block)
    return "".join(lines)

bayer_blocks = {
    "Bayer luma denoise very low": [
        "00000a610a0f0d",
        "cdccac3f",
        "15",
        "cdcccc3d",
        "1d",
        "ae50223f",
        "0a0f0d",
        "c3f5a83f",
        "15",
        "cdcccc3d",
        "1d",
        "95806d3e",
        "0a0f0d",
        "6666863f",
        "15",
        "cdcc4c3d",
        "1d",
        "09997a3e",
        "0a0f0d",
        "9a99593f",
        "15",
        "cdcc4c3d",
        "1d",
        "0e06743e",
        "0a0a0d",
        "cdcc4c3f",
        "1d",
        "68ceb13e",
        "12050d0000a0401dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise low": [
        "0000c03f",
        "15",
        "cdcccc3d",
        "1d",
        "65a5113f",
        "0a0f0d",
        "c3f5a83f",
        "15",
        "cdcccc3d",
        "1d",
        "5a469a3e",
        "0a0f0d",
        "cdcc4c3f",
        "15",
        "9a99993d",
        "1d",
        "6616913e",
        "0a0f0d",
        "9a99193f",
        "15",
        "0000803d",
        "1d",
        "f20bbf3e",
        "0a0a0d",
        "295c0f3f",
        "1d",
        "d1ff143f",
        "12050d000020411dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise med": [
        "1f856b3f",
        "15",
        "cdcccc3d",
        "1d",
        "14fa003f",
        "0a0f0d",
        "6666863f",
        "15",
        "cdcccc3d",
        "1d",
        "49ccbd3e",
        "0a0f0d",
        "7b142e3f",
        "15",
        "cdcccc3d",
        "1d",
        "37e0a43e",
        "0a0f0d",
        "8fc2f53e",
        "15",
        "9a99993d",
        "1d",
        "7b0a023f",
        "0a0a0d",
        "295c0f3f",
        "1d",
        "d1ff143f",
        "12050d0000a0411dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise high": [
        "9a99993f",
        "15",
        "9a99193e",
        "1d",
        "1093243f",
        "0a0f0d",
        "9a99593f",
        "15",
        "cdcccc3d",
        "1d",
        "d08a203f",
        "0a0f0d",
        "ec51b83e",
        "15",
        "cdcccc3d",
        "1d",
        "54eef13e",
        "0a0f0d",
        "cdcccc3e",
        "15",
        "cdcccc3d",
        "1d",
        "93d7b93e",
        "0a0a0d",
        "295c8f3e",
        "1d",
        "af3c9f3d",
        "12050d000020421dcdcccc3f250000003f0a610a0f0d"
    ],
    "Bayer luma denoise very high": [
        "0000803f",
        "15",
        "9a99193e",
        "1d",
        "1093243f",
        "0a0f0d",
        "3333733f",
        "15",
        "cdcccc3d",
        "1d",
        "d08a203f",
        "0a0f0d",
        "ec51b83e",
        "15",
        "cdcccc3d",
        "1d",
        "54eef13e",
        "0a0f0d",
        "cdcccc3e",
        "15",
        "cdcccc3d",
        "1d",
        "93d7b93e",
        "0a0a0d",
        "295c8f3e",
        "1d",
        "af3c9f3d",
        "12050d0000a0421dcdcccc3f250000003f00"
    ]
}

bayer_levels = [
    {"name": "Bayer luma denoise very low", "default": [1.00, 0.10, 0.634044, 0.90, 0.10, 0.231936, 0.85, 0.050, 0.244724, 0.80, 0.050, 0.238304, 0.75, 0.347278]},
    {"name": "Bayer luma denoise low",      "default": [0.80, 0.10, 0.568930, 0.70, 0.10, 0.301318, 0.70, 0.075, 0.283374, 0.60, 0.0625, 0.373138, 0.70, 0.464653]},
    {"name": "Bayer luma denoise med",      "default": [0.70, 0.10, 0.503816, 0.80, 0.10, 0.370699, 0.60, 0.10, 0.322023, 0.40, 0.075, 0.507972, 0.50, 0.582028]},
    {"name": "Bayer luma denoise high",     "default": [0.60, 0.15, 0.642869, 0.50, 0.10, 0.627118, 0.25, 0.10, 0.472521, 0.25, 0.10, 0.362973, 0.20, 0.0777525]},
    {"name": "Bayer luma denoise very high", "default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
]

def generate_bayer_hex(values_list, level_names):
    lines = []
    for i, values in enumerate(values_list):
        name = level_names[i]["name"]
        block = deepcopy(bayer_blocks[name])
        if name == "Bayer luma denoise very low":
            idxs = [1,3,5, 7,9,11, 13,15,17, 19,21,23, 25,27]
        else:
            idxs = [0,2,4, 6,8,10, 12,14,16, 18,20,22, 24,26]
        repl = [
            float_to_hex(values[0]), float_to_hex(values[1]), float_to_hex(values[2]),
            float_to_hex(values[3]), float_to_hex(values[4]), float_to_hex(values[5]),
            float_to_hex(values[6]), float_to_hex(values[7]), float_to_hex(values[8]),
            float_to_hex(values[9]), float_to_hex(values[10]), float_to_hex(values[11]),
            float_to_hex(values[12]), float_to_hex(values[13]),
        ]
        for pos, hx in zip(idxs, repl):
            block[pos] = hx
        lines.append("".join(block))
    return "".join(lines)

def parse_bayer_hex(hexstr):
    h = norm_hex(hexstr)
    offset = 0
    out = []
    for idx in range(5):
        l1 = h[offset:offset+8]; offset += 8 + 2
        l1a = h[offset:offset+8]; offset += 8 + 2
        l1b = h[offset:offset+8]; offset += 8 + 6
        l2 = h[offset:offset+8]; offset += 8 + 2
        l2a = h[offset:offset+8]; offset += 8 + 2
        l2b = h[offset:offset+8]; offset += 8 + 6
        l3 = h[offset:offset+8]; offset += 8 + 2
        l3a = h[offset:offset+8]; offset += 8 + 2
        l3b = h[offset:offset+8]; offset += 8 + 6
        l4 = h[offset:offset+8]; offset += 8 + 2
        l4a = h[offset:offset+8]; offset += 8 + 2
        l4b = h[offset:offset+8]; offset += 8 + 6
        l5 = h[offset:offset+8]; offset += 8 + 2
        l5a = h[offset:offset+8]; offset += 8 + 44
        out.append([
            hex_to_float(l1), hex_to_float(l1a), hex_to_float(l1b),
            hex_to_float(l2), hex_to_float(l2a), hex_to_float(l2b),
            hex_to_float(l3), hex_to_float(l3a), hex_to_float(l3b),
            hex_to_float(l4), hex_to_float(l4a), hex_to_float(l4b),
            hex_to_float(l5), hex_to_float(l5a),
        ])
    return out

st.set_page_config(page_title="HEX Generator", layout="wide")
st.title("🔧 Sharp Main ID14 + Luma Denoise")

tab1, tab2 = st.tabs(["🔍 Sharp Main ID14", "🌪️ Luma Denoise"])

with tab1:
    if "id14_loaded" not in st.session_state:
        parsed = parse_sharp_id14(SHARP_MAIN_ID14_DEFAULT_HEX)
        for idx in range(5):
            st.session_state[f"id14_l1_{idx}_temp"] = float(round(parsed[idx][0], 6))
            st.session_state[f"id14_l1a_{idx}_temp"] = float(round(parsed[idx][1], 6))
            st.session_state[f"id14_l2_{idx}_temp"] = float(round(parsed[idx][2], 6))
            st.session_state[f"id14_l2a_{idx}_temp"] = float(round(parsed[idx][3], 6))
            st.session_state[f"id14_l3_{idx}_temp"] = float(round(parsed[idx][4], 6))
            st.session_state[f"id14_l3a_{idx}_temp"] = float(round(parsed[idx][5], 6))
        st.session_state["id14_loaded"] = True

    id14_inputs = []
    for idx, name in enumerate(levels_sharp):
        with st.expander(name, expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"id14_l1_{idx}_temp", 0.0), format="%.4f", key=f"id14_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"id14_l1a_{idx}_temp", 0.0), format="%.4f", key=f"id14_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"id14_l2_{idx}_temp", 0.0), format="%.4f", key=f"id14_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"id14_l2a_{idx}_temp", 0.0), format="%.4f", key=f"id14_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"id14_l3_{idx}_temp", 0.0), format="%.4f", key=f"id14_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"id14_l3a_{idx}_temp", 0.0), format="%.4f", key=f"id14_l3a_{idx}")
            id14_inputs.append([l1, l1a, l2, l2a, l3, l3a])

    if st.button("🚀 Сгенерировать Sharp Main ID14 HEX"):
        full_hex = generate_sharp_id14(id14_inputs)
        st.code(full_hex, language="text")
        st.text_input("Patch line", value=f"0x{SHARP_MAIN_ID14_ADDR:X}:{full_hex}", key="id14_patchline")

    with st.expander("🔸Парсер Sharp Main ID14", expanded=False):
        hex_input_id14 = st.text_area("HEX для Sharp Main ID14:", value=SHARP_MAIN_ID14_DEFAULT_HEX, height=200, key="id14_parser_input")
        if st.button("🔍 Распарсить Sharp Main ID14 HEX"):
            if not hex_input_id14.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    parsed = parse_sharp_id14(hex_input_id14)
                    for idx in range(5):
                        st.session_state[f"id14_l1_{idx}_temp"] = float(round(parsed[idx][0], 6))
                        st.session_state[f"id14_l1a_{idx}_temp"] = float(round(parsed[idx][1], 6))
                        st.session_state[f"id14_l2_{idx}_temp"] = float(round(parsed[idx][2], 6))
                        st.session_state[f"id14_l2a_{idx}_temp"] = float(round(parsed[idx][3], 6))
                        st.session_state[f"id14_l3_{idx}_temp"] = float(round(parsed[idx][4], 6))
                        st.session_state[f"id14_l3a_{idx}_temp"] = float(round(parsed[idx][5], 6))
                    st.success("✅ Поля Sharp Main ID14 обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Sharp Main ID14: {e}")

with tab2:
    if "luma_loaded" not in st.session_state:
        parsed = parse_bayer_hex(LUMA_DENOISE_DEFAULT_HEX)
        for idx in range(5):
            vals = parsed[idx]
            st.session_state[f"bayer_l1_{idx}_temp"] = float(round(vals[0], 6))
            st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(vals[1], 6))
            st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(vals[2], 6))
            st.session_state[f"bayer_l2_{idx}_temp"] = float(round(vals[3], 6))
            st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(vals[4], 6))
            st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(vals[5], 6))
            st.session_state[f"bayer_l3_{idx}_temp"] = float(round(vals[6], 6))
            st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(vals[7], 6))
            st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(vals[8], 6))
            st.session_state[f"bayer_l4_{idx}_temp"] = float(round(vals[9], 6))
            st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(vals[10], 6))
            st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(vals[11], 6))
            st.session_state[f"bayer_l5_{idx}_temp"] = float(round(vals[12], 6))
            st.session_state[f"bayer_l5a_{idx}_temp"] = float(round(vals[13], 6))
        st.session_state["luma_loaded"] = True

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

    if st.button("🚀 Сгенерировать HEX (Luma Denoise)"):
        full_hex = generate_bayer_hex(bayer_inputs, bayer_levels)
        st.code(full_hex, language="text")
        st.text_input("Patch line", value=f"0x{LUMA_DENOISE_ADDR:X}:{full_hex}", key="luma_patchline")

    with st.expander("🔸Парсер Luma Denoise", expanded=False):
        hex_input_bayer = st.text_area("HEX:", value=LUMA_DENOISE_DEFAULT_HEX, height=200, key="bayer_parser_input")
        if st.button("🔍 Распарсить Luma Denoise HEX"):
            if not hex_input_bayer.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    parsed = parse_bayer_hex(hex_input_bayer)
                    for idx in range(5):
                        vals = parsed[idx]
                        st.session_state[f"bayer_l1_{idx}_temp"] = float(round(vals[0], 6))
                        st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(vals[1], 6))
                        st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(vals[2], 6))
                        st.session_state[f"bayer_l2_{idx}_temp"] = float(round(vals[3], 6))
                        st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(vals[4], 6))
                        st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(vals[5], 6))
                        st.session_state[f"bayer_l3_{idx}_temp"] = float(round(vals[6], 6))
                        st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(vals[7], 6))
                        st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(vals[8], 6))
                        st.session_state[f"bayer_l4_{idx}_temp"] = float(round(vals[9], 6))
                        st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(vals[10], 6))
                        st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(vals[11], 6))
                        st.session_state[f"bayer_l5_{idx}_temp"] = float(round(vals[12], 6))
          
