# -*- coding: utf-8 -*-
import datetime
import streamlit as st

# 天干、地支
tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
dizhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干合（五合）
gan_he = {
    "甲": "己", "己": "甲",
    "乙": "庚", "庚": "乙",
    "丙": "辛", "辛": "丙",
    "丁": "壬", "壬": "丁",
    "戊": "癸", "癸": "戊"
}

# 天干冲（四冲）
gan_chong = {
    "甲": "庚", "庚": "甲",
    "乙": "辛", "辛": "乙",
    "丙": "壬", "壬": "丙",
    "丁": "癸", "癸": "丁"
}

# 地支合（六合）
zhi_he = {
    "子": "丑", "丑": "子",
    "寅": "亥", "亥": "寅",
    "卯": "戌", "戌": "卯",
    "辰": "酉", "酉": "辰",
    "巳": "申", "申": "巳",
    "午": "未", "未": "午"
}

# 地支冲（相隔6位）
zhi_chong = {dz: dizhi[(i + 6) % 12] for i, dz in enumerate(dizhi)}

# 获取地支进一 / 退一
def zhi_next(zhi):
    return dizhi[(dizhi.index(zhi) + 1) % 12]

def zhi_prev(zhi):
    return dizhi[(dizhi.index(zhi) - 1) % 12]

# 生成六十甲子
def ganzhi_list():
    result = []
    for i in range(60):
        tg = tiangan[i % 10]
        dz = dizhi[i % 12]
        result.append(tg + dz)
    return result

# 年份与干支映射
def year_ganzhi_map(start=1900, end=2100):
    gzs = ganzhi_list()
    base_year = 1984  # 甲子年
    year_map = {}
    for year in range(start, end + 1):
        index = (year - base_year) % 60
        year_map[year] = gzs[index]
    return year_map

# 根据一个柱求吉凶干支
def calc_jixiong(gz):
    tg = gz[0]
    dz = gz[1]
    results = {"吉": [], "凶": []}

    tg_he = gan_he.get(tg, "")
    dz_he = zhi_he.get(dz, "")
    tg_ch = gan_chong.get(tg, "")
    dz_ch = zhi_chong.get(dz, "")

    if tg_he and dz_he:
        shuang_he = tg_he + dz_he
        jin_yi = tg_he + zhi_next(dz_he)
        results["吉"].extend([shuang_he, jin_yi])

    if tg_ch and dz_ch:
        shuang_ch = tg_ch + dz_ch
        tui_yi = tg_ch + zhi_prev(dz_ch)
        results["凶"].extend([shuang_ch, tui_yi])

    return results


# ===== Streamlit 网页版 =====
st.set_page_config(page_title="八字吉凶年份查询", page_icon="🔮", layout="centered")

st.title("八字吉凶年份查询 🔮")

year_zhu = st.text_input("请输入年柱（例：甲子）").strip()
month_zhu = st.text_input("请输入月柱（例：乙丑）").strip()
day_zhu = st.text_input("请输入日柱（例：丙寅）").strip()
time_zhu = st.text_input("请输入时柱（如未知填入“不知道”）").strip()

if st.button("查询"):
    if not (year_zhu and month_zhu and day_zhu):
        st.error("请至少输入年柱、月柱、日柱")
    else:
        current_year = datetime.datetime.now().year
        zhus = [year_zhu, month_zhu, day_zhu]
        if time_zhu and time_zhu != "不知道":
            zhus.append(time_zhu)  # 只加已知时柱

        all_ji = set()
        all_xiong = set()

        for zhu in zhus:
            result = calc_jixiong(zhu)
            all_ji.update(result["吉"])
            all_xiong.update(result["凶"])

        year_map = year_ganzhi_map()

        # 吉年输出
        st.subheader("🎉 吉年")
        for gz in sorted(all_ji, key=lambda x: ganzhi_list().index(x) if x in ganzhi_list() else 999):
            years = [y for y, gz_y in year_map.items() if gz_y == gz]
            if years:
                year_strs = []
                for y in years:
                    if y >= current_year:
                        year_strs.append(f"<b>{gz}{y}年★</b>")
                    else:
                        year_strs.append(f"{gz}{y}年")
                st.markdown(
                    f"<span style='color:red'>{gz}: {', '.join(year_strs)}</span>",
                    unsafe_allow_html=True
                )

        # 凶年输出
        st.subheader("☠️ 凶年")
        for gz in sorted(all_xiong, key=lambda x: ganzhi_list().index(x) if x in ganzhi_list() else 999):
            years = [y for y, gz_y in year_map.items() if gz_y == gz]
            if years:
                year_strs = []
                for y in years:
                    if y >= current_year:
                        year_strs.append(f"<b>{gz}{y}年★</b>")
                    else:
                        year_strs.append(f"{gz}{y}年")
                st.markdown(
                    f"<span style='color:#333'>{gz}: {', '.join(year_strs)}</span>",
                    unsafe_allow_html=True
                )
