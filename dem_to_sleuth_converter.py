#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DEM to SLEUTH Converter
將台灣 DEM 資料轉換為 SLEUTH 所需的 GIF 格式
"""

import numpy as np
from PIL import Image
import rasterio
from rasterio.enums import Resampling
import os
import sys
from pathlib import Path

def dem_to_slope_gif(dem_path, output_path, target_size=None):
    """
    將 DEM TIFF 檔案轉換為坡度 GIF 檔案
    
    Args:
        dem_path (str): DEM TIFF 檔案路徑
        output_path (str): 輸出 GIF 檔案路徑
        target_size (tuple): 目標圖像大小 (width, height)，None 表示使用原始大小
    """
    print(f"正在處理 DEM 檔案: {dem_path}")
    
    with rasterio.open(dem_path) as src:
        print(f"原始檔案資訊:")
        print(f"  大小: {src.width} x {src.height}")
        print(f"  座標系統: {src.crs}")
        print(f"  解析度: {src.res}")
        print(f"  資料範圍: {src.bounds}")
        
        # 讀取高程資料
        elevation = src.read(1)
        
        # 處理 NoData 值
        nodata = src.nodata
        if nodata is not None:
            elevation = np.where(elevation == nodata, 0, elevation)
        
        # 將負值設為 0 (海平面以下)
        elevation = np.maximum(elevation, 0)
        
        print(f"高程資料統計:")
        print(f"  最小值: {np.min(elevation)} 公尺")
        print(f"  最大值: {np.max(elevation)} 公尺") 
        print(f"  平均值: {np.mean(elevation):.2f} 公尺")
        
        # 計算坡度 (使用簡單的梯度方法)
        print("正在計算坡度...")
        
        # 計算 x 和 y 方向的梯度
        dy, dx = np.gradient(elevation.astype(float))
        
        # 坡度計算 (弧度轉度數)
        slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
        slope_deg = np.degrees(slope_rad)
        
        print(f"坡度資料統計:")
        print(f"  最小坡度: {np.min(slope_deg):.2f} 度")
        print(f"  最大坡度: {np.max(slope_deg):.2f} 度")
        print(f"  平均坡度: {np.mean(slope_deg):.2f} 度")
        
        # 重新調整大小（如果需要）
        if target_size:
            print(f"調整圖像大小至: {target_size}")
            slope_img = Image.fromarray(slope_deg.astype(np.float32))
            slope_img = slope_img.resize(target_size, Image.Resampling.LANCZOS)
            slope_deg = np.array(slope_img)
        
        # 正規化坡度值到 0-255 範圍
        slope_normalized = np.clip(slope_deg * 255 / 90, 0, 255).astype(np.uint8)
        
        # 創建 PIL 圖像
        slope_image = Image.fromarray(slope_normalized, mode='L')
        
        # 轉換為索引顏色模式 (SLEUTH 要求)
        slope_image = slope_image.convert('P')
        
        # 儲存為 GIF
        slope_image.save(output_path, 'GIF')
        print(f"✓ 坡度 GIF 已儲存: {output_path}")
        print(f"  檔案大小: {os.path.getsize(output_path) / 1024:.1f} KB")
        
        return True

def dem_to_elevation_gif(dem_path, output_path, target_size=None):
    """
    將 DEM TIFF 檔案直接轉換為高程 GIF 檔案
    
    Args:
        dem_path (str): DEM TIFF 檔案路徑  
        output_path (str): 輸出 GIF 檔案路徑
        target_size (tuple): 目標圖像大小 (width, height)
    """
    print(f"正在處理高程資料: {dem_path}")
    
    with rasterio.open(dem_path) as src:
        # 讀取高程資料
        elevation = src.read(1)
        
        # 處理 NoData 值
        nodata = src.nodata
        if nodata is not None:
            elevation = np.where(elevation == nodata, 0, elevation)
        
        # 將負值設為 0
        elevation = np.maximum(elevation, 0)
        
        # 重新調整大小（如果需要）
        if target_size:
            print(f"調整圖像大小至: {target_size}")
            elev_img = Image.fromarray(elevation.astype(np.float32))
            elev_img = elev_img.resize(target_size, Image.Resampling.LANCZOS)
            elevation = np.array(elev_img)
        
        # 正規化高程值到 0-255 範圍
        max_elev = np.max(elevation)
        if max_elev > 0:
            elevation_normalized = (elevation * 255 / max_elev).astype(np.uint8)
        else:
            elevation_normalized = elevation.astype(np.uint8)
        
        # 創建並儲存 GIF
        elev_image = Image.fromarray(elevation_normalized, mode='L')
        elev_image = elev_image.convert('P')
        elev_image.save(output_path, 'GIF')
        
        print(f"✓ 高程 GIF 已儲存: {output_path}")
        print(f"  最大高程: {max_elev:.1f} 公尺")
        
        return True

def main():
    """主程式"""
    print("=== DEM to SLEUTH 轉換器 ===")
    
    # 設定檔案路徑
    dem_file = "dem_20m.tif"
    sleuth_input_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_full")
    
    # 確保輸出目錄存在
    sleuth_input_dir.mkdir(parents=True, exist_ok=True)
    
    # 檢查 DEM 檔案是否存在
    if not os.path.exists(dem_file):
        print(f"✗ 找不到 DEM 檔案: {dem_file}")
        return False
    
    # 轉換為坡度 GIF (SLEUTH 主要需要這個)
    slope_output = sleuth_input_dir / "taiwan.slope.gif"
    print(f"\n1. 轉換坡度資料...")
    if dem_to_slope_gif(dem_file, str(slope_output)):
        print("✓ 坡度轉換成功")
    else:
        print("✗ 坡度轉換失敗")
        return False
    
    # 也轉換高程資料供參考
    elevation_output = sleuth_input_dir / "taiwan.elevation.gif"
    print(f"\n2. 轉換高程資料...")
    if dem_to_elevation_gif(dem_file, str(elevation_output)):
        print("✓ 高程轉換成功")
    else:
        print("✗ 高程轉換失敗")
    
    print(f"\n=== 轉換完成 ===")
    print(f"輸出檔案位於: {sleuth_input_dir}")
    print(f"- taiwan.slope.gif (供 SLEUTH 使用)")
    print(f"- taiwan.elevation.gif (供參考)")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"錯誤: {e}")
        sys.exit(1)