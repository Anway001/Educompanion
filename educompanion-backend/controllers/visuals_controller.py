import os, re, textwrap
from pathlib import Path
import matplotlib.pyplot as plt
import graphviz
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter
import pdfplumber, pytesseract
import easyocr
from flask import request, jsonify

def extract_text(path):
    print(f"[visuals_controller] Calling extract_text for {path}")
    """Extract text from PDF or image with preprocessing and OCR fallback."""
    ext = Path(path).suffix.lower()
    text = ""

    if ext == ".pdf":
        print("[visuals_controller] Processing PDF file")
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""

    elif ext in [".png", ".jpg", ".jpeg", ".tif", ".bmp"]:
        print("[visuals_controller] Processing image file")
        img = Image.open(path).convert("L")
        img = img.filter(ImageFilter.MedianFilter())
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(2)
        img = img.point(lambda x: 0 if x < 140 else 255, '1')
        img = img.resize((img.width * 2, img.height * 2))

        config = r'--oem 3 --psm 6'
        text = pytesseract.image_to_string(img, config=config).strip()
        print(f"[visuals_controller] Pytesseract extracted text: {textwrap.shorten(text, width=100)}")

        # Fallback to EasyOCR if OCR too weak
        if len(text.split()) < 5:
            print("[visuals_controller] Pytesseract result weak, falling back to EasyOCR")
            reader = easyocr.Reader(['en'])
            result = reader.readtext(path, detail=0)
            text = "\n".join(result)
            print(f"[visuals_controller] EasyOCR extracted text: {textwrap.shorten(text, width=100)}")

    else:
        raise ValueError("Unsupported file type: " + ext)

    print("\n📝 Extracted Text Preview:")
    print(textwrap.shorten(text, width=500, placeholder="..."))
    return text.strip()


# ------------------------------- 
# 🧩 Context detection for axis labels
# ------------------------------- 
def detect_axis_labels(text):
    print("[visuals_controller] Calling detect_axis_labels")
    """Try to guess what X and Y represent based on text."""
    text_lower = text.lower()

    # Patterns like "X-axis: Vertex", "Y-axis: Degree"
    x_match = re.search(r"x[- ]axis[:\\s]+([\\w\\s]+)", text_lower)
    y_match = re.search(r"y[- ]axis[:\\s]+([\\w\\s]+)", text_lower)

    if x_match and y_match:
        labels = x_match.group(1).title(), y_match.group(1).title()
        print(f"[visuals_controller] Detected axis labels using pattern 1: {labels}")
        return labels

    # Patterns like "Degree vs Vertex"
    vs_match = re.search(r"([\\w\\s]+)\\s+vs\\s+([\\w\\s]+)", text_lower)
    if vs_match:
        y_label = vs_match.group(1).strip().title()
        x_label = vs_match.group(2).strip().title()
        labels = x_label, y_label
        print(f"[visuals_controller] Detected axis labels using pattern 2: {labels}")
        return labels

    # Patterns like "Table showing Marks of Students"
    show_match = re.search(r"showing\\s+([\\w\\s]+)\\s+of\\s+([\\w\\s]+)", text_lower)
    if show_match:
        y_label = show_match.group(1).strip().title()
        x_label = show_match.group(2).strip().title()
        labels = x_label, y_label
        print(f"[visuals_controller] Detected axis labels using pattern 3: {labels}")
        return labels

    # Fallback
    print("[visuals_controller] No specific axis labels detected, using fallback.")
    return "Label", "Value"


# ------------------------------- 
# 🔍 Improved Numeric Data Extraction
# ------------------------------- 
def detect_numeric_sections(text):
    print("[visuals_controller] Calling detect_numeric_sections")
    """Detect numeric data like 'Degree of vertex A is 2' or 'Vertex B: 4'."""
    patterns = [
        r"(?:degree\\s*of\\s*)?vertex\\s*([A-Za-z0-9]+)\\s*(?:is|=|:|has\\s*degree\\s*of)?\\s*(\d+)",
        r"([A-Za-z0-9._ -]+)\\s*[:=]\\s*(\d+(?:\\.\\d+)?)"
    ]
    matches = []
    for pat in patterns:
        matches += re.findall(pat, text, flags=re.I)

    if not matches:
        print("[visuals_controller] No numeric sections found.")
        return None

    print(f"[visuals_controller] Found {len(matches)} potential numeric matches.")
    df = pd.DataFrame(matches, columns=["Label", "Value"])
    df["Label"] = df["Label"].str.strip().str.replace(r"\\s+", " ", regex=True)
    df["Value"] = pd.to_numeric(df["Value"], errors="coerce")
    df.dropna(inplace=True)

    df = df.groupby("Label", as_index=False)["Value"].sum()
    print("[visuals_controller] Processed numeric data into DataFrame:")
    print(df.head())
    return df.drop_duplicates()


# ------------------------------- 
# 📊 Chart Generation
# ------------------------------- 
def make_bar_chart(df, outdir, x_label, y_label):
    print(f"[visuals_controller] Calling make_bar_chart for {outdir}")
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
    print(f"[visuals_controller] Saved bar chart to {out}")


def make_pie_chart(df, outdir, title):
    print(f"[visuals_controller] Calling make_pie_chart for {outdir}")
    """Generate a clean pie chart with only percentages + labels."""
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
    print(f"[visuals_controller] Saved pie chart to {out}")
    return out


