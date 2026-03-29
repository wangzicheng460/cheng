import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
# --- 配置页面 ---
st.set_page_config(page_title="UC脂质代谢重构诊断系统", layout="wide")

# ===================== 这里我帮你改好了 =====================
# 去掉了 D盘 本地路径，直接使用当前文件夹
# 图片和文案 直接和 app.py 放在一起即可
# ===========================================================
BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FLOWCHART_PATH = os.path.join(BASE_PATH, "绘图.png")
IMAGE_DIR = BASE_PATH
TEXT_DIR = BASE_PATH


# --- 通用工具函数 ---
def read_text_file(file_name):
    file_path = os.path.join(TEXT_DIR, file_name)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"读取文件出错: {e}"
    return f"未找到文案文件: {file_name}"


def display_result_page(title, file_name, image_list):
    st.title(title)
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()

    description = read_text_file(file_name)
    with st.expander("查看详细研究方法与流程说明", expanded=False):
        st.text(description)

    st.divider()

    for img_name in image_list:
        img_path = os.path.join(IMAGE_DIR, img_name)
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, caption=f"结果展示: {img_name}")
        else:
            st.warning(f"文件未找到: {img_path}")


# --- 模拟模型运行逻辑 ---
def run_mbds_model(vnn1_value):
    status = "脂质代谢紊乱" if vnn1_value > 5.0 else "脂质代谢正常"
    return status


def run_diagnostic_models(vnn1_value):
    ml_risk = min(99.9, (vnn1_value * 12.5))
    dnn_risk = min(99.9, (vnn1_value * 13.2))
    avg_risk = (ml_risk + dnn_risk) / 2
    return round(avg_risk, 2)


# --- 路由控制 ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 1. 首页 ---
if st.session_state.page == 'home':
    st.title("项目名称：解码肠道时空——UC中VNN1介导的脂质代谢紊乱")

    st.header("研究背景与简介")
    intro_text = read_text_file("introduction.txt")
    st.text(intro_text)

    st.header("流程总览")
    if os.path.exists(FLOWCHART_PATH):
        image = Image.open(FLOWCHART_PATH)
        st.image(image, caption="研究技术路线总览图")
    else:
        st.warning(f"未找到流程图文件，请检查路径：{FLOWCHART_PATH}")

    st.divider()
    st.subheader("核心功能模块")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📊 MBDS脂质代谢紊乱预测"):
            st.session_state.page = 'mbds'
            st.rerun()
    with col2:
        if st.button("🩺 UC临床诊断预测"):
            st.session_state.page = 'diagnosis'
            st.rerun()

    st.divider()
    st.subheader("多组学研究结果")
    r1, r2, r3, r4 = st.columns(4)
    with r1:
        if st.button("🧬 Bulk RNA-seq结果"):
            st.session_state.page = 'bulk_rna'
            st.rerun()
    with r2:
        if st.button("🧩 scRNA-seq结果"):
            st.session_state.page = 'scrna'
            st.rerun()
    with r3:
        if st.button("📍 stRNA-seq结果"):
            st.session_state.page = 'strna'
            st.rerun()
    with r4:
        if st.button("💊 药物筛选结果"):
            st.session_state.page = 'drug'
            st.rerun()

# --- 2. 功能页面 ---
elif st.session_state.page == 'mbds':
    st.title("MBDS 脂质代谢紊乱预测中心")
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()
    vnn1_input = st.number_input("请输入 VNN1 基因表达量:", min_value=0.0001, step=0.1, format="%.4f")
    if st.button("运行 MBDS 模型"):
        result = run_mbds_model(vnn1_input)
        if "紊乱" in result:
            st.error(f"预测结果：{result}")
        else:
            st.success(f"预测结果：{result}")

elif st.session_state.page == 'diagnosis':
    st.title("UC 智能诊断中心")
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()
    vnn1_diag = st.number_input("请输入 VNN1 基因表达量 (用于诊断预测):", min_value=0.0001, step=0.1, format="%.4f")
    if st.button("预测"):
        risk_score = run_diagnostic_models(vnn1_diag)
        st.metric(label="患病风险评分", value=f"{risk_score}%")

elif st.session_state.page == 'bulk_rna':
    display_result_page("Bulk RNA-seq 分析结果", "Bulk.txt", ["1.png", "2.png", "3.png", "4.png", "5.png"])

elif st.session_state.page == 'scrna':
    display_result_page("scRNA-seq 分析结果", "scRNA.txt", ["7.png", "8.png", "9.png", "10.png"])

elif st.session_state.page == 'strna':
    display_result_page("stRNA-seq 分析结果", "stRNA.txt", ["11.png"])

elif st.session_state.page == 'drug':
    display_result_page("药物筛选结果", "AIDD.txt", ["12.png", "13.png"])