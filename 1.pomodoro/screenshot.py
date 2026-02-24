"""
アプリケーションのスクリーンショット用スクリプト
主要な画面を表示してキャプチャ
"""

import os
from gamification import GamificationManager, Achievement


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_main_menu():
    """メインメニュー画面"""
    clear_screen()
    
    # テストデータ作成
    manager = GamificationManager("screenshot_data.json")
    
    # サンプルデータを追加
    for i in range(15):
        manager.complete_pomodoro()
    
    stats = manager.get_stats()
    
    print("=" * 60)
    print("🍅 ポモドーロタイマー - ゲーミフィケーション版")
    print("=" * 60)
    print(f"レベル: {stats['level']} | XP: {stats['xp']} (次のレベルまで: {stats['xp_to_next_level']})")
    print(f"合計完了: {stats['total_completed']} | 現在のストリーク: {stats['current_streak']}日 🔥")
    print(f"今週: {stats['weekly_completed']}回 | 今月: {stats['monthly_completed']}回")
    print("=" * 60)
    print("\n【メニュー】")
    print("1. ポモドーロ開始")
    print("2. 統計を見る")
    print("3. 実績を見る")
    print("4. 終了")
    print()
    print("選択してください (1-4): _")
    print()


def show_statistics():
    """統計画面"""
    manager = GamificationManager("screenshot_data.json")
    stats = manager.get_stats()
    
    print("=" * 60)
    print("📊 統計情報")
    print("=" * 60)
    print(f"\n【レベル情報】")
    print(f"  現在のレベル: {stats['level']}")
    print(f"  経験値: {stats['xp']} XP")
    print(f"  次のレベルまで: {stats['xp_to_next_level']} XP")
    
    print(f"\n【完了統計】")
    print(f"  合計完了: {stats['total_completed']}回")
    print(f"  今週の完了: {stats['weekly_completed']}回")
    print(f"  今月の完了: {stats['monthly_completed']}回")
    
    print(f"\n【ストリーク】")
    print(f"  現在のストリーク: {stats['current_streak']}日 🔥")
    print(f"  最長ストリーク: {stats['longest_streak']}日")
    
    # 週間グラフ
    print(f"\n【週間グラフ（過去7日）】")
    weekly_stats = manager.get_weekly_stats()
    max_count = max([s["count"] for s in weekly_stats] + [1])
    
    for stat in weekly_stats:
        bar_length = int((stat["count"] / max_count) * 20) if max_count > 0 else 0
        bar = "█" * bar_length
        print(f"  {stat['weekday']} {stat['date']}: {bar} {stat['count']}")
    
    print("\n" + "=" * 60)


def show_achievements():
    """実績画面"""
    manager = GamificationManager("screenshot_data.json")
    achievements = manager.get_achievement_list()
    
    print("=" * 60)
    print("🏆 実績バッジ")
    print("=" * 60)
    
    earned_count = sum(1 for a in achievements if a["earned"])
    print(f"\n獲得済み: {earned_count}/{len(achievements)}\n")
    
    for achievement in achievements:
        status = "✅" if achievement["earned"] else "⬜"
        print(f"{status} {achievement['name']}")
        print(f"   {achievement['description']}\n")
    
    print("=" * 60)


def show_completion_message():
    """完了メッセージ画面"""
    print("\n" + "=" * 60)
    print("🎉 ポモドーロ完了！")
    print("=" * 60)
    print(f"📈 +10 XP 獲得！")
    print(f"🎊 レベルアップ！ レベル 2 に到達！")
    print(f"🔥 ストリーク更新！ 1日連続！")
    print("\n🏆 新しい実績を獲得！")
    print(f"  - 初めてのポモドーロ: 最初のポモドーロを完了")
    print("=" * 60)


if __name__ == "__main__":
    # 各画面を順番に表示
    print("\n=== 1. メインメニュー画面 ===\n")
    show_main_menu()
    
    print("\n\n=== 2. 統計画面 ===\n")
    show_statistics()
    
    print("\n\n=== 3. 実績画面 ===\n")
    show_achievements()
    
    print("\n\n=== 4. 完了メッセージ ===\n")
    show_completion_message()
    
    # クリーンアップ
    if os.path.exists("screenshot_data.json"):
        os.remove("screenshot_data.json")
    
    print("\n\n✅ スクリーンショット用画面表示完了")
