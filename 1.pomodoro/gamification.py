"""
ゲーミフィケーション機能モジュール
経験値、レベル、実績バッジ、ストリークを管理
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict


class Achievement:
    """実績バッジクラス"""
    
    # 実績定義
    ACHIEVEMENTS = {
        "first_pomodoro": {
            "name": "初めてのポモドーロ",
            "description": "最初のポモドーロを完了",
            "condition": lambda stats: stats["total_completed"] >= 1
        },
        "streak_3": {
            "name": "3日連続",
            "description": "3日連続でポモドーロを完了",
            "condition": lambda stats: stats["current_streak"] >= 3
        },
        "streak_7": {
            "name": "1週間連続",
            "description": "7日連続でポモドーロを完了",
            "condition": lambda stats: stats["current_streak"] >= 7
        },
        "weekly_10": {
            "name": "週間10回完了",
            "description": "1週間で10回のポモドーロを完了",
            "condition": lambda stats: stats["weekly_completed"] >= 10
        },
        "level_5": {
            "name": "レベル5達成",
            "description": "レベル5に到達",
            "condition": lambda stats: stats["level"] >= 5
        },
        "level_10": {
            "name": "レベル10達成",
            "description": "レベル10に到達",
            "condition": lambda stats: stats["level"] >= 10
        },
        "total_50": {
            "name": "ベテラン",
            "description": "合計50回のポモドーロを完了",
            "condition": lambda stats: stats["total_completed"] >= 50
        },
        "total_100": {
            "name": "マスター",
            "description": "合計100回のポモドーロを完了",
            "condition": lambda stats: stats["total_completed"] >= 100
        }
    }
    
    @classmethod
    def check_achievements(cls, stats: Dict) -> List[str]:
        """新しく獲得した実績をチェック"""
        earned = []
        for achievement_id, achievement in cls.ACHIEVEMENTS.items():
            if achievement_id not in stats.get("earned_achievements", []):
                if achievement["condition"](stats):
                    earned.append(achievement_id)
        return earned


class GamificationManager:
    """ゲーミフィケーション管理クラス"""
    
    # レベルアップに必要なXP（累積）
    XP_PER_LEVEL = 100
    XP_PER_POMODORO = 10
    
    def __init__(self, data_file: str = "gamification_data.json"):
        self.data_file = Path(data_file)
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """データファイルから読み込み"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._create_initial_data()
    
    def _create_initial_data(self) -> Dict:
        """初期データ作成"""
        return {
            "xp": 0,
            "level": 1,
            "total_completed": 0,
            "current_streak": 0,
            "longest_streak": 0,
            "last_completion_date": None,
            "earned_achievements": [],
            "completion_history": []  # {"date": "YYYY-MM-DD", "count": n}
        }
    
    def _save_data(self):
        """データファイルに保存"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def complete_pomodoro(self) -> Dict:
        """ポモドーロ完了時の処理"""
        result = {
            "xp_gained": self.XP_PER_POMODORO,
            "level_up": False,
            "new_achievements": [],
            "streak_updated": False
        }
        
        # XP加算
        self.data["xp"] += self.XP_PER_POMODORO
        
        # レベルアップチェック
        new_level = (self.data["xp"] // self.XP_PER_LEVEL) + 1
        if new_level > self.data["level"]:
            self.data["level"] = new_level
            result["level_up"] = True
        
        # 完了数カウント
        self.data["total_completed"] += 1
        
        # ストリーク更新
        today = datetime.now().strftime("%Y-%m-%d")
        last_date = self.data["last_completion_date"]
        
        if last_date:
            last_dt = datetime.strptime(last_date, "%Y-%m-%d")
            today_dt = datetime.strptime(today, "%Y-%m-%d")
            diff = (today_dt - last_dt).days
            
            if diff == 1:
                # 連続
                self.data["current_streak"] += 1
                result["streak_updated"] = True
            elif diff == 0:
                # 同日
                pass
            else:
                # 途切れた
                self.data["current_streak"] = 1
                result["streak_updated"] = True
        else:
            self.data["current_streak"] = 1
            result["streak_updated"] = True
        
        # 最長ストリーク更新
        if self.data["current_streak"] > self.data["longest_streak"]:
            self.data["longest_streak"] = self.data["current_streak"]
        
        self.data["last_completion_date"] = today
        
        # 完了履歴更新
        self._update_completion_history(today)
        
        # 実績チェック
        stats = self.get_stats()
        new_achievements = Achievement.check_achievements(stats)
        if new_achievements:
            self.data["earned_achievements"].extend(new_achievements)
            result["new_achievements"] = new_achievements
        
        self._save_data()
        return result
    
    def _update_completion_history(self, date: str):
        """完了履歴を更新"""
        history = self.data["completion_history"]
        
        # 今日のエントリを探す
        for entry in history:
            if entry["date"] == date:
                entry["count"] += 1
                return
        
        # 新しいエントリを追加
        history.append({"date": date, "count": 1})
    
    def get_stats(self) -> Dict:
        """統計情報を取得"""
        return {
            "xp": self.data["xp"],
            "level": self.data["level"],
            "xp_to_next_level": self.XP_PER_LEVEL - (self.data["xp"] % self.XP_PER_LEVEL),
            "total_completed": self.data["total_completed"],
            "current_streak": self.data["current_streak"],
            "longest_streak": self.data["longest_streak"],
            "earned_achievements": self.data["earned_achievements"],
            "weekly_completed": self._get_weekly_completed(),
            "monthly_completed": self._get_monthly_completed()
        }
    
    def _get_weekly_completed(self) -> int:
        """今週の完了数"""
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        
        total = 0
        for entry in self.data["completion_history"]:
            entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
            if entry_date >= week_ago:
                total += entry["count"]
        
        return total
    
    def _get_monthly_completed(self) -> int:
        """今月の完了数"""
        today = datetime.now()
        month_ago = today - timedelta(days=30)
        
        total = 0
        for entry in self.data["completion_history"]:
            entry_date = datetime.strptime(entry["date"], "%Y-%m-%d")
            if entry_date >= month_ago:
                total += entry["count"]
        
        return total
    
    def get_weekly_stats(self) -> List[Dict]:
        """週間統計（過去7日分）"""
        stats = []
        today = datetime.now()
        
        for i in range(7):
            date = (today - timedelta(days=6-i)).strftime("%Y-%m-%d")
            count = 0
            
            for entry in self.data["completion_history"]:
                if entry["date"] == date:
                    count = entry["count"]
                    break
            
            stats.append({
                "date": date,
                "count": count,
                "weekday": datetime.strptime(date, "%Y-%m-%d").strftime("%a")
            })
        
        return stats
    
    def get_monthly_stats(self) -> List[Dict]:
        """月間統計（過去30日分）"""
        stats = []
        today = datetime.now()
        
        for i in range(30):
            date = (today - timedelta(days=29-i)).strftime("%Y-%m-%d")
            count = 0
            
            for entry in self.data["completion_history"]:
                if entry["date"] == date:
                    count = entry["count"]
                    break
            
            stats.append({
                "date": date,
                "count": count
            })
        
        return stats
    
    def get_achievement_list(self) -> List[Dict]:
        """実績リスト取得"""
        earned = self.data["earned_achievements"]
        achievements = []
        
        for achievement_id, achievement in Achievement.ACHIEVEMENTS.items():
            achievements.append({
                "id": achievement_id,
                "name": achievement["name"],
                "description": achievement["description"],
                "earned": achievement_id in earned
            })
        
        return achievements
