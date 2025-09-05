import streamlit as st
import random
from datetime import datetime
import pandas as pd
import qrcode
import io
import base64
from PIL import Image, ImageDraw, ImageFont

class LogisticsPuzzleGame:
    def __init__(self):
        self.init_session_state()
        
    def init_session_state(self):
        """Initialize all session state variables"""
        if 'tasks_data' not in st.session_state:
            st.session_state.tasks_data = self.create_logistics_tasks()
        if 'current_task' not in st.session_state:
            st.session_state.current_task = 0
        if 'task_solutions' not in st.session_state:
            st.session_state.task_solutions = {i: [None] * 5 for i in range(5)}
        if 'task_pieces_shuffled' not in st.session_state:
            st.session_state.task_pieces_shuffled = {}
            self.shuffle_current_task_pieces()
        if 'player_score' not in st.session_state:
            st.session_state.player_score = 0
        if 'completed_subtasks' not in st.session_state:
            st.session_state.completed_subtasks = set()
        if 'player_name' not in st.session_state:
            st.session_state.player_name = ""
        if 'game_started' not in st.session_state:
            st.session_state.game_started = False
        if 'high_scores' not in st.session_state:
            st.session_state.high_scores = []
        if 'app_url' not in st.session_state:
            # This will be updated after deployment
            st.session_state.app_url = "https://logisticsgame.streamlit.app"
            
    def create_logistics_tasks(self):
        """Create all logistics tasks and subtasks"""
        return {
            0: {
                "title": "Warehouse Management",
                "icon": "📦",
                "color": "#3498db",
                "description": "Manage warehouse operations efficiently from receiving to reporting",
                "subtasks": [
                    "Receive and inspect incoming inventory shipments",
                    "Sort and categorize items by product type",
                    "Update inventory management database systems",
                    "Assign optimal storage locations in warehouse",
                    "Generate comprehensive inventory status reports"
                ]
            },
            1: {
                "title": "Transportation Planning",
                "icon": "🚛", 
                "color": "#e74c3c",
                "description": "Plan and optimize delivery routes for maximum efficiency",
                "subtasks": [
                    "Analyze customer delivery destinations and requirements",
                    "Calculate optimal route distances and travel times",
                    "Schedule vehicle assignments and driver coordination",
                    "Optimize fuel consumption and delivery efficiency",
                    "Prepare detailed delivery manifests and documentation"
                ]
            },
            2: {
                "title": "Supply Chain Coordination",
                "icon": "🤝",
                "color": "#27ae60",
                "description": "Coordinate relationships with suppliers and vendors",
                "subtasks": [
                    "Contact suppliers to request competitive price quotes",
                    "Negotiate favorable delivery terms and conditions",
                    "Schedule important supplier meetings and reviews",
                    "Monitor and evaluate incoming supply quality standards",
                    "Maintain updated supplier database and contact information"
                ]
            },
            3: {
                "title": "Order Fulfillment",
                "icon": "📋",
                "color": "#f39c12",
                "description": "Process customer orders from receipt to shipment",
                "subtasks": [
                    "Process and validate incoming customer orders",
                    "Verify product availability in current inventory",
                    "Pick required items efficiently from warehouse shelves",
                    "Package orders securely with appropriate materials",
                    "Generate accurate shipping labels and tracking information"
                ]
            },
            4: {
                "title": "Inventory Control",
                "icon": "📊",
                "color": "#9b59b6",
                "description": "Maintain optimal inventory levels and stock control",
                "subtasks": [
                    "Monitor current stock levels across all products",
                    "Identify critically low inventory items requiring attention",
                    "Create and submit new purchase orders to suppliers",
                    "Track supplier delivery schedules and expected arrivals",
                    "Update stock management records and system databases"
                ]
            }
        }
    
    def shuffle_current_task_pieces(self):
        """Shuffle pieces for the current task only"""
        current_task = st.session_state.current_task
        task_data = st.session_state.tasks_data[current_task]
        
        # Create pieces for current task
        pieces = []
        for i, subtask in enumerate(task_data["subtasks"]):
            piece = {
                "id": f"{current_task}_{i}",
                "task_id": current_task,
                "piece_id": i,
                "text": subtask,
                "color": task_data["color"],
                "icon": task_data["icon"]
            }
            pieces.append(piece)
        
        # Shuffle the pieces
        random.shuffle(pieces)
        st.session_state.task_pieces_shuffled[current_task] = pieces
    
    def apply_custom_css(self):
        """Apply custom CSS styling with drag-and-drop effects"""
        st.markdown("""
        <style>
        .main-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 2rem;
            border-radius: 20px;
            color: white;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        }
        
        .task-selector {
            background: #34495e;
            padding: 1rem;
            border-radius: 15px;
            margin: 1rem 0;
            color: white;
            text-align: center;
        }
        
        .puzzle-piece {
            padding: 1rem;
            margin: 0.5rem;
            border-radius: 12px;
            border: 3px solid #bdc3c7;
            cursor: grab;
            transition: all 0.3s ease;
            color: white;
            font-weight: 500;
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            user-select: none;
        }
        
        .puzzle-piece:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            border-color: #f39c12;
        }
        
        .puzzle-piece:active {
            cursor: grabbing;
            transform: scale(0.98);
        }
        
        .piece-correct {
            background: #27ae60 !important;
            border-color: #1e8449 !important;
            animation: correctPlacement 0.5s ease-in-out;
        }
        
        .piece-wrong {
            background: #e74c3c !important;
            border-color: #c0392b !important;
        }
        
        .piece-pool {
            background: #6c757d;
            border-color: #495057;
        }
        
        @keyframes correctPlacement {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
        }
        
        .drop-zone {
            border: 3px dashed #bdc3c7;
            border-radius: 12px;
            min-height: 100px;
            padding: 1rem;
            margin: 0.5rem 0;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #ecf0f1;
            transition: all 0.3s ease;
            position: relative;
        }
        
        .drop-zone:hover {
            border-color: #3498db;
            background: #ebf3fd;
            transform: scale(1.02);
        }
        
        .drop-zone.filled {
            border-style: solid;
            border-color: #27ae60;
            background: #d5f4e6;
        }
        
        .drop-zone.empty {
            border-color: #3498db;
            background: #ebf3fd;
        }
        
        .task-progress {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 10px;
            margin: 1rem 0;
            border-left: 5px solid #3498db;
        }
        
        .score-card {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        .qr-container {
            background: white;
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 1rem 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .pieces-pool {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 15px;
            border: 2px solid #dee2e6;
            min-height: 300px;
        }
        
        .subtask-score {
            background: #28a745;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 20px;
            font-size: 0.8rem;
            position: absolute;
            top: -10px;
            right: -10px;
            animation: scorePopup 0.5s ease-in-out;
        }
        
        @keyframes scorePopup {
            0% { transform: scale(0); opacity: 0; }
            50% { transform: scale(1.2); opacity: 1; }
            100% { transform: scale(1); opacity: 1; }
        }
        
        /* Mobile responsiveness */
        @media (max-width: 768px) {
            .main-header {
                padding: 1rem;
            }
            .main-header h1 {
                font-size: 1.5rem !important;
            }
            .puzzle-piece {
                font-size: 0.85rem;
                padding: 0.8rem;
                min-height: 70px;
            }
            .drop-zone {
                min-height: 80px;
            }
        }
        </style>
        """, unsafe_allow_html=True)
    
    def main(self):
        """Main app interface"""
        st.set_page_config(
            page_title="Logistics Puzzle Challenge v1.0",
            page_icon="🚛",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        self.apply_custom_css()
        
        # Welcome screen for new users
        if not st.session_state.game_started:
            self.show_welcome_screen()
            return
        
        # Header
        st.markdown("""
        <div class="main-header">
            <h1>🚛 Logistics Puzzle Challenge v1.0</h1>
            <p>Master logistics one task at a time! Arrange subtasks in correct order.</p>
            <p><strong>Current Challenge:</strong> Complete each subtask correctly to earn points instantly!</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        self.create_sidebar()
        
        # Task selector
        self.display_task_selector()
        
        # Main content layout
        col1, col2 = st.columns([3, 2])
        
        with col1:
            self.display_current_task_area()
            
        with col2:
            self.display_current_task_pieces()
    
    def show_welcome_screen(self):
        """Show welcome screen"""
        st.markdown("""
        <div class="main-header">
            <h1>🚛 Welcome to Logistics Puzzle Challenge!</h1>
            <p>Master logistics skills through interactive puzzles!</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("""
            ### 🎯 How It Works:
            **Work on ONE task at a time** - no mixing, no confusion!
            
            1. **Select a logistics task** from the 5 available
            2. **See only 5 pieces** for that specific task
            3. **Drag and arrange** them in the correct order
            4. **Get 4 points immediately** for each correct placement
            5. **Complete all tasks** to become a Logistics Master!
            
            ### 📋 5 Logistics Challenges:
            - 📦 **Warehouse Management** - Inventory operations (20 points)
            - 🚛 **Transportation Planning** - Route optimization (20 points)
            - 🤝 **Supply Chain Coordination** - Supplier management (20 points)
            - 📋 **Order Fulfillment** - Customer order processing (20 points)
            - 📊 **Inventory Control** - Stock level management (20 points)
            
            ### 🏆 New Scoring System:
            - ✅ **4 points per correct subtask** (immediate feedback!)
            - ✅ **20 points per completed task**
            - ✅ **100 points maximum total**
            - ✅ **Green pieces** show correct placements
            - ✅ **Instant gratification** - no waiting!
            
            ### 💡 Why This Is Better:
            - 🎯 **Focus on one task** at a time
            - 🔄 **True drag-and-drop** experience
            - ⚡ **Immediate scoring** and feedback
            - 📱 **Mobile-optimized** for touch devices
            - 🎨 **Visual feedback** with color changes
            """)
            
            # Player name input
            player_name = st.text_input(
                "🏷️ Enter your name to start the challenge:", 
                placeholder="Your Name",
                help="This will be used for the high scores leaderboard"
            )
            
            if st.button("🚀 Start the Challenge!", type="primary", use_container_width=True):
                if player_name.strip():
                    st.session_state.player_name = player_name.strip()
                    st.session_state.game_started = True
                    st.rerun()
                else:
                    st.error("Please enter your name to continue!")
    
    def create_sidebar(self):
        """Create sidebar with game info and controls"""
        st.sidebar.title("🎮 Game Dashboard")
        
        # Player info
        st.sidebar.success(f"👤 **Player:** {st.session_state.player_name}")
        
        # Score display
        max_possible = sum(1 for _ in st.session_state.completed_subtasks) * 4
        st.sidebar.markdown(f"""
        <div class="score-card">
            <h2>🏆 {st.session_state.player_score}/100</h2>
            <p>Points Earned</p>
            <small>{len(st.session_state.completed_subtasks)}/25 Subtasks Complete</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Task progress overview
        st.sidebar.markdown("### 📋 Progress Overview")
        tasks = ["📦 Warehouse", "🚛 Transport", "🤝 Supply Chain", "📋 Orders", "📊 Inventory"]
        
        for i, task_name in enumerate(tasks):
            completed_subtasks_count = sum(1 for task_slot in st.session_state.task_solutions[i] 
                                         if task_slot is not None and f"{i}_{task_slot['piece_id']}" in st.session_state.completed_subtasks)
            
            if completed_subtasks_count == 5:
                st.sidebar.success(f"✅ {task_name} (5/5)")
            elif completed_subtasks_count > 0:
                st.sidebar.info(f"🔄 {task_name} ({completed_subtasks_count}/5)")
            else:
                st.sidebar.info(f"⏳ {task_name} (0/5)")
        
        # Overall progress
        total_completed = len(st.session_state.completed_subtasks)
        progress = total_completed / 25
        st.sidebar.progress(progress, text=f"Overall: {int(progress*100)}%")
        
        # Controls
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🛠️ Game Controls")
        
        col1, col2 = st.sidebar.columns(2)
        with col1:
            if st.button("🔄 Shuffle", help="Shuffle current task pieces"):
                self.shuffle_current_task_pieces()
                st.rerun()
        
        with col2:
            if st.button("💡 Hint", help="Get a helpful hint"):
                self.show_hint()
        
        if st.sidebar.button("🏆 High Scores", use_container_width=True):
            self.show_high_scores()
        
        if st.sidebar.button("🆕 New Game", use_container_width=True):
            self.reset_game()
        
        # QR Code generation
        st.sidebar.markdown("---")
        if st.sidebar.button("📱 Generate QR Code", use_container_width=True):
            self.show_qr_code()
        
        # Instructions
        with st.sidebar.expander("📖 How to Play"):
            st.markdown("""
            **Playing the Game:**
            1. **Select a task** using the task selector
            2. **See 5 pieces** for that task only
            3. **Drag pieces** to the correct positions (1-5)
            4. **Watch pieces turn green** when placed correctly
            5. **Earn 4 points immediately** for each correct placement
            6. **Complete all 5 tasks** to win!
            
            **New Features:**
            - 🎯 **One task at a time** - no confusion
            - 🎨 **Instant visual feedback** - green = correct
            - ⚡ **Immediate scoring** - 4 points per subtask
            - 📱 **Touch-friendly** drag and drop
            """)
    
    def display_task_selector(self):
        """Display task selector with visual progress"""
        st.markdown("### 🎯 Select Your Challenge")
        
        # Create task selection buttons
        cols = st.columns(5)
        tasks_data = st.session_state.tasks_data
        
        for i, (task_id, task_data) in enumerate(tasks_data.items()):
            with cols[i]:
                # Count completed subtasks for this task
                completed_count = sum(1 for task_slot in st.session_state.task_solutions[task_id] 
                                    if task_slot is not None and f"{task_id}_{task_slot['piece_id']}" in st.session_state.completed_subtasks)
                
                # Determine button style
                if completed_count == 5:
                    button_type = "primary"
                    status = "✅ Complete"
                elif completed_count > 0:
                    button_type = "secondary" 
                    status = f"🔄 {completed_count}/5"
                else:
                    button_type = "secondary"
                    status = "⏳ Start"
                
                # Task button
                if st.button(
                    f"{task_data['icon']}\n{task_data['title']}\n{status}",
                    key=f"task_select_{task_id}",
                    type=button_type,
                    use_container_width=True
                ):
                    st.session_state.current_task = task_id
                    if task_id not in st.session_state.task_pieces_shuffled:
                        self.shuffle_current_task_pieces()
                    st.rerun()
        
        # Current task info
        current_task_data = tasks_data[st.session_state.current_task]
        st.markdown(f"""
        <div class="task-selector">
            <h3>{current_task_data['icon']} Currently Working On: {current_task_data['title']}</h3>
            <p>{current_task_data['description']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    def display_current_task_area(self):
        """Display the current task solution area"""
        current_task = st.session_state.current_task
        current_task_data = st.session_state.tasks_data[current_task]
        
        st.subheader(f"🎯 {current_task_data['icon']} {current_task_data['title']} - Solution Area")
        st.info("Drag pieces from the right panel to the correct positions below!")
        
        # Display solution slots
        for slot_id in range(5):
            piece = st.session_state.task_solutions[current_task][slot_id]
            
            if piece is not None:
                # Check if piece is correctly placed
                is_correct = (piece['piece_id'] == slot_id)
                piece_class = "piece-correct" if is_correct else "piece-wrong"
                
                # Show placed piece
                st.markdown(f"""
                <div class="puzzle-piece {piece_class}" style="position: relative;">
                    <div style="text-align: center;">
                        <div style="font-size: 1.1em; margin-bottom: 0.3em;">
                            {current_task_data['icon']} {'✅' if is_correct else '❌'}
                        </div>
                        <div style="font-size: 0.9em; line-height: 1.2;">
                            <strong>Step {slot_id + 1}:</strong> {piece['text']}
                        </div>
                        <div style="font-size: 0.8em; margin-top: 0.3em; opacity: 0.8;">
                            Click to remove
                        </div>
                    </div>
                    {f'<div class="subtask-score">+4 pts</div>' if is_correct else ''}
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden remove button
                if st.button("Remove Piece", key=f"remove_{current_task}_{slot_id}", help="Remove this piece"):
                    self.remove_piece(current_task, slot_id)
                    st.rerun()
            else:
                # Show empty slot
                st.markdown(f"""
                <div class="drop-zone empty">
                    <div style="text-align: center; color: #7f8c8d;">
                        <div style="font-size: 1.5em;">📥</div>
                        <div style="font-size: 1em;"><strong>Step {slot_id + 1}</strong></div>
                        <div style="font-size: 0.8em;">Drop piece here</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Hidden place button
                if st.button("Place Here", key=f"place_{current_task}_{slot_id}", help="Place selected piece here"):
                    if hasattr(st.session_state, 'selected_piece'):
                        self.place_piece(current_task, slot_id, st.session_state.selected_piece)
                        st.rerun()
    
    def display_current_task_pieces(self):
        """Display pieces for the current task only"""
        current_task = st.session_state.current_task
        current_task_data = st.session_state.tasks_data[current_task]
        
        # Get available pieces (not yet placed)
        if current_task not in st.session_state.task_pieces_shuffled:
            self.shuffle_current_task_pieces()
        
        all_pieces = st.session_state.task_pieces_shuffled[current_task]
        placed_piece_ids = set()
        
        # Find which pieces are already placed
        for slot in st.session_state.task_solutions[current_task]:
            if slot is not None:
                placed_piece_ids.add(slot['id'])
        
        available_pieces = [p for p in all_pieces if p['id'] not in placed_piece_ids]
        
        st.subheader(f"🧩 {current_task_data['icon']} Task Pieces ({len(available_pieces)} available)")
        
        if not available_pieces:
            st.success("🎉 All pieces for this task have been placed!")
            return
        
        st.markdown("""
        <div class="pieces-pool">
        """, unsafe_allow_html=True)
        
        st.info("Click on a piece below to select it, then click a position slot on the left!")
        
        # Display available pieces
        for piece in available_pieces:
            # Check if this piece is selected
            selected_class = ""
            if hasattr(st.session_state, 'selected_piece') and st.session_state.selected_piece and st.session_state.selected_piece['id'] == piece['id']:
                selected_class = "border: 3px solid #f39c12 !important; box-shadow: 0 0 15px rgba(243, 156, 18, 0.5) !important;"
            
            # Create styled piece
            st.markdown(f"""
            <div class="puzzle-piece piece-pool" style="background: {piece['color']}; {selected_class}">
                <div style="text-align: center;">
                    <div style="font-size: 1.1em; margin-bottom: 0.3em;">{piece['icon']}</div>
                    <div style="font-size: 0.9em; line-height: 1.2;">{piece['text']}</div>
                    <div style="font-size: 0.7em; margin-top: 0.3em; opacity: 0.8;">Click to select</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Hidden select button
            if st.button("Select This Piece", key=f"select_{piece['id']}", help=f"Select: {piece['text']}"):
                st.session_state.selected_piece = piece
                st.success(f"✅ Selected: {piece['text'][:50]}...")
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Show selected piece info
        if hasattr(st.session_state, 'selected_piece') and st.session_state.selected_piece:
            piece = st.session_state.selected_piece
            st.info(f"🎯 **Selected:** {piece['icon']} {piece['text']}")
            st.markdown("👈 Now click on a position slot on the left to place this piece!")
    
    def place_piece(self, task_id, slot_id, piece):
        """Place a piece in the specified slot"""
        if not piece:
            st.warning("⚠️ Please select a piece first!")
            return
        
        # Ensure piece belongs to current task
        if piece['task_id'] != task_id:
            st.error("❌ This piece doesn't belong to the current task!")
            return
        
        # Place the piece
        st.session_state.task_solutions[task_id][slot_id] = piece
        
        # Check if correctly placed and award points immediately
        if piece['piece_id'] == slot_id:
            subtask_id = f"{task_id}_{piece['piece_id']}"
            if subtask_id not in st.session_state.completed_subtasks:
                st.session_state.completed_subtasks.add(subtask_id)
                st.session_state.player_score += 4
                st.success(f"🎉 Correct placement! +4 points! Total: {st.session_state.player_score}")
                
                # Check if task is complete
                task_complete = all(
                    st.session_state.task_solutions[task_id][i] is not None and 
                    st.session_state.task_solutions[task_id][i]['piece_id'] == i 
                    for i in range(5)
                )
                
                if task_complete:
                    st.balloons()
                    task_name = st.session_state.tasks_data[task_id]['title']
                    st.success(f"🏆 {task_name} COMPLETED! All subtasks correct!")
                    
                    # Check if all tasks complete
                    if len(st.session_state.completed_subtasks) == 25:
                        st.success("🎯 AMAZING! ALL TASKS COMPLETED! You're a true Logistics Master!")
                        self.save_high_score()
        
        # Clear selection
        if hasattr(st.session_state, 'selected_piece'):
            del st.session_state.selected_piece
    
    def remove_piece(self, task_id, slot_id):
        """Remove a piece from a slot"""
        piece = st.session_state.task_solutions[task_id][slot_id]
        if piece:
            # Remove from solution
            st.session_state.task_solutions[task_id][slot_id] = None
            
            # Remove points if it was correctly placed
            subtask_id = f"{task_id}_{piece['piece_id']}"
            if subtask_id in st.session_state.completed_subtasks:
                st.session_state.completed_subtasks.remove(subtask_id)
                st.session_state.player_score -= 4
                st.info(f"Piece removed. -4 points. Total: {st.session_state.player_score}")
    
    def show_qr_code(self):
        """Generate and display QR code for the app"""
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(st.session_state.app_url)
            qr.make(fit=True)
            
            # Create image
            qr_img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes for Streamlit
            buf = io.BytesIO()
            qr_img.save(buf, format='PNG')
            byte_im = buf.getvalue()
            
            # Display QR code
            st.sidebar.markdown("### 📱 Share This Game")
            st.sidebar.image(byte_im, caption="Scan to play!", width=200)
            st.sidebar.success(f"Share this QR code!\n\n{st.session_state.app_url}")
            
            # Provide download link
            st.sidebar.download_button(
                label="💾 Download QR Code",
                data=byte_im,
                file_name="logistics_puzzle_qr.png",
                mime="image/png"
            )
            
        except Exception as e:
            st.sidebar.error("QR code generation failed. Try after deployment!")
    
    def show_hint(self):
        """Show task-specific hints"""
        current_task = st.session_state.current_task
        task_data = st.session_state.tasks_data[current_task]
        
        hints = {
            0: [  # Warehouse Management
                "💡 Start with receiving - you need inventory before you can sort it!",
                "💡 Sorting comes before updating systems - organize first, then record!",
                "💡 Database updates happen after physical sorting is complete!",
                "💡 Storage assignment happens after you know what you have!",
                "💡 Reports are always generated last - after all work is done!"
            ],
            1: [  # Transportation Planning
                "💡 Begin by analyzing where deliveries need to go!",
                "💡 Calculate distances after you know the destinations!",
                "💡 Vehicle scheduling requires distance information first!",
                "💡 Optimization comes after basic planning is complete!",
                "💡 Documentation (manifests) are prepared last!"
            ],
            2: [  # Supply Chain Coordination
                "💡 Start by contacting suppliers - you need quotes first!",
                "💡 Negotiation happens after you have initial quotes!",
                "💡 Meetings are scheduled during the negotiation process!",
                "💡 Quality monitoring happens after supplies start arriving!",
                "💡 Database maintenance is ongoing throughout the process!"
            ],
            3: [  # Order Fulfillment
                "💡 Everything starts with processing the incoming order!",
                "💡 Check inventory before promising delivery!",
                "💡 Pick items only after verifying they're available!",
                "💡 Package items after they're picked from shelves!",
                "💡 Generate shipping labels as the final step!"
            ],
            4: [  # Inventory Control
                "💡 Start by monitoring what you currently have!",
                "💡 Identify shortages after reviewing current levels!",
                "💡 Create purchase orders for items that are low!",
                "💡 Track when new supplies will arrive!",
                "💡 Update records after everything is processed!"
            ]
        }
        
        task_hints = hints.get(current_task, ["💡 Think about the logical order of operations!"])
        hint = random.choice(task_hints)
        st.info(hint)
    
    def show_high_scores(self):
        """Display high scores leaderboard"""
        if st.session_state.high_scores:
            st.subheader("🏆 High Scores Leaderboard")
            
            df = pd.DataFrame(st.session_state.high_scores)
            df = df.sort_values('score', ascending=False).head(10)
            df.index = range(1, len(df) + 1)
            
            st.dataframe(
                df[['name', 'score', 'subtasks_completed', 'date']], 
                use_container_width=True,
                column_config={
                    "name": "Player Name",
                    "score": "Score", 
                    "subtasks_completed": "Subtasks Done",
                    "date": "Date Achieved"
                }
            )
        else:
            st.info("🎯 No high scores yet! Complete subtasks to be the first on the leaderboard!")
    
    def save_high_score(self):
        """Save player's high score"""
        score_entry = {
            'name': st.session_state.player_name,
            'score': st.session_state.player_score,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'subtasks_completed': len(st.session_state.completed_subtasks)
        }
        st.session_state.high_scores.append(score_entry)
        st.success(f"🎉 High score saved! {st.session_state.player_name}: {st.session_state.player_score} points")
    
    def reset_game(self):
        """Reset the entire game"""
        # Keep high scores and player name, reset everything else
        high_scores = st.session_state.high_scores
        
        # Clear game state
        for key in ['current_task', 'task_solutions', 'task_pieces_shuffled', 
                   'player_score', 'completed_subtasks', 'game_started']:
            if key in st.session_state:
                del st.session_state[key]
        
        # Reset selected piece
        if hasattr(st.session_state, 'selected_piece'):
            del st.session_state.selected_piece
        
        # Restore high scores
        st.session_state.high_scores = high_scores
        
        st.rerun()

def main():
    """Main function to run the app"""
    game = LogisticsPuzzleGame()
    game.main()

if __name__ == "__main__":
    main()
