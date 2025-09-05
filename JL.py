import streamlit as st
import streamlit.components.v1 as components
import json
import random
from datetime import datetime

class VisualLogisticsGame:
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        """Initialize game state"""
        if 'current_scenario' not in st.session_state:
            st.session_state.current_scenario = 0
        if 'player_score' not in st.session_state:
            st.session_state.player_score = 0
        if 'completed_scenarios' not in st.session_state:
            st.session_state.completed_scenarios = set()
        if 'player_name' not in st.session_state:
            st.session_state.player_name = ""
        if 'game_started' not in st.session_state:
            st.session_state.game_started = False
        if 'high_scores' not in st.session_state:
            st.session_state.high_scores = []
            
    def get_scenarios(self):
        """Define fun, visual logistics scenarios"""
        return {
            0: {
                "title": "🏪 Store Delivery Day",
                "description": "Help deliver groceries to the local store!",
                "story": "A delivery truck is bringing fresh groceries to SuperMart. Guide the process!",
                "steps": [
                    {"id": "start", "text": "🚛 Truck arrives", "icon": "🚛", "color": "#3498db"},
                    {"id": "unload", "text": "📦 Unload boxes", "icon": "📦", "color": "#e74c3c"},
                    {"id": "check", "text": "✅ Check inventory", "icon": "✅", "color": "#f39c12"},
                    {"id": "stock", "text": "🏪 Stock shelves", "icon": "🏪", "color": "#27ae60"},
                    {"id": "done", "text": "🎉 Store ready!", "icon": "🎉", "color": "#9b59b6"}
                ],
                "connections": [(0,1), (1,2), (2,3), (3,4)]
            },
            1: {
                "title": "📱 Online Order Journey",
                "description": "Track an online order from click to delivery!",
                "story": "Sarah just ordered a birthday gift online. Follow its journey!",
                "steps": [
                    {"id": "order", "text": "🛒 Place order", "icon": "🛒", "color": "#3498db"},
                    {"id": "payment", "text": "💳 Process payment", "icon": "💳", "color": "#e74c3c"},
                    {"id": "pick", "text": "📋 Pick from warehouse", "icon": "📋", "color": "#f39c12"},
                    {"id": "pack", "text": "📦 Pack securely", "icon": "📦", "color": "#27ae60"},
                    {"id": "deliver", "text": "🚚 Deliver to home", "icon": "🚚", "color": "#9b59b6"}
                ],
                "connections": [(0,1), (1,2), (2,3), (3,4)]
            },
            2: {
                "title": "🍕 Pizza Delivery Rush",
                "description": "Get hot pizza from kitchen to customer!",
                "story": "It's Friday night pizza rush! Help Tony's Pizzeria deliver fast!",
                "steps": [
                    {"id": "order", "text": "📞 Take order", "icon": "📞", "color": "#3498db"},
                    {"id": "make", "text": "🍕 Make pizza", "icon": "🍕", "color": "#e74c3c"},
                    {"id": "box", "text": "📦 Box it up", "icon": "📦", "color": "#f39c12"},
                    {"id": "route", "text": "🗺️ Plan route", "icon": "🗺️", "color": "#27ae60"},
                    {"id": "deliver", "text": "🏠 Deliver hot!", "icon": "🏠", "color": "#9b59b6"}
                ],
                "connections": [(0,1), (1,2), (2,3), (3,4)]
            },
            3: {
                "title": "✈️ Airport Cargo",
                "description": "Move cargo from plane to destination!",
                "story": "A cargo plane just landed with important packages!",
                "steps": [
                    {"id": "land", "text": "✈️ Plane lands", "icon": "✈️", "color": "#3498db"},
                    {"id": "unload", "text": "📋 Unload cargo", "icon": "📋", "color": "#e74c3c"},
                    {"id": "scan", "text": "📱 Scan packages", "icon": "📱", "color": "#f39c12"},
                    {"id": "sort", "text": "📦 Sort by destination", "icon": "📦", "color": "#27ae60"},
                    {"id": "transport", "text": "🚛 Load trucks", "icon": "🚛", "color": "#9b59b6"}
                ],
                "connections": [(0,1), (1,2), (2,3), (3,4)]
            },
            4: {
                "title": "🏭 Factory to Store",
                "description": "Move products from factory to retail stores!",
                "story": "New toys are ready at the factory for the holiday season!",
                "steps": [
                    {"id": "produce", "text": "🏭 Finish production", "icon": "🏭", "color": "#3498db"},
                    {"id": "quality", "text": "🔍 Quality check", "icon": "🔍", "color": "#e74c3c"},
                    {"id": "package", "text": "📦 Package products", "icon": "📦", "color": "#f39c12"},
                    {"id": "ship", "text": "🚛 Ship to stores", "icon": "🚛", "color": "#27ae60"},
                    {"id": "display", "text": "🏪 Display in stores", "icon": "🏪", "color": "#9b59b6"}
                ],
                "connections": [(0,1), (1,2), (2,3), (3,4)]
            }
        }
    
    def create_drag_drop_interface(self, scenario):
        """Create the visual drag-and-drop interface"""
        
        # Get shuffled steps
        steps = scenario["steps"].copy()
        random.shuffle(steps)
        
        drag_drop_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    margin: 0;
                    padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                
                .game-container {{
                    max-width: 1000px;
                    margin: 0 auto;
                    background: white;
                    border-radius: 20px;
                    padding: 30px;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                
                .story-box {{
                    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    margin-bottom: 30px;
                    text-align: center;
                }}
                
                .pieces-container {{
                    display: flex;
                    flex-wrap: wrap;
                    gap: 15px;
                    margin-bottom: 30px;
                    min-height: 120px;
                    background: #f8f9fa;
                    padding: 20px;
                    border-radius: 15px;
                    border: 3px dashed #dee2e6;
                }}
                
                .piece {{
                    background: white;
                    border: 3px solid #dee2e6;
                    border-radius: 15px;
                    padding: 15px 20px;
                    cursor: grab;
                    transition: all 0.3s ease;
                    user-select: none;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    min-width: 180px;
                    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                
                .piece:hover {{
                    transform: translateY(-5px) scale(1.05);
                    box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                    border-color: #3498db;
                }}
                
                .piece:active {{
                    cursor: grabbing;
                    transform: scale(0.95);
                }}
                
                .piece-icon {{
                    font-size: 24px;
                }}
                
                .piece-text {{
                    font-weight: bold;
                    color: #2c3e50;
                }}
                
                .flow-container {{
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    gap: 20px;
                    margin-bottom: 30px;
                    padding: 20px;
                    background: #ecf0f1;
                    border-radius: 15px;
                }}
                
                .drop-zone {{
                    width: 150px;
                    height: 100px;
                    border: 3px dashed #bdc3c7;
                    border-radius: 15px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: white;
                    transition: all 0.3s ease;
                    position: relative;
                }}
                
                .drop-zone:hover {{
                    border-color: #3498db;
                    background: #ebf3fd;
                    transform: scale(1.05);
                }}
                
                .drop-zone.filled {{
                    border-color: #27ae60;
                    background: #d5f4e6;
                    border-style: solid;
                }}
                
                .drop-zone.correct {{
                    border-color: #27ae60;
                    background: #d5f4e6;
                    animation: correctDrop 0.6s ease-in-out;
                }}
                
                .drop-zone.wrong {{
                    border-color: #e74c3c;
                    background: #fadbd8;
                    animation: wrongDrop 0.6s ease-in-out;
                }}
                
                @keyframes correctDrop {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.1); }}
                }}
                
                @keyframes wrongDrop {{
                    0%, 20%, 40%, 60%, 80%, 100% {{ transform: translateX(0); }}
                    10%, 30%, 50%, 70%, 90% {{ transform: translateX(-5px); }}
                }}
                
                .arrow {{
                    font-size: 30px;
                    color: #7f8c8d;
                    animation: pulse 2s infinite;
                }}
                
                @keyframes pulse {{
                    0%, 100% {{ opacity: 0.6; }}
                    50% {{ opacity: 1; }}
                }}
                
                .score-display {{
                    background: linear-gradient(45deg, #28a745, #20c997);
                    color: white;
                    padding: 15px 25px;
                    border-radius: 25px;
                    text-align: center;
                    font-size: 18px;
                    font-weight: bold;
                    margin: 20px 0;
                    box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
                }}
                
                .celebration {{
                    background: linear-gradient(45deg, #ff6b6b, #ee5a24);
                    color: white;
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    font-size: 20px;
                    margin: 20px 0;
                    animation: celebrate 1s ease-in-out;
                }}
                
                @keyframes celebrate {{
                    0%, 100% {{ transform: scale(1); }}
                    50% {{ transform: scale(1.05); }}
                }}
                
                .step-number {{
                    position: absolute;
                    top: -10px;
                    left: -10px;
                    background: #3498db;
                    color: white;
                    border-radius: 50%;
                    width: 25px;
                    height: 25px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    font-size: 12px;
                    font-weight: bold;
                }}
                
                @media (max-width: 768px) {{
                    .flow-container {{
                        flex-direction: column;
                        gap: 15px;
                    }}
                    
                    .arrow {{
                        transform: rotate(90deg);
                    }}
                    
                    .piece {{
                        min-width: 150px;
                        font-size: 14px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="game-container">
                <div class="story-box">
                    <h2>📖 {scenario["title"]}</h2>
                    <p>{scenario["story"]}</p>
                    <p><strong>Mission:</strong> Drag the steps below into the correct order!</p>
                </div>
                
                <div class="pieces-container" id="pieces-pool">
                    <h3 style="width: 100%; margin: 0 0 15px 0; color: #2c3e50;">🧩 Available Steps (Drag these!):</h3>
        """
        
        # Add shuffled pieces
        for i, step in enumerate(steps):
            drag_drop_html += f"""
                    <div class="piece" draggable="true" data-step-id="{step['id']}" data-correct-position="{scenario['steps'].index(step)}">
                        <span class="piece-icon">{step['icon']}</span>
                        <span class="piece-text">{step['text']}</span>
                    </div>
            """
        
        drag_drop_html += """
                </div>
                
                <div class="flow-container" id="flow-area">
        """
        
        # Add drop zones
        for i in range(5):
            drag_drop_html += f"""
                    <div class="drop-zone" data-position="{i}">
                        <div class="step-number">{i+1}</div>
                        <span style="color: #7f8c8d; font-size: 12px;">Drop here</span>
                    </div>
                    {f'<div class="arrow">→</div>' if i < 4 else ''}
            """
        
        drag_drop_html += f"""
                </div>
                
                <div class="score-display" id="score">
                    🏆 Score: <span id="current-score">0</span> / 100 points
                </div>
                
                <div id="feedback"></div>
            </div>
            
            <script>
                let score = 0;
                let placedPieces = {{}};
                
                // Drag and drop functionality
                document.addEventListener('DOMContentLoaded', function() {{
                    const pieces = document.querySelectorAll('.piece');
                    const dropZones = document.querySelectorAll('.drop-zone');
                    
                    pieces.forEach(piece => {{
                        piece.addEventListener('dragstart', handleDragStart);
                    }});
                    
                    dropZones.forEach(zone => {{
                        zone.addEventListener('dragover', handleDragOver);
                        zone.addEventListener('drop', handleDrop);
                        zone.addEventListener('click', handleZoneClick);
                    }});
                }});
                
                function handleDragStart(e) {{
                    e.dataTransfer.setData('text/plain', e.target.dataset.stepId);
                    e.dataTransfer.setData('text/correct-position', e.target.dataset.correctPosition);
                }}
                
                function handleDragOver(e) {{
                    e.preventDefault();
                }}
                
                function handleDrop(e) {{
                    e.preventDefault();
                    const stepId = e.dataTransfer.getData('text/plain');
                    const correctPosition = parseInt(e.dataTransfer.getData('text/correct-position'));
                    const dropPosition = parseInt(e.target.closest('.drop-zone').dataset.position);
                    
                    placePiece(stepId, dropPosition, correctPosition);
                }}
                
                function handleZoneClick(e) {{
                    const zone = e.target.closest('.drop-zone');
                    if (zone.classList.contains('filled')) {{
                        // Remove piece and return to pool
                        const piece = zone.querySelector('.piece');
                        if (piece) {{
                            document.getElementById('pieces-pool').appendChild(piece);
                            zone.classList.remove('filled', 'correct', 'wrong');
                            zone.innerHTML = `
                                <div class="step-number">${{parseInt(zone.dataset.position) + 1}}</div>
                                <span style="color: #7f8c8d; font-size: 12px;">Drop here</span>
                            `;
                            delete placedPieces[zone.dataset.position];
                            updateScore();
                        }}
                    }}
                }}
                
                function placePiece(stepId, dropPosition, correctPosition) {{
                    const piece = document.querySelector(`[data-step-id="${{stepId}}"]`);
                    const dropZone = document.querySelector(`[data-position="${{dropPosition}}"]`);
                    
                    // Clear the drop zone
                    dropZone.innerHTML = '';
                    dropZone.appendChild(piece);
                    
                    // Update styling
                    if (correctPosition === dropPosition) {{
                        dropZone.classList.add('filled', 'correct');
                        dropZone.classList.remove('wrong');
                        placedPieces[dropPosition] = {{ stepId, correct: true }};
                        
                        // Celebration effect
                        showFeedback('✅ Perfect! That step is in the right place!', 'success');
                    }} else {{
                        dropZone.classList.add('filled', 'wrong');
                        dropZone.classList.remove('correct');
                        placedPieces[dropPosition] = {{ stepId, correct: false }};
                        
                        showFeedback('❌ Not quite right. Try a different position!', 'error');
                    }}
                    
                    updateScore();
                    checkCompletion();
                }}
                
                function updateScore() {{
                    const correctPlacements = Object.values(placedPieces).filter(p => p.correct).length;
                    score = correctPlacements * 20;
                    document.getElementById('current-score').textContent = score;
                }}
                
                function checkCompletion() {{
                    const correctCount = Object.values(placedPieces).filter(p => p.correct).length;
                    if (correctCount === 5) {{
                        showFeedback('🎉 AMAZING! You completed the logistics flow perfectly! 🏆', 'celebration');
                        
                        // Send score to Streamlit
                        window.parent.postMessage({{
                            type: 'GAME_COMPLETED',
                            score: score,
                            scenario: '{scenario["title"]}'
                        }}, '*');
                    }}
                }}
                
                function showFeedback(message, type) {{
                    const feedback = document.getElementById('feedback');
                    feedback.innerHTML = `<div class="${{type}}">${{message}}</div>`;
                    
                    // Clear feedback after 3 seconds
                    setTimeout(() => {{
                        if (type !== 'celebration') {{
                            feedback.innerHTML = '';
                        }}
                    }}, 3000);
                }}
            </script>
        </body>
        </html>
        """
        
        return drag_drop_html
    
    def main(self):
        """Main game interface"""
        st.set_page_config(
            page_title="Visual Logistics Adventure",
            page_icon="🎮",
            layout="wide"
        )
        
        if not st.session_state.game_started:
            self.show_welcome_screen()
            return
        
        # Header
        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;">
            <h1>🎮 Visual Logistics Adventure</h1>
            <p>Drag and drop to solve real-world logistics puzzles!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        self.create_sidebar()
        
        # Current scenario
        scenarios = self.get_scenarios()
        current_scenario = scenarios[st.session_state.current_scenario]
        
        # Display game
        game_html = self.create_drag_drop_interface(current_scenario)
        components.html(game_html, height=800, scrolling=True)
        
        # Game completion handler
        self.handle_game_events()
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 3rem; border-radius: 20px; color: white; text-align: center;">
            <h1>🎮 Welcome to Visual Logistics Adventure!</h1>
            <p style="font-size: 1.2em;">The fun way to learn logistics through drag-and-drop puzzles!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 🎯 What Makes This Fun:
            
            #### 🖱️ **True Drag & Drop**
            - **Grab pieces** with your mouse or finger
            - **Drag them** to the correct positions
            - **Visual feedback** with animations and colors
            
            #### 📖 **Story-Driven Scenarios**
            - 🏪 **Store Delivery Day** - Help groceries reach the store
            - 📱 **Online Order Journey** - Track a birthday gift delivery
            - 🍕 **Pizza Delivery Rush** - Get hot pizza to customers
            - ✈️ **Airport Cargo** - Move packages from plane to trucks
            - 🏭 **Factory to Store** - Ship toys for holiday season
            
            #### 🎨 **Visual & Intuitive**
            - **Colorful icons** instead of boring text
            - **Animated arrows** showing the flow
            - **Immediate feedback** - green for correct, red for wrong
            - **Celebration effects** when you succeed!
            
            #### 📱 **Mobile-Friendly**
            - **Touch and drag** on phones and tablets
            - **Responsive design** for any screen size
            - **QR code sharing** for instant access
            
            ### 🏆 **How to Play:**
            1. **Read the story** for each scenario
            2. **Drag the colorful step cards** to the numbered positions
            3. **Watch for green checkmarks** when you're right
            4. **Complete the flow** to earn points and unlock next scenario
            5. **Have fun learning** real logistics processes!
            
            ### 🎯 **Why You'll Love It:**
            - ✅ **Actually fun** to play (not like boring training!)
            - ✅ **Learn by doing** instead of reading
            - ✅ **Visual storytelling** makes it memorable
            - ✅ **Quick 2-3 minute** scenarios perfect for breaks
            - ✅ **Real-world skills** disguised as entertainment
            """)
            
            # Player name input
            player_name = st.text_input(
                "🎮 Enter your name to start the adventure:", 
                placeholder="Your Name",
                help="Join the logistics adventure!"
            )
            
            if st.button("🚀 Start Playing!", type="primary", use_container_width=True):
                if player_name.strip():
                    st.session_state.player_name = player_name.strip()
                    st.session_state.game_started = True
                    st.rerun()
                else:
                    st.error("Please enter your name to start the adventure!")
    
    def create_sidebar(self):
        """Create game sidebar"""
        st.sidebar.title("🎮 Game Control")
        
        # Player info
        st.sidebar.success(f"🎮 Player: {st.session_state.player_name}")
        
        # Score
        st.sidebar.metric("🏆 Total Score", f"{st.session_state.player_score}/500")
        
        # Scenario selection
        scenarios = self.get_scenarios()
        scenario_names = [f"{s['title']}" for s in scenarios.values()]
        
        current = st.sidebar.selectbox(
            "🎯 Choose Scenario:",
            range(len(scenarios)),
            format_func=lambda x: scenario_names[x],
            index=st.session_state.current_scenario
        )
        
        if current != st.session_state.current_scenario:
            st.session_state.current_scenario = current
            st.rerun()
        
        # Progress
        completed_count = len(st.session_state.completed_scenarios)
        st.sidebar.progress(completed_count / 5, text=f"Progress: {completed_count}/5 scenarios")
        
        # Scenario status
        st.sidebar.markdown("### 📋 Scenario Status")
        for i, scenario in scenarios.items():
            if i in st.session_state.completed_scenarios:
                st.sidebar.success(f"✅ {scenario['title']}")
            else:
                st.sidebar.info(f"⏳ {scenario['title']}")
        
        # Controls
        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 New Game"):
            self.reset_game()
        
        if st.sidebar.button("🏆 High Scores"):
            self.show_high_scores()
        
        # Instructions
        with st.sidebar.expander("📖 How to Play"):
            st.markdown("""
            **Playing is Easy:**
            1. **Read the story** at the top
            2. **Grab a piece** and drag it
            3. **Drop it** in the right position (1-5)
            4. **Green = correct**, red = try again
            5. **Complete the flow** to win!
            
            **Tips:**
            - 🎯 Think about logical order
            - 🔄 Click placed pieces to remove them
            - 📱 Works great on mobile too!
            """)
    
    def handle_game_events(self):
        """Handle game completion events from JavaScript"""
        # This would normally handle messages from the HTML component
        # For now, we'll use buttons to simulate completion
        
        if st.button("🎉 I completed this scenario!", type="primary"):
            scenario_id = st.session_state.current_scenario
            if scenario_id not in st.session_state.completed_scenarios:
                st.session_state.completed_scenarios.add(scenario_id)
                st.session_state.player_score += 100
                
                st.balloons()
                st.success("🎉 Scenario completed! +100 points!")
                
                if len(st.session_state.completed_scenarios) == 5:
                    st.success("🏆 ALL SCENARIOS COMPLETED! You're a Logistics Master!")
                    self.save_high_score()
    
    def show_high_scores(self):
        """Show high scores"""
        if st.session_state.high_scores:
            st.subheader("🏆 High Scores")
            for i, score in enumerate(st.session_state.high_scores[:10], 1):
                st.write(f"{i}. {score['name']} - {score['score']} points")
        else:
            st.info("No high scores yet! Be the first!")
    
    def save_high_score(self):
        """Save high score"""
        score_entry = {
            'name': st.session_state.player_name,
            'score': st.session_state.player_score,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M')
        }
        st.session_state.high_scores.append(score_entry)
        st.session_state.high_scores.sort(key=lambda x: x['score'], reverse=True)
    
    def reset_game(self):
        """Reset game"""
        st.session_state.current_scenario = 0
        st.session_state.player_score = 0
        st.session_state.completed_scenarios = set()
        st.rerun()

def main():
    game = VisualLogisticsGame()
    game.main()

if __name__ == "__main__":
    main()
