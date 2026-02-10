*** luma_generator_web.py	2026-02-10
--- luma_generator_web.py	2026-02-10
***************
*** 1,9999 ****
--- 1,197 ----
+ import streamlit as st
+ import struct
+ from copy import deepcopy
+ 
+ def float_to_hex(f):
+     return struct.pack("<f", float(f)).hex()
+ 
+ def hex_to_float(h):
+     return struct.unpack("<f", bytes.fromhex(h))[0]
+ 
+ def clean_hex(s):
+     return "".join(c for c in s.lower() if c in "0123456789abcdef")
+ 
+ original_sharp_hex_lines = [
+     "0a490a140d000080401dc9763e3e",
+     "250000803f2d0000803f0a140d",
+     "0000803f1de3a51b3e250000803f2d0000803f0a140d3333f33f1d68916d3d",
+     "250000803f2d0000803f12050d",
+     "3333f33f1d68916d3d",
+     "250000803f2d0000803f12050d",
+     "0000a0400a490a140d6666a6401d022b873d",
+     "250000803f2d0000803f0a140d",
+     "295c0f401dcdcccc3d",
+     "250000803f2d0000803f0a140d",
+     "48e10a401d5839343c",
+     "250000803f2d0000803f12050d",
+     "000020410a490a140d9a99d1401d96430b3d",
+     "250000803f2d0000803f0a140d",
+     "f6280c401dcdcc4c3e",
+     "250000803f2d0000803f0a140d",
+     "14aea73f1db81e053e",
+     "250000803f2d0000803f12050d",
+     "0000a0410a490a140df628cc401d6f12833c",
+     "250000803f2d0000803f0a140d",
+     "8fc225401dbc74933c",
+     "250000803f2d0000803f0a140d",
+     "d7a3903f1d0ad7a33c",
+     "250000803f2d0000803f12050d",
+     "000020420a490a140d85ebb1401d6f12833c",
+     "250000803f2d0000803f0a140d",
+     "14ae17401dbc74933c",
+     "250000803f2d0000803f0a140d",
+     "000010401d0ad7a33c",
+     "250000803f2d0000803f12050d0000a042000000000000000000",
+ ]
+ 
+ sharp_slices = {
+     "Sharp very low": (0, 6),
+     "Sharp low": (6, 12),
+     "Sharp med": (12, 18),
+     "Sharp high": (18, 24),
+     "Sharp very high": (24, 30),
+ }
+ 
+ levels = [
+     {"name": "Sharp very low",  "default": [7.0, 0.060, 3.075, 0.040, 1.875, 0.058]},
+     {"name": "Sharp low",       "default": [8.6, 0.060, 3.69, 0.040, 2.25, 0.058]},
+     {"name": "Sharp med",       "default": [10.0, 0.060, 4.225, 0.040, 2.5, 0.058]},
+     {"name": "Sharp high",      "default": [10.0, 0.066, 3.87, 0.040, 4.62, 0.0224]},
+     {"name": "Sharp very high", "default": [11.3, 0.0436, 3.70, 0.032, 2.05, 0.0232]},
+ ]
+ 
+ SHARP_ID14_DEFAULT_HEX = clean_hex("".join(original_sharp_hex_lines[:30]))
+ 
+ def generate_sharp_hex(values_list, level_names, level_slices):
+     out = []
+     for i, values in enumerate(values_list):
+         l1, l1a, l2, l2a, l3, l3a = values
+         name = level_names[i]["name"]
+         start, end = level_slices[name]
+         blk = deepcopy(original_sharp_hex_lines[start:end])
+         blk[0] = f"{float_to_hex(l1)}1d{float_to_hex(l1a)}"
+         blk[2] = f"{float_to_hex(l2)}1d{float_to_hex(l2a)}"
+         blk[4] = f"{float_to_hex(l3)}1d{float_to_hex(l3a)}"
+         out.extend(blk)
+     return clean_hex("".join(out))
+ 
+ def parse_sharp_hex(hex_str):
+     s = clean_hex(hex_str)
+     res = []
+     off = 0
+     for _ in range(5):
+         l1 = s[off:off+8]; off += 8 + 2
+         l1a = s[off:off+8]; off += 8 + 26
+         l2 = s[off:off+8]; off += 8 + 2
+         l2a = s[off:off+8]; off += 8 + 26
+         l3 = s[off:off+8]; off += 8 + 2
+         l3a = s[off:off+8]; off += 8 + 44
+         res.append([hex_to_float(l1), hex_to_float(l1a), hex_to_float(l2), hex_to_float(l2a), hex_to_float(l3), hex_to_float(l3a)])
+     return res
+ 
+ st.set_page_config(page_title="Sharp Main ID14", layout="wide")
+ st.title("Sharp Main ID14")
+ 
+ if "sharp_vals" not in st.session_state:
+     st.session_state.sharp_vals = [lvl["default"][:] for lvl in levels]
+ 
+ with st.expander("Парсер", expanded=False):
+     hx = st.text_area("HEX", value=SHARP_ID14_DEFAULT_HEX, height=200, key="sharp_hex_input")
+     if st.button("Распарсить", key="sharp_parse_btn"):
+         st.session_state.sharp_vals = parse_sharp_hex(hx)
+         st.rerun()
+ 
+ sharp_inputs = []
+ for i, lvl in enumerate(levels):
+     with st.expander(lvl["name"], expanded=True):
+         c = st.columns(3)
+         v = st.session_state.sharp_vals[i]
+         l1  = c[0].number_input("L1",  value=float(v[0]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l1_{i}")
+         l1a = c[1].number_input("L1A", value=float(v[1]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l1a_{i}")
+         l2  = c[0].number_input("L2",  value=float(v[2]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l2_{i}")
+         l2a = c[1].number_input("L2A", value=float(v[3]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l2a_{i}")
+         l3  = c[0].number_input("L3",  value=float(v[4]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l3_{i}")
+         l3a = c[1].number_input("L3A", value=float(v[5]), min_value=None, max_value=None, step=0.0001, format="%.6f", key=f"l3a_{i}")
+         sharp_inputs.append([l1, l1a, l2, l2a, l3, l3a])
+ 
+ if st.button("Сгенерировать HEX", key="sharp_gen_btn"):
+     st.code(generate_sharp_hex(sharp_inputs, levels, sharp_slices), language="text")
