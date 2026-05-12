from typing import Dict, Any, List


class SustainabilityAdvisor:
    def __init__(self):
        self.knowledge_base = {
            "crop_rotation": {
                "en": "Rotate legumes with cereals to fix nitrogen naturally and break pest cycles.",
                "sw": "Zungusha mazao ya kunde na nafaka ili kurekebisha nitrojeni kiasili na kuvunja mzunguko wa wadudu.",
                "fr": "Faites pivoter les légumineuses avec les céréales pour fixer naturellement l'azote.",
            },
            "water_conservation": {
                "en": "Install drip irrigation to reduce water usage by up to 60% while increasing yields.",
                "sw": "Sakinisha umwagiliaji kwa njia ya matone ili kupunguza matumizi ya maji kwa hadi 60%.",
                "fr": "Installez l'irrigation goutte à goutte pour réduire la consommation d'eau jusqu'à 60%.",
            },
            "soil_health": {
                "en": "Add compost and practice no-till farming to improve soil organic matter by 1% annually.",
                "sw": "Ongeza mbolea na ufanye kilimo kisicho na kulima ili kuboresha viumbe hai vya udongo.",
                "fr": "Ajoutez du compost et pratiquez le semis direct pour améliorer la matière organique du sol.",
            },
            "agroforestry": {
                "en": "Plant native trees along farm boundaries to increase biodiversity and carbon capture by 30%.",
                "sw": "Panda miti asilia kando ya shamba ili kuongeza bioanuwai na kunasa kaboni kwa 30%.",
                "fr": "Plantez des arbres indigènes en bordure des fermes pour augmenter la biodiversité.",
            },
            "carbon_credits": {
                "en": "Your farm could earn carbon credits worth $15-30 per tonne of CO2 sequestered.",
                "sw": "Shamba lako linaweza kupata mikopo ya kaboni yenye thamani ya $15-30 kwa tani ya CO2.",
                "fr": "Votre ferme pourrait gagner des crédits carbone d'une valeur de 15 à 30 dollars par tonne de CO2.",
            },
        }

    def get_recommendations(self, farm_data: Dict[str, Any], language: str = "en") -> List[Dict[str, str]]:
        recommendations = []
        practices = str(farm_data.get("sustainability_practices", "")).lower()

        if "crop rotation" not in practices and "rotation" not in practices:
            recommendations.append({
                "topic": "crop_rotation",
                "advice": self.knowledge_base["crop_rotation"].get(language, self.knowledge_base["crop_rotation"]["en"]),
                "priority": "high",
                "category": "soil_health",
            })

        if "drip" not in str(farm_data.get("irrigation_type", "")).lower():
            recommendations.append({
                "topic": "water_conservation",
                "advice": self.knowledge_base["water_conservation"].get(language, self.knowledge_base["water_conservation"]["en"]),
                "priority": "high",
                "category": "water",
            })

        if "compost" not in practices and "organic" not in practices:
            recommendations.append({
                "topic": "soil_health",
                "advice": self.knowledge_base["soil_health"].get(language, self.knowledge_base["soil_health"]["en"]),
                "priority": "medium",
                "category": "soil_health",
            })

        if "agroforestry" not in practices and "tree" not in practices:
            recommendations.append({
                "topic": "agroforestry",
                "advice": self.knowledge_base["agroforestry"].get(language, self.knowledge_base["agroforestry"]["en"]),
                "priority": "medium",
                "category": "biodiversity",
            })

        recommendations.append({
            "topic": "carbon_credits",
            "advice": self.knowledge_base["carbon_credits"].get(language, self.knowledge_base["carbon_credits"]["en"]),
            "priority": "low",
            "category": "finance",
        })

        return recommendations[:5]

    def get_climate_adaptation_advice(self, region: str, language: str = "en") -> Dict[str, str]:
        advice = {
            "arid": {
                "en": "Plant drought-resistant crop varieties and implement water harvesting systems.",
                "sw": "Panda aina za mazao zinazostahimili ukame na kutekeleza mifumo ya kuvuna maji.",
                "fr": "Plantez des variétés de cultures résistantes à la sécheresse.",
            },
            "tropical": {
                "en": "Use improved drainage systems and plant windbreaks to protect against extreme rainfall.",
                "sw": "Tumia mifumo bora ya mifereji ya maji na panda ua la upepo.",
                "fr": "Utilisez des systèmes de drainage améliorés et plantez des brise-vent.",
            },
        }

        region_key = "arid"
        for key in advice:
            if key.replace("_", " ") in region.lower():
                region_key = key
                break

        return {
            "region": region,
            "advice": advice.get(region_key, {}).get(language, advice["arid"]["en"]),
        }


advisor = SustainabilityAdvisor()
