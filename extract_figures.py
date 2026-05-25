import os
import json
import base64

notebooks = {
    "spam_lr": "spam mail/Logistic Regression.ipynb",
    "spam_nb": "spam mail/Naive_Bayes_(GaussianNB).ipynb",
    "spam_svm": "spam mail/SVM.ipynb",
    "sale_pred": "predicting product sale/Predicting_product_sale_ippynb.ipynb",
    "img_seg": "image segment/Image_segmentation.ipynb",
    "house_pred": "predict house price/predecting_house_price.ipynb"
}

output_dir = "figures"
os.makedirs(output_dir, exist_ok=True)

print("Starting figures extraction...")

for name, path in notebooks.items():
    if not os.path.exists(path):
        print(f"Not found: {path}")
        continue
    
    with open(path, "r", encoding="utf-8") as f:
        try:
            nb = json.load(f)
        except Exception as e:
            print(f"Error loading {path}: {e}")
            continue
            
    img_idx = 1
    for cell in nb.get("cells", []):
        if cell.get("cell_type") == "code":
            # Loop through outputs
            for output in cell.get("outputs", []):
                if "data" in output and "image/png" in output["data"]:
                    img_data = output["data"]["image/png"]
                    if isinstance(img_data, list):
                        img_data = "".join(img_data)
                    
                    try:
                        img_bytes = base64.b64decode(img_data)
                        filename = f"{name}_fig_{img_idx}.png"
                        filepath = os.path.join(output_dir, filename)
                        with open(filepath, "wb") as img_file:
                            img_file.write(img_bytes)
                        print(f"-> Extracted: {filepath}")
                        img_idx += 1
                    except Exception as e:
                        print(f"Error decoding image in {path}: {e}")

print("Figures extraction completed successfully!")
