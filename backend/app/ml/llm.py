from typing import Dict, List, Any

TREATMENT_DATABASE = {
    "叶斑病": {
        "light": {
            "pesticides": [
                {"name": "多菌灵", "concentration": "50% 可湿性粉剂 800-1000倍液", "method": "叶面喷雾"},
                {"name": "百菌清", "concentration": "75% 可湿性粉剂 600-800倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "加强通风透光，降低田间湿度",
                "及时清除病叶，减少病原基数",
                "避免大水漫灌，提倡滴灌"
            ],
            "safety_interval": "施药后7-10天方可采收"
        },
        "medium": {
            "pesticides": [
                {"name": "苯醚甲环唑", "concentration": "10% 水分散粒剂 1500-2000倍液", "method": "叶面喷雾"},
                {"name": "戊唑醇", "concentration": "43% 悬浮剂 3000-4000倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "立即摘除严重病叶",
                "加强肥水管理，增强植株抗病力",
                "避免偏施氮肥，适当增施磷钾肥"
            ],
            "safety_interval": "施药后10-14天方可采收"
        },
        "severe": {
            "pesticides": [
                {"name": "氟硅唑", "concentration": "40% 乳油 8000-10000倍液", "method": "叶面喷雾"},
                {"name": "咪鲜胺", "concentration": "25% 乳油 1000-1500倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "拔除严重病株，带出田外销毁",
                "全田喷雾处理，防止蔓延",
                "考虑轮作换茬，减少病原积累"
            ],
            "safety_interval": "施药后14-21天方可采收"
        }
    },
    "锈病": {
        "light": {
            "pesticides": [
                {"name": "粉锈宁", "concentration": "20% 乳油 1500-2000倍液", "method": "叶面喷雾"},
                {"name": "三唑酮", "concentration": "15% 可湿性粉剂 1000-1200倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "及时浇水，保证田间湿度适宜",
                "增施有机肥，提高植株抗病能力"
            ],
            "safety_interval": "施药后7天方可采收"
        },
        "medium": {
            "pesticides": [
                {"name": "丙环唑", "concentration": "25% 乳油 2000-2500倍液", "method": "叶面喷雾"},
                {"name": "烯唑醇", "concentration": "12.5% 可湿性粉剂 2000-3000倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "摘除底部老叶，改善通风条件",
                "避免在早晨露水未干时进行农事操作"
            ],
            "safety_interval": "施药后10-14天方可采收"
        },
        "severe": {
            "pesticides": [
                {"name": "腈菌唑", "concentration": "12.5% 乳油 1500-2000倍液", "method": "叶面喷雾"},
                {"name": "氟环唑", "concentration": "50% 悬浮剂 1500-2000倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "严重病田块考虑提前收获",
                "收获后彻底清除残体",
                "与非寄主作物轮作2-3年"
            ],
            "safety_interval": "施药后14-21天方可采收"
        }
    },
    "白粉病": {
        "light": {
            "pesticides": [
                {"name": "多抗霉素", "concentration": "10% 可湿性粉剂 500-800倍液", "method": "叶面喷雾"},
                {"name": "武夷菌素", "concentration": "2% 水剂 150-200倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "加强通风，降低棚内湿度",
                "适当控水，避免叶面结露"
            ],
            "safety_interval": "施药后5-7天方可采收"
        },
        "medium": {
            "pesticides": [
                {"name": "翠贝", "concentration": "50% 干悬浮剂 3000-4000倍液", "method": "叶面喷雾"},
                {"name": "凯润", "concentration": "25% 乳油 1500-2000倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "及时整枝打叉，摘除病叶",
                "增施钙硅肥，增强细胞壁厚度"
            ],
            "safety_interval": "施药后7-10天方可采收"
        },
        "severe": {
            "pesticides": [
                {"name": "醚菌酯", "concentration": "50% 水分散粒剂 3000-4000倍液", "method": "叶面喷雾"},
                {"name": "吡唑醚菌酯", "concentration": "25% 乳油 1000-2000倍液", "method": "叶面喷雾"}
            ],
            "farming_tips": [
                "拔除重病株，控制蔓延",
                "使用硫磺熏蒸进行辅助防治",
                "收获后进行土壤消毒"
            ],
            "safety_interval": "施药后10-14天方可采收"
        }
    }
}

DEFAULT_TREATMENT = {
    "pesticides": [
        {"name": "广谱杀菌剂", "concentration": "按说明书使用", "method": "叶面喷雾"}
    ],
    "farming_tips": [
        "加强田间管理",
        "合理施肥，增强抗病力",
        "及时清除病残体"
    ],
    "safety_interval": "施药后7-14天方可采收"
}

class TreatmentGenerator:
    def __init__(self):
        self.db = TREATMENT_DATABASE

    def generate(self, disease: str, severity: str, crop_type: str) -> Dict[str, Any]:
        disease_data = self.db.get(disease, {})

        if not disease_data:
            return DEFAULT_TREATMENT

        severity_data = disease_data.get(severity, disease_data.get("light", DEFAULT_TREATMENT))

        return severity_data
