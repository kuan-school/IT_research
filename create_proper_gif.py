#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
創建符合SLEUTH要求的標準GIF格式檔案
確保GIF標頭正確為"GIF87a"
"""

from PIL import Image
import numpy as np
from pathlib import Path

def create_sleuth_gif(input_path, output_path):
    """創建符合SLEUTH要求的GIF檔案"""
    print(f"轉換 {input_path} -> {output_path}")
    
    try:
        # 開啟原始圖片
        img = Image.open(input_path)
        
        # 轉換為灰階模式
        if img.mode != 'L':
            img = img.convert('L')
        
        # 確保尺寸為200x200
        if img.size != (200, 200):
            img = img.resize((200, 200), Image.Resampling.NEAREST)
        
        # 保存為GIF87a格式
        # PIL預設會創建GIF87a格式
        img.save(output_path, 'GIF', save_all=False)
        
        # 驗證檔案標頭
        with open(output_path, 'rb') as f:
            header = f.read(6)
            if header.startswith(b'GIF87a'):
                print(f"✓ 成功創建GIF87a格式: {output_path}")
                return True
            elif header.startswith(b'GIF89a'):
                print(f"⚠️  創建了GIF89a格式，嘗試轉換為GIF87a")
                # 重新保存為GIF87a
                img.save(output_path, 'GIF', version='GIF87a')
                with open(output_path, 'rb') as f2:
                    header2 = f2.read(6)
                    if header2.startswith(b'GIF87a'):
                        print(f"✓ 成功轉換為GIF87a: {output_path}")
                        return True
                    else:
                        print(f"✗ 仍然是{header2.decode('ascii', errors='ignore')}格式")
                        return False
            else:
                print(f"✗ 未知格式: {header}")
                return False
                
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def main():
    print("=== 創建標準SLEUTH GIF檔案 ===")
    
    input_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_fixed")
    output_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_sleuth")
    
    # 創建輸出目錄
    output_dir.mkdir(exist_ok=True)
    
    # 處理所有GIF檔案
    gif_files = list(input_dir.glob("*.gif"))
    
    success_count = 0
    for gif_file in gif_files:
        output_file = output_dir / gif_file.name
        if create_sleuth_gif(gif_file, output_file):
            success_count += 1
    
    print(f"\n成功轉換 {success_count}/{len(gif_files)} 個檔案")
    
    # 創建新的scenario檔案
    if success_count == len(gif_files):
        create_sleuth_scenario()

def create_sleuth_scenario():
    """創建使用標準GIF檔案的scenario"""
    scenario_content = """# Standard SLEUTH Taiwan Test Scenario
INPUT_DIR=Input/taiwan_sleuth/
OUTPUT_DIR=Output/taiwan_sleuth_test/
WHIRLGIF_BINARY=Whirlgif/whirlgif

ECHO(YES/NO)=yes

WRITE_COEFF_FILE(YES/NO)=yes
WRITE_AVG_FILE(YES/NO)=yes
WRITE_STD_DEV_FILE(YES/NO)=yes
WRITE_MEMORY_MAP(YES/NO)=YES
LOGGING(YES/NO)=YES

LOG_LANDCLASS_SUMMARY(YES/NO)=no
LOG_SLOPE_WEIGHTS(YES/NO)=no
LOG_READS(YES/NO)=yes
LOG_WRITES(YES/NO)=yes
LOG_COLORTABLES(YES/NO)=no
LOG_PROCESSING_STATUS(0:off/1:low verbosity/2:high verbosity)=1
LOG_TRANSITION_MATRIX(YES/NO)=no
LOG_URBANIZATION_ATTEMPTS(YES/NO)=no
LOG_INITIAL_COEFFICIENTS(YES/NO)=no
LOG_BASE_STATISTICS(YES/NO)=yes
LOG_DEBUG(YES/NO)=no
LOG_TIMINGS(0:off/1:low verbosity/2:high verbosity)=1

NUM_WORKING_GRIDS=4
RANDOM_SEED=1
MONTE_CARLO_ITERATIONS=1

CALIBRATION_DIFFUSION_START=25
CALIBRATION_DIFFUSION_STEP=1
CALIBRATION_DIFFUSION_STOP=25

CALIBRATION_BREED_START=50
CALIBRATION_BREED_STEP=1
CALIBRATION_BREED_STOP=50

CALIBRATION_SPREAD_START=75
CALIBRATION_SPREAD_STEP=1
CALIBRATION_SPREAD_STOP=75

CALIBRATION_SLOPE_START=85
CALIBRATION_SLOPE_STEP=1
CALIBRATION_SLOPE_STOP=85

CALIBRATION_ROAD_START=40
CALIBRATION_ROAD_STEP=1
CALIBRATION_ROAD_STOP=40

PREDICTION_DIFFUSION_BEST_FIT=25
PREDICTION_BREED_BEST_FIT=50
PREDICTION_SPREAD_BEST_FIT=75
PREDICTION_SLOPE_BEST_FIT=85
PREDICTION_ROAD_BEST_FIT=40

PREDICTION_START_DATE=2020
PREDICTION_STOP_DATE=2025

URBAN_DATA=taiwan.urban.1994.gif
URBAN_DATA=taiwan.urban.2000.gif
URBAN_DATA=taiwan.urban.2010.gif
URBAN_DATA=taiwan.urban.2015.gif

ROAD_DATA=taiwan.roads.1994.gif
ROAD_DATA=taiwan.roads.2000.gif
ROAD_DATA=taiwan.roads.2010.gif
ROAD_DATA=taiwan.roads.2015.gif

EXCLUDED_DATA=taiwan.excluded.gif
SLOPE_DATA=taiwan.slope.gif

WRITE_COLOR_KEY_IMAGES(YES/NO)=yes
ECHO_IMAGE_FILES(YES/NO)=yes
ANIMATION(YES/NO)=yes

DATE_COLOR=0XFFFFFF
SEED_COLOR=0X0000FF
WATER_COLOR=0X0066CC

PROBABILITY_COLOR=0, 20, , 
PROBABILITY_COLOR=20, 40, 0X90EE90,
PROBABILITY_COLOR=40, 60, 0X32CD32,
PROBABILITY_COLOR=60, 80, 0X228B22,
PROBABILITY_COLOR=80, 100, 0XFF0000,

LANDUSE_CLASS=0, Unclass, UNC, 0X000000
LANDUSE_CLASS=1, Urban, URB, 0XFF0000
LANDUSE_CLASS=2, Other, , 0X228B22

VIEW_GROWTH_TYPES(YES/NO)=NO
VIEW_DELTATRON_AGING(YES/NO)=NO

ROAD_GRAV_SENSITIVITY=0.01
SLOPE_SENSITIVITY=0.1
CRITICAL_LOW=0.97
CRITICAL_HIGH=1.3
CRITICAL_SLOPE=21.0
BOOM=1.01
BUST=0.9
"""
    
    scenario_path = Path("SLEUTH3.0beta_p01_linux/Scenarios/scenario.taiwan_sleuth")
    with open(scenario_path, 'w') as f:
        f.write(scenario_content)
    
    print(f"✓ 已創建scenario檔案: {scenario_path}")

if __name__ == "__main__":
    main()