#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
台灣資料轉換範例腳本
示範如何使用 TaiwanToSLEUTH 轉換器
"""

import sys
from pathlib import Path
from taiwan_to_sleuth_converter import TaiwanToSLEUTH

def convert_taipei_data():
    """轉換台北市資料範例"""
    
    # 初始化轉換器
    converter = TaiwanToSLEUTH(
        output_dir="./SLEUTH3.0beta_p01_linux/Input/taiwan_taipei",
        resolution=100  # 100公尺解析度
    )
    
    # 檢查工具是否可用
    if not converter.check_gdal_tools():
        print("請先安裝 GDAL 工具")
        return False
    
    # 定義資料路徑
    base_path = Path(".")
    topo_path = base_path / "113年經建版地形圖數值資料檔(比例尺二萬五千分之一)(SHP檔)" / "圖檔"
    landuse_path = base_path / "land_use_data"
    dem_path = base_path / "分幅_臺北市20MDEM(2024)" / "*.grd"  # 需要合併多個檔案
    
    # 1. 轉換建築物資料為 Urban GIF
    print("=== Converting Urban Data ===")
    
    # 收集台北地區的建築物 shapefile
    urban_shapefiles = []
    taipei_tiles = ["96232", "97233"]  # 台北市相關圖幅
    
    for tile in taipei_tiles:
        for subtile in ["NE", "NW", "SE", "SW"]:
            tile_dir = topo_path / f"{tile}{subtile}" / "向量25K"
            if tile_dir.exists():
                build_files = list(tile_dir.glob("Build*.shp")) + list(tile_dir.glob("Builtup*.shp"))
                urban_shapefiles.extend(build_files)
    
    if urban_shapefiles:
        # 假設有多個年份的資料，這裡使用 2024 年
        converter.shapefile_to_urban_gif(urban_shapefiles, "taiwan", 2024)
    else:
        print("找不到建築物 shapefile")
    
    # 2. 轉換道路資料為 Roads GIF
    print("\n=== Converting Roads Data ===")
    
    # 收集道路 shapefile
    road_shapefiles = []
    road_types = ["HSRrdL", "MRTrdL"]  # 高鐵、捷運
    
    for tile in taipei_tiles:
        for subtile in ["NE", "NW", "SE", "SW"]:
            tile_dir = topo_path / f"{tile}{subtile}" / "向量25K"
            if tile_dir.exists():
                for road_type in road_types:
                    road_files = list(tile_dir.glob(f"{road_type}.shp"))
                    road_shapefiles.extend(road_files)
    
    # 也可以使用 OSM 道路資料
    osm_road = base_path / "road_taiwan.geojson"
    if osm_road.exists():
        road_shapefiles.append(osm_road)
    
    if road_shapefiles:
        converter.shapefile_to_roads_gif(road_shapefiles, "taiwan", 2024)
    else:
        print("找不到道路 shapefile")
    
    # 3. 轉換土地利用資料為 Landuse GIF
    print("\n=== Converting Landuse Data ===")
    
    # 使用多個年份的 NetCDF 資料
    landuse_years = {
        1956: "1956_500m_6PFT.nc",
        1982: "1982_500m_6PFT.nc", 
        1994: "1994_500m_6PFT.nc",
        2000: "2000_500m_6PFT.nc",
        2010: "2010_500m_6PFT.nc",
        2015: "2015_500m_6PFT.nc"
    }
    
    for year, filename in landuse_years.items():
        netcdf_file = landuse_path / filename
        if netcdf_file.exists():
            converter.netcdf_to_landuse_gif(netcdf_file, "taiwan", year)
        else:
            print(f"找不到 {filename}")
    
    # 4. 轉換 DEM 為 Slope GIF
    print("\n=== Converting DEM to Slope ===")
    
    # 使用全台 DEM (如果台北市 DEM 需要先合併多個檔案)
    full_taiwan_dem = base_path / "不分幅_全台20MDEM(2024)" / "不分幅_台灣20MDEM(2024).tif"
    if full_taiwan_dem.exists():
        converter.dem_to_slope_gif(full_taiwan_dem, "taiwan")
    else:
        print("找不到 DEM 檔案")
    
    # 5. 創建排除區域 GIF
    print("\n=== Creating Excluded Areas ===")
    
    # 收集水體 shapefile
    water_shapefiles = []
    water_types = ["LakeA", "CoastL", "CoastA"]
    
    for tile in taipei_tiles:
        for subtile in ["NE", "NW", "SE", "SW"]:
            tile_dir = topo_path / f"{tile}{subtile}" / "向量25K"
            if tile_dir.exists():
                for water_type in water_types:
                    water_files = list(tile_dir.glob(f"{water_type}.shp"))
                    water_shapefiles.extend(water_files)
    
    if water_shapefiles:
        converter.create_excluded_gif(water_shapefiles, "taiwan")
    else:
        print("找不到水體 shapefile")
    
    print("\n=== Conversion Complete ===")
    print(f"輸出檔案位於: {converter.output_dir}")
    return True

def convert_full_taiwan_data():
    """轉換全台灣資料範例 (僅處理可用的資料)"""
    
    converter = TaiwanToSLEUTH(
        output_dir="./SLEUTH3.0beta_p01_linux/Input/taiwan_full",
        resolution=500  # 全台使用較低解析度
    )
    
    base_path = Path(".")
    landuse_path = base_path / "land_use_data"
    
    print("=== Converting Full Taiwan Landuse Data ===")
    
    # 轉換歷史土地利用資料
    landuse_years = {
        1904: "1904_500m_6PFT.nc",
        1924: "1924_500m_6PFT.nc",
        1956: "1956_500m_6PFT.nc",
        1982: "1982_500m_6PFT.nc",
        1994: "1994_500m_6PFT.nc", 
        2000: "2000_500m_6PFT.nc",
        2005: "2005_500m_6PFT.nc",
        2010: "2010_500m_6PFT.nc",
        2015: "2015_500m_6PFT.nc"
    }
    
    for year, filename in landuse_years.items():
        print(f"Converting landuse data for {year}...")
        netcdf_file = landuse_path / filename
        if netcdf_file.exists():
            try:
                converter.netcdf_to_landuse_gif(netcdf_file, "taiwan", year)
                print(f"✓ Successfully converted {year}")
            except Exception as e:
                print(f"✗ Error converting landuse data: {e}")
        else:
            print(f"✗ File not found: {filename}")
    
    # 轉換 DEM 為 Slope  
    print("Converting DEM to slope...")
    full_taiwan_dem = base_path / "不分幅_全台20MDEM(2024)" / "不分幅_台灣20MDEM(2024).tif"
    if full_taiwan_dem.exists():
        try:
            converter.dem_to_slope_gif(full_taiwan_dem, "taiwan")
            print("✓ Successfully converted DEM to slope")
        except Exception as e:
            print(f"✗ Error converting slope data: {e}")
    else:
        print(f"✗ DEM file not found: {full_taiwan_dem}")
    
    print("Full Taiwan conversion complete!")

if __name__ == "__main__":
    print("台灣資料轉 SLEUTH 格式轉換器")
    print("=" * 40)
    
    choice = input("選擇轉換模式:\n1. 台北市區域\n2. 全台灣\n請輸入 (1 或 2): ")
    
    if choice == "1":
        convert_taipei_data()
    elif choice == "2":
        convert_full_taiwan_data()
    else:
        print("無效選擇")
        sys.exit(1)