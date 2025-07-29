#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修復Taiwan GIF格式問題，使其與demo200格式匹配
"""

from PIL import Image
import numpy as np
from pathlib import Path

def analyze_and_fix_gif(demo_path, taiwan_path, output_path):
    """分析demo格式並修復taiwan格式"""
    print(f"\n=== 修復 {taiwan_path} ===")
    
    try:
        # 開啟demo檔案作為參考
        demo_img = Image.open(demo_path)
        print(f"Demo格式: {demo_img.mode}, 尺寸: {demo_img.size}")
        
        # 開啟taiwan檔案
        taiwan_img = Image.open(taiwan_path) 
        print(f"Taiwan格式: {taiwan_img.mode}, 尺寸: {taiwan_img.size}")
        
        # 確保Taiwan圖片與demo格式一致
        if taiwan_img.mode != demo_img.mode:
            print(f"轉換模式從 {taiwan_img.mode} 到 {demo_img.mode}")
            if demo_img.mode == 'P':
                # 轉換為索引色彩模式
                taiwan_fixed = taiwan_img.convert('P', palette=Image.ADAPTIVE, colors=256)
            else:
                taiwan_fixed = taiwan_img.convert(demo_img.mode)
        else:
            taiwan_fixed = taiwan_img.copy()
        
        # 如果demo有調色盤，使用相同的調色盤
        if demo_img.mode == 'P' and demo_img.getpalette():
            demo_palette = demo_img.getpalette()
            print(f"使用demo調色盤，顏色數: {len(demo_palette)//3}")
            taiwan_fixed.putpalette(demo_palette)
        
        # 儲存修復後的檔案
        taiwan_fixed.save(output_path, 'GIF', optimize=False)
        print(f"✓ 已儲存修復檔案: {output_path}")
        
        # 驗證修復結果
        verify_img = Image.open(output_path)
        print(f"修復後格式: {verify_img.mode}, 尺寸: {verify_img.size}")
        
        return True
        
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def create_proper_gif(input_array, output_path, is_slope=False):
    """從numpy陣列創建符合SLEUTH格式的GIF"""
    print(f"創建標準GIF: {output_path}")
    
    try:
        # 確保資料在0-255範圍內
        if input_array.dtype != np.uint8:
            if is_slope:
                # 坡度資料標準化到0-255
                input_array = ((input_array - input_array.min()) / 
                              (input_array.max() - input_array.min()) * 255).astype(np.uint8)
            else:
                input_array = input_array.astype(np.uint8)
        
        # 創建圖片
        img = Image.fromarray(input_array, mode='L')
        
        # 轉換為索引色彩模式
        img_p = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        
        # 儲存為GIF
        img_p.save(output_path, 'GIF', optimize=False)
        print(f"✓ 已創建: {output_path}")
        
        return True
        
    except Exception as e:
        print(f"✗ 錯誤: {e}")
        return False

def main():
    print("=== 修復Taiwan GIF格式 ===")
    
    demo_dir = Path("SLEUTH3.0beta_p01_linux/Input/demo200")
    taiwan_input_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_small")
    
    # 創建修復後檔案目錄
    fixed_dir = Path("SLEUTH3.0beta_p01_linux/Input/taiwan_fixed")
    fixed_dir.mkdir(exist_ok=True)
    
    # 需要修復的檔案對應關係
    file_mappings = [
        ("demo200.slope.gif", "taiwan.slope.gif"),
        ("demo200.urban.1930.gif", "taiwan.urban.1994.gif"),
        ("demo200.urban.1950.gif", "taiwan.urban.2000.gif"),  
        ("demo200.urban.1970.gif", "taiwan.urban.2010.gif"),
        ("demo200.urban.1990.gif", "taiwan.urban.2015.gif"),
        ("demo200.roads.1930.gif", "taiwan.roads.1994.gif"),
        ("demo200.roads.1950.gif", "taiwan.roads.2000.gif"),
        ("demo200.roads.1970.gif", "taiwan.roads.2010.gif"),
        ("demo200.roads.1990.gif", "taiwan.roads.2015.gif")
    ]
    
    # 修復每個檔案
    for demo_file, taiwan_file in file_mappings:
        demo_path = demo_dir / demo_file
        taiwan_path = taiwan_input_dir / taiwan_file
        output_path = fixed_dir / taiwan_file
        
        if demo_path.exists() and taiwan_path.exists():
            analyze_and_fix_gif(demo_path, taiwan_path, output_path)
        else:
            print(f"檔案不存在: {demo_path} 或 {taiwan_path}")
    
    # 處理excluded檔案（沒有對應demo檔案）
    excluded_path = taiwan_input_dir / "taiwan.excluded.gif"
    if excluded_path.exists():
        # 直接複製excluded檔案並轉換格式
        img = Image.open(excluded_path)
        img_fixed = img.convert('P', palette=Image.ADAPTIVE, colors=256)
        img_fixed.save(fixed_dir / "taiwan.excluded.gif", 'GIF', optimize=False)
        print(f"✓ 已處理excluded檔案")
    
    print(f"\n完成！修復後的檔案已儲存至: {fixed_dir}")
    
    # 創建新的scenario檔案
    create_fixed_scenario()

def create_fixed_scenario():
    """創建使用修復檔案的scenario"""
    scenario_content = """# Fixed Taiwan SLEUTH Test Scenario
INPUT_DIR=Input/taiwan_fixed/
OUTPUT_DIR=Output/taiwan_fixed_test/
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
    
    scenario_path = Path("SLEUTH3.0beta_p01_linux/Scenarios/scenario.taiwan_fixed")
    with open(scenario_path, 'w') as f:
        f.write(scenario_content)
    
    print(f"✓ 已創建scenario檔案: {scenario_path}")

if __name__ == "__main__":
    main()