# ------------------------------- 
# ⚙️ Algorithm / Flowchart Detection
# ------------------------------- 
def detect_algorithm_section(text):
    print("[visuals_controller] Calling detect_algorithm_section")
    """Detect algorithmic or procedural steps and title."""
    algo_keywords = ["algorithm", "procedure", "steps to implement", "step", "input", "output"]
    if not any(k.lower() in text.lower() for k in algo_keywords):
        print("[visuals_controller] No algorithm keywords found.")
        return None, None

    print("[visuals_controller] Algorithm keywords found, proceeding with detection.")
    title_match = re.search(r"(Algorithm\\s*[\\w\\s-]*)" , text, re.I)
    title = title_match.group(1).strip() if title_match else "Algorithm Flowchart"

    match = re.search(r"(step\\s*1.*?)(?:\\n\\s*\\n|$)", text, flags=re.IGNORECASE | re.DOTALL)
    algo_text = match.group(1) if match else text
    print(f"[visuals_controller] Detected algorithm title: {title}")
    return algo_text.strip(), title


def extract_steps(text):
    print("[visuals_controller] Calling extract_steps")
    """Extract algorithm steps (including Input/Output)."""
    if not text:
        return []
    steps = []
    for line in text.splitlines():
        if re.search(r"(\\bstep\\s*\d+|^\d+\.)", line, re.I) or line.lower().startswith(("input", "output")):
            clean = re.sub(r"^\\s*(step\\s*\d+\.?|\d+\.?|-|\*)\\s*", "", line.strip(), flags=re.I)
            if clean:
                steps.append(clean)
    print(f"[visuals_controller] Extracted {len(steps)} algorithm steps.")
    return steps


def make_flowchart(steps, outdir, title="Algorithm Flowchart"):
    print(f"[visuals_controller] Calling make_flowchart for {outdir}")
    """Generate a flowchart from detected steps with a title."""
    dot = graphviz.Digraph(format="png")
    dot.attr(rankdir="TB", node="box", style="rounded,filled", fillcolor="white")

    # Add title node
    dot.node("title", title, shape="plaintext", fontsize="16", fontname="Helvetica-Bold")

    prev_node = "title"
    for i, s in enumerate(steps):
        node_id = f"n{i}"
        dot.node(node_id, textwrap.fill(s, 30))
        dot.edge(prev_node, node_id)
        prev_node = node_id
    
    rendered_path = dot.render(os.path.join(outdir, "flowchart"), cleanup=True)
    print(f"[visuals_controller] Saved flowchart to {rendered_path}")
    return rendered_path


# ============================================================ 
# 🚀 4) Main Processor
# ============================================================ 
def process_file_controller():
    print("\n" + "="*50)
    print("[visuals_controller] Received new request in process_file_controller")
    if 'file' not in request.files:
        print("[visuals_controller] Error: No file part in request")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        print("[visuals_controller] Error: No selected file")
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = file.filename
        print(f"[visuals_controller] Processing file: {filename}")
        # MODIFIED: Use an absolute path for the output directory
        backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        outdir_name = f"outputs_{Path(filename).stem}"
        outdir = os.path.join(backend_dir, 'generated', outdir_name)
        os.makedirs(outdir, exist_ok=True)
        print(f"[visuals_controller] Output directory: {outdir}")
        
        filepath = os.path.join(outdir, filename)
        file.save(filepath)
        print(f"[visuals_controller] File saved to: {filepath}")

        text = extract_text(filepath)
        results = {"extracted_chars": len(text.strip())}
        print(f"[visuals_controller] Extracted {results['extracted_chars']} characters.")

        # Detect axis context
        x_label, y_label = detect_axis_labels(text)
        print(f"[visuals_controller] Detected axis labels: X={x_label}, Y={y_label}")

        # --- Chart Data Detection ---
        print("[visuals_controller] Detecting numeric sections for charts...")
        df = detect_numeric_sections(text)
        if df is not None and not df.empty:
            print("[visuals_controller] Numeric data found, generating charts.")
            # MODIFIED: Return paths relative to the 'generated' directory
            results["bar_chart"] = os.path.join(outdir_name, "barchart.png")
            make_bar_chart(df, outdir, x_label, y_label)
            results["pie_chart"] = os.path.join(outdir_name, "piechart.png")
            make_pie_chart(df, outdir, f"{y_label} Distribution")
        else:
            print("[visuals_controller] No numeric data found for charts.")
            results["chart_info"] = "❌ No numeric data found for charts."

        # --- Algorithm Detection ---
        print("[visuals_controller] Detecting algorithm section...")
        algo_text, algo_title = detect_algorithm_section(text)
        if algo_text:
            print("[visuals_controller] Algorithm section found, extracting steps.")
            steps = extract_steps(algo_text)
            if steps:
                print("[visuals_controller] Steps found, generating flowchart.")
                # MODIFIED: Return path relative to the 'generated' directory
                results["flowchart"] = os.path.join(outdir_name, "flowchart.png")
                make_flowchart(steps, outdir, title=algo_title)
            else:
                print("[visuals_controller] Algorithm detected but no clear steps found.")
                results["flowchart"] = "⚠️ Algorithm detected but no clear steps found."
        else:
            print("[visuals_controller] No algorithm detected.")
            results["flowchart"] = "❌ No algorithm detected."

        print("[visuals_controller] Processing complete, returning results.")
        print("="*50 + "\n")
        return jsonify(results), 200