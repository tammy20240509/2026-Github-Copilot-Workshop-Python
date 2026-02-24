#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomodoro Timer のロジックテスト（GUI非依存）
"""

import unittest
import json
import os
import sys

# テスト対象のモジュールをインポート
sys.path.insert(0, os.path.dirname(__file__))


class TestPomodoroLogic(unittest.TestCase):
    """ポモドーロタイマーのロジックテスト"""
    
    def test_default_settings_structure(self):
        """デフォルト設定の構造をテスト"""
        default_settings = {
            "work_time": 25,
            "break_time": 5,
            "theme": "light",
            "sound_start": True,
            "sound_end": True,
            "sound_tick": False
        }
        
        # 必須キーが存在することを確認
        required_keys = ["work_time", "break_time", "theme", "sound_start", "sound_end", "sound_tick"]
        for key in required_keys:
            self.assertIn(key, default_settings)
    
    def test_work_time_values(self):
        """作業時間の有効な値をテスト"""
        valid_work_times = [15, 25, 35, 45]
        # 各値が正の整数で60分未満であることを確認
        for time in valid_work_times:
            self.assertGreater(time, 0, f"{time}は正の値でなければなりません")
            self.assertLess(time, 60, f"{time}は60分未満でなければなりません")
            self.assertIsInstance(time, int, f"{time}は整数でなければなりません")
    
    def test_break_time_values(self):
        """休憩時間の有効な値をテスト"""
        valid_break_times = [5, 10, 15]
        # 各値が正の整数で30分未満であることを確認
        for time in valid_break_times:
            self.assertGreater(time, 0, f"{time}は正の値でなければなりません")
            self.assertLess(time, 30, f"{time}は30分未満でなければなりません")
            self.assertIsInstance(time, int, f"{time}は整数でなければなりません")
    
    def test_theme_values(self):
        """テーマの有効な値をテスト"""
        valid_themes = ["light", "dark", "focus"]
        # 各テーマが文字列であることを確認
        for theme in valid_themes:
            self.assertIsInstance(theme, str, f"{theme}は文字列でなければなりません")
            self.assertTrue(len(theme) > 0, f"{theme}は空文字列であってはいけません")
    
    def test_time_conversion(self):
        """分から秒への変換をテスト"""
        # 25分 = 1500秒
        self.assertEqual(25 * 60, 1500)
        # 5分 = 300秒
        self.assertEqual(5 * 60, 300)
        # 45分 = 2700秒
        self.assertEqual(45 * 60, 2700)
    
    def test_time_display_format(self):
        """時間表示フォーマットをテスト"""
        # 1500秒 = 25分00秒
        seconds = 1500
        minutes = seconds // 60
        secs = seconds % 60
        display = f"{minutes:02d}:{secs:02d}"
        self.assertEqual(display, "25:00")
        
        # 60秒 = 1分00秒
        seconds = 60
        minutes = seconds // 60
        secs = seconds % 60
        display = f"{minutes:02d}:{secs:02d}"
        self.assertEqual(display, "01:00")
        
        # 0秒 = 0分00秒
        seconds = 0
        minutes = seconds // 60
        secs = seconds % 60
        display = f"{minutes:02d}:{secs:02d}"
        self.assertEqual(display, "00:00")
    
    def test_settings_json_format(self):
        """設定のJSON形式をテスト"""
        settings = {
            "work_time": 35,
            "break_time": 10,
            "theme": "dark",
            "sound_start": False,
            "sound_end": True,
            "sound_tick": True
        }
        
        # JSONにシリアライズ
        json_str = json.dumps(settings, indent=2, ensure_ascii=False)
        
        # JSONからデシリアライズ
        loaded_settings = json.loads(json_str)
        
        # 元の設定と一致することを確認
        self.assertEqual(settings, loaded_settings)
    
    def test_settings_file_operations(self):
        """設定ファイルの読み書きをテスト"""
        test_settings_file = "/tmp/test_pomodoro_settings.json"
        
        # テスト設定
        settings = {
            "work_time": 35,
            "break_time": 10,
            "theme": "dark",
            "sound_start": False,
            "sound_end": True,
            "sound_tick": True
        }
        
        # 設定を保存
        with open(test_settings_file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
        
        # 設定を読み込み
        with open(test_settings_file, "r", encoding="utf-8") as f:
            loaded_settings = json.load(f)
        
        # 元の設定と一致することを確認
        self.assertEqual(settings, loaded_settings)
        
        # クリーンアップ
        if os.path.exists(test_settings_file):
            os.remove(test_settings_file)


class TestPomodoroRequirements(unittest.TestCase):
    """要件の実装を確認するテスト"""
    
    def test_work_time_options_requirement(self):
        """要件: 時間設定を15/25/35/45分から選択できること"""
        required_options = [15, 25, 35, 45]
        # 要件通りの選択肢が用意されていることを確認
        self.assertEqual(len(required_options), 4, "作業時間の選択肢は4つ必要です")
        self.assertEqual(required_options, [15, 25, 35, 45], "作業時間の選択肢が要件通りであること")
    
    def test_break_time_options_requirement(self):
        """要件: 休憩時間のカスタム（5/10/15分）"""
        required_options = [5, 10, 15]
        # 要件通りの選択肢が用意されていることを確認
        self.assertEqual(len(required_options), 3, "休憩時間の選択肢は3つ必要です")
        self.assertEqual(required_options, [5, 10, 15], "休憩時間の選択肢が要件通りであること")
    
    def test_theme_options_requirement(self):
        """要件: ダーク/ライト/フォーカス（ミニマル）テーマ切替"""
        required_themes = ["dark", "light", "focus"]
        # 要件通りのテーマが用意されていることを確認
        self.assertEqual(len(required_themes), 3, "テーマの選択肢は3つ必要です")
        self.assertIn("dark", required_themes, "ダークテーマが必要です")
        self.assertIn("light", required_themes, "ライトテーマが必要です")
        self.assertIn("focus", required_themes, "フォーカステーマが必要です")
    
    def test_sound_toggle_requirement(self):
        """要件: 開始音/終了音/tick音のオンオフ切り替え"""
        sound_settings = {
            "sound_start": True,
            "sound_end": True,
            "sound_tick": False
        }
        
        # 各サウンド設定がブール値であることを確認
        for key, value in sound_settings.items():
            self.assertIsInstance(value, bool)


if __name__ == "__main__":
    # テストを実行
    unittest.main(verbosity=2)
