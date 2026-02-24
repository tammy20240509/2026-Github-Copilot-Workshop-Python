#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pomodoro Timer App with Customization Features
カスタマイズ可能なポモドーロタイマーアプリケーション
"""

import tkinter as tk
from tkinter import ttk
import json
import os
from datetime import datetime

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x600")
        
        # デフォルト設定
        self.settings = {
            "work_time": 25,  # 分
            "break_time": 5,  # 分
            "theme": "light",
            "sound_start": True,
            "sound_end": True,
            "sound_tick": False
        }
        
        # 設定を読み込む
        self.load_settings()
        
        # タイマー状態
        self.is_running = False
        self.is_work_time = True
        self.time_left = self.settings["work_time"] * 60
        self.timer_id = None
        
        # UIを構築
        self.create_ui()
        self.apply_theme()
        
    def create_ui(self):
        """UIコンポーネントを作成"""
        # メインフレーム
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill="both")
        
        # タイトルラベル
        self.title_label = tk.Label(
            main_frame,
            text="作業時間",
            font=("Arial", 16, "bold")
        )
        self.title_label.pack(pady=10)
        
        # タイマー表示
        self.timer_label = tk.Label(
            main_frame,
            text="25:00",
            font=("Arial", 48, "bold")
        )
        self.timer_label.pack(pady=20)
        
        # コントロールボタンフレーム
        control_frame = tk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        self.start_button = tk.Button(
            control_frame,
            text="開始",
            command=self.toggle_timer,
            font=("Arial", 12),
            width=10
        )
        self.start_button.pack(side="left", padx=5)
        
        self.reset_button = tk.Button(
            control_frame,
            text="リセット",
            command=self.reset_timer,
            font=("Arial", 12),
            width=10
        )
        self.reset_button.pack(side="left", padx=5)
        
        # 設定フレーム
        settings_frame = tk.LabelFrame(
            main_frame,
            text="設定",
            font=("Arial", 12, "bold"),
            padx=15,
            pady=15
        )
        settings_frame.pack(pady=20, fill="x")
        
        # 作業時間設定
        work_time_frame = tk.Frame(settings_frame)
        work_time_frame.pack(fill="x", pady=5)
        tk.Label(work_time_frame, text="作業時間:", font=("Arial", 10)).pack(side="left")
        self.work_time_var = tk.IntVar(value=self.settings["work_time"])
        for time in [15, 25, 35, 45]:
            tk.Radiobutton(
                work_time_frame,
                text=f"{time}分",
                variable=self.work_time_var,
                value=time,
                command=self.update_work_time,
                font=("Arial", 9)
            ).pack(side="left", padx=5)
        
        # 休憩時間設定
        break_time_frame = tk.Frame(settings_frame)
        break_time_frame.pack(fill="x", pady=5)
        tk.Label(break_time_frame, text="休憩時間:", font=("Arial", 10)).pack(side="left")
        self.break_time_var = tk.IntVar(value=self.settings["break_time"])
        for time in [5, 10, 15]:
            tk.Radiobutton(
                break_time_frame,
                text=f"{time}分",
                variable=self.break_time_var,
                value=time,
                command=self.update_break_time,
                font=("Arial", 9)
            ).pack(side="left", padx=5)
        
        # テーマ設定
        theme_frame = tk.Frame(settings_frame)
        theme_frame.pack(fill="x", pady=5)
        tk.Label(theme_frame, text="テーマ:", font=("Arial", 10)).pack(side="left")
        self.theme_var = tk.StringVar(value=self.settings["theme"])
        for theme in [("light", "ライト"), ("dark", "ダーク"), ("focus", "フォーカス")]:
            tk.Radiobutton(
                theme_frame,
                text=theme[1],
                variable=self.theme_var,
                value=theme[0],
                command=self.update_theme,
                font=("Arial", 9)
            ).pack(side="left", padx=5)
        
        # サウンド設定
        sound_frame = tk.Frame(settings_frame)
        sound_frame.pack(fill="x", pady=5)
        tk.Label(sound_frame, text="サウンド:", font=("Arial", 10)).pack(anchor="w")
        
        self.sound_start_var = tk.BooleanVar(value=self.settings["sound_start"])
        tk.Checkbutton(
            sound_frame,
            text="開始音",
            variable=self.sound_start_var,
            command=self.update_sound_settings,
            font=("Arial", 9)
        ).pack(anchor="w", padx=20)
        
        self.sound_end_var = tk.BooleanVar(value=self.settings["sound_end"])
        tk.Checkbutton(
            sound_frame,
            text="終了音",
            variable=self.sound_end_var,
            command=self.update_sound_settings,
            font=("Arial", 9)
        ).pack(anchor="w", padx=20)
        
        self.sound_tick_var = tk.BooleanVar(value=self.settings["sound_tick"])
        tk.Checkbutton(
            sound_frame,
            text="Tick音",
            variable=self.sound_tick_var,
            command=self.update_sound_settings,
            font=("Arial", 9)
        ).pack(anchor="w", padx=20)
    
    def apply_theme(self):
        """選択されたテーマを適用"""
        theme = self.settings["theme"]
        
        if theme == "dark":
            bg_color = "#2b2b2b"
            fg_color = "#ffffff"
            timer_color = "#4CAF50"
        elif theme == "focus":
            bg_color = "#f5f5f5"
            fg_color = "#333333"
            timer_color = "#FF6B6B"
        else:  # light
            bg_color = "#ffffff"
            fg_color = "#000000"
            timer_color = "#2196F3"
        
        self.root.configure(bg=bg_color)
        
        # すべてのウィジェットに色を適用
        for widget in self.root.winfo_children():
            self._apply_colors_recursive(widget, bg_color, fg_color)
        
        self.timer_label.configure(fg=timer_color)
    
    def _apply_colors_recursive(self, widget, bg_color, fg_color):
        """再帰的にウィジェットに色を適用"""
        try:
            if isinstance(widget, (tk.Label, tk.Frame, tk.LabelFrame)):
                widget.configure(bg=bg_color, fg=fg_color)
            elif isinstance(widget, (tk.Button, tk.Radiobutton, tk.Checkbutton)):
                widget.configure(bg=bg_color, fg=fg_color, activebackground=bg_color, activeforeground=fg_color)
        except tk.TclError:
            pass
        
        for child in widget.winfo_children():
            self._apply_colors_recursive(child, bg_color, fg_color)
    
    def toggle_timer(self):
        """タイマーの開始/一時停止を切り替え"""
        if self.is_running:
            self.pause_timer()
        else:
            self.start_timer()
    
    def start_timer(self):
        """タイマーを開始"""
        self.is_running = True
        self.start_button.configure(text="一時停止")
        
        if self.settings["sound_start"]:
            self.play_sound("start")
        
        self.run_timer()
    
    def pause_timer(self):
        """タイマーを一時停止"""
        self.is_running = False
        self.start_button.configure(text="再開")
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
    
    def reset_timer(self):
        """タイマーをリセット"""
        self.is_running = False
        self.start_button.configure(text="開始")
        
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        self.is_work_time = True
        self.time_left = self.settings["work_time"] * 60
        self.update_display()
        self.title_label.configure(text="作業時間")
    
    def run_timer(self):
        """タイマーを1秒進める"""
        if self.is_running:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_display()
                
                if self.settings["sound_tick"]:
                    self.play_sound("tick")
                
                self.timer_id = self.root.after(1000, self.run_timer)
            else:
                # タイマー終了
                self.timer_complete()
    
    def timer_complete(self):
        """タイマー完了時の処理"""
        if self.settings["sound_end"]:
            self.play_sound("end")
        
        # 作業時間と休憩時間を切り替え
        self.is_work_time = not self.is_work_time
        
        if self.is_work_time:
            self.time_left = self.settings["work_time"] * 60
            self.title_label.configure(text="作業時間")
        else:
            self.time_left = self.settings["break_time"] * 60
            self.title_label.configure(text="休憩時間")
        
        self.update_display()
        self.is_running = False
        self.start_button.configure(text="開始")
    
    def update_display(self):
        """タイマー表示を更新"""
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.timer_label.configure(text=f"{minutes:02d}:{seconds:02d}")
    
    def update_work_time(self):
        """作業時間設定を更新"""
        self.settings["work_time"] = self.work_time_var.get()
        if self.is_work_time and not self.is_running:
            self.time_left = self.settings["work_time"] * 60
            self.update_display()
        self.save_settings()
    
    def update_break_time(self):
        """休憩時間設定を更新"""
        self.settings["break_time"] = self.break_time_var.get()
        if not self.is_work_time and not self.is_running:
            self.time_left = self.settings["break_time"] * 60
            self.update_display()
        self.save_settings()
    
    def update_theme(self):
        """テーマ設定を更新"""
        self.settings["theme"] = self.theme_var.get()
        self.apply_theme()
        self.save_settings()
    
    def update_sound_settings(self):
        """サウンド設定を更新"""
        self.settings["sound_start"] = self.sound_start_var.get()
        self.settings["sound_end"] = self.sound_end_var.get()
        self.settings["sound_tick"] = self.sound_tick_var.get()
        self.save_settings()
    
    def play_sound(self, sound_type):
        """サウンドを再生（プレースホルダー）"""
        # 実際のサウンド再生は環境に応じて実装
        # ここではコンソールに出力するだけ
        sound_names = {
            "start": "開始音",
            "end": "終了音",
            "tick": "Tick音"
        }
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {sound_names.get(sound_type, sound_type)} を再生")
    
    def load_settings(self):
        """設定をファイルから読み込む"""
        settings_file = os.path.join(
            os.path.dirname(__file__),
            "settings.json"
        )
        
        if os.path.exists(settings_file):
            try:
                with open(settings_file, "r", encoding="utf-8") as f:
                    loaded_settings = json.load(f)
                    self.settings.update(loaded_settings)
            except Exception as e:
                print(f"設定の読み込みエラー: {e}")
    
    def save_settings(self):
        """設定をファイルに保存"""
        settings_file = os.path.join(
            os.path.dirname(__file__),
            "settings.json"
        )
        
        try:
            with open(settings_file, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"設定の保存エラー: {e}")

def main():
    """アプリケーションのエントリーポイント"""
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
