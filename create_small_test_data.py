#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create smaller test data for SLEUTH Taiwan simulation
"""

import numpy as np
from PIL import Image
from pathlib import Path

def resize_gif(input_path, output_path, target_size=(200, 200)):
    """調整 GIF 檔案大小"""
    print(f"調整 {input_path} 大小至 {target_size}")
    
    try:
        # 開啟圖片
        img = Image.open(input_path)
        
        # 調整大小
        img_resized = img.resize(target_size, Image.Resampling.NEAREST)
        
        # 確保是 P 模式（索引色彩）
        if img_resized.mode != 'P':
            img_resized = img_resized.convert('P')
        
        # 儲存
        img_resized.save(output_path, 'GIF')
        print(f"✓ 已儲存至: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def main():
    print("=== 創建小型測試資料 ===")
    
    # 設定路徑
    input_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_full")
    output_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_small")
    
    # 確保輸出目錄存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 需要調整的檔案
    files_to_resize = [
        "taiwan.slope.gif",
        "taiwan.elevation.gif", 
        "taiwan.excluded.gif",
        "taiwan.urban.1994.gif",
        "taiwan.urban.2000.gif",
        "taiwan.urban.2005.gif",
        "taiwan.urban.2010.gif", 
        "taiwan.urban.2015.gif",
        "taiwan.roads.1994.gif",
        "taiwan.roads.2000.gif",
        "taiwan.roads.2005.gif",
        "taiwan.roads.2010.gif",
        "taiwan.roads.2015.gif"
    ]
    
    # 調整所有檔案大小
    for filename in files_to_resize:
        input_file = input_dir / filename
        output_file = output_dir / filename
        
        if input_file.exists():
            resize_gif(input_file, output_file, target_size=(200, 200))
        else:
            print(f"檔案不存在: {input_file}")
    
    print(f"\n完成！小型測試資料已創建於: {output_dir}")

if __name__ == "__main__":
    main()