# 台灣 SLEUTH 使用指南

## 🚀 快速開始

### 1. 安裝必要工具

```bash
# macOS 使用 Homebrew 安裝 GDAL
brew install gdal

# 安裝 Python 依賴
pip install gdal xarray rasterio pillow numpy matplotlib
```

### 2. 檢查工具是否正確安裝

```bash
python taiwan_to_sleuth_converter.py --check-tools
```

### 3. 轉換資料

```bash
# 運行轉換範例
python convert_taiwan_data_example.py

# 選擇 1 (台北市) 或 2 (全台灣)
```

### 4. 執行 SLEUTH 模型

```bash
cd SLEUTH3.0beta_p01_linux

# 測試模式 (快速驗證)
./grow test Scenarios/scenario.taiwan_test

# 校正模式 (找出最佳參數)
./grow calibrate Scenarios/scenario.taiwan_calibrate

# 預測模式 (未來發展預測)
./grow predict Scenarios/scenario.taiwan_predict
```

## 📁 檔案結構

```
IT_research/
├── taiwan_to_sleuth_converter.py          # 主要轉換器
├── convert_taiwan_data_example.py         # 使用範例
├── taiwan_data_conversion_plan.md         # 轉換計劃文件
├── taiwan_sleuth_usage_guide.md          # 本使用指南
│
├── SLEUTH3.0beta_p01_linux/
│   ├── Input/
│   │   └── taiwan_taipei/                 # 轉換後的台北資料
│   │       ├── taiwan.urban.YYYY.gif
│   │       ├── taiwan.roads.YYYY.gif
│   │       ├── taiwan.landuse.YYYY.gif
│   │       ├── taiwan.slope.gif
│   │       └── taiwan.excluded.gif
│   │
│   ├── Output/
│   │   ├── taiwan_test/                   # 測試結果
│   │   ├── taiwan_calibrate/              # 校正結果
│   │   └── taiwan_predict/                # 預測結果
│   │
│   └── Scenarios/
│       ├── scenario.taiwan_test           # 測試配置
│       ├── scenario.taiwan_calibrate      # 校正配置
│       └── scenario.taiwan_predict        # 預測配置
│
└── [原始資料目錄]
    ├── 113年經建版地形圖數値資料檔.../
    ├── land_use_data/
    ├── 不分幅_全台20MDEM(2024)/
    └── ...
```

## 🔧 轉換器功能說明

### TaiwanToSLEUTH 類別方法

1. **`shapefile_to_urban_gif()`**
   - 輸入：建築物 Shapefile 列表
   - 輸出：Urban GIF 檔案
   - 用途：城市區域標識

2. **`shapefile_to_roads_gif()`**
   - 輸入：道路 Shapefile 列表
   - 輸出：Roads GIF 檔案
   - 用途：道路網絡影響

3. **`netcdf_to_landuse_gif()`**
   - 輸入：NetCDF 土地利用檔案
   - 輸出：Landuse GIF 檔案
   - 用途：土地利用轉換

4. **`dem_to_slope_gif()`**
   - 輸入：DEM 檔案 (TIF/GRD)
   - 輸出：Slope GIF 檔案
   - 用途：地形限制因子

5. **`create_excluded_gif()`**
   - 輸入：水體 Shapefile 列表
   - 輸出：Excluded GIF 檔案
   - 用途：不可建築區域

## 📊 Scenario 檔案說明

### scenario.taiwan_test
- **用途**：快速測試和驗證
- **特點**：少量 Monte Carlo 迭代，詳細日誌
- **適用**：初次使用，資料格式驗證

### scenario.taiwan_calibrate
- **用途**：模型校正，尋找最佳參數
- **特點**：多組參數組合，較長執行時間
- **適用**：歷史資料擬合，參數優化

### scenario.taiwan_predict
- **用途**：未來發展預測
- **特點**：使用校正後的最佳參數
- **適用**：政策分析，規劃決策

## ⚙️ 重要參數說明

### 模型係數 (需要校正)

1. **DIFFUSION** (10-50)
   - 自發性城市成長
   - 台灣都市密集，建議較高值

2. **BREED** (20-80)
   - 新城市中心生成機率
   - 台灣多核心發展特性

3. **SPREAD** (30-90)
   - 有機成長機率
   - 台灣城市擴張快速

4. **SLOPE_RESISTANCE** (80-95)
   - 坡度發展阻力
   - 台灣山地多，建議高阻力值

5. **ROAD_GRAVITY** (20-80)
   - 道路影響力
   - 台灣交通便利，影響力大

## 🗓️ 時間序列設定

### 歷史資料年份
基於現有 NetCDF 資料：
- 1904, 1924, 1956, 1982, 1994, 2000, 2005, 2010, 2015

### 預測期間
- 起始：2015 年
- 終點：2040-2050 年

## 🎯 模型執行流程

### 1. 測試階段
```bash
./grow test Scenarios/scenario.taiwan_test
```
- 檢查資料格式是否正確
- 驗證模型能否正常執行
- 查看初步結果

### 2. 校正階段
```bash
./grow calibrate Scenarios/scenario.taiwan_calibrate
```
- 尋找最佳參數組合
- 與歷史資料進行擬合
- 生成校正統計報告

### 3. 預測階段
```bash
./grow predict Scenarios/scenario.taiwan_predict
```
- 使用最佳參數進行預測
- 生成未來發展情境
- 輸出機率分布圖

## 📈 結果分析

### 主要輸出檔案

1. **GIF 圖像**
   - 年度城市發展圖
   - 機率分布圖
   - 成長類型圖

2. **統計檔案**
   - `control_stats.log`: 校正統計
   - `avg.log`: 平均值
   - `std_dev.log`: 標準差

3. **動畫檔案**
   - `animated_*.gif`: 時序動畫

## ⚠️ 注意事項

1. **資料準備**
   - 確保所有 GIF 檔案解析度一致
   - 檢查座標系統統一性
   - 驗證資料時間序列完整性

2. **計算資源**
   - 校正階段需要大量計算時間
   - 確保足夠的磁碟空間
   - 監控記憶體使用情況

3. **參數調整**
   - 根據校正結果調整預測參數
   - 考慮台灣特有的都市化特性
   - 參考相關研究的參數設定

## 🔍 問題排除

### 常見錯誤

1. **無法找到輸入檔案**
   - 檢查 INPUT_DIR 路徑
   - 確認 GIF 檔案存在

2. **記憶體不足**
   - 降低解析度
   - 減少工作網格數量
   - 使用較小的研究區域

3. **轉換失敗**
   - 檢查 GDAL 安裝
   - 驗證原始資料格式
   - 查看轉換器錯誤訊息

### 偵錯技巧

1. **啟用詳細日誌**
   ```
   LOG_PROCESSING_STATUS=2
   LOG_DEBUG=yes
   ```

2. **檢查中間檔案**
   - 查看轉換過程中的臨時檔案
   - 使用 QGIS 視覺化檢查

3. **段階測試**
   - 先測試小區域
   - 逐步增加複雜度