import gradio as gr
from ultralytics import YOLO
from PIL import Image
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- Animal Info Dictionary ---
animal_info = {
    "alligator": {
        "habitat": "Freshwater environments such as swamps, marshes, and rivers in the southeastern United States and parts of China.",
        "background": "Alligators are large reptiles known for their powerful bite and armored bodies.",
        "harmful": True,
        "advantages": "Control fish and turtle populations, maintain wetland balance.",
        "disadvantages": "Can attack humans or livestock if threatened.",
        "age": "35-50 years in the wild",
        "icon": "🐊",
        "country_distribution": {"USA": 50, "China": 20, "India": 10, "Pakistan": 10, "Bangladesh": 10}
    },
    "bear": {
        "habitat": "Forests, mountains, tundra, and grasslands in North America, Europe, and Asia.",
        "background": "Bears are large mammals with a varied diet. Some species, like the polar bear, are apex predators.",
        "harmful": True,
        "advantages": "Disperse seeds, control insect populations, maintain ecosystem balance.",
        "disadvantages": "Can be dangerous to humans if surprised or provoked.",
        "age": "20-25 years in the wild",
        "icon": "🐻",
        "country_distribution": {"Russia": 30, "India": 25, "China": 20, "Pakistan": 15, "Japan": 10}
    },
    "boar": {
        "habitat": "Forests, grasslands, and farmlands worldwide.",
        "background": "Wild boars are aggressive omnivores known for rooting behavior and adaptability.",
        "harmful": True,
        "advantages": "Soil aeration through rooting, part of food chain.",
        "disadvantages": "Can damage crops and spread disease.",
        "age": "10-14 years",
        "icon": "🐗",
        "country_distribution": {"India": 30, "Pakistan": 25, "Bangladesh": 20, "Nepal": 15, "China": 10}
    },
    "cougar": {
        "habitat": "Mountains, forests, and deserts across the Americas.",
        "background": "Also known as mountain lions, cougars are solitary and elusive big cats.",
        "harmful": True,
        "advantages": "Regulate deer population, support biodiversity.",
        "disadvantages": "Rarely, they can attack humans or livestock.",
        "age": "8-13 years in the wild",
        "icon": "🐆",
        "country_distribution": {"USA": 50, "Canada": 25, "Mexico": 15, "Brazil": 5, "Colombia": 5}
    },
    "coyote": {
        "habitat": "Grasslands, deserts, and forests across North America.",
        "background": "Coyotes are clever and adaptable canines found near both rural and urban areas.",
        "harmful": "Sometimes",
        "advantages": "Control rodent populations, clean up carrion.",
        "disadvantages": "Can attack livestock or pets.",
        "age": "10-14 years in the wild",
        "icon": "🐺",
        "country_distribution": {"USA": 60, "Mexico": 20, "Canada": 10, "India": 5, "Pakistan": 5}
    },
    "deer": {
        "habitat": "Forests, grasslands, and mountainous regions worldwide.",
        "background": "Deer are herbivorous mammals known for antlers and gentle behavior.",
        "harmful": False,
        "advantages": "Prey for predators, help seed dispersal.",
        "disadvantages": "Can damage crops or vegetation if overpopulated.",
        "age": "6-14 years",
        "icon": "🦌",
        "country_distribution": {"India": 40, "Pakistan": 20, "Nepal": 15, "Bangladesh": 15, "China": 10}
    },
    "fox": {
        "habitat": "Forests, grasslands, mountains, and urban areas around the world.",
        "background": "Foxes are small, cunning omnivores known for their adaptability.",
        "harmful": "Rarely",
        "advantages": "Control pests like rodents and insects.",
        "disadvantages": "May prey on poultry or small pets.",
        "age": "3-6 years in the wild",
        "icon": "🦊",
        "country_distribution": {"India": 30, "Pakistan": 25, "Nepal": 15, "Bangladesh": 15, "China": 15}
    },
    "moose": {
        "habitat": "Boreal forests and cold regions in the Northern Hemisphere.",
        "background": "Moose are the largest species in the deer family with large antlers.",
        "harmful": False,
        "advantages": "Support predator populations, maintain vegetation balance.",
        "disadvantages": "Can damage forests and be a road hazard.",
        "age": "15-20 years",
        "icon": "🦌",
        "country_distribution": {"Russia": 30, "Canada": 30, "USA": 20, "China": 10, "Pakistan": 10}
    },
    "raccoon": {
        "habitat": "Forests, wetlands, and urban areas in the Americas.",
        "background": "Raccoons are intelligent nocturnal mammals known for their dexterous paws.",
        "harmful": "Sometimes",
        "advantages": "Help control insects and small pests.",
        "disadvantages": "Can spread diseases and raid garbage.",
        "age": "2-3 years in the wild",
        "icon": "🦝",
        "country_distribution": {"USA": 50, "Canada": 20, "Mexico": 10, "India": 10, "Pakistan": 10}
    },
    "skunk": {
        "habitat": "Woodlands, fields, and suburban areas in the Americas.",
        "background": "Skunks are known for their defensive spray and black-and-white fur.",
        "harmful": "Rarely",
        "advantages": "Control insect and rodent populations.",
        "disadvantages": "Can cause odor nuisance, transmit rabies.",
        "age": "3-7 years",
        "icon": "🦨",
        "country_distribution": {"USA": 40, "Mexico": 25, "India": 15, "Pakistan": 10, "China": 10}
    },
    "snake": {
        "habitat": "Various habitats including forests, deserts, wetlands, and grasslands.",
        "background": "Snakes are legless reptiles with diverse diets and venomous or constricting methods.",
        "harmful": "Sometimes",
        "advantages": "Control pests like rodents, part of food chain.",
        "disadvantages": "Some species are venomous and dangerous to humans.",
        "age": "9-20 years",
        "icon": "🐍",
        "country_distribution": {"India": 30, "Pakistan": 25, "Bangladesh": 15, "Nepal": 15, "China": 15}
    },
    "wolf": {
        "habitat": "Forests, tundra, deserts, mountains, and grasslands of North America, Europe, and Asia.",
        "background": "Wolves are highly social animals that live and hunt in packs. They are ancestors of domestic dogs.",
        "harmful": "Sometimes",
        "advantages": "Control populations of deer and other prey, support ecosystem health.",
        "disadvantages": "Rarely attack humans, but can threaten livestock.",
        "age": "6-8 years in the wild",
        "icon": "🐺",
        "country_distribution": {"India": 30, "China": 25, "Mongolia": 20, "Pakistan": 15, "Kazakhstan": 10}
    }
}

