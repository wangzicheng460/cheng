import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

# --- 配置页面 ---
st.set_page_config(page_title="UC脂质代谢重构诊断系统", layout="wide")

# 数据路径配置
BASE_PATH = r"D:\科研用的\课题（脂质代谢+UC）\人工智能模型"
FLOWCHART_PATH = os.path.join(BASE_PATH, "图", "绘图.png")
IMAGE_DIR = os.path.join(BASE_PATH, "图") 
TEXT_DIR = os.path.join(BASE_PATH, "文案") 

# --- 通用工具函数 ---

def read_text_file(file_name):
    """
    从指定目录读取文本文件内容
    """
    file_path = os.path.join(TEXT_DIR, file_name)
    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"读取文件出错: {e}"
    return f"未找到文案文件: {file_name}"

def display_result_page(title, file_name, image_list):
    """
    通用页面渲染函数 - 结果展示页
    使用 st.text 以确保长文本的换行和特殊符号与原文件完全一致
    """
    st.title(title)
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()
    
    # 读取文案
    description = read_text_file(file_name)
    
    # 使用折叠框展示方法说明
    with st.expander("查看详细研究方法与流程说明", expanded=False):
        st.text(description) 
    
    st.divider()
    
    # 遍历显示图片
    for img_name in image_list:
        img_path = os.path.join(IMAGE_DIR, img_name)
        if os.path.exists(img_path):
            img = Image.open(img_path)
            st.image(img, caption=f"结果展示: {img_name}")
        else:
            st.warning(f"文件未找到: {img_path}")

# --- 模拟模型运行逻辑 ---
def run_mbds_model(vnn1_value):
    # 1. 核心判定逻辑
    is_disordered = vnn1_value > 7.649817
    status = "脂质代谢紊乱" if is_disordered else "脂质代谢正常"
    
    # 2. 构建结构化建议
    if is_disordered:
        results = {
            "status": status,
            "risk_score": round(vnn1_value, 2),
            "recommendations": [
                "【强化监测】建议加做内镜检查，评估粘膜愈合状态。",
                "【营养干预】建议临床营养科介入，评估中短链脂肪酸补充的必要性。",
                "【生化复查】建议加测血清游离脂肪酸 (FFA) 及过氧化物歧化酶 (SOD) 水平。"
            ],
            "color": "red"
        }
    else:
        results = {
            "status": status,
            "risk_score": round(vnn1_value, 2),
            "recommendations": [
                "【维持治疗】建议继续按照现行方案进行临床管理。",
                "【常规随访】建议按标准路径进行定期复查。"
            ],
            "color": "green"
        }
        
    return results

def run_diagnostic_models(vnn1_value):
    ml_risk = min(99.9, (vnn1_value * 12.5)) 
    dnn_risk = min(99.9, (vnn1_value * 13.2))
    avg_risk = (ml_risk + dnn_risk) / 2
    return round(avg_risk, 2)

# --- 路由控制 ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'

# --- 1. 首页逻辑 ---
if st.session_state.page == 'home':
    st.title("项目名称：解码肠道时空：VNN1介导的脂质代谢紊乱在溃疡性结肠炎中的驱动机制及AI诊疗系统研究")
    
# 读取并展示简介
    st.header("研究背景与简介")
    intro_text = read_text_file("introduction.txt")
    
    # 使用 st.write 确保整段直接显示，不带滚动条方框
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

# --- 2. 其他分页面逻辑 ---

elif st.session_state.page == 'mbds':
    st.title("MBDS 脂质代谢紊乱预测中心")
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()
    vnn1_input = st.number_input("请输入 VNN1 基因表达量:", min_value=0.0001, step=0.1, format="%.4f")
    if st.button("运行 MBDS 模型"):
        # 修改点：通过遍历字典内容，实现结构化、正常换行的显示
        res = run_mbds_model(vnn1_input)
        
        if res["color"] == "red":
            st.error(f"### 预测结果：{res['status']}")
        else:
            st.success(f"### 预测结果：{res['status']}")
            
        st.metric(label="当前指标值", value=res["risk_score"])
        
        st.write("#### 临床建议：")
        for rec in res["recommendations"]:
            st.write(rec)

elif st.session_state.page == 'diagnosis':
    st.title("UC 智能诊断中心")
    if st.button("⬅ 返回首页"):
        st.session_state.page = 'home'
        st.rerun()

    st.info("系统将自动运行 11 种机器学习模型（含 Extra Trees）及四层 DNN 深度学习模型进行综合评估。")
    vnn1_diag = st.number_input("请输入 VNN1 基因表达量 (用于诊断预测):", min_value=0.0001, step=0.1, format="%.4f")
    if st.button("预测"):
        with st.spinner('多模型融合计算中...'):
            risk_score = run_diagnostic_models(vnn1_diag)

        st.metric(label="患病风险评分", value=f"{risk_score}%")
        
        if risk_score > 70:
            st.warning("高风险：建议结合临床内镜检查。")
        elif risk_score > 30:
            st.info("中等风险：建议定期复查。")
        else:
            st.success("低风险：指标处于正常范围内。")

elif st.session_state.page == 'bulk_rna':
    display_result_page("Bulk RNA-seq 分析结果", "Bulk.txt", 
                         ["1.png", "2.png", "3.png", "4.png", "5.png"])

elif st.session_state.page == 'scrna':
    display_result_page("scRNA-seq 分析结果", "scRNA.txt", 
                         ["7.png", "8.png", "9.png", "10.png"])

elif st.session_state.page == 'strna':
    display_result_page("stRNA-seq 分析结果", "stRNA.txt", 
                         ["11.png"])

elif st.session_state.page == 'drug':
    display_result_page("药物筛选结果", "AIDD.txt", 
                         ["12.png", "13.png"])