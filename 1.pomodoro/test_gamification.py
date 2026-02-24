"""
ゲーミフィケーション機能のテスト
"""

import unittest
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from gamification import GamificationManager, Achievement


class TestGamificationManager(unittest.TestCase):
    """GamificationManagerのテストクラス"""
    
    def setUp(self):
        """テストセットアップ"""
        self.test_file = "test_gamification_data.json"
        if Path(self.test_file).exists():
            os.remove(self.test_file)
        self.manager = GamificationManager(self.test_file)
    
    def tearDown(self):
        """テストクリーンアップ"""
        if Path(self.test_file).exists():
            os.remove(self.test_file)
    
    def test_initial_data(self):
        """初期データのテスト"""
        stats = self.manager.get_stats()
        self.assertEqual(stats["level"], 1)
        self.assertEqual(stats["xp"], 0)
        self.assertEqual(stats["total_completed"], 0)
        self.assertEqual(stats["current_streak"], 0)
    
    def test_complete_pomodoro_xp(self):
        """ポモドーロ完了でXP獲得のテスト"""
        result = self.manager.complete_pomodoro()
        self.assertEqual(result["xp_gained"], 10)
        stats = self.manager.get_stats()
        self.assertEqual(stats["xp"], 10)
        self.assertEqual(stats["total_completed"], 1)
    
    def test_level_up(self):
        """レベルアップのテスト"""
        # 100 XP でレベル2
        for _ in range(10):
            self.manager.complete_pomodoro()
        
        stats = self.manager.get_stats()
        self.assertEqual(stats["level"], 2)
        self.assertEqual(stats["xp"], 100)
    
    def test_streak_same_day(self):
        """同日複数完了時のストリークテスト"""
        self.manager.complete_pomodoro()
        stats1 = self.manager.get_stats()
        self.assertEqual(stats1["current_streak"], 1)
        
        # 同じ日にもう一度
        self.manager.complete_pomodoro()
        stats2 = self.manager.get_stats()
        self.assertEqual(stats2["current_streak"], 1)  # ストリークは変わらない
    
    def test_streak_consecutive_days(self):
        """連続日のストリークテスト"""
        # 1日目
        self.manager.complete_pomodoro()
        stats1 = self.manager.get_stats()
        self.assertEqual(stats1["current_streak"], 1)
        
        # 2日目（手動で日付を変更）
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        self.manager.data["last_completion_date"] = yesterday
        self.manager.complete_pomodoro()
        stats2 = self.manager.get_stats()
        self.assertEqual(stats2["current_streak"], 2)
    
    def test_streak_broken(self):
        """ストリーク途切れのテスト"""
        # 1日目
        self.manager.complete_pomodoro()
        
        # 3日前に変更（ストリーク途切れる）
        three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
        self.manager.data["last_completion_date"] = three_days_ago
        self.manager.complete_pomodoro()
        
        stats = self.manager.get_stats()
        self.assertEqual(stats["current_streak"], 1)  # リセットされる
    
    def test_achievement_first_pomodoro(self):
        """初回ポモドーロ実績のテスト"""
        result = self.manager.complete_pomodoro()
        self.assertIn("first_pomodoro", result["new_achievements"])
    
    def test_achievement_streak_3(self):
        """3日連続実績のテスト"""
        # 3日連続でポモドーロ完了をシミュレート
        for i in range(3):
            if i > 0:
                # 前日の日付を設定
                date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
                self.manager.data["last_completion_date"] = date
                self.manager._save_data()
            result = self.manager.complete_pomodoro()
        
        stats = self.manager.get_stats()
        self.assertEqual(stats["current_streak"], 3)
        self.assertIn("streak_3", stats["earned_achievements"])
    
    def test_weekly_stats(self):
        """週間統計のテスト"""
        self.manager.complete_pomodoro()
        weekly = self.manager.get_weekly_stats()
        
        self.assertEqual(len(weekly), 7)  # 7日分
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 今日のデータを確認
        today_stat = [s for s in weekly if s["date"] == today][0]
        self.assertEqual(today_stat["count"], 1)
    
    def test_monthly_stats(self):
        """月間統計のテスト"""
        self.manager.complete_pomodoro()
        monthly = self.manager.get_monthly_stats()
        
        self.assertEqual(len(monthly), 30)  # 30日分
    
    def test_data_persistence(self):
        """データ永続化のテスト"""
        self.manager.complete_pomodoro()
        stats1 = self.manager.get_stats()
        
        # 新しいインスタンスを作成
        manager2 = GamificationManager(self.test_file)
        stats2 = manager2.get_stats()
        
        self.assertEqual(stats1["xp"], stats2["xp"])
        self.assertEqual(stats1["total_completed"], stats2["total_completed"])


class TestAchievement(unittest.TestCase):
    """Achievementクラスのテストクラス"""
    
    def test_check_achievements_first_pomodoro(self):
        """初回ポモドーロ実績チェックのテスト"""
        stats = {
            "total_completed": 1,
            "current_streak": 1,
            "weekly_completed": 1,
            "level": 1,
            "earned_achievements": []
        }
        
        new_achievements = Achievement.check_achievements(stats)
        self.assertIn("first_pomodoro", new_achievements)
    
    def test_check_achievements_already_earned(self):
        """既に獲得済みの実績は返さないテスト"""
        stats = {
            "total_completed": 1,
            "current_streak": 1,
            "weekly_completed": 1,
            "level": 1,
            "earned_achievements": ["first_pomodoro"]
        }
        
        new_achievements = Achievement.check_achievements(stats)
        self.assertNotIn("first_pomodoro", new_achievements)
    
    def test_check_achievements_level_5(self):
        """レベル5実績チェックのテスト"""
        stats = {
            "total_completed": 50,
            "current_streak": 1,
            "weekly_completed": 10,
            "level": 5,
            "earned_achievements": []
        }
        
        new_achievements = Achievement.check_achievements(stats)
        self.assertIn("level_5", new_achievements)


if __name__ == "__main__":
    unittest.main()
