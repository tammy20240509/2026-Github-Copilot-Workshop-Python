"""
ゲーミフィケーション機能のデモスクリプト
アプリケーションの機能を素早く確認するためのテスト
"""

import os
from datetime import datetime, timedelta
from gamification import GamificationManager, Achievement


def clear_screen():
    """画面クリア"""
    os.system('cls' if os.name == 'nt' else 'clear')


def demo_basic_functionality():
    """基本機能のデモ"""
    print("=" * 60)
    print("🎮 ゲーミフィケーション機能デモ")
    print("=" * 60)
    
    # テストファイルを使用
    demo_file = "demo_gamification_data.json"
    if os.path.exists(demo_file):
        os.remove(demo_file)
    
    manager = GamificationManager(demo_file)
    
    print("\n【初期状態】")
    stats = manager.get_stats()
    print(f"  レベル: {stats['level']}")
    print(f"  経験値: {stats['xp']}")
    print(f"  完了数: {stats['total_completed']}")
    
    print("\n【ポモドーロ1回完了】")
    result = manager.complete_pomodoro()
    print(f"  +{result['xp_gained']} XP 獲得")
    if result["new_achievements"]:
        print(f"  🏆 新しい実績: {result['new_achievements']}")
    
    stats = manager.get_stats()
    print(f"  現在のXP: {stats['xp']}")
    print(f"  次のレベルまで: {stats['xp_to_next_level']} XP")
    
    print("\n【10回完了してレベルアップ】")
    for i in range(9):
        manager.complete_pomodoro()
    
    stats = manager.get_stats()
    print(f"  現在のレベル: {stats['level']}")
    print(f"  現在のXP: {stats['xp']}")
    print(f"  完了数: {stats['total_completed']}")
    
    print("\n【3日連続でストリーク実績獲得】")
    # 日付を操作して3日連続をシミュレート
    for day in range(2):
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        manager.data["last_completion_date"] = yesterday
        manager._save_data()
        result = manager.complete_pomodoro()
    
    stats = manager.get_stats()
    print(f"  現在のストリーク: {stats['current_streak']}日")
    print(f"  獲得した実績: {stats['earned_achievements']}")
    
    print("\n【実績一覧】")
    achievements = manager.get_achievement_list()
    for achievement in achievements:
        status = "✅" if achievement["earned"] else "⬜"
        print(f"  {status} {achievement['name']}: {achievement['description']}")
    
    print("\n【週間統計】")
    weekly_stats = manager.get_weekly_stats()
    for stat in weekly_stats:
        print(f"  {stat['weekday']} {stat['date']}: {stat['count']}回")
    
    print("\n【最終統計】")
    print(f"  レベル: {stats['level']}")
    print(f"  経験値: {stats['xp']}")
    print(f"  完了数: {stats['total_completed']}")
    print(f"  今週の完了: {stats['weekly_completed']}回")
    print(f"  今月の完了: {stats['monthly_completed']}回")
    print(f"  現在のストリーク: {stats['current_streak']}日")
    print(f"  最長ストリーク: {stats['longest_streak']}日")
    
    print("\n" + "=" * 60)
    print("✅ デモ完了！")
    print("=" * 60)
    
    # クリーンアップ
    if os.path.exists(demo_file):
        os.remove(demo_file)


if __name__ == "__main__":
    demo_basic_functionality()
