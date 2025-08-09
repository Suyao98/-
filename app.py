import streamlit as st
from datetime import datetime

# -------------------
# 天干地支规则定义
# -------------------

# 天干合
tiangan_he = {
    '甲': '己', '己': '甲',
    '乙': '庚', '庚': '乙',
    '丙': '辛', '辛': '丙',
    '丁': '壬', '壬': '丁',
    '戊': '癸', '癸': '戊'
}

# 地支合
dizhi_he = {
    '子': '丑', '丑': '子',
    '寅': '亥', '亥': '寅',
    '卯': '戌', '戌': '卯',
    '辰': '酉', '酉': '辰',
    '巳': '申', '申': '巳',
    '午': '未', '未': '午'
}

# 天干冲（已改为四冲规则）
tiangan_chong = {
    '甲': '庚', '庚': '甲',
    '乙': '辛', '辛': '乙',
    '癸': '丁', '丁': '癸',
    '壬': '丙', '丙': '壬'
}

# 地支冲
dizhi_chong = {
    '子': '午', '午': '子',
    '丑': '未', '未': '丑',
    '寅': '申', '申': '寅',
    '卯': '酉', '酉': '卯',
    '辰': '戌', '戌': '辰',
    '巳': '亥', '亥': '巳'
}

# 60甲子列表
jiazi_list = [
    '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉',
    '甲戌', '乙亥', '丙子', '丁丑', '戊寅', '己卯', '庚辰', '辛巳', '壬午', '癸未',
    '甲申', '乙酉', '丙戌', '丁亥', '戊子', '己丑', '庚寅', '辛卯', '壬辰', '癸巳',
    '甲午', '乙未', '丙申', '丁酉', '戊戌', '己亥', '庚子', '辛丑', '壬寅', '癸卯',
    '甲辰', '乙巳', '丙午', '丁未', '戊申', '己酉', '庚戌', '辛亥', '壬子', '癸丑',
    '甲寅', '乙卯', '丙辰', '丁巳', '戊午', '己未', '庚申', '辛酉', '壬戌', '癸亥'
]

# 公历年份与干支对照（1900-2100示例，可扩展）
year_ganzhi_map = {}
start_year = 1900
for i in range(len(jiazi_list)):
    year_ganzhi_map[start_year + i] = jiazi_list[i % 60]

# -------------------
# 查找吉凶
# -------------------
def find_jixiong(zhu):
    tg, dz = zhu[0], zhu[1]
    ji, xiong = [], []

    # 双合
    he_tg = tiangan_he.get(tg)
    he_dz = dizhi_he.get(dz)
    if he_tg and he_dz:
        ji.append(he_tg + he_dz)  # 双合结果
        # 进一
        idx = jiazi_list.index(he_tg + he_dz)
        ji.append(jiazi_list[(idx + 1) % 60])

    # 双冲
    chong_tg = tiangan_chong.get(tg)
    chong_dz = dizhi_chong.get(dz)
    if chong_tg and chong_dz:
        xiong.append(chong_tg + chong_dz)  # 双冲结果
        # 退一
        idx = jiazi_list.index(chong_tg + chong_dz)
        xiong.append(jiazi_list[(idx - 1) % 60])

    return ji, xiong

# -------------------
# 分析八字
# -------------------
def analyze_bazi(nianzhu, yuezhu, rizhu, shizhu):
    all_ji, all_xiong = [], []

    for zhu in [nianzhu, yuezhu, rizhu]:
        ji, xiong = find_jixiong(zhu)
        all_ji.extend(ji)
        all_xiong.extend(xiong)

    if shizhu != "不知道":
        ji, xiong = find_jixiong(shizhu)
        all_ji.extend(ji)
        all_xiong.extend(xiong)

    # 去重
    all_ji = list(set(all_ji))
    all_xiong = list(set(all_xiong))

    # 查年份
    ji_years = {gz: [y for y, g in year_ganzhi_map.items() if g == gz] for gz in all_ji if gz in jiazi_list}
    xiong_years = {gz: [y for y, g in year_ganzhi_map.items() if g == gz] for gz in all_xiong if gz in jiazi_list}

    return ji_years, xiong_years

# -------------------
# Streamlit 界面
# -------------------
st.title("八字吉凶年份查询")
st.write("输入四柱（时柱可填“不知道”），程序将根据双合、双冲规则推算吉凶年份。")

nianzhu = st.text_input("请输入年柱（如 甲子）")
yuezhu = st.text_input("请输入月柱（如 乙丑）")
rizhu = st.text_input("请输入日柱（如 丙寅）")
shizhu = st.text_input("请输入时柱（如 不知道）", value="不知道")

if st.button("查询"):
    if not nianzhu or not yuezhu or not rizhu:
        st.error("年柱、月柱、日柱必须填写")
    else:
        ji_list, xiong_list = analyze_bazi(nianzhu, yuezhu, rizhu, shizhu)
        current_year = datetime.now().year

        st.subheader("吉年")
        for gz, years in ji_list.items():
            if years:
                year_str = "，".join([f"**{y}年**" if y >= current_year else f"{y}年" for y in years])
                st.write(f"{gz}：{year_str}")

        st.subheader("凶年")
        for gz, years in xiong_list.items():
            if years:
                year_str = "，".join([f"**{y}年**" if y >= current_year else f"{y}年" for y in years])
                st.write(f"{gz}：{year_str}")

