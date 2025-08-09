import streamlit as st
from datetime import datetime

# 天干地支
tiangan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
dizhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

# 双合规则（天干合 + 地支合）
tiangan_he = {"甲": "己", "乙": "庚", "丙": "辛", "丁": "壬", "戊": "癸",
              "己": "甲", "庚": "乙", "辛": "丙", "壬": "丁", "癸": "戊"}
dizhi_he = {"子": "丑", "丑": "子", "寅": "亥", "卯": "戌", "辰": "酉", "巳": "申",
            "午": "未", "未": "午", "申": "巳", "酉": "辰", "戌": "卯", "亥": "寅"}

# 双冲规则（天干冲 + 地支冲）
tiangan_chong = {"甲": "庚", "乙": "辛", "丙": "壬", "丁": "癸", "庚": "甲",
                 "辛": "乙", "壬": "丙", "癸": "丁"}
dizhi_chong = {"子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
               "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳"}

# 生成 1900-2100 年的干支
def generate_ganzhi_years():
    years = {}
    start_tg_index = tiangan.index("庚")  # 1900年为庚子年
    start_dz_index = dizhi.index("子")
    for y in range(1900, 2101):
        tg = tiangan[(start_tg_index + (y - 1900)) % 10]
        dz = dizhi[(start_dz_index + (y - 1900)) % 12]
        years[f"{tg}{dz}"] = y
    return years

ganzhi_years = generate_ganzhi_years()

def find_jixiong(pillar):
    tg, dz = pillar[0], pillar[1]
    ji_tg = tiangan_he[tg]
    ji_dz = dizhi_he[dz]
    xiong_tg = tiangan_chong[tg]
    xiong_dz = dizhi_chong[dz]

    # 吉：双合
    ji1 = ji_tg + ji_dz  # 双合
    ji2 = ji_tg + dizhi[(dizhi.index(ji_dz) + 1) % 12]  # 天干合+地支合进一

    # 凶：双冲
    xiong1 = xiong_tg + xiong_dz
    xiong2 = xiong_tg + dizhi[(dizhi.index(xiong_dz) - 1) % 12]  # 天干冲+地支冲退一

    return [ji1, ji2], [xiong1, xiong2]

def filter_existing_years(gz_list):
    return [f"{gz}{ganzhi_years[gz]}年" for gz in gz_list if gz in ganzhi_years]

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

    # 过滤不存在的年份
    all_ji = filter_existing_years(all_ji)
    all_xiong = filter_existing_years(all_xiong)

    return all_ji, all_xiong

# ----------------- Streamlit UI -----------------
st.title("八字吉凶年份查询")

nianzhu = st.text_input("请输入年柱（如：戊寅）")
yuezhu = st.text_input("请输入月柱（如：庚子）")
rizhu = st.text_input("请输入日柱（如：乙卯）")
shizhu = st.text_input("请输入时柱（如未知填入不知道）", value="不知道")

if st.button("查询吉凶年份"):
    if not (nianzhu and yuezhu and rizhu):
        st.error("年柱、月柱、日柱必须填写！")
    else:
        ji_list, xiong_list = analyze_bazi(nianzhu, yuezhu, rizhu, shizhu)
        current_year = datetime.now().year

        st.subheader("吉年")
        for j in ji_list:
            y = int(j[-5:-1])
            if y >= current_year:
                st.markdown(f"**{j}** ✅")
            else:
                st.write(j)

        st.subheader("凶年")
        for x in xiong_list:
            y = int(x[-5:-1])
            if y >= current_year:
                st.markdown(f"**{x}** ⚠️")
            else:
                st.write(x)
