#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析SLEUTH GIF格式差異
"""

from PIL import Image
import numpy as np
from pathlib import Path

def analyze_gif(filepath):
    """分析GIF檔案的詳細資訊"""
    print(f"\n=== 分析 {filepath} ===")
    
    try:
        img = Image.open(filepath)
        
        print(f"模式: {img.mode}")
        print(f"尺寸: {img.size}")
        print(f"格式: {img.format}")
        
        # 獲取調色盤資訊
        if img.mode == 'P':
            palette = img.getpalette()
            if palette:
                # 調色盤長度（RGB值，每個顏色3個值）
                num_colors = len(palette) // 3
                print(f"調色盤顏色數量: {num_colors}")
                
                # 前10個顏色
                print("前10個顏色 (RGB):")
                for i in range(min(10, num_colors)):
                    r, g, b = palette[i*3:(i+1)*3]
                    print(f"  {i}: ({r}, {g}, {b})")
        
        # 獲取像素值統計
        pixels = np.array(img)
        unique_values = np.unique(pixels)
        print(f"唯一像素值數量: {len(unique_values)}")
        print(f"像素值範圍: {pixels.min()} - {pixels.max()}")
        print(f"前10個唯一值: {unique_values[:10]}")
        
        # 檔案大小
        file_size = Path(filepath).stat().st_size
        print(f"檔案大小: {file_size} bytes")
        
        return {
            'mode': img.mode,
            'size': img.size,
            'format': img.format,
            'unique_values': unique_values,
            'num_colors': len(palette) // 3 if img.mode == 'P' and palette else 0,
            'file_size': file_size,
            'pixels': pixels
        }
        
    except Exception as e:
        print(f"錯誤: {e}")
        return None

def main():
    print("=== GIF格式分析 ===")
    
    # 分析demo200檔案
    demo_files = [
        "SLEUTH3.0beta_p01_linux/Input/demo200/demo200.slope.gif",
        "SLEUTH3.0beta_p01_linux/Input/demo200/demo200.urban.1930.gif",
        "SLEUTH3.0beta_p01_linux/Input/demo200/demo200.roads.1930.gif"
    ]
    
    # 分析taiwan檔案  
    taiwan_files = [
        "SLEUTH3.0beta_p01_linux/Input/taiwan_small/taiwan.slope.gif",
        "SLEUTH3.0beta_p01_linux/Input/taiwan_small/taiwan.urban.1994.gif",
        "SLEUTH3.0beta_p01_linux/Input/taiwan_small/taiwan.roads.1994.gif"
    ]
    
    print("\n" + "="*50)
    print("DEMO200 檔案分析")
    print("="*50)
    
    demo_results = {}
    for filepath in demo_files:
        if Path(filepath).exists():
            demo_results[filepath] = analyze_gif(filepath)
    
    print("\n" + "="*50)
    print("TAIWAN 檔案分析")
    print("="*50)
    
    taiwan_results = {}
    for filepath in taiwan_files:
        if Path(filepath).exists():
            taiwan_results[filepath] = analyze_gif(filepath)
    
    # 比較分析
    print("\n" + "="*50)
    print("格式差異比較")
    print("="*50)
    
    if demo_results and taiwan_results:
        print("\n主要差異:")
        
        # 比較slope檔案
        demo_slope = demo_results.get("SLEUTH3.0beta_p01_linux/Input/demo200/demo200.slope.gif")
        taiwan_slope = taiwan_results.get("SLEUTH3.0beta_p01_linux/Input/taiwan_small/taiwan.slope.gif")
        
        if demo_slope and taiwan_slope:
            print(f"\nSlope檔案比較:")
            print(f"  Demo200 - 模式: {demo_slope['mode']}, 尺寸: {demo_slope['size']}, 唯一值: {len(demo_slope['unique_values'])}")
            print(f"  Taiwan  - 模式: {taiwan_slope['mode']}, 尺寸: {taiwan_slope['size']}, 唯一值: {len(taiwan_slope['unique_values'])}")
            
            if demo_slope['mode'] != taiwan_slope['mode']:
                print(f"  ⚠️  模式不同: {demo_slope['mode']} vs {taiwan_slope['mode']}")
            
            if demo_slope['num_colors'] != taiwan_slope['num_colors']:
                print(f"  ⚠️  調色盤顏色數量不同: {demo_slope['num_colors']} vs {taiwan_slope['num_colors']}")

if __name__ == "__main__":
    main()