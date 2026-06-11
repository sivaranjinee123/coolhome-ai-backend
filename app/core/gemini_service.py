"""
GEMINI SERVICE - ULTRA DETAILED DEBUGGING
Shows EVERYTHING that happens
"""

import os
import json
from typing import List
import requests
from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    """Service to interact with Google Gemini API - WITH DEBUGGING"""
    
    def __init__(self):
        """Initialize Gemini service"""
        
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        print("\n" + "="*70)
        print("🔧 GEMINI SERVICE INITIALIZATION")
        print("="*70)
        
        if not self.api_key:
            print("❌ ERROR: GEMINI_API_KEY not found in .env")
            print("   FIX: Add this line to .env:")
            print("   GEMINI_API_KEY=your_actual_key_here")
            self.available = False
        else:
            print(f"✅ API Key loaded")
            print(f"   Length: {len(self.api_key)} characters")
            print(f"   Format: {self.api_key[:30]}...")
            self.available = True
        
        print(f"✅ API URL: {self.api_url}")
        print("="*70 + "\n")
    
    def generate_ai_recommendations(self, room_features: dict) -> List[dict]:
        """Generate recommendations - WITH DEBUGGING"""
        
        if not self.available:
            print("❌ Gemini not available - check .env file")
            return []
        
        try:
            print("\n" + "="*70)
            print("🤖 CALLING GEMINI API - DETAILED DEBUG")
            print("="*70)
            
            # ============================================================
            # STEP 1: CREATE PROMPT
            # ============================================================
            print("\n📝 STEP 1: CREATE PROMPT")
            print("-" * 70)
            
            prompt = self._create_prompt(room_features)
            print(f"✅ Prompt created")
            print(f"   Length: {len(prompt)} characters")
            print(f"   First 100 chars: {prompt[:100]}...")
            
            # ============================================================
            # STEP 2: PREPARE REQUEST
            # ============================================================
            print("\n📤 STEP 2: PREPARE REQUEST")
            print("-" * 70)
            
            headers = {"Content-Type": "application/json"}
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            }
                        ]
                    }
                ]
            }
            
            print(f"✅ Headers: {headers}")
            print(f"✅ Payload keys: {list(payload.keys())}")
            print(f"✅ API Endpoint: {self.api_url}")
            print(f"✅ Full URL: {self.api_url}?key={self.api_key[:20]}...")
            
            # ============================================================
            # STEP 3: SEND REQUEST
            # ============================================================
            print("\n🌐 STEP 3: SEND REQUEST TO GEMINI")
            print("-" * 70)
            
            print("📤 Sending POST request...")
            response = requests.post(
                f"{self.api_url}?key={self.api_key}",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            print(f"✅ Response received")
            print(f"   HTTP Status: {response.status_code}")
            print(f"   Response Time: ~5 seconds")
            print(f"   Response Size: {len(response.text)} bytes")
            
            # ============================================================
            # STEP 4: CHECK STATUS
            # ============================================================
            print("\n🔍 STEP 4: CHECK RESPONSE STATUS")
            print("-" * 70)
            
            if response.status_code != 200:
                print(f"❌ ERROR: HTTP {response.status_code}")
                print(f"   Response text (first 500 chars):")
                print(f"   {response.text[:500]}")
                
                # Try to parse error
                try:
                    error_json = response.json()
                    print(f"   Parsed error: {json.dumps(error_json, indent=2)}")
                except:
                    print(f"   (Could not parse as JSON)")
                
                return []
            
            print(f"✅ HTTP Status 200 - Success!")
            
            # ============================================================
            # STEP 5: PARSE JSON RESPONSE
            # ============================================================
            print("\n📥 STEP 5: PARSE RESPONSE JSON")
            print("-" * 70)
            
            try:
                response_data = response.json()
                print(f"✅ Response is valid JSON")
                print(f"   Keys: {list(response_data.keys())}")
            except json.JSONDecodeError as e:
                print(f"❌ ERROR: Invalid JSON in response")
                print(f"   Error: {str(e)}")
                print(f"   Response (first 300 chars): {response.text[:300]}")
                return []
            
            # ============================================================
            # STEP 6: NAVIGATE RESPONSE STRUCTURE
            # ============================================================
            print("\n🗂️ STEP 6: NAVIGATE RESPONSE STRUCTURE")
            print("-" * 70)
            
            if "candidates" not in response_data:
                print(f"❌ ERROR: No 'candidates' key in response")
                print(f"   Available keys: {list(response_data.keys())}")
                return []
            
            print(f"✅ Found 'candidates' key")
            
            candidates = response_data["candidates"]
            print(f"   Candidates count: {len(candidates)}")
            
            if len(candidates) == 0:
                print(f"❌ ERROR: Candidates list is empty")
                return []
            
            candidate = candidates[0]
            print(f"✅ Got first candidate")
            print(f"   Keys: {list(candidate.keys())}")
            
            if "content" not in candidate:
                print(f"❌ ERROR: No 'content' in candidate")
                return []
            
            content = candidate["content"]
            print(f"✅ Got content")
            print(f"   Keys: {list(content.keys())}")
            
            if "parts" not in content:
                print(f"❌ ERROR: No 'parts' in content")
                return []
            
            parts = content["parts"]
            print(f"✅ Got parts")
            print(f"   Parts count: {len(parts)}")
            
            if len(parts) == 0:
                print(f"❌ ERROR: Parts list is empty")
                return []
            
            part = parts[0]
            print(f"✅ Got first part")
            print(f"   Keys: {list(part.keys())}")
            
            if "text" not in part:
                print(f"❌ ERROR: No 'text' in part")
                print(f"   Available keys: {list(part.keys())}")
                return []
            
            text = part["text"]
            print(f"✅ Got text from response")
            print(f"   Text length: {len(text)} characters")
            print(f"   First 150 chars: {text[:150]}...")
            
            # ============================================================
            # STEP 7: PARSE RESPONSE
            # ============================================================
            print("\n🔄 STEP 7: PARSE RECOMMENDATIONS")
            print("-" * 70)
            
            recommendations = self._parse_response(text)
            
            print(f"✅ Successfully parsed {len(recommendations)} recommendations")
            print("="*70 + "\n")
            
            return recommendations
        
        except Exception as e:
            print(f"\n❌ UNEXPECTED ERROR:")
            print(f"   Type: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            print(f"   Full traceback:")
            import traceback
            traceback.print_exc()
            print("="*70 + "\n")
            return []
    
    def _create_prompt(self, room_features: dict) -> str:
        """Create detailed prompt for Gemini"""
        
        prompt = f"""You are an expert in passive cooling for Indian homes.

Room characteristics:
- Windows: {room_features.get('windows', 'unknown')}
- Ventilation: {room_features.get('ventilation', 'unknown')}
- Sunlight: {room_features.get('sunlight', 'unknown')}
- Window direction: {room_features.get('window_direction', 'unknown')}
- Indoor plants: {room_features.get('indoor_plants', 'no')}
- Furniture density: {room_features.get('furniture_density', 'unknown')}
- Airflow obstruction: {room_features.get('airflow_obstruction', 'unknown')}

Provide exactly 5 cooling recommendations as JSON array.

Each must have: category, action, expected_impact, cost, implementation_difficulty

Return ONLY valid JSON, no other text:
[
  {{
    "category": "string",
    "action": "string",
    "expected_impact": "string",
    "cost": "string",
    "implementation_difficulty": "string"
  }}
]"""
        
        return prompt
    
    def _parse_response(self, response_text: str) -> List[dict]:
        """Parse Gemini's response - WITH DEBUGGING"""
        
        print("   Cleaning response text...")
        
        if not response_text:
            print("   ❌ Empty response text")
            return []
        
        try:
            text = response_text
            
            # Remove markdown
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
                print("   ✅ Removed ```json markers")
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]
                print("   ✅ Removed ``` markers")
            
            text = text.strip()
            
            print(f"   Cleaned text: {text[:100]}...")
            
            # Parse JSON
            print("   Parsing JSON...")
            recommendations = json.loads(text)
            
            print(f"   ✅ Valid JSON parsed")
            print(f"   Type: {type(recommendations)}")
            
            if not isinstance(recommendations, list):
                print(f"   ❌ Not a list, it's {type(recommendations)}")
                return []
            
            print(f"   Array length: {len(recommendations)}")
            
            # Validate
            print("   Validating recommendations...")
            validated = []
            for i, rec in enumerate(recommendations):
                print(f"     Rec {i}: {list(rec.keys())}")
                required = ["category", "action", "expected_impact"]
                missing = [f for f in required if f not in rec]
                
                if missing:
                    print(f"     ❌ Missing: {missing}")
                    continue
                
                rec["source"] = "gemini"
                validated.append(rec)
                print(f"     ✅ Valid")
            
            print(f"   ✅ Validated {len(validated)} recommendations")
            return validated
        
        except json.JSONDecodeError as e:
            print(f"   ❌ JSON Parse Error: {str(e)}")
            print(f"   Response (first 300 chars): {response_text[:300]}")
            return []
        except Exception as e:
            print(f"   ❌ Error: {type(e).__name__}: {str(e)}")
            return []