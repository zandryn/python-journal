import os
import json
import pathlib
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

"""
extracts and returns basic and exif metadata from an image file.
returns a dictionary with all metadata instead of just printing.
"""
def get_image_metadata(imagename):
    metadata = {
        "filename": str(imagename),
        "basic_info": {},
        "exif_data": {},
        "gps_data": {},
        "error": None
    }

    try:
        # read the image data using pil
        image = Image.open(imagename)

        # --- basic metadata ---
        metadata["basic_info"] = {
            "filename": str(image.filename),
            "size": image.size,
            "height": image.height,
            "width": image.width,
            "format": image.format,
            "mode": image.mode,
            "is_animated": getattr(image, "is_animated", False),
            "frames": getattr(image, "n_frames", 1)
        }

        # --- exif data ---
        exifdata = image.getexif()
        if exifdata:
            for tag_id in exifdata:
                # get the tag name
                tag = TAGS.get(tag_id, tag_id)
                data = exifdata.get(tag_id)

                # handle gps data separately
                if tag == "GPSInfo" and isinstance(data, dict):
                    gps_dict = {}
                    for gps_tag in data:
                        gps_name = GPSTAGS.get(gps_tag, gps_tag)
                        gps_dict[gps_name] = data[gps_tag]
                    metadata["gps_data"] = gps_dict
                else:
                    # handle bytes data safely
                    if isinstance(data, bytes):
                        # try to decode, otherwise show repr
                        try:
                            data = data.decode('utf-8')
                        except:
                            data = repr(data)

                    metadata["exif_data"][tag] = str(data) if data else None

    except FileNotFoundError:
        metadata["error"] = f"Image not found at {imagename}"
    except Exception as e:
        metadata["error"] = f"Error processing {imagename}: {str(e)}"

    return metadata

"""prints the metadata dictionary"""
def print_metadata(metadata):
    print("=" * 50)
    print(f"Processing Image: **{metadata['filename']}**")
    print("=" * 50)

    if metadata["error"]:
        print(f"ERROR: {metadata['error']}")
        return

    # print basic info
    print("\n**Basic Image Info:**")
    for key, value in metadata["basic_info"].items():
        print(f"  {key:20}: {value}")

    # print exif data
    if metadata["exif_data"]:
        print("\n**EXIF Data:**")
        for key, value in metadata["exif_data"].items():
            # truncate long values for display
            display_value = str(value)[:100] + "..." if len(str(value)) > 100 else value
            print(f"  {key:20}: {display_value}")
    else:
        print("\n**No EXIF data found.**")

    # print gps data
    if metadata["gps_data"]:
        print("\n**GPS Data:**")
        for key, value in metadata["gps_data"].items():
            print(f"  {key:20}: {value}")

    print("\n" + "-" * 50 + "\n")

"""saves all metadata to a json file"""
def save_to_json(all_metadata, filename="image_metadata.json"):
    # convert any non-serializable objects
    def make_serializable(obj):
        if isinstance(obj, tuple):
            return list(obj)
        elif isinstance(obj, bytes):
            return repr(obj)
        return obj

    serializable_data = []
    for metadata in all_metadata:
        clean_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, dict):
                clean_metadata[key] = {k: make_serializable(v) for k, v in value.items()}
            else:
                clean_metadata[key] = make_serializable(value)
        serializable_data.append(clean_metadata)

    with open(filename, 'w') as f:
        json.dump(serializable_data, f, indent=2)
    print(f"\nMetadata saved to {filename}")


def main():
    # get all image files (case-insensitive)
    supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.webp'}

    # debug: show all files in directory
    all_files = list(pathlib.Path('.').iterdir())
    print(f"Total files in directory: {len(all_files)}")

    # find image files
    image_files = []
    skipped_files = []

    for f in pathlib.Path('.').iterdir():
        if f.is_file():
            if f.suffix.lower() in supported_formats:
                image_files.append(f)
                print(f"✓ Found: {f.name}")
            elif any(ext in f.name.lower() for ext in ['jpg', 'jpeg', 'png']):
                skipped_files.append(f)
                print(f"✗ Skipped: {f.name} (suffix: '{f.suffix}')")

    if skipped_files:
        print(f"\nNote: Some files with image-like names were skipped. Check their extensions.")

    if not image_files:
        print(f"\nNo image files found in the current directory.")
        print(f"Supported formats: {', '.join(supported_formats)}")
        return

    print(f"\nProcessing {len(image_files)} image(s)...\n")

    all_metadata = []

    # process each image
    for image_path in image_files:
        print(f">>> Attempting to process: {image_path.name}")
        metadata = get_image_metadata(image_path)
        all_metadata.append(metadata)

        # check if there was an error with this specific file
        if metadata.get("error"):
            print(f"!!! Error with {image_path.name}: {metadata['error']}")

        print_metadata(metadata)

    # ask if user wants to save to json
    if all_metadata:
        save_option = input("\nWould you like to save all metadata to JSON? (y/n): ").strip().lower()
        if save_option == 'y':
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            json_filename = f"image_metadata_{timestamp}.json"
            save_to_json(all_metadata, json_filename)

if __name__ == "__main__":
    main()