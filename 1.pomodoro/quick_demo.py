"""
簡易デモ：ポモドーロタイマーの動作確認
タイマーの時間を短縮してテスト
"""

import time
import os
from gamification import GamificationManager, Achievement


class QuickDemoTimer:
    """デモ用の簡易タイマー"""
    
    def __init__(self):
        self.gamification = GamificationManager("quick_demo_data.json")
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        stats = self.gamification.get_stats()
        print("=" * 60)
        print("🍅 ポモドーロタイマー - ゲーミフィケーション版 (デモモード)")
        print("=" * 60)
        print(f"レベル: {stats['level']} | XP: {stats['xp']} (次のレベルまで: {stats['xp_to_next_level']})")
        print(f"合計完了: {stats['total_completed']} | 現在のストリーク: {stats['current_streak']}日 🔥")
        print(f"今週: {stats['weekly_completed']}回 | 今月: {stats['monthly_completed']}回")
        print("=" * 60)
    
    def quick_timer(self, seconds: int, label: str):
        """簡易タイマー（数秒）"""
        print(f"\n{label} 開始！ ({seconds}秒のデモ)")
        for i in range(seconds, 0, -1):
            print(f"\r⏱️  残り: {i}秒  ", end="", flush=True)
            time.sleep(1)
        print("\n✅ 完了！")
    
    def complete_pomodoro(self):
        """ポモドーロ完了処理"""
        result = self.gamification.complete_pomodoro()
        
        print("\n" + "=" * 60)
        print("🎉 ポモドーロ完了！")
        print("=" * 60)
        print(f"📈 +{result['xp_gained']} XP 獲得！")
        
        if result["level_up"]:
            stats = self.gamification.get_stats()
            print(f"🎊 レベルアップ！ レベル {stats['level']} に到達！")
        
        if result["streak_updated"]:
            stats = self.gamification.get_stats()
            print(f"🔥 ストリーク更新！ {stats['current_streak']}日連続！")
        
        if result["new_achievements"]:
            print("\n🏆 新しい実績を獲得！")
            for achievement_id in result["new_achievements"]:
                achievement = Achievement.ACHIEVEMENTS[achievement_id]
                print(f"  - {achievement['name']}: {achievement['description']}")
        
        print("=" * 60)
    
    def run_demo(self):
        """デモ実行"""
        self.clear_screen()
        print("\n🎮 ポモドーロタイマー - クイックデモ\n")
        print("このデモでは実際のタイマーの動作を短時間で確認できます。")
        print("（実際は25分ですが、デモでは5秒で動作します）\n")
        
        input("Enterキーを押してデモを開始...")
        
        # ポモドーロ1回目
        self.clear_screen()
        self.display_header()
        self.quick_timer(5, "🍅 集中作業")
        self.complete_pomodoro()
        
        input("\nEnterキーで統計を表示...")
        
        # 統計表示
        self.clear_screen()
        stats = self.gamification.get_stats()
        print("=" * 60)
        print("📊 統計情報")
        print("=" * 60)
        print(f"\n【レベル情報】")
        print(f"  現在のレベル: {stats['level']}")
        print(f"  経験値: {stats['xp']} XP")
        print(f"  次のレベルまで: {stats['xp_to_next_level']} XP")
        
        print(f"\n【完了統計】")
        print(f"  合計完了: {stats['total_completed']}回")
        
        print(f"\n【獲得した実績】")
        for achievement_id in stats['earned_achievements']:
            achievement = Achievement.ACHIEVEMENTS[achievement_id]
            print(f"  ✅ {achievement['name']}")
        
        print("\n" + "=" * 60)
        print("\n✅ デモ完了！")
        print(f"\nデモデータは quick_demo_data.json に保存されています。")
        print("削除する場合は: rm quick_demo_data.json")


if __name__ == "__main__":
    demo = QuickDemoTimer()
    demo.run_demo()
