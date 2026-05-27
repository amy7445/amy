from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class TrendPredictor:
    def __init__(self):
        self.model = None
        self._load_model()

    def _load_model(self):
        pass

    def predict(self, crop_type: str, start_date: str, days: int = 7) -> Dict[str, Any]:
        start = datetime.strptime(start_date, "%Y-%m-%d")

        base_probabilities = {
            "番茄": [35, 42, 38, 45, 52, 48, 55],
            "黄瓜": [40, 45, 50, 48, 55, 52, 58],
            "小麦": [25, 30, 28, 35, 32, 38, 40],
            "水稻": [45, 50, 48, 55, 52, 58, 60],
            "玉米": [30, 35, 38, 42, 40, 45, 48],
            "马铃薯": [35, 40, 38, 45, 42, 50, 48]
        }

        probabilities = base_probabilities.get(crop_type, [40] * 7)

        dates = []
        predictions = []

        for i in range(days):
            date = start + timedelta(days=i)
            dates.append(date.strftime("%m-%d"))

            prob = probabilities[i] if i < len(probabilities) else 50
            prob = max(10, min(90, prob + random.randint(-5, 5)))

            predictions.append({
                "date": dates[-1],
                "probability": prob,
                "risk_level": "低风险" if prob < 30 else ("中风险" if prob < 60 else "高风险"),
                "suggestion": self._get_suggestion(prob)
            })

        return {
            "crop_type": crop_type,
            "start_date": start_date,
            "dates": dates,
            "probabilities": probabilities[:days],
            "predictions": predictions
        }

    def _get_suggestion(self, probability: float) -> str:
        if probability < 30:
            return "病害风险较低，维持正常管理即可"
        elif probability < 60:
            return "注意监测病情发展，必要时进行预防性施药"
        else:
            return "高风险！建议立即进行防治处理，加强田间巡查"
