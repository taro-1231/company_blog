import os
from PIL import Image
from flask import current_app

# 送信フォームでimgはデータベースに直接入れれないからこんなことしてる
def add_featured_image(upload_image):
    image_filename=upload_image.filename
    # 画像ファイルの保存先、カンマでつなげれる
    filepath=os.path.join(current_app.root_path,r'static\featured_image',image_filename)
    image_size=(800,800)
    # openはこの関数が呼ばれたら表示するのではなく,imgの形を整えている
    image=Image.open(upload_image)
    image.thumbnail(image_size)
    image.save(filepath)
    # これはデータベース行らしい
    return image_filename
