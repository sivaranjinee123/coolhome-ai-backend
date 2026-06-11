"""
API ROUTES (UPDATED WITH NEW JSON FORMAT)
Matches the new JSON format from Member 1's frontend
"""

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
from typing import Optional, List
from app.core.recommendations import RecommendationEngine
from app.core.gemini_service import GeminiService

# ============================================================
# SETUP
# ============================================================

router = APIRouter(prefix="/api", tags=["api"])
rec_engine = RecommendationEngine()
gemini_service = GeminiService()


# ============================================================
# DATA MODELS (Updated to match frontend JSON)
# ============================================================

class RoomFeatures(BaseModel):
    """
    Updated to match new JSON format from frontend
    
    Example from frontend:
    {
      "windows": 1,
      "ventilation": "poor",
      "sunlight": "high",
      "indoor_plants": false,
      "furniture_density": "high",
      "airflow_obstruction": "high"
    }
    """
    
    # Required fields
    windows: int
    ventilation: str  # "poor", "moderate", "good"
    sunlight: str    # "low", "moderate", "high"
    furniture_density: str  # "low", "moderate", "high"
    airflow_obstruction: str  # "low", "moderate", "high"
    
    # Optional fields
    indoor_plants: bool = False
    window_direction: Optional[str] = None  # "north", "south", "east", "west"
    curtain_type: Optional[str] = None
    roof_visible: Optional[bool] = None
    room_size: Optional[float] = None
    location: Optional[str] = None
    current_temperature: Optional[float] = None


class Recommendation(BaseModel):
    """Single recommendation"""
    category: str
    action: str
    priority: Optional[str] = None
    expected_impact: str
    cost: Optional[str] = None
    implementation_difficulty: Optional[str] = None
    details: Optional[str] = None
    source: Optional[str] = None


# ============================================================
# ENDPOINTS
# ============================================================

@router.get("/health")
async def health_check():
    """Check if backend is running"""
    return {
        "status": "healthy",
        "message": "CoolHome AI Backend is running!",
        "gemini_available": gemini_service.available
    }


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "CoolHome AI Backend",
        "status": "running ✅",
        "docs": "http://localhost:8000/docs"
    }


@router.post("/recommendations")
async def get_recommendations(room_features: RoomFeatures):
    """
    Get rule-based recommendations
    
    INPUT: Room features from frontend
    OUTPUT: 10 prioritized recommendations
    """
    
    try:
        # Convert to dictionary
        room_data = room_features.dict()
        
        # Remove None values to avoid issues
        room_data = {k: v for k, v in room_data.items() if v is not None}
        
        # Generate recommendations
        recommendations = rec_engine.generate_recommendations(room_data)
        
        # Add source
        for rec in recommendations:
            rec["source"] = "rule_based"
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "total": len(recommendations),
            "method": "rule_based",
            "message": f"Generated {len(recommendations)} rule-based recommendations"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error generating recommendations: {str(e)}"
        }


@router.post("/recommendations-ai")
async def get_ai_recommendations(room_features: RoomFeatures):
    """
    Get AI-powered recommendations from Gemini
    """
    
    try:
        # Check if Gemini is available
        if not gemini_service.available:
            return {
                "status": "error",
                "message": "Gemini API not configured. Please set GEMINI_API_KEY in .env file"
            }
        
        # Convert to dictionary
        room_data = room_features.dict()
        room_data = {k: v for k, v in room_data.items() if v is not None}
        
        print(f"📤 Sending to Gemini: {room_data}")
        
        # Get AI recommendations
        recommendations = gemini_service.generate_ai_recommendations(room_data)
        
        print(f"📥 Received from Gemini: {recommendations}")
        
        if not recommendations:
            return {
                "status": "error",
                "message": "Failed to generate recommendations from Gemini. Check server logs."
            }
        
        return {
            "status": "success",
            "recommendations": recommendations,
            "total": len(recommendations),
            "method": "ai_generated",
            "message": f"Generated {len(recommendations)} AI-powered recommendations"
        }
    
    except Exception as e:
        print(f"❌ Error in get_ai_recommendations: {str(e)}")
        return {
            "status": "error",
            "message": f"Error: {str(e)}"
        }