# --- Custom CSS (Modern Professional Look) ---
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

body, .gradio-container {
    font-family: 'Inter', sans-serif;
    background-color: #F4F6F7;
}

h1 {
    color: #1B4F72 !important;
    text-align: center;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem;
    background: -webkit-linear-gradient(45deg, #1B4F72, #2E86C1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.animal-card {
    background-color: #FFFFFF;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    border: 1px solid #E0E0E0;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.animal-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 15px rgba(0, 0, 0, 0.1);
}

.animal-icon {
    font-size: 2rem;
    margin-right: 10px;
    vertical-align: middle;
}

.animal-title {
    font-size: 1.4rem;
    font-weight: 700;
    color: #2E86C1;
    vertical-align: middle;
}

.tag {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 700;
    text-transform: uppercase;
    display: inline-block;
    float: right;
}

.tag-dangerous { background-color: rgba(231, 76, 60, 0.1); color: #C0392B; }
.tag-safe { background-color: rgba(39, 174, 96, 0.1); color: #27AE60; }
.tag-caution { background-color: rgba(241, 196, 15, 0.1); color: #D35400; }

.animal-detail {
    margin-top: 8px;
    font-size: 0.95rem;
    line-height: 1.5;
    color: #34495E;
}

.animal-detail strong {
    color: #1B4F72;
}
"""

# --- Helper Functions ---

def render_animal_card_html(animal_name):
    info = animal_info.get(animal_name.lower())
    if info:
        icon = info.get("icon", "")
        harmful = info.get('harmful')
        if harmful is True:
            tag_class = "tag-dangerous"
            tag_text = "Dangerous"
            harmful_text = "Yes"
        elif harmful is False:
            tag_class = "tag-safe"
            tag_text = "Safe"
            harmful_text = "No"
        else:
            tag_class = "tag-caution"
            tag_text = "Caution"
            harmful_text = "Sometimes"

        html = f"""
        <div class='animal-card'>
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid #eee; padding-bottom:8px;">
                <div>
                    <span class='animal-icon'>{icon}</span>
                    <span class='animal-title'>{animal_name.title()}</span>
                </div>
                <span class='tag {tag_class}'>{tag_text}</span>
            </div>
            <div class='animal-detail'><strong>Habitat:</strong> {info['habitat']}</div>
            <div class='animal-detail'><strong>Background:</strong> {info['background']}</div>
            <div class='animal-detail'><strong>Harmful to Humans:</strong> {harmful_text}</div>
            <div class='animal-detail'><strong>Advantages:</strong> {info['advantages']}</div>
            <div class='animal-detail'><strong>Disadvantages:</strong> {info['disadvantages']}</div>
            <div class='animal-detail'><strong>Lifespan:</strong> {info['age']}</div>
        </div>
        """
        return html
    else:
        return f"<div style='padding:10px;'><strong>{animal_name.title()}:</strong> No info available.</div>"

# This function processes a single image and returns the annotated image and detected animals
def process_image_for_detection(image):
    if image is None:
        return None, []

    model_path = "best.pt"
    if not os.path.exists(model_path):
        # Return an error or empty results if model is not found
        return None, [], "<div style='color:red;'>Error: best.pt model not found!</div>"

    model = YOLO(model_path)
    results = model.predict(image)

    result_image = results[0].plot()

    detected_animals = []
    names = results[0].names
    for box in results[0].boxes:
        class_id = int(box.cls[0])
        detected_animals.append(names[class_id])

    return result_image, detected_animals

def detect_objects(image, history):
    if image is None:
        return None, "", history, history

    # Call the core image processing function
    result_image, detected_animals = process_image_for_detection(image)

    # Check if process_image_for_detection returned an error message
    if isinstance(result_image, str) and "Error" in result_image:
        return None, result_image, history, history # Return error message if model not found

    # Update History
    new_history = history + [detected_animals]

    # Generate Info HTML
    info_html = ""
    unique_animals = set(detected_animals)
    if unique_animals:
        info_html += "<h3 style='color:#2E86C1; margin-top:20px;'>🐾 Animals Detected</h3>"
        for animal in unique_animals:
            info_html += render_animal_card_html(animal)
    else:
        info_html = "<div style='padding:20px; text-align:center; color:#7F8C8D;'>No dangerous animals detected.</div>"

    return result_image, info_html, new_history, new_history # Return updated history

def get_history_html(history):
    # Flatten history
    all_animals = set()
    for detection in history:
        all_animals.update(detection)

    if not all_animals:
        return "<div style='text-align:center; padding:20px;'>No detection history yet.</div>"

    html = "<h3 style='color:#1B4F72;'>📜 Full Detection History</h3>"
    for animal in all_animals:
        html += render_animal_card_html(animal)
    return html

def get_history_dataframe(history):
    data = []
    for idx, animals in enumerate(history, 1):
        for animal in animals:
            data.append({"Upload ID": idx, "Animal": animal.title()})
    return pd.DataFrame(data)

def export_csv(history):
    df = get_history_dataframe(history)
    csv_path = "detection_history.csv"
    df.to_csv(csv_path, index=False)
    return csv_path

def generate_graph(history):
    all_animals = set()
    for detection in history:
        all_animals.update(detection)

    selectable_animals = [
        animal for animal in all_animals
        if animal in animal_info and "country_distribution" in animal_info[animal]
    ]

    if not selectable_animals:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, "No data available for graph yet.", ha='center', va='center')
        ax.axis('off')
        return gr.update(choices=[], value=None), fig

    # Default to first animal if available
    first_animal = selectable_animals[0]
    return gr.update(choices=[a.title() for a in selectable_animals], value=first_animal.title()), update_plot(first_animal.title())

def update_plot(selected_animal_title):
    if not selected_animal_title:
        return None

    animal_key = selected_animal_title.lower()
    if animal_key not in animal_info or "country_distribution" not in animal_info[animal_key]:
        return None

    dist = animal_info[animal_key]["country_distribution"]
    countries = list(dist.keys())
    percentages = list(dist.values())

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(countries, percentages, color='#2E86C1')
    ax.set_ylabel('Population Distribution (%)')
    ax.set_title(f'{selected_animal_title} Distribution in Asia')
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height}%', ha='center', va='bottom')

    plt.tight_layout()
    return fig

# --- App Layout ---
with gr.Blocks(theme=gr.themes.Soft(), css=custom_css, title="Dangerous Animal Detection") as demo:

    # State for history: List of lists of strings
    history_state = gr.State([])

    gr.HTML("<h1>🐾 Dangerous Animal Detection</h1>")
    gr.HTML("<h4 style='text-align:center; color:#7F8C8D;'>Professional Edition • Developed by Bu Ali</h4>")

    with gr.Tabs() as tabs:

        # --- Tab 1: Detection ---
        with gr.TabItem("🔍 Detection"):
            with gr.Row():
                with gr.Column(scale=1):
                    input_image = gr.Image(type="pil", label="Upload Image", sources=['upload'])
                    detect_btn = gr.Button("Detect Animals", variant="primary")
                    reset_btn = gr.Button("Reset Image", variant="secondary")

                with gr.Column(scale=1):
                    output_image = gr.Image(label="Detection Result")

            output_info = gr.HTML(label="Animal Info")

            detect_btn.click(
                detect_objects,
                inputs=[input_image, history_state],
                outputs=[output_image, output_info, history_state, history_state] # Update state
            )
            reset_btn.click(lambda: None, None, input_image)

        # --- Tab 2: History ---
        with gr.TabItem("📜 History"):

            refresh_hist_btn = gr.Button("Refresh History")
            history_html = gr.HTML()
            history_table = gr.Dataframe(label="Detailed Log")
            download_csv = gr.File(label="Download CSV")

            def update_history_tab(history):
                html = get_history_html(history)
                df = get_history_dataframe(history)
                csv = export_csv(history)
                return html, df, csv

            refresh_hist_btn.click(
                update_history_tab,
                inputs=[history_state],
                outputs=[history_html, history_table, download_csv]
            )
            # Also auto-update when entering tab (approximate with button for now as tab select event is tricky in some versions)

        # --- Tab 3: Graph ---
        with gr.TabItem("🌏 Population Graph"):
            refresh_graph_btn = gr.Button("Load Graph Data")
            animal_dropdown = gr.Dropdown(label="Select Animal", choices=[])
            population_plot = gr.Plot(label="Population Distribution")

            refresh_graph_btn.click(
                generate_graph,
                inputs=[history_state],
                outputs=[animal_dropdown, population_plot]
            )

            animal_dropdown.change(
                update_plot,
                inputs=[animal_dropdown],
                outputs=[population_plot]
            )

    # Footer
    gr.HTML("<hr><div style='text-align:center; color:#95A5A6; padding:20px;'>© 2025 Dangerous Animal Detection App</div>")

if __name__ == "__main__":
    demo.launch(share=True)