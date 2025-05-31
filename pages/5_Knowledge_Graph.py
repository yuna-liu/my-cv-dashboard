import pandas as pd
from pyvis.network import Network
import streamlit as st
import streamlit.components.v1 as components

# 📂 Load from data directory
nodes_df = pd.read_csv("data/nodes.csv")
edges_df = pd.read_csv("data/edges.csv")

def build_knowledge_graph(nodes_df, edges_df):
    net = Network(height="600px", width="100%", notebook=False)
    color_map = {
        "person": "#FF7F50",
        "education": "#87CEFA",
        "certification": "#DA70D6",
        "skill": "#90EE90",
        "project": "#FFD700"
    }

    for _, row in nodes_df.iterrows():
        net.add_node(row['id'], label=row['label'], title=row['type'], color=color_map.get(row['type'], "#D3D3D3"))

    for _, row in edges_df.iterrows():
        net.add_edge(row['source'], row['target'], title=row['relation'])

    return net

net = build_knowledge_graph(nodes_df, edges_df)
net.save_graph("knowledge_graph.html")
components.html(open("knowledge_graph.html", "r", encoding="utf-8").read(), height=600)
