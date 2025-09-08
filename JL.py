import streamlit as st
import streamlit.components.v1 as components
import json
import random
from datetime import datetime

class VisualLogisticsGame:
    def __init__(self):
        self.init_session_state()

    def init_session_state(self):
        """Initialize game state for a single scenario."""
        if 'player_score' not in st.session_state:
            st.session_state.player_score = 0
        if 'scenario_completed' not in st.session_state:
            st.session_state.scenario_completed = False
        if 'player_name' not in st.session_state:
            st.session_state.player_name = ""
        if 'game_started' not in st.session_state:
            st.session_state.game_started = False
        if 'high_scores' not in st.session_state:
            st.session_state.high_scores = []

    def get_scenario(self):
        """Define the single, detailed industry-level logistics scenario."""
        return {
            "title": "📱 Global Gadget Supply Chain",
            "description": "Orchestrate a new smartphone's journey from raw materials to a customer's hands!",
            "story": "A new cutting-edge smartphone, the 'Innova X', is launching. Your mission is to correctly sequence its complex international supply chain process.",
            "steps": [
                {"id": "sourcing", "text": "⛏️ Raw Material Sourcing", "icon": "⛏️", "color": "#1abc9c"},
                {"id": "component", "text": "⚙️ Component Manufacturing", "icon": "⚙️", "color": "#3498db"},
                {"id": "assembly", "text": "🏭 Final Assembly", "icon": "🏭", "color": "#9b59b6"},
                {"id": "quality", "text": "🔍 Quality Control & Packaging", "icon": "🔍", "color": "#e67e22"},
                {"id": "freight", "text": "🚢 Global Freight Shipping", "icon": "🚢", "color": "#e74c3c"},
                {"id": "customs", "text": "🛂 Customs Clearance", "icon": "🛂", "color": "#f1c40f"},
                {"id": "distribution", "text": "🚚 Regional Distribution Center", "icon": "🚚", "color": "#2ecc71"},
                {"id": "retail", "text": "🏪 Retail Store Stocking", "icon": "🏪", "color": "#34495e"}
            ],
            "connections": [(i, i+1) for i in range(7)] # Dynamic connections
        }

    def create_drag_drop_interface(self, scenario):
        """Create the visual drag-and-drop interface."""
        # Get shuffled steps for the puzzle
        steps = scenario["steps"].copy()
        random.shuffle(steps)
        num_steps = len(scenario["steps"])

        drag_drop_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif; margin: 0; padding: 20px;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh;
                }}
                .game-container {{
                    max-width: 1200px; margin: 0 auto; background: white;
                    border-radius: 20px; padding: 30px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                }}
                .story-box {{
                    background: linear-gradient(45deg, #ff6b6b, #ee5a24); color: white;
                    padding: 20px; border-radius: 15px; margin-bottom: 30px; text-align: center;
                }}
                .pieces-container {{
                    display: flex; flex-wrap: wrap; gap: 15px; margin-bottom: 30px;
                    min-height: 120px; background: #f8f9fa; padding: 20px;
                    border-radius: 15px; border: 3px dashed #dee2e6;
                }}
                .piece {{
                    background: white; border: 3px solid #dee2e6; border-radius: 15px;
                    padding: 15px 20px; cursor: grab; transition: all 0.3s ease;
                    user-select: none; display: flex; align-items: center; gap: 10px;
                    min-width: 200px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                }}
                .piece:hover {{
                    transform: translateY(-5px) scale(1.05); box-shadow: 0 8px 25px rgba(0,0,0,0.2);
                    border-color: #3498db;
                }}
                .piece:active {{ cursor: grabbing; transform: scale(0.95); }}
                .piece-icon {{ font-size: 24px; }}
                .piece-text {{ font-weight: bold; color: #2c3e50; }}
                .flow-container {{
                    display: flex; flex-wrap: wrap; justify-content: center; align-items: center; gap: 10px;
                    margin-bottom: 30px; padding: 20px; background: #ecf0f1; border-radius: 15px;
                }}
                .drop-zone {{
                    width: 180px; height: 100px; border: 3px dashed #bdc3c7; border-radius: 15px;
                    display: flex; align-items: center; justify-content: center;
                    background: white; transition: all 0.3s ease; position: relative;
                }}
                .drop-zone:hover {{
                    border-color: #3498db; background: #ebf3fd; transform: scale(1.05);
                }}
                .drop-zone.filled {{ border-style: solid; }}
                .drop-zone.correct {{
                    border-color: #27ae60; background: #d5f4e6;
                    animation: correctDrop 0.6s ease-in-out;
                }}
                .drop-zone.wrong {{
                    border-color: #e74c3c; background: #fadbd8;
                    animation: wrongDrop 0.6s ease-in-out;
                }}
                @keyframes correctDrop {{ 0%, 100% {{ transform: scale(1); }} 50% {{ transform: scale(1.1); }} }}
                @keyframes wrongDrop {{
                    0%, 100% {{ transform: translateX(0); }}
                    25%, 75% {{ transform: translateX(-8px); }}
                    50% {{ transform: translateX(8px); }}
                }}
                .arrow {{ font-size: 30px; color: #7f8c8d; animation: pulse 2s infinite; }}
                @keyframes pulse {{ 0%, 100% {{ opacity: 0.6; }} 50% {{ opacity: 1; }} }}
                .score-display, .celebration, .feedback-msg {{
                    color: white; padding: 15px 25px; border-radius: 25px;
                    text-align: center; font-size: 18px; font-weight: bold;
                    margin: 20px 0;
                }}
                .score-display {{ background: linear-gradient(45deg, #28a745, #20c997); }}
                .celebration {{ background: linear-gradient(45deg, #f39c12, #f1c40f); }}
                .feedback-msg.success {{ background: #27ae60; }}
                .feedback-msg.error {{ background: #e74c3c; }}
                .step-number {{
                    position: absolute; top: -10px; left: -10px; background: #3498db;
                    color: white; border-radius: 50%; width: 25px; height: 25px;
                    display: flex; align-items: center; justify-content: center;
                    font-size: 12px; font-weight: bold;
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
                    <h3 style="width: 100%; margin: 0 0 15px 0; color: #2c3e50;">🧩 Available Steps:</h3>
                    {''.join([f"""
                    <div class="piece" draggable="true" data-step-id="{step['id']}" data-correct-position="{scenario['steps'].index(step)}">
                        <span class="piece-icon">{step['icon']}</span>
                        <span class="piece-text">{step['text']}</span>
                    </div>""" for step in steps])}
                </div>
                <div class="flow-container" id="flow-area">
                    {''.join([f"""
                    <div class="drop-zone" data-position="{i}">
                        <div class="step-number">{i+1}</div>
                        <span style="color: #7f8c8d; font-size: 12px;">Drop here</span>
                    </div>
                    {f'<div class="arrow">→</div>' if i < num_steps - 1 else ''}
                    """ for i in range(num_steps)])}
                </div>
                <div class="score-display" id="score">
                    🏆 Score: <span id="current-score">0</span> / 100 points
                </div>
                <div id="feedback"></div>
            </div>
            <script>
                const numSteps = {num_steps};
                let placedPieces = {{}};

                document.addEventListener('DOMContentLoaded', function() {{
                    const pieces = document.querySelectorAll('.piece');
                    const dropZones = document.querySelectorAll('.drop-zone');
                    
                    pieces.forEach(piece => piece.addEventListener('dragstart', e => {{
                        e.dataTransfer.setData('text/plain', e.target.dataset.stepId);
                        e.dataTransfer.setData('text/correct-position', e.target.dataset.correctPosition);
                    }}));
                    
                    dropZones.forEach(zone => {{
                        zone.addEventListener('dragover', e => e.preventDefault());
                        zone.addEventListener('drop', handleDrop);
                        zone.addEventListener('click', handleZoneClick);
                    }});
                }});

                function handleDrop(e) {{
                    e.preventDefault();
                    const stepId = e.dataTransfer.getData('text/plain');
                    const correctPosition = parseInt(e.dataTransfer.getData('text/correct-position'));
                    const dropZone = e.target.closest('.drop-zone');
                    const dropPosition = parseInt(dropZone.dataset.position);
                    
                    if (dropZone.classList.contains('filled')) return; // Prevent dropping on a filled zone

                    placePiece(stepId, dropPosition, correctPosition);
                }}

                function handleZoneClick(e) {{
                    const zone = e.target.closest('.drop-zone');
                    if (!zone.classList.contains('filled')) return;
                    
                    const piece = zone.querySelector('.piece');
                    if (piece) {{
                        document.getElementById('pieces-pool').appendChild(piece);
                        zone.classList.remove('filled', 'correct', 'wrong');
                        zone.innerHTML = `<div class="step-number">${{parseInt(zone.dataset.position) + 1}}</div>
                                          <span style="color: #7f8c8d; font-size: 12px;">Drop here</span>`;
                        delete placedPieces[zone.dataset.position];
                        updateScore();
                    }}
                }}

                function placePiece(stepId, dropPosition, correctPosition) {{
                    const piece = document.querySelector(`[data-step-id="${{stepId}}"]`);
                    const dropZone = document.querySelector(`[data-position="${{dropPosition}}"]`);
                    
                    dropZone.innerHTML = '';
                    dropZone.appendChild(piece);
                    
                    const isCorrect = correctPosition === dropPosition;
                    dropZone.classList.add('filled', isCorrect ? 'correct' : 'wrong');
                    dropZone.classList.remove(isCorrect ? 'wrong' : 'correct');
                    placedPieces[dropPosition] = {{ stepId, correct: isCorrect }};
                    
                    showFeedback(isCorrect ? '✅ Perfect! That step is in the right place!' : '❌ Not quite right. Try a different position!', isCorrect ? 'success' : 'error');
                    
                    updateScore();
                    checkCompletion();
                }}

                function updateScore() {{
                    const correctPlacements = Object.values(placedPieces).filter(p => p.correct).length;
                    const score = Math.round((correctPlacements / numSteps) * 100);
                    document.getElementById('current-score').textContent = score;
                }}

                function checkCompletion() {{
                    const correctCount = Object.values(placedPieces).filter(p => p.correct).length;
                    if (correctCount === numSteps) {{
                        showFeedback('🎉 AMAZING! You completed the supply chain flow perfectly! 🏆', 'celebration');
                        window.parent.postMessage({{ type: 'GAME_COMPLETED', score: 100 }}, '*');
                    }}
                }}

                function showFeedback(message, type) {{
                    const feedback = document.getElementById('feedback');
                    feedback.innerHTML = `<div class="feedback-msg ${{type}}">${{message}}</div>`;
                    if (type !== 'celebration') {{
                        setTimeout(() => {{ feedback.innerHTML = ''; }}, 3000);
                    }}
                }}
            </script>
        </body>
        </html>
        """
        return drag_drop_html

    def main(self):
        """Main game interface."""
        st.set_page_config(page_title="Global Supply Chain Challenge", page_icon="🌐", layout="wide")

        if not st.session_state.game_started:
            self.show_welcome_screen()
            return

        st.markdown("""
        <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                     padding: 2rem; border-radius: 15px; color: white; text-align: center; margin-bottom: 2rem;">
            <h1>🌐 Global Supply Chain Challenge</h1>
            <p>Drag and drop to solve a real-world logistics puzzle!</p>
        </div>
        """, unsafe_allow_html=True)

        self.create_sidebar()

        scenario = self.get_scenario()
        if st.session_state.scenario_completed:
            st.success("🏆 Mission Accomplished! You've successfully mapped the supply chain!")
            st.balloons()
            st.metric("Final Score", "100/100")
            if st.button("🔄 Play Again"):
                self.reset_game()
        else:
            game_html = self.create_drag_drop_interface(scenario)
            # Use streamlit-javascript to handle the callback
            from streamlit_javascript import st_javascript
            result = st_javascript(f"window.addEventListener('message', event => Streamlit.setComponentValue(event.data));", key="game_listener")

            if result and result.get("type") == "GAME_COMPLETED":
                self.handle_game_completion(result.get("score", 0))
            
            components.html(game_html, height=1000, scrolling=True)

    def show_welcome_screen(self):
        """Show the welcome screen."""
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                     padding: 3rem; border-radius: 20px; color: white; text-align: center;">
            <h1>🌐 Welcome to the Global Supply Chain Challenge!</h1>
            <p style="font-size: 1.2em;">The fun way to learn complex logistics through an interactive puzzle!</p>
        </div>
        """, unsafe_allow_html=True)

        _, col2, _ = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            ### 🎯 The Challenge:
            You are the new head of logistics for a global tech company launching the **"Innova X" smartphone**. 
            Your task is to correctly sequence the entire supply chain, from sourcing raw materials in one continent to putting the final product in a customer's hands in another.
            
            #### ✨ **Features:**
            - **🖱️ True Drag & Drop:** Physically move each process step into its correct place.
            - **🏭 Industry-Level Scenario:** Tackle an 8-step process that mirrors real-world operations.
            - **🎨 Visual & Intuitive:** Colorful icons and instant animated feedback guide you.
            - **🏆 Score & Compete:** Earn a perfect score and add your name to the high scores list!
            
            ### 🏆 **How to Play:**
            1.  **Read the mission** to understand the goal.
            2.  **Drag the colorful step cards** from the top pool to the numbered positions.
            3.  **Watch for green checkmarks** for correct placements.
            4.  **Complete the entire flow** to win the challenge!
            """)
            
            player_name = st.text_input("👤 Enter your name to begin:", placeholder="Logistics Champion")
            if st.button("🚀 Start Challenge!", type="primary", use_container_width=True):
                if player_name.strip():
                    st.session_state.player_name = player_name.strip()
                    st.session_state.game_started = True
                    st.rerun()
                else:
                    st.error("Please enter your name to start!")

    def create_sidebar(self):
        """Create the game sidebar."""
        st.sidebar.title("🎮 Game Control")
        st.sidebar.success(f"👤 Player: {st.session_state.player_name}")
        st.sidebar.metric("🏆 Score", f"{st.session_state.player_score}/100")

        st.sidebar.progress(1 if st.session_state.scenario_completed else 0, text="Challenge Progress")

        st.sidebar.markdown("---")
        if st.sidebar.button("🔄 New Game"):
            self.reset_game(full_reset=True)
        
        self.show_high_scores()

        with st.sidebar.expander("📖 How to Play"):
            st.markdown("""
            1.  **Drag a piece** from the top section.
            2.  **Drop it** on a numbered slot.
            3.  **Green** = correct! **Red** = wrong.
            4.  Click a placed piece to return it.
            """)

    def handle_game_completion(self, score):
        """Handle the game completion event from JavaScript."""
        if not st.session_state.scenario_completed:
            st.session_state.player_score = score
            st.session_state.scenario_completed = True
            self.save_high_score()
            st.rerun()

    def show_high_scores(self):
        """Display high scores in the sidebar."""
        st.sidebar.markdown("---")
        st.sidebar.subheader("🏆 High Scores")
        # Load high scores from a more persistent state if desired
        if st.session_state.high_scores:
            for i, score in enumerate(st.session_state.high_scores[:5], 1):
                st.sidebar.write(f"**{i}. {score['name']}** - {score['score']} pts ({score['date']})")
        else:
            st.sidebar.info("No high scores yet. Be the first!")

    def save_high_score(self):
        """Save high score to session state."""
        score_entry = {
            'name': st.session_state.player_name,
            'score': st.session_state.player_score,
            'date': datetime.now().strftime('%Y-%m-%d')
        }
        st.session_state.high_scores.append(score_entry)
        st.session_state.high_scores.sort(key=lambda x: x['score'], reverse=True)

    def reset_game(self, full_reset=False):
        """Reset game state."""
        st.session_state.player_score = 0
        st.session_state.scenario_completed = False
        if full_reset:
            st.session_state.game_started = False
            st.session_state.player_name = ""
        st.rerun()


if __name__ == "__main__":
    # NOTE: You need to install streamlit-javascript for this to work
    # pip install streamlit-javascript
    game = VisualLogisticsGame()
    game.main()
