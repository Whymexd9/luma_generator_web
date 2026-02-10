import streamlit as st
import struct
from copy import deepcopy

def float_to_hex(f):
    return struct.pack("<f", float(f)).hex()

def hex_to_float(h):
    return struct.unpack("<f", bytes.fromhex(h))[0]

def normalize_hex(s: str) -> str:
    return "".join(ch for ch in s.strip().lower() if ch in "0123456789abcdef")

SHARP_MAIN_ID14_ADDR = 0x110E63E
SHARP_MAIN_ID14_DEFAULT_HEX = normalize_hex(
    "0a490a140d000080401dc9763e3e250000803f2d0000803f0a140d0000803f1de3a51b3e250000803f2d0000803f0a140d3333f33f1d68916d3d250000803f2d0000803f12050d0000a0400a490a140d6666a6401d022b873d250000803f2d0000803f0a140d295c0f401dcdcccc3d250000803f2d0000803f0a140d48e10a401d5839343c250000803f2d0000803f12050d000020410a490a140d9a99d1401d96430b3d250000803f2d0000803f0a140df6280c401dcdcc4c3e250000803f2d0000803f0a140d14aea73f1db81e053e250000803f2d0000803f12050d0000a0410a490a140df628cc401d6f12833c250000803f2d0000803f0a140d8fc225401dbc74933c250000803f2d0000803f0a140dd7a3903f1d0ad7a33c250000803f2d0000803f12050d000020420a490a140d85ebb1401d6f12833c250000803f2d0000803f0a140d14ae17401dbc74933c250000803f2d0000803f0a140d000010401d0ad7a33c250000803f2d0000803f12050d0000a042000000000000000000"
)

LUMA_DENOISE_ADDR = 0x110A2EE
LUMA_DENOISE_DEFAULT_HEX = normalize_hex(
    "00000a610a0f0dcdccac3f15cdcccc3d1dae50223f0a0f0dc3f5a83f15cdcccc3d1d95806d3e0a0f0d6666863f15cdcc4c3d1d09997a3e0a0f0d9a99593f15cdcc4c3d1d0e06743e0a0a0dcdcc4c3f1d68ceb13e12050d0000a0401dcdcccc3f250000003f0a610a0f0d0000c03f15cdcccc3d1d65a5113f0a0f0dc3f5a83f15cdcccc3d1d5a469a3e0a0f0dcdcc4c3f159a99993d1d6616913e0a0f0d9a99193f150000803d1df20bbf3e0a0a0d3333333f1dffe6ed3e12050d000020411dcdcccc3f250000003f0a610a0f0d1f856b3f15cdcccc3d1d14fa003f0a0f0d6666863f15cdcccc3d1d49ccbd3e0a0f0d7b142e3f15cdcccc3d1d37e0a43e0a0f0d8fc2f53e159a99993d1d7b0a023f0a0a0d295c0f3f1dd1ff143f12050d0000a0411dcdcccc3f250000003f0a610a0f0d9a99993f159a99193e1d1093243f0a0f0d9a99593f15cdcccc3d1dd08a203f0a0f0dec51b83e15cdcccc3d1d54eef13e0a0f0dcdcccc3e15cdcccc3d1d93d7b93e0a0a0d295c8f3e1daf3c9f3d12050d000020421dcdcccc3f250000003f0a610a0f0d0000803f159a99193e1d1093243f0a0f0d3333733f15cdcccc3d1dd08a203f0a0f0dec51b83e15cdcccc3d1d54eef13e0a0f0dcdcccc3e15cdcccc3d1d93d7b93e0a0a0d295c8f3e1daf3c9f3d12050d0000a0421dcdcccc3f250000003f00"
)

def parse_sharp_main_like_tab1(full_hex: str, levels=5):
    h = normalize_hex(full_hex)
    out = []
    offset = 0
    for _ in range(levels):
        l1 = h[offset:offset+8]; offset += 8 + 2
        l1a = h[offset:offset+8]; offset += 8 + 26
        l2 = h[offset:offset+8]; offset += 8 + 2
        l2a = h[offset:offset+8]; offset += 8 + 26
        l3 = h[offset:offset+8]; offset += 8 + 2
        l3a = h[offset:offset+8]; offset += 8 + 44
        out.append([hex_to_float(l1), hex_to_float(l1a), hex_to_float(l2), hex_to_float(l2a), hex_to_float(l3), hex_to_float(l3a)])
    return out

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
    "000080411d77be9f3c",
    "250000803f2d0000803f0a140d",
    "666646401dc1caa13c",
    "250000803f2d0000803f0a140d",
    "85ebf13f1d0ad7a33c",
    "250000803f2d0000803f12050d000020420a490a140d",
    "000094411d728a8e3c",
    "250000803f2d0000803f0a140d",
    "cdcc2c401dbe30993c",
    "250000803f2d0000803f0a140d",
    "9a99d93f1d0ad7a33c",
    "250000803f2d0000803f12050d0000a042000000"
]

