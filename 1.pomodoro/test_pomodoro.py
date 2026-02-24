#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomodoro Timer のテスト
"""

import unittest
import json
import os
import sys
from unittest.mock import Mock, patch
import tkinter as tk

# app.pyをインポート
sys.path.insert(0, os.path.dirname(__file__))
from app import PomodoroTimer


class TestPomodoroTimer(unittest.TestCase):
    """PomodoroTimerのテストクラス"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.root = tk.Tk()
        self.root.withdraw()  # ウィンドウを表示しない
        self.app = PomodoroTimer(self.root)
        
        # テスト用設定ファイルのパス
        self.test_settings_file = os.path.join(
            os.path.dirname(__file__),
            "test_settings.json"
        )
    
    def tearDown(self):
        """各テストの後に実行"""
        # タイマーを停止
        if self.app.timer_id:
            self.root.after_cancel(self.app.timer_id)
        
        self.root.destroy()
        
        # テスト用設定ファイルを削除
        if os.path.exists(self.test_settings_file):
            os.remove(self.test_settings_file)
    
    def test_default_settings(self):
        """デフォルト設定のテスト"""
        self.assertEqual(self.app.settings["work_time"], 25)
        self.assertEqual(self.app.settings["break_time"], 5)
        self.assertEqual(self.app.settings["theme"], "light")
        self.assertTrue(self.app.settings["sound_start"])
        self.assertTrue(self.app.settings["sound_end"])
        self.assertFalse(self.app.settings["sound_tick"])
    
    def test_work_time_options(self):
        """作業時間の選択肢をテスト"""
        work_times = [15, 25, 35, 45]
        for time in work_times:
            self.app.work_time_var.set(time)
            self.app.update_work_time()
            self.assertEqual(self.app.settings["work_time"], time)
    
    def test_break_time_options(self):
        """休憩時間の選択肢をテスト"""
        break_times = [5, 10, 15]
        for time in break_times:
            self.app.break_time_var.set(time)
            self.app.update_break_time()
            self.assertEqual(self.app.settings["break_time"], time)
    
    def test_theme_options(self):
        """テーマの選択肢をテスト"""
        themes = ["light", "dark", "focus"]
        for theme in themes:
            self.app.theme_var.set(theme)
            self.app.update_theme()
            self.assertEqual(self.app.settings["theme"], theme)
    
    def test_sound_settings(self):
        """サウンド設定のテスト"""
        # 開始音をオフ
        self.app.sound_start_var.set(False)
        self.app.update_sound_settings()
        self.assertFalse(self.app.settings["sound_start"])
        
        # 終了音をオフ
        self.app.sound_end_var.set(False)
        self.app.update_sound_settings()
        self.assertFalse(self.app.settings["sound_end"])
        
        # Tick音をオン
        self.app.sound_tick_var.set(True)
        self.app.update_sound_settings()
        self.assertTrue(self.app.settings["sound_tick"])
    
    def test_timer_initialization(self):
        """タイマーの初期化をテスト"""
        self.assertFalse(self.app.is_running)
        self.assertTrue(self.app.is_work_time)
        self.assertEqual(self.app.time_left, 25 * 60)  # 25分
    
    def test_timer_display(self):
        """タイマー表示のテスト"""
        self.app.time_left = 1500  # 25分
        self.app.update_display()
        self.assertEqual(self.app.timer_label.cget("text"), "25:00")
        
        self.app.time_left = 60  # 1分
        self.app.update_display()
        self.assertEqual(self.app.timer_label.cget("text"), "01:00")
        
        self.app.time_left = 0
        self.app.update_display()
        self.assertEqual(self.app.timer_label.cget("text"), "00:00")
    
    def test_toggle_timer(self):
        """タイマーの開始/停止をテスト"""
        # 開始
        self.assertFalse(self.app.is_running)
        self.app.toggle_timer()
        self.assertTrue(self.app.is_running)
        self.assertEqual(self.app.start_button.cget("text"), "一時停止")
        
        # 一時停止
        self.app.toggle_timer()
        self.assertFalse(self.app.is_running)
        self.assertEqual(self.app.start_button.cget("text"), "再開")
    
    def test_reset_timer(self):
        """タイマーのリセットをテスト"""
        # タイマーを開始
        self.app.toggle_timer()
        self.assertTrue(self.app.is_running)
        
        # 時間を進める
        self.app.time_left = 1200  # 20分
        
        # リセット
        self.app.reset_timer()
        self.assertFalse(self.app.is_running)
        self.assertEqual(self.app.time_left, 25 * 60)
        self.assertEqual(self.app.start_button.cget("text"), "開始")
    
    @patch('builtins.open', create=True)
    def test_save_settings(self, mock_open):
        """設定の保存をテスト"""
        mock_file = Mock()
        mock_open.return_value.__enter__.return_value = mock_file
        
        self.app.settings["work_time"] = 35
        self.app.save_settings()
        
        mock_open.assert_called_once()
    
    def test_work_time_update_while_running(self):
        """タイマー実行中の作業時間変更をテスト"""
        # タイマーを開始
        self.app.toggle_timer()
        original_time = self.app.time_left
        
        # 作業時間を変更（実行中は適用されないはず）
        self.app.work_time_var.set(35)
        self.app.update_work_time()
        
        # タイマーの残り時間は変わらない
        self.assertEqual(self.app.time_left, original_time)


class TestPomodoroTimerIntegration(unittest.TestCase):
    """統合テスト"""
    
    def setUp(self):
        """各テストの前に実行"""
        self.root = tk.Tk()
        self.root.withdraw()
        
        # テスト用設定ファイルを削除
        self.settings_file = os.path.join(
            os.path.dirname(__file__),
            "settings.json"
        )
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
    
    def tearDown(self):
        """各テストの後に実行"""
        self.root.destroy()
        
        # テスト用設定ファイルを削除
        if os.path.exists(self.settings_file):
            os.remove(self.settings_file)
    
    def test_settings_persistence(self):
        """設定の永続化をテスト"""
        # 最初のアプリインスタンスで設定を変更
        app1 = PomodoroTimer(self.root)
        app1.work_time_var.set(35)
        app1.update_work_time()
        app1.theme_var.set("dark")
        app1.update_theme()
        app1.save_settings()
        
        # 新しいアプリインスタンスで設定が読み込まれるか確認
        app2 = PomodoroTimer(self.root)
        self.assertEqual(app2.settings["work_time"], 35)
        self.assertEqual(app2.settings["theme"], "dark")


if __name__ == "__main__":
    # テストを実行
    unittest.main(verbosity=2)
