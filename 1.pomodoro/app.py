"""
ポモドーロタイマーアプリケーション（ゲーミフィケーション機能付き）
"""

import time
import os
from datetime import datetime
from gamification import GamificationManager, Achievement


class PomodoroTimer:
    """ポモドーロタイマークラス"""
    
    WORK_DURATION = 25 * 60  # 25分
    SHORT_BREAK = 5 * 60     # 5分
    LONG_BREAK = 15 * 60     # 15分
    
    def __init__(self):
        self.gamification = GamificationManager("1.pomodoro/gamification_data.json")
        self.session_count = 0
    
    def clear_screen(self):
        """画面クリア"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def display_header(self):
        """ヘッダー表示"""
        stats = self.gamification.get_stats()
        print("=" * 60)
        print("🍅 ポモドーロタイマー - ゲーミフィケーション版")
        print("=" * 60)
        print(f"レベル: {stats['level']} | XP: {stats['xp']} (次のレベルまで: {stats['xp_to_next_level']})")
        print(f"合計完了: {stats['total_completed']} | 現在のストリーク: {stats['current_streak']}日 🔥")
        print(f"今週: {stats['weekly_completed']}回 | 今月: {stats['monthly_completed']}回")
        print("=" * 60)
    
    def start_timer(self, duration: int, label: str) -> bool:
        """タイマー開始（簡易版：1秒ごとに表示更新）"""
        print(f"\n{label} 開始！ ({duration // 60}分)")
        print("Ctrl+C で中断\n")
        
        try:
            for remaining in range(duration, 0, -1):
                minutes = remaining // 60
                seconds = remaining % 60
                print(f"\r⏱️  残り時間: {minutes:02d}:{seconds:02d}", end="", flush=True)
                time.sleep(1)
            
            print("\n\n✅ 完了！")
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  中断されました")
            return False
    
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
    
    def run_pomodoro_session(self):
        """ポモドーロセッション実行"""
        self.clear_screen()
        self.display_header()
        
        # 作業時間
        if self.start_timer(self.WORK_DURATION, "🍅 集中作業"):
            self.complete_pomodoro()
            self.session_count += 1
            
            # 休憩時間
            if self.session_count % 4 == 0:
                input("\nEnterキーを押して長い休憩を開始...")
                self.start_timer(self.LONG_BREAK, "☕ 長い休憩")
            else:
                input("\nEnterキーを押して短い休憩を開始...")
                self.start_timer(self.SHORT_BREAK, "☕ 短い休憩")
    
    def show_statistics(self):
        """統計表示"""
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
        print(f"  今週の完了: {stats['weekly_completed']}回")
        print(f"  今月の完了: {stats['monthly_completed']}回")
        
        print(f"\n【ストリーク】")
        print(f"  現在のストリーク: {stats['current_streak']}日 🔥")
        print(f"  最長ストリーク: {stats['longest_streak']}日")
        
        # 週間グラフ
        print(f"\n【週間グラフ（過去7日）】")
        weekly_stats = self.gamification.get_weekly_stats()
        max_count = max([s["count"] for s in weekly_stats] + [1])
        
        for stat in weekly_stats:
            bar_length = int((stat["count"] / max_count) * 20) if max_count > 0 else 0
            bar = "█" * bar_length
            print(f"  {stat['weekday']} {stat['date']}: {bar} {stat['count']}")
        
        print("\n" + "=" * 60)
        input("\nEnterキーで戻る...")
    
    def show_achievements(self):
        """実績表示"""
        self.clear_screen()
        achievements = self.gamification.get_achievement_list()
        
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
        input("\nEnterキーで戻る...")
    
    def show_menu(self):
        """メインメニュー表示"""
        self.clear_screen()
        self.display_header()
        
        print("\n【メニュー】")
        print("1. ポモドーロ開始")
        print("2. 統計を見る")
        print("3. 実績を見る")
        print("4. 終了")
        print()
        
        choice = input("選択してください (1-4): ").strip()
        return choice
    
    def run(self):
        """アプリケーション実行"""
        while True:
            choice = self.show_menu()
            
            if choice == "1":
                self.run_pomodoro_session()
            elif choice == "2":
                self.show_statistics()
            elif choice == "3":
                self.show_achievements()
            elif choice == "4":
                print("\n👋 お疲れ様でした！")
                break
            else:
                print("\n⚠️  無効な選択です")
                time.sleep(1)


def main():
    """メイン関数"""
    timer = PomodoroTimer()
    timer.run()


if __name__ == "__main__":
    main()
