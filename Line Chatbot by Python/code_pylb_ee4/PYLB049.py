import GT
import cv2
from stability_ai import text2image
api_key   = "***************************************"
engine_id = "***************************************"
filename_save = "image_out14.jpg"

prompt_text_th = "กล้วยยิ้มมีความสุขมากๆ"
prompt_text_en = GT.translate(prompt_text_th,'th','en') # th --> en
print(prompt_text_th)
print(prompt_text_en)
try:
    text2image(api_key,engine_id,prompt_text_en,filename_save)

    img = cv2.imread(filename_save)
    cv2.imshow("text2image",img)
    cv2.waitKey()
    cv2.destroyAllWindows()
except:
    print("no response")
