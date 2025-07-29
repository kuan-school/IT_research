#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建Taiwan背景檔案
"""

from PIL import Image
import numpy as np

def create_background_gif():
    """創建200x200的黑色背景GIF檔案"""
    # 創建200x200黑色圖片
    img_array = np.zeros((200, 200), dtype=np.uint8)
    
    # 創建PIL圖片
    img = Image.fromarray(img_array, mode='L')
    
    # 儲存為GIF87a格式
    output_path = "SLEUTH3.0beta_p01_linux/Input/taiwan_sleuth/taiwan.background.gif"
    img.save(output_path, 'GIF')
    
    # 驗證檔案標頭
    with open(output_path, 'rb') as f:
        header = f.read(6)
        if header.startswith(b'GIF87a'):
            print(f"✓ 成功創建背景檔案: {output_path}")
            return True
        else:
            print(f"✗ 格式錯誤: {header}")
            return False

if __name__ == "__main__":
    create_background_gif()