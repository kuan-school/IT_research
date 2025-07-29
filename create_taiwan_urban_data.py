#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create Taiwan Urban Data for SLEUTH
從土地利用資料提取都市區域並創建時間序列資料
"""

import numpy as np
from PIL import Image
import xarray as xr
from pathlib import Path
import sys

def create_urban_from_landuse(netcdf_path, output_path, year, target_size=(512, 512)):
    """
    從 NetCDF 土地利用資料創建都市 GIF
    
    Args:
        netcdf_path: NetCDF 檔案路徑
        output_path: 輸出 GIF 路徑  
        year: 年份
        target_size: 目標圖像大小
    """
    print(f"處理 {year} 年土地利用資料...")
    
    try:
        # 讀取 NetCDF 資料
        ds = xr.open_dataset(netcdf_path, engine='netcdf4')
        print(f"資料維度: {ds.dims}")
        
        # 尋找土地利用類型資料
        if 'LU_TYPE' in ds.data_vars:
            data_var = 'LU_TYPE'
            data = ds[data_var].values
        else:
            # 尋找其他可能的土地利用變數
            possible_vars = [var for var in ds.data_vars.keys() 
                           if 'LU' in var.upper() or 'PFT' in var.upper() or 'TYPE' in var.upper()]
            if possible_vars:
                data_var = possible_vars[0]
                data = ds[data_var].values
            else:
                print("找不到土地利用資料變數")
                return False
        
        print(f"使用變數: {data_var}")
        print(f"資料形狀: {data.shape}")
        print(f"資料範圍: {np.min(data)} - {np.max(data)}")
        
        # 如果是 3D 資料，取第一個時間片段
        if len(data.shape) == 3:
            data = data[0]
        
        # 處理 NaN 值
        data = np.nan_to_num(data, nan=0)
        
        # 創建都市遮罩
        # 根據 README 檔案，PFT 分類中 08 = 建成區
        # 但讓我們先檢查實際存在的值
        unique_values = np.unique(data)
        print(f"資料中的唯一值: {unique_values}")
        
        # 根據 README，08 = 建成區
        urban_value = 8
            
        print(f"使用建成區值: {urban_value}")
        urban_mask = (data == urban_value).astype(np.uint8) * 255
        
        print(f"都市像素數量: {np.sum(urban_mask > 0)}")
        print(f"都市面積比例: {np.sum(urban_mask > 0) / (data.shape[0] * data.shape[1]) * 100:.2f}%")
        
        # 調整大小
        if target_size:
            urban_img = Image.fromarray(urban_mask)
            urban_img = urban_img.resize(target_size, Image.Resampling.NEAREST)
            urban_mask = np.array(urban_img)
        
        # 創建 GIF
        urban_image = Image.fromarray(urban_mask, mode='L')
        urban_image = urban_image.convert('P')
        
        # 設定簡單的調色盤（黑白）
        palette = []
        for i in range(256):
            palette.extend([i, i, i])  # 灰階
        urban_image.putpalette(palette)
        
        urban_image.save(output_path, 'GIF')
        print(f"✓ 都市 GIF 已儲存: {output_path}")
        
        ds.close()
        return True
        
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def create_simple_road_data(template_path, output_path, density=0.02):
    """
    創建簡單的道路網絡資料
    """
    print(f"創建道路資料: {output_path}")
    
    try:
        # 讀取模板圖像
        template = Image.open(template_path)
        width, height = template.size
        
        # 創建簡單的道路網格
        road_data = np.zeros((height, width), dtype=np.uint8)
        
        # 添加主要道路（垂直和水平線）
        spacing = int(1.0 / density)
        
        # 垂直道路
        for x in range(0, width, spacing):
            if x < width:
                road_data[:, x] = 255
        
        # 水平道路  
        for y in range(0, height, spacing):
            if y < height:
                road_data[y, :] = 255
                
        print(f"道路像素數量: {np.sum(road_data > 0)}")
        
        # 創建 GIF
        road_image = Image.fromarray(road_data)
        road_image = road_image.convert('P')
        
        # 設定調色盤
        palette = []
        for i in range(256):
            palette.extend([i, i, i])
        road_image.putpalette(palette)
        
        road_image.save(output_path, 'GIF')
        print(f"✓ 道路 GIF 已儲存: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ 道路資料創建失敗: {e}")
        return False

def create_excluded_areas(template_path, output_path):
    """
    創建排除區域（海洋、湖泊等）
    """
    print(f"創建排除區域: {output_path}")
    
    try:
        template = Image.open(template_path)
        width, height = template.size
        
        # 創建簡單的排除區域（邊界）
        excluded = np.zeros((height, width), dtype=np.uint8)
        
        # 邊界設為排除區域
        border_width = 10
        excluded[:border_width, :] = 255  # 上邊界
        excluded[-border_width:, :] = 255  # 下邊界
        excluded[:, :border_width] = 255  # 左邊界
        excluded[:, -border_width:] = 255  # 右邊界
        
        # 創建 GIF
        excluded_image = Image.fromarray(excluded)
        excluded_image = excluded_image.convert('P')
        
        palette = []
        for i in range(256):
            palette.extend([i, i, i])
        excluded_image.putpalette(palette)
        
        excluded_image.save(output_path, 'GIF')
        print(f"✓ 排除區域 GIF 已儲存: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ 排除區域創建失敗: {e}")
        return False

def main():
    print("=== 創建台灣 SLEUTH 都市資料 ===")
    
    # 設定路徑
    base_path = Path(".")
    landuse_path = base_path / "land_use_data"
    output_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_full")
    
    # 確保輸出目錄存在
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 年份和對應的 NetCDF 檔案
    years_data = {
        1994: "1994_500m_6PFT.nc",
        2000: "2000_500m_6PFT.nc", 
        2005: "2005_500m_6PFT.nc",
        2010: "2010_500m_6PFT.nc",
        2015: "2015_500m_6PFT.nc"
    }
    
    # 創建都市資料
    print("\n1. 創建都市時間序列資料...")
    urban_files = []
    for year, filename in years_data.items():
        netcdf_file = landuse_path / filename
        output_file = output_dir / f"taiwan.urban.{year}.gif"
        
        if netcdf_file.exists():
            if create_urban_from_landuse(netcdf_file, output_file, year):
                urban_files.append(output_file)
        else:
            print(f"找不到檔案: {filename}")
    
    if not urban_files:
        print("✗ 沒有成功創建都市資料")
        return False
    
    # 使用第一個都市檔案作為模板創建道路資料
    print("\n2. 創建道路資料...")
    template_file = urban_files[0]
    
    for year in years_data.keys():
        road_file = output_dir / f"taiwan.roads.{year}.gif"
        create_simple_road_data(template_file, road_file, density=0.01)
    
    # 創建排除區域
    print("\n3. 創建排除區域...")
    excluded_file = output_dir / "taiwan.excluded.gif"
    create_excluded_areas(template_file, excluded_file)
    
    print(f"\n=== 完成 ===")
    print(f"檔案輸出至: {output_dir}")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"錯誤: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)