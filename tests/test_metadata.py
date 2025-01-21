from PIL import Image
import piexif

def get_exif(img_path):
    image=Image.open(img_path)
    exif_dict=piexif.load(img_path)
    return exif_dict
def main():
    my_img_path="output_image_with_maker_note.jpg"
    expected_img_path="Sample Files/cm_jomsom_airport-25-01-14-05-15-00-AM.jpg"
    print(get_exif(my_img_path))
    print("==========================================")
    print(get_exif(expected_img_path))
main()