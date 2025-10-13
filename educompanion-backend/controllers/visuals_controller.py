import os
import textwrap
import re
from pathlib import Path
from flask import request, jsonify
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from PIL import Image, ImageEnhance, ImageFilter
import pdfplumber, pytesseract, easyocr

# Directory to store generated outputs
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATED_DIR = os.path.join(BACKEND_DIR, "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)

# -------------------------
# Helper functions
# -------------------------

def extract_text(path):
    ext = Path(path).suffix.lower()
    text = ""

    if ext == ".pdf":
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
    elif ext in [".png", ".jpg", ".jpeg", ".tif", ".bmp"]:
        img = Image.open(path).convert("L")
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.point(lambda x: 0 if x < 140 else 255, '1')
        img = img.resize((img.width * 2, img.height * 2))

        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=config).strip()

        if len(text.split()) < 5:
            reader = easyocr.Reader(['en'])
            result = reader.readtext(path, detail=0)
            text = "\n".join(result)
    else:
        raise ValueError("Unsupported file type: " + ext)

    return text.strip()


def detect_axis_labels(text):
    text_lower = text.lower()
    x_match = re.search(r"x[- ]axis[:\s]+([\w\s]+)", text_lower)
    y_match = re.search(r"y[- ]axis[:\s]+([\w\s]+)", text_lower)
    if x_match and y_match:
        return x_match.group(1).title(), y_match.group(1).title()

    vs_match = re.search(r"([\w\s]+)\s+vs\s+([\w\s]+)", text_lower)
    if vs_match:
        y_label = vs_match.group(1).strip().title()
        x_label = vs_match.group(2).strip().title()
        return x_label, y_label

    show_match = re.search(r"showing\s+([\w\s]+)\s+of\s+([\w\s]+)", text_lower)
    if show_match:
        y_label = show_match.group(1).strip().title()
        x_label = show_match.group(2).strip().title()
        return x_label, y_label

    return "Label", "Value"


def detect_numeric_sections(text):
    patterns = [
        r"(?:degree\s*of\s*)?vertex\s*([A-Za-z0-9]+)\s*(?:is|=|:|has\s*degree\s*of)?\s*(\d+)",
        r"([A-Za-z0-9._ -]+)\s*[:=]\s*(\d+(?:\.\d+)?)",
    ]
    matches = []
    for pat in patterns:
        matches += re.findall(pat, text, flags=re.I)

    if not matches:
        return None

    df = pd.DataFrame(matches, columns=["Label", "Value"])
    df["Label"] = df["Label"].str.strip().str.replace(r"\s+", " ", regex=True)
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(inplace=True)
    df = df.groupby("Label", as_index=False)["Value"].sum()
    return df.drop_duplicates()


def make_bar_chart(df, outdir, x_label, y_label):
    plt.figure(figsize=(8, 4))
    plt.bar(df["Label"], df["Value"], color="#1f77b4", edgecolor="black")
    plt.xticks(rotation=45, ha='right')
    plt.title(f"{y_label} vs {x_label}")
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    out = os.path.join(outdir, "barchart.png")
    plt.tight_layout()
    plt.savefig(out, dpi=150)
    plt.close()
    return out


def make_pie_chart(df, outdir, title):
    plt.figure(figsize=(6, 6))
    df = df.groupby("Label", as_index=False)["Value"].sum()
    df = df.sort_values(by="Value", ascending=False)
    plt.pie(
        df["Value"],
        labels=df["Label"],
        autopct=lambda p: f"{p:.1f}%",
        startangle=90,
        labeldistance=1.1,
        wedgeprops=dict(edgecolor="white")
    )
    plt.title(title, fontsize=14, fontweight="bold")
    plt.tight_layout()
    out = os.path.join(outdir, "piechart.png")
    plt.savefig(out, dpi=200)
    plt.close()
    return out


def detect_algorithm_section(text):
    algo_keywords = ["algorithm", "procedure", "steps to implement", "step", "input", "output"]
    if not any(k.lower() in text.lower() for k in algo_keywords):
        return None, None

    title_match = re.search(r"(Algorithm\s*[\w\s-]*)", text, re.I)
    title = title_match.group(1).strip() if title_match else "Algorithm Flowchart"

    match = re.search(r"(step\s*1.*?)(?:\n\s*\n|$)", text, flags=re.IGNORECASE | re.DOTALL)
    algo_text = match.group(1) if match else text
    return algo_text.strip(), title


def extract_steps(text):
    steps = []
    for line in text.splitlines():
        if re.search(r"(\bstep\s*\d+|^\d+\.)", line, re.I) or line.lower().startswith(("input", "output")):
            clean = re.sub(r"^\s*(step\s*\d+\.?|\d+\.|-|\*)\s*", "", line.strip(), flags=re.I)
            if clean:
                steps.append(clean)
    return steps


