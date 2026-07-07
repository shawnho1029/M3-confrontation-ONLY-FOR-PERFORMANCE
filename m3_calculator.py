import sys

def main():
    # 設定標準輸出為 UTF-8，以防止 Windows 命令提示字元中的編碼問題
    sys.stdout.reconfigure(encoding='utf-8')

    print("==================================================")
    print("           Mon3tr 重獲體定幀部署計算器            ")
    print("==================================================")

    # 1. 輸入當前攻速
    try:
        as_input = input("請輸入您的當前攻速（初始值為100，如120）：").strip()
        attack_speed = float(as_input)
        if attack_speed <= 0:
            print("錯誤：攻速必須大於零。")
            return
    except ValueError:
        print("錯誤：請輸入有效的數字。")
        return

    # 2. 選擇重構體生命值狀態（傻貓指數）
    print("\n請選擇重構體生命值狀態（影響演出用香水的回血能力）：")
    print("1. 有救 (生命值在 [8000, 12000) 之間)")
    print("2. 難救 (生命值在 [12000, 24000) 之間) [預設]")
    
    state_input = input("選擇狀態 (1-2，直接按回車預設為 2)：").strip()
    if state_input == "":
        state = 3  # 難救
    else:
        try:
            choice = int(state_input)
            if choice == 1:
                state = 2  # 有救
            elif choice == 2:
                state = 3  # 難救
            else:
                print("輸入無效，將使用預設的難救狀態。")
                state = 3
        except ValueError:
            print("輸入無效，將使用預設的難救狀態。")
            state = 3

    # 3. 計算第一A動畫長度 L1
    # 基礎攻擊間隔為 2.85 秒，在當前攻速下：
    # L1 = min(85, round(2.85 * 3000 / AS))
    l1_raw = 8550.0 / attack_speed
    l1 = max(1, min(85, round(l1_raw)))
    
    print(f"\n[計算分析]")
    print(f"Mon3tr 第一A動畫長度：{l1} 幀 (原始計算值為 {l1_raw:.2f} 幀)")
    
    # 4. 定幀部署餘數計算
    # 部署明椒/Mon3tr為第 0 幀，重構體在第 T_dep 幀部署。
    # 首次攻擊索敵在第 32 幀。
    # 重構體部署幀不能是 3 的倍數，即 T_dep % 3 != 0 (固定排除 3n 幀)。
    
    valid_mod = []
    has_solution = True
    
    if state == 2:  # 有救
        # T_dep % 3 != 0 且 T_dep % 3 != L1 % 3
        for m in [1, 2]:
            if m != (l1 % 3):
                valid_mod.append(m)
    elif state == 3:  # 難救
        # T_dep % 3 != 0 且 T_dep % 3 == L1 % 3
        for m in [1, 2]:
            if m == (l1 % 3):
                valid_mod.append(m)
        if not valid_mod:
            has_solution = False

    # 5. 輸出定幀部署結果
    if not has_solution:
        print("\n[部署建議]")
        print("警告：在目前狀態與攻速下，重構體部署無解，首次與後續攻擊無法同時治療到重構體！")
    else:
        print("\n[部署建議]")
        print(f"重構體應在符合以下幀數規律的時間點進行手動部署：")
        
        result_desc = []
        example_frames = []
        for m in valid_mod:
            result_desc.append(f"3n + {m} 幀")
            # 生成幾個具體的部署幀（T_dep >= 1）
            for n in range(5):
                frame = 3 * n + m
                example_frames.append(frame)
        
        example_frames.sort()
        print(f"建議規律：{' 或 '.join(result_desc)}")
        print(f"推薦具體部署幀示例（以 Mon3tr 部署時間點為第 0 幀）：")
        print(f"第 {', '.join(map(str, example_frames[:8]))} 幀")

    # 6. 攻速推薦區間驗證
    # 影片中推薦的持續奶攻速列表
    recommended_intervals = [
        (124, 124), (129, 130), (135, 136), (142, 143), (149, 151),
        (157, 159), (167, 169), (177, 180), (188, 192), (202, 206),
        (217, 222), (235, 240), (256, 263), (281, 289), (311, 322),
        (349, 363), (398, 417), (463, 488), (552, 589)
    ]
    
    is_recommended = False
    for low, high in recommended_intervals:
        if low <= attack_speed <= high:
            is_recommended = True
            break
            
    if is_recommended:
        print("\n[持續治療驗證]")
        print("優良：您的當前攻速符合持續治療推薦區間，在推薦幀部署後可以實現持續治療！")
    else:
        print("\n[持續治療驗證]")
        print("警告：當前攻速不符合持續治療的推薦區間，可能無法維持後續的治療循環。")
        # 尋找最近的推薦攻速
        flat_list = []
        for r in recommended_intervals:
            flat_list.extend(range(r[0], r[1] + 1))
        
        # 尋找最近的值
        closest_speed = min(flat_list, key=lambda x: abs(x - attack_speed))
        print(f"建議將攻速調整至鄰近的推薦攻速：{closest_speed}（或其他推薦區間：124, 129-130, 135-136 等）")

    print("==================================================")

if __name__ == '__main__':
    main()