sharp_slices = {
    "Sharp very low": (0, 6),
    "Sharp low": (6, 12),
    "Sharp med": (12, 18),
    "Sharp high": (18, 24),
    "Sharp very high": (24, 30)
}

sharp_bento_slices = {
    "Sharp bento low": (30, 36),
    "Sharp bento high": (36, 42)
}

all_sharp_levels = [
    {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
    {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
    {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
    {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
    {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
    {"name": "Sharp bento low", "default": [16.0, 0.0195, 3.10, 0.01975, 1.89, 0.02]},
    {"name": "Sharp bento high","default": [18.5, 0.0174, 2.70, 0.0187, 1.70, 0.02]}
]

main_sharp_levels = all_sharp_levels[:5]
bento_sharp_levels = all_sharp_levels[5:]

original_sharp_hex_lines3 = [
    "000080401dc9763e3e",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "0000803f1de3a51b3e",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "3333f33f1d68916d3d",
    "250000803f2d0000803f35c3f5a83e12050d0000a0400a580a190d",
    "9a9909411d8fc2753d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "f6286c401d0ad7233d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "000010401d68916d3d",
    "250000803f2d0000803f35c3f5a83e12050d000020410a580a190d",
    "000020411d8fc2753d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "333387401d0ad7233d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "000020401d68916d3d",
    "250000803f2d0000803f35c3f5a83e12050d0000a0410a580a190d",
    "000020411d022b873d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "14ae77401d0ad7233d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "0ad793401d3480b73c",
    "250000803f2d0000803f35c3f5a83e12050d000020420a580a190d",
    "cdcc34411dea95323d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "cdcc6c401d6f12033d",
    "250000803f2d0000803f35c3f5a83e0a190d",
    "333303401ded0dbe3c",
    "250000803f2d0000803f35c3f5a83e12050d0000a042"
]

all_sharp_levels3 = [
    {"name": "Sharp very low",  "default": [4.0, 0.186, 1.0, 0.1520, 1.9, 0.058]},
    {"name": "Sharp low",       "default": [5.2, 0.066, 2.24, 0.1, 2.17, 0.011]},
    {"name": "Sharp med",       "default": [6.55, 0.034, 2.19, 0.2, 1.31, 0.13]},
    {"name": "Sharp high",      "default": [6.38, 0.016, 2.59, 0.018, 1.13, 0.02]},
    {"name": "Sharp very high", "default": [5.56, 0.016, 2.37, 0.018, 2.25, 0.02]},
]

original_sharp_hex_lines4 = [
    "000080401dc9763e3e",
    "258fc2f53c2d0000003f0a140d",
    "0000803f1de3a51b3e",
    "258fc2f53c2d0000003f0a140d",
    "3333f33f1d68916d3d",
    "258fc2f53c2d0000003f12050d0000a0400a490a140d",
    "9a9909411d8fc2753d",
    "258fc2f53c2d0000003f0a140d",
    "f6286c401d0ad7233d",
    "258fc2f53c2d0000003f0a140d",
    "000010401d68916d3d",
    "258fc2f53c2d0000003f12050d000020410a490a140d",
    "000020411d8fc2753d",
    "258fc2f53c2d0000003f0a140d",
    "333387401d0ad7233d",
    "258fc2f53c2d0000003f0a140d",
    "000020401d68916d3d",
    "258fc2f53c2d0000003f12050d0000a0410a490a140d",
    "000020411d022b873d",
    "258fc2f53c2d0000003f0a140d",
    "14ae77401d0ad7233d",
    "258fc2f53c2d0000003f0a140d",
    "0ad793401d3480b73c",
    "258fc2f53c2d0000003f12050d000020420a490a140d",
    "cdcc34411dea95323d",
    "258fc2f53c2d0000003f0a140d",
    "cdcc6c401d6f12033d",
    "258fc2f53c2d0000003f0a140d",
    "333303401ded0dbe3c",
    "258fc2f53c2d0000003f12050d0000a042"
]

all_sharp_levels4 = [
    {"name": "Sharp very low",  "default": [4.0, 0.186, 1.0, 0.1520, 1.9, 0.058]},
    {"name": "Sharp low",       "default": [5.2, 0.066, 2.24, 0.1, 2.17, 0.011]},
    {"name": "Sharp med",       "default": [6.55, 0.034, 2.19, 0.2, 1.31, 0.13]},
    {"name": "Sharp high",      "default": [6.38, 0.016, 2.59, 0.018, 1.13, 0.02]},
    {"name": "Sharp very high", "default": [5.56, 0.016, 2.37, 0.018, 2.25, 0.02]},
]

def generate_sharp_hex(values_list, level_names, level_slices):
    lines = []
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]
        modified_block = deepcopy(original_sharp_hex_lines[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"
        lines.extend(modified_block)
    return "".join(lines)

def generate_sharp_hex3(values_list, level_names, level_slices):
    lines = []
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]
        modified_block = deepcopy(original_sharp_hex_lines3[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"
        lines.extend(modified_block)
    return "".join(lines)

def generate_sharp_hex4(values_list, level_names, level_slices):
    lines = []
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]
        modified_block = deepcopy(original_sharp_hex_lines4[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"
        lines.extend(modified_block)
    return "".join(lines)

def generate_bento_sharp_hex(values_list, level_names, level_slices):
    lines = []
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a = values
        name = level_names[i]["name"]
        start, end = level_slices[name]
        modified_block = deepcopy(original_sharp_hex_lines[start:end])
        modified_block[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
        modified_block[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
        modified_block[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"
        lines.extend(modified_block)
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
    {"name": "Bayer luma denoise very high","default": [0.65, 0.15, 0.642869, 0.75, 0.10, 0.627118, 0.38, 0.10, 0.472521, 0.30, 0.10, 0.362973, 0.25, 0.0777525]}
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

def generate_chroma_hex(values_list, level_names):
    lines = []
    for i, values in enumerate(values_list):
        l1, l1a, l2, l2a, l3, l3a, l4, l4a = values
        level_hex = (
            f"{float_to_hex(l1)}1d{float_to_hex(l1a)}0a0a0d"
            f"{float_to_hex(l2)}1d{float_to_hex(l2a)}0a0a0d"
            f"{float_to_hex(l3)}1d{float_to_hex(l3a)}0a0a0d"
            f"{float_to_hex(l4)}1d{float_to_hex(l4a)}"
        )
        if i == len(values_list) - 4:
            level_hex += "12050d0000803f0a3e0a050d0000a0400a0a0d"
        if i == len(values_list) - 3:
            level_hex += "12050d0000a0400a3e0a050d0000a0400a0a0d"
        if i == len(values_list) - 2:
            level_hex += "12050d000020410a3e0a050d0000a0400a0a0d"
        lines.append(level_hex)
    return "".join(lines)

st.set_page_config(page_title="HEX Sharp & Denoise Generator", layout="wide")
st.title("🔧 Sharp & Bayer Denoise HEX Code Generator")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    ["🔍 Sharp Main ID15", "🔍 Sharp Main ID14", "🔍 Sharp Main ID16", "🍱 Sharp Bento", "🔍 Sharp Main ID12", "🌪️ Luma Denoise", "Chroma Denoise"]
)

with tab1:
    st.markdown("### 🔧 Редактирование основных Sharp уровней: 10A8B45")
    sharp_inputs = []
    for idx, level in enumerate(main_sharp_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"sharp_l3a_{idx}")
            sharp_inputs.append([l1, l1a, l2, l2a, l3, l3a])
    if st.button("🚀 Сгенерировать основной Sharp HEX"):
        full_hex = generate_sharp_hex(sharp_inputs, main_sharp_levels, sharp_slices)
        st.code(full_hex, language="text")
    with st.expander("🔸Парсер Sharp Main Levels", expanded=False):
        hex_input_main = st.text_area("HEX для Main Sharp:", value="", height=200, key="main_parser_input")
        if st.button("🔍 Распарсить Main Sharp HEX"):
            if not hex_input_main.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    results = []
                    offset = 0
                    for level_name in ["very low", "low", "med", "high", "very high"]:
                        l1 = hex_input_main[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_main[offset:offset+8]
                        offset += 8 + 26
                        l2 = hex_input_main[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_main[offset:offset+8]
                        offset += 8 + 26
                        l3 = hex_input_main[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_main[offset:offset+8]
                        offset += 8 + 44
                        results.append({"L1": l1, "L1A": l1a, "L2": l2, "L2A": l2a, "L3": l3, "L3A": l3a})
                    for idx, res in enumerate(results):
                        st.session_state[f"sharp_l1_{idx}_temp"] = float(round(hex_to_float(res["L1"]), 6))
                        st.session_state[f"sharp_l1a_{idx}_temp"] = float(round(hex_to_float(res["L1A"]), 6))
                        st.session_state[f"sharp_l2_{idx}_temp"] = float(round(hex_to_float(res["L2"]), 6))
                        st.session_state[f"sharp_l2a_{idx}_temp"] = float(round(hex_to_float(res["L2A"]), 6))
                        st.session_state[f"sharp_l3_{idx}_temp"] = float(round(hex_to_float(res["L3"]), 6))
                        st.session_state[f"sharp_l3a_{idx}_temp"] = float(round(hex_to_float(res["L3A"]), 6))
                    st.success("✅ Поля Main Sharp обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Main Sharp: {e}")

with tab2:
    st.markdown("### 🔧 Sharp Main ID14")
    st.code(f"Address: 0x{SHARP_MAIN_ID14_ADDR:X}", language="text")
    st.text_input("Patch line (addr:hex)", value=f"0x{SHARP_MAIN_ID14_ADDR:X}:{SHARP_MAIN_ID14_DEFAULT_HEX}", key="patchline_sharp_id14")
    if "id14_defaults_loaded" not in st.session_state:
        vals = parse_sharp_main_like_tab1(SHARP_MAIN_ID14_DEFAULT_HEX, levels=5)
        for idx in range(5):
            st.session_state[f"2sharp_l1_{idx}_temp"] = float(round(vals[idx][0], 6))
            st.session_state[f"2sharp_l1a_{idx}_temp"] = float(round(vals[idx][1], 6))
            st.session_state[f"2sharp_l2_{idx}_temp"] = float(round(vals[idx][2], 6))
            st.session_state[f"2sharp_l2a_{idx}_temp"] = float(round(vals[idx][3], 6))
            st.session_state[f"2sharp_l3_{idx}_temp"] = float(round(vals[idx][4], 6))
            st.session_state[f"2sharp_l3a_{idx}_temp"] = float(round(vals[idx][5], 6))
        st.session_state["id14_defaults_loaded"] = True
    id14_levels = [
        {"name": "Sharp very low", "default": [0, 0, 0, 0, 0, 0]},
        {"name": "Sharp low", "default": [0, 0, 0, 0, 0, 0]},
        {"name": "Sharp med", "default": [0, 0, 0, 0, 0, 0]},
        {"name": "Sharp high", "default": [0, 0, 0, 0, 0, 0]},
        {"name": "Sharp very high", "default": [0, 0, 0, 0, 0, 0]},
    ]
    sharp_inputs2 = []
    for idx, level in enumerate(id14_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"2sharp_l1_{idx}_temp", 0.0), format="%.4f", key=f"2sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"2sharp_l1a_{idx}_temp", 0.0), format="%.4f", key=f"2sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"2sharp_l2_{idx}_temp", 0.0), format="%.4f", key=f"2sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"2sharp_l2a_{idx}_temp", 0.0), format="%.4f", key=f"2sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"2sharp_l3_{idx}_temp", 0.0), format="%.4f", key=f"2sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"2sharp_l3a_{idx}_temp", 0.0), format="%.4f", key=f"2sharp_l3a_{idx}")
            sharp_inputs2.append([l1, l1a, l2, l2a, l3, l3a])
    if st.button("🚀 Сгенерировать Sharp Main ID14 HEX"):
        full_hex = generate_sharp_hex(sharp_inputs2, id14_levels, sharp_slices)
        st.code(full_hex, language="text")
        st.text_input("Patch line (result)", value=f"0x{SHARP_MAIN_ID14_ADDR:X}:{full_hex}", key="patchline_sharp_id14_result")
    with st.expander("🔸Парсер Sharp Main ID14", expanded=False):
        hex_input_main2 = st.text_area("HEX для Sharp Main ID14:", value=SHARP_MAIN_ID14_DEFAULT_HEX, height=200, key="main_parser_input2")
        if st.button("🔍 Распарсить Sharp Main ID14 HEX"):
            if not hex_input_main2.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    vals = parse_sharp_main_like_tab1(hex_input_main2, levels=5)
                    for idx in range(5):
                        st.session_state[f"2sharp_l1_{idx}_temp"] = float(round(vals[idx][0], 6))
                        st.session_state[f"2sharp_l1a_{idx}_temp"] = float(round(vals[idx][1], 6))
                        st.session_state[f"2sharp_l2_{idx}_temp"] = float(round(vals[idx][2], 6))
                        st.session_state[f"2sharp_l2a_{idx}_temp"] = float(round(vals[idx][3], 6))
                        st.session_state[f"2sharp_l3_{idx}_temp"] = float(round(vals[idx][4], 6))
                        st.session_state[f"2sharp_l3a_{idx}_temp"] = float(round(vals[idx][5], 6))
                    st.success("✅ Поля Sharp Main ID14 обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Sharp Main ID14: {e}")

with tab3:
    st.markdown("### 🔧 Редактирование основных Sharp уровней: 10A8D55")
    sharp_inputs3 = []
    for idx, level in enumerate(all_sharp_levels3):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"3sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"3sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"3sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"3sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"3sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"3sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"3sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"3sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"3sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"3sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"3sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"3sharp_l3a_{idx}")
            sharp_inputs3.append([l1, l1a, l2, l2a, l3, l3a])
    if st.button("🚀 Сгенерировать основной Sharp HEX ID16"):
        full_hex = generate_sharp_hex3(sharp_inputs3, all_sharp_levels3, sharp_slices)
        st.code(full_hex, language="text")
    with st.expander("🔸Парсер Sharp Main Levels", expanded=False):
        hex_input_main3 = st.text_area("HEX для Main Sharp ID16:", value="", height=200, key="main_parser_input3")
        if st.button("🔍 Распарсить Main Sharp HEX ID16"):
            if not hex_input_main3.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    results = []
                    offset = 0
                    for level_name in ["very low", "low", "med", "high", "very high"]:
                        l1 = hex_input_main3[offset:offset+8]
                        offset += 8 + 2
                        l1a = hex_input_main3[offset:offset+8]
                        offset += 8 + 36
                        l2 = hex_input_main3[offset:offset+8]
                        offset += 8 + 2
                        l2a = hex_input_main3[offset:offset+8]
                        offset += 8 + 36
                        l3 = hex_input_main3[offset:offset+8]
                        offset += 8 + 2
                        l3a = hex_input_main3[offset:offset+8]
                        offset += 8 + 54
                        results.append({"L1": l1, "L1A": l1a, "L2": l2, "L2A": l2a, "L3": l3, "L3A": l3a})
                    for idx, res in enumerate(results):
                        st.session_state[f"3sharp_l1_{idx}_temp"] = float(round(hex_to_float(res["L1"]), 6))
                        st.session_state[f"3sharp_l1a_{idx}_temp"] = float(round(hex_to_float(res["L1A"]), 6))
                        st.session_state[f"3sharp_l2_{idx}_temp"] = float(round(hex_to_float(res["L2"]), 6))
                        st.session_state[f"3sharp_l2a_{idx}_temp"] = float(round(hex_to_float(res["L2A"]), 6))
                        st.session_state[f"3sharp_l3_{idx}_temp"] = float(round(hex_to_float(res["L3"]), 6))
                        st.session_state[f"3sharp_l3a_{idx}_temp"] = float(round(hex_to_float(res["L3A"]), 6))
                    st.success("✅ Поля Main Sharp ID16 обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Main Sharp ID16: {e}")

with tab4:
    st.markdown("### 🍱 Редактирование Bento Sharp уровней")
    bento_inputs = []
    with st.expander("Sharp bento low", expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=st.session_state.get("bento_l1_0_temp", 16.0), format="%.4f", key="bento_l1_0")
        l1a = cols[1].number_input("L1A", value=st.session_state.get("bento_l1a_0_temp", 0.0195), format="%.4f", key="bento_l1a_0")
        l2 = cols[0].number_input("L2", value=st.session_state.get("bento_l2_0_temp", 3.10), format="%.4f", key="bento_l2_0")
        l2a = cols[1].number_input("L2A", value=st.session_state.get("bento_l2a_0_temp", 0.01975), format="%.4f", key="bento_l2a_0")
        l3 = cols[0].number_input("L3", value=st.session_state.get("bento_l3_0_temp", 1.89), format="%.4f", key="bento_l3_0")
        l3a = cols[1].number_input("L3A", value=st.session_state.get("bento_l3a_0_temp", 0.02), format="%.4f", key="bento_l3a_0")
        bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])
    with st.expander("Sharp bento high", expanded=True):
        cols = st.columns(3)
        l1 = cols[0].number_input("L1", value=st.session_state.get("bento_l1_1_temp", 18.5), format="%.4f", key="bento_l1_1")
        l1a = cols[1].number_input("L1A", value=st.session_state.get("bento_l1a_1_temp", 0.0174), format="%.4f", key="bento_l1a_1")
        l2 = cols[0].number_input("L2", value=st.session_state.get("bento_l2_1_temp", 2.70), format="%.4f", key="bento_l2_1")
        l2a = cols[1].number_input("L2A", value=st.session_state.get("bento_l2a_1_temp", 0.0187), format="%.4f", key="bento_l2a_1")
        l3 = cols[0].number_input("L3", value=st.session_state.get("bento_l3_1_temp", 1.70), format="%.4f", key="bento_l3_1")
        l3a = cols[1].number_input("L3A", value=st.session_state.get("bento_l3a_1_temp", 0.02), format="%.4f", key="bento_l3a_1")
        bento_inputs.append([l1, l1a, l2, l2a, l3, l3a])
    if st.button("🚀 Сгенерировать Bento Sharp HEX"):
        full_hex = generate_bento_sharp_hex(bento_inputs, bento_sharp_levels, sharp_bento_slices)
        st.code(full_hex, language="text")
    with st.expander("Парсер Sharp Bento Low & High", expanded=False):
        hex_input_bento = st.text_area("HEX для Bento уровней:", value="", height=200, key="bento_parser_input")
        if st.button("🔍 Распарсить Sharp Bento HEX"):
            if not hex_input_bento.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    offset = 0
                    l1_low = hex_input_bento[offset:offset+8]; offset += 8 + 2
                    l1a_low = hex_input_bento[offset:offset+8]; offset += 8 + 26
                    l2_low = hex_input_bento[offset:offset+8]; offset += 8 + 2
                    l2a_low = hex_input_bento[offset:offset+8]; offset += 8 + 26
                    l3_low = hex_input_bento[offset:offset+8]; offset += 8 + 2
                    l3a_low = hex_input_bento[offset:offset+8]; offset += 8 + 44
                    l1_high = hex_input_bento[offset:offset+8]; offset += 8 + 2
                    l1a_high = hex_input_bento[offset:offset+8]; offset += 8 + 26
                    l2_high = hex_input_bento[offset:offset+8]; offset += 8 + 2
                    l2a_high = hex_input_bento[offset:offset+8]; offset += 8 + 26
                    l3_high = hex_input_bento[offset:offset+8]; offset += 8 + 2
                    l3a_high = hex_input_bento[offset:offset+8]
                    for idx, (l1, l1a, l2, l2a, l3, l3a) in enumerate([
                        [l1_low, l1a_low, l2_low, l2a_low, l3_low, l3a_low],
                        [l1_high, l1a_high, l2_high, l2a_high, l3_high, l3a_high],
                    ]):
                        st.session_state[f"bento_l1_{idx}_temp"] = float(round(hex_to_float(l1), 6))
                        st.session_state[f"bento_l1a_{idx}_temp"] = float(round(hex_to_float(l1a), 6))
                        st.session_state[f"bento_l2_{idx}_temp"] = float(round(hex_to_float(l2), 6))
                        st.session_state[f"bento_l2a_{idx}_temp"] = float(round(hex_to_float(l2a), 6))
                        st.session_state[f"bento_l3_{idx}_temp"] = float(round(hex_to_float(l3), 6))
                        st.session_state[f"bento_l3a_{idx}_temp"] = float(round(hex_to_float(l3a), 6))
                    st.success("✅ Поля Sharp Bento обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Bento: {e}")

with tab5:
    st.markdown("### 🔧 Редактирование основных Sharp уровней: 10A8315")
    sharp_inputs4 = []
    for idx, level in enumerate(all_sharp_levels4):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(3)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"4sharp_l1_{idx}_temp", level["default"][0]), format="%.4f", key=f"4sharp_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"4sharp_l1a_{idx}_temp", level["default"][1]), format="%.4f", key=f"4sharp_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"4sharp_l2_{idx}_temp", level["default"][2]), format="%.4f", key=f"4sharp_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"4sharp_l2a_{idx}_temp", level["default"][3]), format="%.4f", key=f"4sharp_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"4sharp_l3_{idx}_temp", level["default"][4]), format="%.4f", key=f"4sharp_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"4sharp_l3a_{idx}_temp", level["default"][5]), format="%.4f", key=f"4sharp_l3a_{idx}")
            sharp_inputs4.append([l1, l1a, l2, l2a, l3, l3a])
    if st.button("🚀 Сгенерировать основной Sharp HEX ID12"):
        full_hex = generate_sharp_hex4(sharp_inputs4, all_sharp_levels4, sharp_slices)
        st.code(full_hex, language="text")
    with st.expander("🔸Парсер Sharp Main Levels", expanded=False):
        hex_input_main4 = st.text_area("HEX для Main Sharp ID12:", value="", height=200, key="main_parser_input4")
        if st.button("🔍 Распарсить Main Sharp HEX ID12"):
            if not hex_input_main4.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    results = []
                    offset = 0
                    for level_name in ["very low", "low", "med", "high", "very high"]:
                        l1 = hex_input_main4[offset:offset+8]; offset += 8 + 2
                        l1a = hex_input_main4[offset:offset+8]; offset += 8 + 26
                        l2 = hex_input_main4[offset:offset+8]; offset += 8 + 2
                        l2a = hex_input_main4[offset:offset+8]; offset += 8 + 26
                        l3 = hex_input_main4[offset:offset+8]; offset += 8 + 2
                        l3a = hex_input_main4[offset:offset+8]; offset += 8 + 44
                        results.append({"L1": l1, "L1A": l1a, "L2": l2, "L2A": l2a, "L3": l3, "L3A": l3a})
                    for idx, res in enumerate(results):
                        st.session_state[f"4sharp_l1_{idx}_temp"] = float(round(hex_to_float(res["L1"]), 6))
                        st.session_state[f"4sharp_l1a_{idx}_temp"] = float(round(hex_to_float(res["L1A"]), 6))
                        st.session_state[f"4sharp_l2_{idx}_temp"] = float(round(hex_to_float(res["L2"]), 6))
                        st.session_state[f"4sharp_l2a_{idx}_temp"] = float(round(hex_to_float(res["L2A"]), 6))
                        st.session_state[f"4sharp_l3_{idx}_temp"] = float(round(hex_to_float(res["L3"]), 6))
                        st.session_state[f"4sharp_l3a_{idx}_temp"] = float(round(hex_to_float(res["L3A"]), 6))
                    st.success("✅ Поля Main Sharp ID12 обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Main Sharp ID12: {e}")

with tab6:
    st.markdown("### 🌪️ Настройка параметров Luma Denoise")
    st.code(f"Address: 0x{LUMA_DENOISE_ADDR:X}", language="text")
    st.text_input("Patch line (addr:hex)", value=f"0x{LUMA_DENOISE_ADDR:X}:{LUMA_DENOISE_DEFAULT_HEX}", key="patchline_luma_default")
    if "luma_defaults_loaded" not in st.session_state:
        hex_input_bayer = LUMA_DENOISE_DEFAULT_HEX
        offset = 0
        for idx in range(5):
            l1 = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l1a = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l1b = hex_input_bayer[offset:offset+8]; offset += 8 + 6
            l2 = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l2a = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l2b = hex_input_bayer[offset:offset+8]; offset += 8 + 6
            l3 = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l3a = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l3b = hex_input_bayer[offset:offset+8]; offset += 8 + 6
            l4 = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l4a = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l4b = hex_input_bayer[offset:offset+8]; offset += 8 + 6
            l5 = hex_input_bayer[offset:offset+8]; offset += 8 + 2
            l5a = hex_input_bayer[offset:offset+8]; offset += 8 + 44
            st.session_state[f"bayer_l1_{idx}_temp"] = float(round(hex_to_float(l1), 6))
            st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(hex_to_float(l1a), 6))
            st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(hex_to_float(l1b), 6))
            st.session_state[f"bayer_l2_{idx}_temp"] = float(round(hex_to_float(l2), 6))
            st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(hex_to_float(l2a), 6))
            st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(hex_to_float(l2b), 6))
            st.session_state[f"bayer_l3_{idx}_temp"] = float(round(hex_to_float(l3), 6))
            st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(hex_to_float(l3a), 6))
            st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(hex_to_float(l3b), 6))
            st.session_state[f"bayer_l4_{idx}_temp"] = float(round(hex_to_float(l4), 6))
            st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(hex_to_float(l4a), 6))
            st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(hex_to_float(l4b), 6))
            st.session_state[f"bayer_l5_{idx}_temp"] = float(round(hex_to_float(l5), 6))
            st.session_state[f"bayer_l5a_{idx}_temp"] = float(round(hex_to_float(l5a), 6))
        st.session_state["luma_defaults_loaded"] = True
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
    if st.button("🚀 Сгенерировать HEX (Bayer Denoise)"):
        full_hex = generate_bayer_hex(bayer_inputs, bayer_levels)
        st.code(full_hex, language="text")
        st.text_input("Patch line (result)", value=f"0x{LUMA_DENOISE_ADDR:X}:{full_hex}", key="patchline_luma_result")
    with st.expander("Парсер для Bayer Denoise", expanded=False):
        hex_input_bayer2 = st.text_area("Вставь HEX-строку сюда:", value="", height=200, key="bayer_parser_input_inside_3")
        if st.button("🔍 Распарсить HEX (автозаполнение)"):
            if not hex_input_bayer2.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    h = normalize_hex(hex_input_bayer2)
                    offset = 0
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
                        st.session_state[f"bayer_l1_{idx}_temp"] = float(round(hex_to_float(l1), 6))
                        st.session_state[f"bayer_l1a_{idx}_temp"] = float(round(hex_to_float(l1a), 6))
                        st.session_state[f"bayer_l1b_{idx}_temp"] = float(round(hex_to_float(l1b), 6))
                        st.session_state[f"bayer_l2_{idx}_temp"] = float(round(hex_to_float(l2), 6))
                        st.session_state[f"bayer_l2a_{idx}_temp"] = float(round(hex_to_float(l2a), 6))
                        st.session_state[f"bayer_l2b_{idx}_temp"] = float(round(hex_to_float(l2b), 6))
                        st.session_state[f"bayer_l3_{idx}_temp"] = float(round(hex_to_float(l3), 6))
                        st.session_state[f"bayer_l3a_{idx}_temp"] = float(round(hex_to_float(l3a), 6))
                        st.session_state[f"bayer_l3b_{idx}_temp"] = float(round(hex_to_float(l3b), 6))
                        st.session_state[f"bayer_l4_{idx}_temp"] = float(round(hex_to_float(l4), 6))
                        st.session_state[f"bayer_l4a_{idx}_temp"] = float(round(hex_to_float(l4a), 6))
                        st.session_state[f"bayer_l4b_{idx}_temp"] = float(round(hex_to_float(l4b), 6))
                        st.session_state[f"bayer_l5_{idx}_temp"] = float(round(hex_to_float(l5), 6))
                        st.session_state[f"bayer_l5a_{idx}_temp"] = float(round(hex_to_float(l5a), 6))
                    st.success("✅ Поля ввода обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Bayer Denoise: {e}")

