import streamlit as st
from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import tempfile
import os

st.set_page_config(page_title="Knowledge Graph Viewer", layout="wide")
st.title("🧠 Knowledge Graph Viewer")

# 创建图谱
G = nx.Graph()
G.add_node("Yuna", title="Me")
G.add_node("Education", title="My Education")
G.add_node("Certifications", title="My Certifications")
G.add_node("Data Engineer", title="Job Role")
G.add_edge("Yuna", "Education")
G.add_edge("Yuna", "Certifications")
G.add_edge("Yuna", "Data Engineer")

# 使用 Pyvis 渲染
net = Network(height="600px", width="100%", bgcolor="#ffffff", font_color="black")
net.from_nx(G)

# 创建临时 HTML 文件保存图
with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
    tmp_path = tmp_file.name
    net.save_graph(tmp_path)

# 嵌入 HTML 图谱到 Streamlit
with open(tmp_path, "r", encoding="utf-8") as f:
    html = f.read()
components.html(html, height=650, scrolling=True)

# 可选清理
os.remove(tmp_path)