@router.post("/recommendations-hybrid")
async def get_hybrid_recommendations(room_features: RoomFeatures):
    """
    Get both rule-based AND AI recommendations combined
    """
    
    try:
        room_data = room_features.dict()
        room_data = {k: v for k, v in room_data.items() if v is not None}
        
        # Get rule-based
        rule_based = rec_engine.generate_recommendations(room_data)
        for rec in rule_based:
            rec["source"] = "rule_based"
        
        # Get AI (if available)
        ai_generated = []
        if gemini_service.available:
            ai_generated = gemini_service.generate_ai_recommendations(room_data)
        else:
            print("⚠️ Gemini not available, using rule-based only")
        
        # Combine
        combined = rule_based.copy()
        rule_actions = {rec["action"].lower() for rec in rule_based}
        for ai_rec in ai_generated:
            if ai_rec["action"].lower() not in rule_actions:
                combined.append(ai_rec)
        
        # Sort by priority
        def priority_value(rec):
            priority = rec.get("priority", "low")
            return {"high": 0, "medium": 1, "low": 2}.get(priority, 2)
        
        combined.sort(key=priority_value)
        
        return {
            "status": "success",
            "rule_based": rule_based,
            "ai_generated": ai_generated,
            "combined": combined[:15],
            "total_combined": len(combined),
            "message": f"Generated {len(rule_based)} rule-based + {len(ai_generated)} AI recommendations"
        }
    
    except Exception as e:
        print(f"❌ Error in get_hybrid_recommendations: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/analyze")
async def analyze_room(
    room_features: RoomFeatures,
    location: Optional[str] = None
):
    """
    Full analysis with hybrid recommendations and scores
    """
    
    try:
        room_data = room_features.dict()
        room_data = {k: v for k, v in room_data.items() if v is not None}
        
        # Get recommendations
        rule_based = rec_engine.generate_recommendations(room_data)
        for rec in rule_based:
            rec["source"] = "rule_based"
        
        ai_generated = []
        if gemini_service.available:
            ai_generated = gemini_service.generate_ai_recommendations(room_data)
        
        # Combine
        combined = rule_based.copy()
        rule_actions = {rec["action"].lower() for rec in rule_based}
        for ai_rec in ai_generated:
            if ai_rec["action"].lower() not in rule_actions:
                combined.append(ai_rec)
        
        combined.sort(key=lambda x: {"high": 0, "medium": 1, "low": 2}.get(x.get("priority", "low"), 2))
        
        # Placeholder scores
        scores = {
            "cooling_score": 45,
            "sustainability_score": 55,
            "energy_savings_score": 50,
            "potential_cooling_score": 78,
        }
        
        return {
            "status": "success",
            "location": location or room_features.location,
            "current_temperature": room_features.current_temperature,
            "room_features": room_data,
            "recommendations": combined[:15],
            "scores": scores,
            "message": "Full analysis complete"
        }
    
    except Exception as e:
        print(f"❌ Error in analyze: {str(e)}")
        return {
            "status": "error",
            "message": str(e)
        }


@router.post("/score")
async def calculate_score(room_features: RoomFeatures):
    """Calculate scores (placeholder - Member 3)"""
    
    try:
        return {
            "status": "success",
            "current_scores": {
                "cooling_score": 45,
                "sustainability_score": 55,
                "energy_savings_score": 50
            },
            "potential_scores": {
                "cooling_score": 78,
                "sustainability_score": 85,
                "energy_savings_score": 82
            }
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/history")
async def get_history(user_id: str):
    """Get user history (placeholder - Member 3)"""
    try:
        return {
            "status": "success",
            "user_id": user_id,
            "analyses": []
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.post("/save-analysis")
async def save_analysis(
    user_id: str,
    room_features: RoomFeatures,
    analysis_id: Optional[str] = None
):
    """Save analysis (placeholder - Member 3)"""
    try:
        return {
            "status": "saved",
            "user_id": user_id,
            "analysis_id": analysis_id or "auto_generated"
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}