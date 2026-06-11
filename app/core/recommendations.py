"""
COOLING INTELLIGENCE ENGINE
This is the brain of CoolHome AI
Takes room information, outputs recommendations
"""


class RecommendationEngine:
    """
    This class generates cooling recommendations based on room features.
    
    Think of it like a doctor:
    - Input: Patient symptoms (room features)
    - Output: Treatment recommendations (cooling tips)
    """
    
    def __init__(self):
        """Initialize the engine (called when you create it)"""
        self.recommendations = []  # List to store recommendations
    
    # ============================================================
    # MAIN METHOD - This is called with room data
    # ============================================================
    
    def generate_recommendations(self, room_features: dict) -> list:
        """
        MAIN METHOD: Takes room data, returns recommendations
        
        Input example:
        {
            "windows": 2,
            "ventilation": "poor",
            "sunlight": "high",
            "window_direction": "west"
        }
        
        Output example:
        [
            {
                "category": "Ventilation",
                "action": "Open opposite windows",
                "priority": "high",
                "expected_impact": "5-10°C reduction"
            },
            { more recommendations... }
        ]
        """
        
        # STEP 1: Reset recommendations list (start fresh)
        self.recommendations = []
        
        # STEP 2: Check each room feature and add relevant recommendations
        # Think: "For THIS room condition, what should we recommend?"
        
        self._check_ventilation(room_features)       # Check if windows/fans needed
        self._check_sunlight(room_features)          # Check if shade needed
        self._check_roof_type(room_features)         # Check if roof paint needed
        self._check_indoor_environment(room_features) # Check if plants/paint needed
        self._check_furniture(room_features)         # Check if furniture blocking
        
        # STEP 3: Sort by priority (HIGH first, then MEDIUM, then LOW)
        self._sort_by_priority()
        
        # STEP 4: Return top 10 recommendations
        return self.recommendations[:10]
    
    
    # ============================================================
    # RECOMMENDATION METHODS (Each checks ONE thing)
    # ============================================================
    
    def _check_ventilation(self, features: dict):
        """
        CHECK VENTILATION
        If room has poor ventilation → recommend opening windows
        
        Think of it: "Is air flowing? If no, suggest ways to fix it"
        """
        
        # Get ventilation status from room data
        # If it doesn't exist, default to "poor"
        ventilation = features.get("ventilation", "poor")
        
        # IF ventilation is poor, add recommendations
        if ventilation == "poor":
            
            # RECOMMENDATION 1: Cross-ventilation
            self.recommendations.append({
                "category": "Ventilation",
                "action": "Open opposite windows for cross-ventilation (morning & evening)",
                "priority": "high",
                "expected_impact": "5-10°C reduction",
                "cost": "Free",
                "implementation_difficulty": "Easy",
                "details": "Opening windows on opposite sides lets hot air escape, cool air enter"
            })
            
            # RECOMMENDATION 2: Exhaust fan
            self.recommendations.append({
                "category": "Ventilation",
                "action": "Install an exhaust fan to pull hot air out",
                "priority": "high",
                "expected_impact": "3-7°C reduction",
                "cost": "₹1000-3000",
                "implementation_difficulty": "Medium",
                "details": "Exhaust fans actively remove hot air. Install at high point of room."
            })
        
        # IF ventilation is moderate (not bad, not great)
        elif ventilation == "moderate":
            self.recommendations.append({
                "category": "Ventilation",
                "action": "Ensure windows stay unblocked",
                "priority": "medium",
                "expected_impact": "2-4°C reduction",
                "cost": "Free",
                "implementation_difficulty": "Easy",
                "details": "Keep windows and screens clean for better air flow"
            })
        
        # If ventilation is "good", we don't recommend anything for ventilation
    
    
    def _check_sunlight(self, features: dict):
        """
        CHECK SUNLIGHT
        If room gets too much sun → recommend shading solutions
        
        Think of it: "Is the room too sunny? If yes, suggest ways to block sun"
        """
        
        # Get sunlight level from room data
        sunlight = features.get("sunlight", "low")
        
        # Get window direction (important for sunlight)
        # A west-facing window gets afternoon sun (very hot!)
        window_direction = features.get("window_direction", "unknown")
        
        # IF sunlight is HIGH
        if sunlight == "high":
            
            # IF window faces WEST or SOUTH (these get most sun)
            if window_direction in ["west", "south"]:
                
                # RECOMMENDATION 1: Reflective curtains
                self.recommendations.append({
                    "category": "Sunlight Reduction",
                    "action": "Install reflective (white/light colored) curtains on windows",
                    "priority": "high",
                    "expected_impact": "4-8°C reduction",
                    "cost": "₹500-1500 per window",
                    "implementation_difficulty": "Easy",
                    "details": "Light colors reflect 50-60% of solar heat. Very effective!"
                })
                
                # RECOMMENDATION 2: External shading
                self.recommendations.append({
                    "category": "Sunlight Reduction",
                    "action": "Add external shading (bamboo screen or shade cloth)",
                    "priority": "high",
                    "expected_impact": "6-12°C reduction",
                    "cost": "₹800-2000",
                    "implementation_difficulty": "Medium",
                    "details": "External shade blocks sun BEFORE it enters room (more effective!)"
                })
            else:
                # For other directions, just recommend light curtains
                self.recommendations.append({
                    "category": "Sunlight Reduction",
                    "action": "Use light-colored curtains on all windows",
                    "priority": "medium",
                    "expected_impact": "3-6°C reduction",
                    "cost": "₹300-800 per window",
                    "implementation_difficulty": "Easy",
                    "details": "Even non-south windows benefit from light curtains"
                })
        
        # IF sunlight is MODERATE
        elif sunlight == "moderate":
            self.recommendations.append({
                "category": "Sunlight Reduction",
                "action": "Use light-colored blinds during daytime",
                "priority": "medium",
                "expected_impact": "2-4°C reduction",
                "cost": "₹200-500",
                "implementation_difficulty": "Easy",
                "details": "Part-time shading helps moderate sun exposure"
            })
    
    
    def _check_roof_type(self, features: dict):
        """
        CHECK ROOF
        If roof is visible/exposed → recommend reflective paint
        
        Think of it: "Does the sun beat down on the roof? If yes, paint it white!"
        """
        
        # Is the roof visible in the analysis? (matters for heat)
        roof_visible = features.get("roof_visible", False)
        
        # IF roof is visible/exposed to sun
        if roof_visible:
            
            # RECOMMENDATION 1: Cool roof paint
            self.recommendations.append({
                "category": "Heat Absorption",
                "action": "Paint roof with white/reflective coating",
                "priority": "high",
                "expected_impact": "3-7°C reduction",
                "cost": "₹500-2000",
                "implementation_difficulty": "Medium",
                "details": "White reflects 70-80% of heat. Dark roofs absorb only 10-20%"
            })
            
            # RECOMMENDATION 2: Roof insulation
            self.recommendations.append({
                "category": "Heat Absorption",
                "action": "Add roof insulation (thermocol or rockwool)",
                "priority": "medium",
                "expected_impact": "5-10°C reduction",
                "cost": "₹2000-5000",
                "implementation_difficulty": "Hard",
                "details": "Insulation creates air gap that slows heat transfer"
            })
    
    
    def _check_indoor_environment(self, features: dict):
        """
        CHECK INDOOR ENVIRONMENT
        - No plants? Recommend adding them
        - Dark walls? Recommend painting light
        
        Think of it: "What's missing inside that could cool things naturally?"
        """
        
        # Does the room have indoor plants?
        has_plants = features.get("indoor_plants", False)
        
        # IF NO plants, recommend adding them
        if not has_plants:
            self.recommendations.append({
                "category": "Passive Cooling",
                "action": "Add 3-5 indoor plants (neem, pothos, tulsi)",
                "priority": "medium",
                "expected_impact": "1-3°C reduction",
                "cost": "₹200-500",
                "implementation_difficulty": "Easy",
                "details": "Plants release cool water vapor. Also improve air quality!"
            })
        
        # ALWAYS recommend water containers (for everyone)
        self.recommendations.append({
            "category": "Passive Cooling",
            "action": "Place water containers (pots/buckets) in room",
            "priority": "medium",
            "expected_impact": "2-4°C reduction",
            "cost": "Free",
            "implementation_difficulty": "Easy",
            "details": "Water evaporation cools air naturally. Refill daily in summer."
        })
        
        # ALWAYS recommend light wall colors
        self.recommendations.append({
            "category": "Heat Absorption",
            "action": "Paint walls with light colors (white, cream, light yellow)",
            "priority": "medium",
            "expected_impact": "2-5°C reduction",
            "cost": "₹1000-3000",
            "implementation_difficulty": "Medium",
            "details": "Dark colors absorb heat. Light colors reflect it."
        })
    
    
    def _check_furniture(self, features: dict):
        """
        CHECK FURNITURE ARRANGEMENT
        If furniture blocks windows → recommend moving it
        
        Think of it: "Is furniture blocking air flow? If yes, suggest moving it"
        """
        
        # How dense is the furniture? ("low", "moderate", "high")
        furniture_density = features.get("furniture_density", "moderate")
        
        # IF furniture is high density (too much stuff!)
        if furniture_density == "high":
            
            # RECOMMENDATION 1: Unblock openings
            self.recommendations.append({
                "category": "Airflow",
                "action": "Rearrange furniture to not block windows and doors",
                "priority": "high",
                "expected_impact": "3-6°C reduction",
                "cost": "Free",
                "implementation_difficulty": "Easy",
                "details": "Blocked windows prevent cross-ventilation. Move furniture to walls."
            })
            
            # RECOMMENDATION 2: Remove heavy curtains during day
            self.recommendations.append({
                "category": "Airflow",
                "action": "Remove heavy curtains during day (6 AM - 6 PM)",
                "priority": "medium",
                "expected_impact": "1-2°C reduction",
                "cost": "Free",
                "implementation_difficulty": "Easy",
                "details": "Heavy fabrics trap heat. Remove during hot hours."
            })
        
        # ALWAYS recommend fans (good for everyone)
        self.recommendations.append({
            "category": "Airflow",
            "action": "Use table/ceiling fans to circulate cool air from windows",
            "priority": "medium",
            "expected_impact": "Makes room feel cooler",
            "cost": "₹500-2000 (if buying new)",
            "implementation_difficulty": "Easy",
            "details": "Fans don't cool but improve air circulation significantly"
        })
    
    
    # ============================================================
    # HELPER METHODS (Do small jobs)
    # ============================================================
    
    def _sort_by_priority(self):
        """
        SORT RECOMMENDATIONS BY PRIORITY
        
        Order should be:
        1. HIGH priority (must do)
        2. MEDIUM priority (should do)
        3. LOW priority (nice to have)
        """
        
        # Define priority order (0 = first, 1 = second, etc.)
        priority_order = {
            "high": 0,
            "medium": 1,
            "low": 2
        }
        
        # Sort the list using this order
        # If priority not found, default to 2 (low)
        self.recommendations.sort(
            key=lambda x: priority_order.get(x.get("priority", "low"), 2)
        )


# ============================================================
# EXAMPLE OF HOW TO USE THIS CLASS
# ============================================================

# If you were to test this right now:
#
# 1. Create the engine
# engine = RecommendationEngine()
#
# 2. Prepare room data (from Member 1's vision API)
# room_data = {
#     "windows": 2,
#     "ventilation": "poor",
#     "sunlight": "high",
#     "window_direction": "west",
#     "roof_visible": True,
#     "indoor_plants": False,
#     "furniture_density": "high"
# }
#
# 3. Get recommendations
# recs = engine.generate_recommendations(room_data)
#
# 4. Print them
# for rec in recs:
#     print(f"{rec['priority'].upper()}: {rec['action']}")
#
# Output:
# HIGH: Open opposite windows for cross-ventilation...
# HIGH: Install an exhaust fan...
# HIGH: Install reflective curtains...
# ... etc