with tab7:
    st.markdown("### 🎨 Chroma Denoise: 010A3C2C")
    chroma_levels = [
        {"name": "Chroma Denoise Low", "default": [5.0, 5.0, 5.0, 5.0, 4.0, 4.0, 4.0, 4.0]},
        {"name": "Chroma Denoise Med", "default": [5.0, 5.0, 5.0, 5.0, 1.0, 4.0, 2.0, 4.0]},
        {"name": "Chroma Denoise High", "default": [5.0, 5.0, 4.0, 5.0, 1.0, 4.0, 1.5, 4.0]},
        {"name": "Chroma Denoise Very High", "default": [4.0, 5.0, 4.0, 5.0, 0.8, 4.0, 1.0, 4.0]}
    ]
    chroma_inputs = []
    for idx, level in enumerate(chroma_levels):
        with st.expander(level["name"], expanded=True):
            cols = st.columns(2)
            l1 = cols[0].number_input("L1", value=st.session_state.get(f"chroma_l1_{idx}_temp", level["default"][0]), format="%.6f", key=f"chroma_l1_{idx}")
            l1a = cols[1].number_input("L1A", value=st.session_state.get(f"chroma_l1a_{idx}_temp", level["default"][1]), format="%.6f", key=f"chroma_l1a_{idx}")
            l2 = cols[0].number_input("L2", value=st.session_state.get(f"chroma_l2_{idx}_temp", level["default"][2]), format="%.6f", key=f"chroma_l2_{idx}")
            l2a = cols[1].number_input("L2A", value=st.session_state.get(f"chroma_l2a_{idx}_temp", level["default"][3]), format="%.6f", key=f"chroma_l2a_{idx}")
            l3 = cols[0].number_input("L3", value=st.session_state.get(f"chroma_l3_{idx}_temp", level["default"][4]), format="%.6f", key=f"chroma_l3_{idx}")
            l3a = cols[1].number_input("L3A", value=st.session_state.get(f"chroma_l3a_{idx}_temp", level["default"][5]), format="%.6f", key=f"chroma_l3a_{idx}")
            l4 = cols[0].number_input("L4", value=st.session_state.get(f"chroma_l4_{idx}_temp", level["default"][6]), format="%.6f", key=f"chroma_l4_{idx}")
            l4a = cols[1].number_input("L4A", value=st.session_state.get(f"chroma_l4a_{idx}_temp", level["default"][7]), format="%.6f", key=f"chroma_l4a_{idx}")
            chroma_inputs.append([l1, l1a, l2, l2a, l3, l3a, l4, l4a])
    if st.button("🚀 Сгенерировать HEX (Chroma Denoise)"):
        full_hex = generate_chroma_hex(chroma_inputs, chroma_levels)
        st.code(full_hex, language="text")
    with st.expander("🔸 Chroma Denoise (все уровни)", expanded=False):
        hex_input_chroma = st.text_area("HEX для Chroma Denoise:", value="", height=200, key="chroma_parser_input_inside")
        if st.button("🔍 Распарсить Chroma Denoise HEX"):
            if not hex_input_chroma.strip():
                st.warning("❌ Вставь HEX-строку для расшифровки!")
            else:
                try:
                    h = normalize_hex(hex_input_chroma)
                    offset = 0
                    results = []
                    for idx in range(4):
                        l1 = h[offset:offset+8]; offset += 8 + 2
                        l1a = h[offset:offset+8]; offset += 8 + 6
                        l2 = h[offset:offset+8]; offset += 8 + 2
                        l2a = h[offset:offset+8]; offset += 8 + 6
                        l3 = h[offset:offset+8]; offset += 8 + 2
                        l3a = h[offset:offset+8]; offset += 8 + 6
                        l4 = h[offset:offset+8]; offset += 8 + 2
                        l4a = h[offset:offset+8]
                        if idx == 3:
                            offset += 8 + 30
                        else:
                            offset += 8 + 38
                        results.append({"L1": l1, "L1A": l1a, "L2": l2, "L2A": l2a, "L3": l3, "L3A": l3a, "L4": l4, "L4A": l4a})
                    for idx, res in enumerate(results):
                        st.session_state[f"chroma_l1_{idx}_temp"] = float(round(hex_to_float(res["L1"]), 6))
                        st.session_state[f"chroma_l1a_{idx}_temp"] = float(round(hex_to_float(res["L1A"]), 6))
                        st.session_state[f"chroma_l2_{idx}_temp"] = float(round(hex_to_float(res["L2"]), 6))
                        st.session_state[f"chroma_l2a_{idx}_temp"] = float(round(hex_to_float(res["L2A"]), 6))
                        st.session_state[f"chroma_l3_{idx}_temp"] = float(round(hex_to_float(res["L3"]), 6))
                        st.session_state[f"chroma_l3a_{idx}_temp"] = float(round(hex_to_float(res["L3A"]), 6))
                        st.session_state[f"chroma_l4_{idx}_temp"] = float(round(hex_to_float(res["L4"]), 6))
                        st.session_state[f"chroma_l4a_{idx}_temp"] = float(round(hex_to_float(res["L4A"]), 6))
                    st.success("✅ Поля Chroma Denoise обновлены")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Ошибка при парсинге Chroma Denoise: {e}")
```0
