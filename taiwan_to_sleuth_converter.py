#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Taiwan Data to SLEUTH Format Converter
將台灣地理資料轉換為 SLEUTH 模型所需的 GIF 格式

Required packages:
pip install gdal xarray rasterio pillow numpy matplotlib
"""

import os
import sys
import subprocess
import numpy as np
import xarray as xr
from PIL import Image
import argparse
from pathlib import Path

class TaiwanToSLEUTH:
    def __init__(self, output_dir="./sleuth_input", resolution=100):
        """
        初始化轉換器
        
        Args:
            output_dir: 輸出目錄
            resolution: 像素解析度 (公尺)
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.resolution = resolution
        
        # 台灣邊界 (TWD97座標系統)
        self.taiwan_bounds = {
            'xmin': 146000,  # 東經約119度
            'xmax': 351000,  # 東經約122度  
            'ymin': 2422000, # 北緯約22度
            'ymax': 2802000  # 北緯約25.5度
        }
        
    def setup_gdal_environment(self):
        """設置 GDAL 環境變數"""
        os.environ['GDAL_DATA'] = '/opt/homebrew/share/gdal'
        print("GDAL environment configured")
        
    def check_gdal_tools(self):
        """檢查 GDAL 工具是否可用"""
        tools = ['gdal_rasterize', 'gdal_translate', 'gdaldem', 'ogr2ogr']
        missing = []
        
        for tool in tools:
            try:
                subprocess.run([tool, '--version'], capture_output=True, check=True)
                print(f"✓ {tool} available")
            except (subprocess.CalledProcessError, FileNotFoundError):
                missing.append(tool)
                print(f"✗ {tool} not found")
        
        if missing:
            print(f"Missing GDAL tools: {missing}")
            print("Install with: brew install gdal")
            return False
        return True
        
    def shapefile_to_urban_gif(self, shapefile_paths, output_name, year):
        """
        將建築物 Shapefile 轉換為 Urban GIF
        
        Args:
            shapefile_paths: 建築物 shapefile 路徑列表
            output_name: 輸出檔案名稱前綴
            year: 年份
        """
        print(f"Converting urban data for {year}...")
        
        # 合併所有建築物 shapefile
        merged_shp = self.output_dir / f"urban_merged_{year}.shp"
        temp_tif = self.output_dir / f"urban_temp_{year}.tif"
        output_gif = self.output_dir / f"{output_name}.urban.{year}.gif"
        
        try:
            # 合併 shapefile
            if len(shapefile_paths) > 1:
                cmd_merge = [
                    'ogr2ogr', '-f', 'ESRI Shapefile', str(merged_shp),
                    str(shapefile_paths[0])
                ]
                subprocess.run(cmd_merge, check=True)
                
                for shp in shapefile_paths[1:]:
                    cmd_append = [
                        'ogr2ogr', '-f', 'ESRI Shapefile', '-update', '-append',
                        str(merged_shp), str(shp)
                    ]
                    subprocess.run(cmd_append, check=True)
            else:
                merged_shp = shapefile_paths[0]
            
            # 柵格化
            cmd_rasterize = [
                'gdal_rasterize',
                '-burn', '255',  # 建築物像素值設為 255 (白色)
                '-tr', str(self.resolution), str(self.resolution),
                '-te', str(self.taiwan_bounds['xmin']), str(self.taiwan_bounds['ymin']),
                       str(self.taiwan_bounds['xmax']), str(self.taiwan_bounds['ymax']),
                '-ot', 'Byte',
                str(merged_shp), str(temp_tif)
            ]
            subprocess.run(cmd_rasterize, check=True)
            
            # 轉換為 GIF
            cmd_gif = [
                'gdal_translate', '-of', 'GIF', '-ot', 'Byte',
                str(temp_tif), str(output_gif)
            ]
            subprocess.run(cmd_gif, check=True)
            
            print(f"✓ Urban GIF created: {output_gif}")
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error converting urban data: {e}")
        finally:
            # 清理臨時檔案
            for temp_file in [temp_tif]:
                if temp_file.exists():
                    temp_file.unlink()
                    
    def shapefile_to_roads_gif(self, road_shapefiles, output_name, year):
        """
        將道路 Shapefile 轉換為 Roads GIF
        
        Args:
            road_shapefiles: 道路 shapefile 路徑列表
            output_name: 輸出檔案名稱前綴  
            year: 年份
        """
        print(f"Converting roads data for {year}...")
        
        merged_shp = self.output_dir / f"roads_merged_{year}.shp"
        temp_tif = self.output_dir / f"roads_temp_{year}.tif"
        output_gif = self.output_dir / f"{output_name}.roads.{year}.gif"
        
        try:
            # 合併道路 shapefile
            if len(road_shapefiles) > 1:
                cmd_merge = [
                    'ogr2ogr', '-f', 'ESRI Shapefile', str(merged_shp),
                    str(road_shapefiles[0])
                ]
                subprocess.run(cmd_merge, check=True)
                
                for shp in road_shapefiles[1:]:
                    cmd_append = [
                        'ogr2ogr', '-f', 'ESRI Shapefile', '-update', '-append',
                        str(merged_shp), str(shp)
                    ]
                    subprocess.run(cmd_append, check=True)
            else:
                merged_shp = road_shapefiles[0]
            
            # 柵格化道路
            cmd_rasterize = [
                'gdal_rasterize',
                '-burn', '255',  # 道路像素值設為 255
                '-tr', str(self.resolution), str(self.resolution),
                '-te', str(self.taiwan_bounds['xmin']), str(self.taiwan_bounds['ymin']),
                       str(self.taiwan_bounds['xmax']), str(self.taiwan_bounds['ymax']),
                '-ot', 'Byte',
                str(merged_shp), str(temp_tif)
            ]
            subprocess.run(cmd_rasterize, check=True)
            
            # 轉換為 GIF
            cmd_gif = [
                'gdal_translate', '-of', 'GIF', '-ot', 'Byte',
                str(temp_tif), str(output_gif)
            ]
            subprocess.run(cmd_gif, check=True)
            
            print(f"✓ Roads GIF created: {output_gif}")
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error converting roads data: {e}")
        finally:
            # 清理臨時檔案
            for temp_file in [temp_tif]:
                if temp_file.exists():
                    temp_file.unlink()
                    
    def netcdf_to_landuse_gif(self, netcdf_path, output_name, year):
        """
        將 NetCDF 土地利用資料轉換為 Landuse GIF
        
        Args:
            netcdf_path: NetCDF 檔案路徑
            output_name: 輸出檔案名稱前綴
            year: 年份
        """
        print(f"Converting landuse data for {year}...")
        
        output_gif = self.output_dir / f"{output_name}.landuse.{year}.gif"
        
        try:
            # 讀取 NetCDF 資料
            ds = xr.open_dataset(netcdf_path)
            
            # 假設變數名為 'PFT' 或類似
            # 需要根據實際檔案結構調整
            if 'PFT' in ds.variables:
                data = ds['PFT'].values
            elif 'landuse' in ds.variables:
                data = ds['landuse'].values
            else:
                # 取第一個資料變數
                var_name = list(ds.data_vars.keys())[0]
                data = ds[var_name].values
                
            # PFT 分類對應到 SLEUTH landuse 分類
            # 原始: 01=Forest, 02=Grassland, 04=Agriculture, 08=Built-up, 13=Water, 26=Bare
            # SLEUTH: 0=Unclass, 1=Urban, 2=Agric, 3=Range, 4=Forest, 5=Water, 6=Wetland, 7=Barren
            landuse_map = {
                1: 4,   # Forest → Forest
                2: 3,   # Grassland → Range  
                4: 2,   # Agriculture → Agric
                8: 1,   # Built-up → Urban
                13: 5,  # Water → Water
                26: 7   # Bare → Barren
            }
            
            # 重新分類
            landuse_data = np.zeros_like(data, dtype=np.uint8)
            for original, sleuth in landuse_map.items():
                landuse_data[data == original] = sleuth
            
            # 轉換為 PIL Image 並儲存為 GIF
            # 注意：可能需要調整座標系統和重新採樣
            img = Image.fromarray(landuse_data, mode='L')
            
            # 重新調整大小到目標解析度
            target_width = int((self.taiwan_bounds['xmax'] - self.taiwan_bounds['xmin']) / self.resolution)
            target_height = int((self.taiwan_bounds['ymax'] - self.taiwan_bounds['ymin']) / self.resolution)
            img = img.resize((target_width, target_height), Image.NEAREST)
            
            img.save(output_gif)
            print(f"✓ Landuse GIF created: {output_gif}")
            
            ds.close()
            
        except Exception as e:
            print(f"✗ Error converting landuse data: {e}")
            
    def dem_to_slope_gif(self, dem_path, output_name):
        """
        將 DEM 轉換為坡度 GIF
        
        Args:
            dem_path: DEM 檔案路徑 (TIF 格式)
            output_name: 輸出檔案名稱前綴
        """
        print("Converting DEM to slope...")
        
        temp_slope_tif = self.output_dir / "slope_temp.tif"
        output_gif = self.output_dir / f"{output_name}.slope.gif"
        
        try:
            # 計算坡度 (以百分比表示)
            cmd_slope = [
                'gdaldem', 'slope', '-p',  # -p 表示百分比
                str(dem_path), str(temp_slope_tif)
            ]
            subprocess.run(cmd_slope, check=True)
            
            # 轉換為 8-bit GIF (0-100% 坡度映射到 0-255)
            cmd_gif = [
                'gdal_translate', '-of', 'GIF', '-ot', 'Byte',
                '-scale', '0', '100', '0', '255',  # 坡度縮放
                '-tr', str(self.resolution), str(self.resolution),
                '-te', str(self.taiwan_bounds['xmin']), str(self.taiwan_bounds['ymin']),
                       str(self.taiwan_bounds['xmax']), str(self.taiwan_bounds['ymax']),
                str(temp_slope_tif), str(output_gif)
            ]
            subprocess.run(cmd_gif, check=True)
            
            print(f"✓ Slope GIF created: {output_gif}")
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error converting slope data: {e}")
        finally:
            # 清理臨時檔案
            if temp_slope_tif.exists():
                temp_slope_tif.unlink()
                
    def create_excluded_gif(self, water_shapefiles, output_name):
        """
        創建排除區域 GIF (水體、海洋等)
        
        Args:
            water_shapefiles: 水體 shapefile 路徑列表
            output_name: 輸出檔案名稱前綴
        """
        print("Creating excluded areas GIF...")
        
        temp_tif = self.output_dir / "excluded_temp.tif"
        output_gif = self.output_dir / f"{output_name}.excluded.gif"
        
        try:
            # 合併水體 shapefile 並柵格化
            merged_shp = self.output_dir / "water_merged.shp"
            
            if len(water_shapefiles) > 1:
                cmd_merge = [
                    'ogr2ogr', '-f', 'ESRI Shapefile', str(merged_shp),
                    str(water_shapefiles[0])
                ]
                subprocess.run(cmd_merge, check=True)
                
                for shp in water_shapefiles[1:]:
                    cmd_append = [
                        'ogr2ogr', '-f', 'ESRI Shapefile', '-update', '-append',
                        str(merged_shp), str(shp)
                    ]
                    subprocess.run(cmd_append, check=True)
            else:
                merged_shp = water_shapefiles[0]
            
            # 柵格化 (排除區域設為 0，其他區域設為 255)
            cmd_rasterize = [
                'gdal_rasterize',
                '-burn', '0',  # 排除區域設為 0 (黑色)
                '-init', '255',  # 背景設為 255 (白色)
                '-tr', str(self.resolution), str(self.resolution),
                '-te', str(self.taiwan_bounds['xmin']), str(self.taiwan_bounds['ymin']),
                       str(self.taiwan_bounds['xmax']), str(self.taiwan_bounds['ymax']),
                '-ot', 'Byte',
                str(merged_shp), str(temp_tif)
            ]
            subprocess.run(cmd_rasterize, check=True)
            
            # 轉換為 GIF
            cmd_gif = [
                'gdal_translate', '-of', 'GIF', '-ot', 'Byte',
                str(temp_tif), str(output_gif)
            ]
            subprocess.run(cmd_gif, check=True)
            
            print(f"✓ Excluded GIF created: {output_gif}")
            
        except subprocess.CalledProcessError as e:
            print(f"✗ Error creating excluded areas: {e}")
        finally:
            # 清理臨時檔案
            for temp_file in [temp_tif]:
                if temp_file.exists():
                    temp_file.unlink()

