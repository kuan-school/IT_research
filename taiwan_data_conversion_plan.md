# 台灣資料轉換為 SLEUTH 輸入格式計劃

## SLEUTH 需要的 5 種 GIF 格式輸入資料

### 1. Urban Data (城市發展資料)
**來源**: 
- Shapefile: BuildA.shp, BuiltupA.shp (建築物和建成區)
- NetCDF: land_use_data/*_6PFT.nc (Built-up land class, LU_TYPE=08)

**轉換流程**:
```bash
# 使用 GDAL 將 Shapefile 轉為柵格
gdal_rasterize -a FIELD_NAME -tr 30 30 -l BuildA BuildA.shp urban_temp.tif
# 轉為 8-bit 灰階 GIF
gdal_translate -of GIF -ot Byte urban_temp.tif taiwan.urban.YYYY.gif
```

### 2. Road Data (道路網絡資料)  
**來源**:
- Shapefile: HSRrdL.shp, MRTrdL.shp (高鐵、捷運線)
- OSM: road_taiwan.geojson (完整道路網)

**轉換流程**:
```bash
# 合併道路資料並柵格化
ogr2ogr -f "ESRI Shapefile" roads_combined.shp road_taiwan.geojson
gdal_rasterize -burn 255 -tr 30 30 roads_combined.shp taiwan.roads.YYYY.gif
```

### 3. Landuse Data (土地利用資料)
**來源**: 
- NetCDF: land_use_data/*_6PFT.nc (完整的土地覆蓋分類)
- 分類對應:
  - 01: Forest → 4  
  - 02: Grassland → 3
  - 04: Agriculture → 2
  - 08: Built-up → 1 (Urban, 由 Urban Data 處理)
  - 13: Inland water → 5
  - 26: Bare soil → 7

**轉換流程**:
```python
# 使用 Python 處理 NetCDF
import xarray as xr
import rasterio
data = xr.open_dataset('1904_500m_6PFT.nc')
# 重新分類並輸出為 GIF
```

### 4. Slope Data (坡度資料)
**來源**: 
- TIF: 不分幅_台灣20MDEM(2024).tif
- GRD: 分幅_臺北市20MDEM(2024)/*.grd

**轉換流程**:
```bash
# 計算坡度
gdaldem slope 不分幅_台灣20MDEM(2024).tif slope_temp.tif
# 轉為百分比坡度並輸出 GIF
gdal_translate -of GIF -ot Byte -scale 0 90 0 255 slope_temp.tif taiwan.slope.gif
```

### 5. Excluded Data (排除區域)
**來源**:
- 海洋區域 (從 CoastL.shp 推導)
- 水體 (從 LakeA.shp)

## 時間序列資料配置

基於現有資料，建議的時間點：
- 1904 (land_use_data)
- 1956 (land_use_data) 
- 1982 (land_use_data)
- 1994 (land_use_data)
- 2000 (land_use_data)
- 2010 (land_use_data)
- 2015 (land_use_data)

## 空間範圍和解析度

- **建議解析度**: 100m (在資料解析度和計算效率間平衡)
- **投影系統**: TWD97 / TM2 (EPSG:3826) 台灣常用坐標系統
- **範圍**: 全台灣或特定區域 (如台北都會區)

## 實作優先順序

1. **先用台北市資料測試** (範圍較小，處理快速)
2. **建立自動化轉換腳本**
3. **驗證資料品質和格式**
4. **創建 scenario 配置檔**
5. **執行 SLEUTH 校正和預測**