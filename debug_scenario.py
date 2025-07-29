#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
調試scenario檔案解析問題
"""

def check_scenario_format(scenario_path):
    """檢查scenario檔案格式"""
    print(f"檢查scenario檔案: {scenario_path}")
    
    with open(scenario_path, 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if line.startswith('SLOPE_DATA'):
            print(f"第{i}行: '{line}'")
            print(f"長度: {len(line)}")
            print(f"字符編碼: {[ord(c) for c in line]}")
            
            # 解析
            if '=' in line:
                key, value = line.split('=', 1)
                print(f"Key: '{key}'")
                print(f"Value: '{value}'")
                print(f"Value stripped: '{value.strip()}'")
                
                if not value.strip():
                    print("⚠️  值為空！")
                elif value.strip().startswith(' '):
                    print("✓ 值以空格開始（符合demo格式）")
                else:
                    print("⚠️  值不以空格開始")

if __name__ == "__main__":
    scenario_path = "SLEUTH3.0beta_p01_linux/Scenarios/scenario.taiwan_sleuth"
    check_scenario_format(scenario_path)
    
    # 也檢查demo200格式作為對比
    demo_path = "SLEUTH3.0beta_p01_linux/Scenarios/scenario.demo200_test"
    check_scenario_format(demo_path)