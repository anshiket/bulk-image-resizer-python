import os
import time
from PIL import Image

# -------------------------
# LITE VERSION LIMITS
# -------------------------
MAX_IMAGES = 5              # Max images per batch
MAX_USES = 3                # Total number of allowed runs
DELAY_PER_IMAGE = 3         # Seconds delay per image
USAGE_FILE = ".lite_usage_count"
# -------------------------

INPUT_FOLDER = "input_images"
OUTPUT_FOLDER = "optimized_images"
TARGET_WIDTH = 1080
QUALITY = 85


def get_usage_count():
    """Read usage count from hidden file."""
    if not os.path.exists(USAGE_FILE):
        return 0
    try:
        with open(USAGE_FILE, "r") as f:
            return int(f.read().strip())
    except:
        return 0


def increment_usage_count():
    """Increase usage count by 1."""
    count = get_usage_count() + 1
    with open(USAGE_FILE, "w") as f:
        f.write(str(count))
    return count


def check_usage_limit():
    """Check and enforce max usage limit."""
    count = get_usage_count()
    if count >= MAX_USES:
        print("\n❌ LITE VERSION LIMIT REACHED")
        print("You have used the free version 3 times.")
        print("Unlock unlimited images & fast processing here:")
        print("👉 https://anshika636.gumroad.com/l/image-tool\n")
        input("Press Enter to exit...")
        exit()

    new_count = increment_usage_count()
    print(f"\n🔹 Lite version use: {new_count}/{MAX_USES} allowed.\n")


def resize_images():
    check_usage_limit()

    # Create output folder if needed
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

    # Check input folder
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Folder '{INPUT_FOLDER}' not found.")
        return

    images = [f for f in os.listdir(INPUT_FOLDER)
              if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if not images:
        print("No images found in input_images/")
        return

    print(f"Found {len(images)} images.")

    if len(images) > MAX_IMAGES:
        print(f"\n⚠ LITE VERSION: Only first {MAX_IMAGES} images will be processed.")
        print("👉 Full version (unlimited images): https://anshika636.gumroad.com/l/image-tool\n")

    images = images[:MAX_IMAGES]

    print(f"Starting optimization for {len(images)} image(s)...\n")

    for img_name in images:
        try:
            img_path = os.path.join(INPUT_FOLDER, img_name)
            with Image.open(img_path) as img:
                aspect_ratio = img.height / img.width
                new_height = int(TARGET_WIDTH * aspect_ratio)

                img = img.resize((TARGET_WIDTH, new_height), Image.Resampling.LANCZOS)

                # Add watermark suffix
                output_name = img_name.rsplit('.', 1)[0] + "_LITE." + img_name.rsplit('.', 1)[1]

                save_path = os.path.join(OUTPUT_FOLDER, output_name)
                img.save(save_path, optimize=True, quality=QUALITY)

                print(f"✔ Processed: {img_name} → {output_name}")

                # Delay for lite version
                print(f"⏳ LITE version delay ({DELAY_PER_IMAGE}s)...")
                time.sleep(DELAY_PER_IMAGE)

        except Exception as e:
            print(f"❌ Error: {e}")

    print("\n--- LITE VERSION DONE ---")
    print("⚡ Full version = instant processing + unlimited images + no watermark")
    print("👉 https://anshika636.gumroad.com/l/image-tool")

    input("\nPress Enter to exit...")


if __name__ == "__main__":
    resize_images()