def main():
    parser = argparse.ArgumentParser(description='Convert Taiwan geographic data to SLEUTH format')
    parser.add_argument('--output-dir', default='./sleuth_input', help='Output directory')
    parser.add_argument('--resolution', type=int, default=100, help='Pixel resolution in meters')
    parser.add_argument('--check-tools', action='store_true', help='Check if GDAL tools are available')
    
    args = parser.parse_args()
    
    converter = TaiwanToSLEUTH(args.output_dir, args.resolution)
    converter.setup_gdal_environment()
    
    if args.check_tools:
        if converter.check_gdal_tools():
            print("All required tools are available!")
        else:
            print("Some tools are missing. Please install GDAL.")
        return
    
    print("Taiwan to SLEUTH Data Converter")
    print("================================")
    print(f"Output directory: {args.output_dir}")
    print(f"Resolution: {args.resolution}m")
    print()
    print("Usage examples:")
    print("1. Check tools: python taiwan_to_sleuth_converter.py --check-tools")
    print("2. Convert data: Use the converter methods in your script")
    print()
    print("Available methods:")
    print("- shapefile_to_urban_gif()")
    print("- shapefile_to_roads_gif()")
    print("- netcdf_to_landuse_gif()")
    print("- dem_to_slope_gif()")
    print("- create_excluded_gif()")

if __name__ == "__main__":
    main()