def make_flowchart_without_dot(steps, outdir, title="Algorithm Flowchart"):
    """Generate flowchart using networkx + matplotlib, no Graphviz required."""
    G = nx.DiGraph()
    prev_node = "Start"
    G.add_node(prev_node)

    for i, step in enumerate(steps):
        node_id = f"Step {i+1}"
        G.add_node(node_id, label=textwrap.fill(step, 30))
        G.add_edge(prev_node, node_id)
        prev_node = node_id

    pos = nx.spring_layout(G, seed=42)  # Deterministic layout

    plt.figure(figsize=(8, len(steps) * 1.5))
    labels = nx.get_node_attributes(G, 'label')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=3000, node_color="#A3C1DA",
            font_size=10, font_weight='bold', arrows=True)
    plt.title(title, fontsize=14)
    os.makedirs(outdir, exist_ok=True)
    out_path = os.path.join(outdir, "flowchart.png")
    plt.savefig(out_path, dpi=200, bbox_inches='tight')
    plt.close()
    return out_path


# -------------------------
# Controller function
# -------------------------

def process_file_controller():
    """Controller to handle file upload and return JSON with generated outputs."""
    if 'file' not in request.files:
        return {"error": "No file part in the request"}, 400

    file = request.files['file']
    if file.filename == "":
        return {"error": "No selected file"}, 400

    # Save uploaded file temporarily
    file_path = os.path.join(GENERATED_DIR, file.filename)
    file.save(file_path)

    # Folder for this file’s visuals
    folder_name = Path(file.filename).stem
    outdir = os.path.join(GENERATED_DIR, folder_name)
    os.makedirs(outdir, exist_ok=True)

    try:
        text = extract_text(file_path)
        results = {"extracted_chars": len(text.strip())}

        # Detect labels and numeric data
        x_label, y_label = detect_axis_labels(text)
        df = detect_numeric_sections(text)
        if df is not None and not df.empty:
            # ✅ Return full API URLs (frontend will normalize correctly)
            results["bar_chart"] = f"/api/visuals/generated/{folder_name}/barchart.png"
            results["pie_chart"] = f"/api/visuals/generated/{folder_name}/piechart.png"

            make_bar_chart(df, outdir, x_label, y_label)
            make_pie_chart(df, outdir, f"{y_label} Distribution")
        else:
            results["chart_info"] = "❌ No numeric data found for charts."

        # Detect and generate algorithm flowchart
        algo_text, algo_title = detect_algorithm_section(text)
        if algo_text:
            steps = extract_steps(algo_text)
            if steps:
                results["flowchart"] = f"/api/visuals/generated/{folder_name}/flowchart.png"
                make_flowchart_without_dot(steps, outdir, title=algo_title)
            else:
                results["flowchart"] = "⚠️ Algorithm detected but no clear steps found."
        else:
            results["flowchart"] = "❌ No algorithm detected."

        return jsonify(results)

    except Exception as e:
        return {"error": str(e)}, 500

    """Controller to handle file upload and return JSON with generated outputs."""
    if 'file' not in request.files:
        return {"error": "No file part in the request"}, 400

    file = request.files['file']
    if file.filename == "":
        return {"error": "No selected file"}, 400

    # Save uploaded file temporarily
    file_path = os.path.join(GENERATED_DIR, file.filename)
    file.save(file_path)

    # Process the file
    outdir = os.path.join(GENERATED_DIR, Path(file.filename).stem)
    os.makedirs(outdir, exist_ok=True)

    try:
        text = extract_text(file_path)
        results = {"extracted_chars": len(text.strip())}

        # Numeric charts
        x_label, y_label = detect_axis_labels(text)
        df = detect_numeric_sections(text)
        if df is not None and not df.empty:
            results["bar_chart"] = f"/generated/{Path(file.filename).stem}/barchart.png"
            results["pie_chart"] = f"/generated/{Path(file.filename).stem}/piechart.png"
            make_bar_chart(df, outdir, x_label, y_label)
            make_pie_chart(df, outdir, f"{y_label} Distribution")
        else:
            results["chart_info"] = "❌ No numeric data found for charts."

        # Algorithm / flowchart
        algo_text, algo_title = detect_algorithm_section(text)
        if algo_text:
            steps = extract_steps(algo_text)
            if steps:
                results["flowchart"] = f"/generated/{Path(file.filename).stem}/flowchart.png"
                make_flowchart_without_dot(steps, outdir, title=algo_title)
            else:
                results["flowchart"] = "⚠️ Algorithm detected but no clear steps found."
        else:
            results["flowchart"] = "❌ No algorithm detected."

        return jsonify(results)

    except Exception as e:
        return {"error": str(e)}, 500
