# 2048 with AI Assistant

A modern web-based implementation of the classic 2048 puzzle game with an intelligent AI assistant to help you make optimal moves. The game features a sleek, responsive UI and a FastAPI backend with sophisticated Monte Carlo simulation-based AI.

![2048 Game Screenshot](https://i.imgur.com/placeholder.png)

## 🎮 Features

### Game Features
- **Customizable Board**: Choose any board size (2x2 to 10x10)
- **Flexible Win Conditions**: Set win tiles from 64 to 8192
- **Undo Functionality**: Take back moves when you make mistakes
- **Game State Management**: Restart or start new games anytime

### AI Assistant
- **Monte Carlo Simulations**: AI runs 50 random simulations per move
- **Intelligent Move Selection**: Chooses moves based on statistical outcomes
- **Performance Feedback**: Shows AI thinking process and move rationale

### User Interface
- **Modern Design**: Beautiful gradient backgrounds and smooth animations
- **Responsive Layout**: Works on desktop, tablet, and mobile devices
- **Keyboard Support**: Use WASD or arrow keys for quick gameplay
- **Visual Feedback**: Color-coded tiles and status notifications
- **Accessibility**: Semantic HTML and proper contrast ratios

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation

1. **Clone or download the project files:**
   ```bash
   # Make sure you have these files:
   # - app.py (FastAPI backend)
   # - main.py (Game logic)
   # - index.html (Web interface)
   # - styles.css (Styling)
   # - script.js (Frontend logic)
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn
   ```

3. **Run the server:**
   ```bash
   uvicorn app:app --reload
   ```

4. **Open your browser and navigate to:**
   ```
   http://localhost:8000
   ```

## 🎯 How to Play

### Starting a Game
1. When you first open the game, you'll see a setup modal
2. Choose your preferred:
   - **Height**: Board height (2-10 cells)
   - **Width**: Board width (2-10 cells)  
   - **Win Tile**: Target tile value (64-8192)
3. Click "Start Game" to begin

### Making Moves
- **Manual Moves**: 
  - Click the directional buttons (↑ ← ↓ →)
  - Use keyboard: WASD or arrow keys
- **AI Assistance**: Click "LET AI MAKE MOVE" for optimal moves
- **Game Actions**: Use Undo, Restart, or New Game as needed

### Game Rules
- Combine tiles with the same number by moving them together
- Each move spawns a new tile (2 or 4)
- Reach the target tile to win!
- Game ends when no moves are possible

## 🤖 AI Strategy

The AI assistant uses a Monte Carlo simulation approach:

1. **Move Evaluation**: For each possible move (up, down, left, right)
2. **Simulation**: Runs 50 random games from that position
3. **Scoring**: Evaluates outcomes based on:
   - Win probability (reaching target tile)
   - Average tile values achieved
   - Game longevity
4. **Selection**: Chooses the move with the highest expected score

This approach balances immediate gains with long-term strategic positioning.

## 🏗️ Project Structure

```
2048-ai-assistant/
├── app.py              # FastAPI web server
├── main.py             # Core game logic and AI
├── index.html          # Main web interface
├── styles.css          # UI styling and animations
├── script.js           # Frontend game controller
└── README.md           # This file
```

### Backend Architecture
- **FastAPI**: Modern, fast web framework for Python
- **Game Class**: Manages game state and user interactions
- **Board Class**: Handles game logic, moves, and validation
- **AI Class**: Implements Monte Carlo tree search for move optimization

### Frontend Architecture
- **Vanilla JavaScript**: No frameworks, pure JS for maximum compatibility
- **CSS Grid**: Responsive board layout that adapts to any size
- **Fetch API**: Clean REST API communication with backend
- **Event-driven**: Keyboard and mouse input handling

## 📱 Responsive Design

The game automatically adapts to different screen sizes:

- **Desktop**: Side-by-side board and controls layout
- **Tablet**: Stacked layout with optimized button sizes
- **Mobile**: Full-width design with touch-friendly controls

## 🎨 Customization

### Changing Board Colors
Edit the tile color classes in `styles.css`:
```css
.board-cell.tile-2 { background: #eee4da; color: #776e65; }
.board-cell.tile-4 { background: #ede0c8; color: #776e65; }
/* Add more tile colors */
```

### Adjusting AI Difficulty
Modify the simulation count in `main.py`:
```python
def get_best_move(self, simulations=50):  # Change this number
```

### Adding New Win Tiles
Update the dropdown options in `index.html`:
```html
<option value="16384">16384</option>
```

## 🐛 Troubleshooting

### Common Issues

**Game board doesn't load:**
- Check browser console for JavaScript errors
- Ensure FastAPI server is running on port 8000
- Verify all files are in the same directory

**AI moves are slow:**
- Reduce simulation count in `main.py`
- Check server performance and memory usage

**Keyboard controls don't work:**
- Click on the game area to focus
- Check browser console for event listener errors

### Browser Compatibility
- **Chrome**: ✅ Full support
- **Firefox**: ✅ Full support  
- **Safari**: ✅ Full support
- **Edge**: ✅ Full support
- **IE**: ❌ Not supported (lacks modern JavaScript features)

## 🔧 API Endpoints

The FastAPI backend provides these endpoints:

- `GET /` - Serve the main HTML page
- `GET /styles.css` - Serve CSS stylesheet
- `GET /script.js` - Serve JavaScript code
- `POST /start_new_game` - Initialize new game with settings
- `POST /restart_game` - Restart with same settings
- `POST /make_user_move` - Process user move
- `POST /make_ai_move` - Let AI make optimal move
- `POST /undo` - Undo last move

## 🤝 Contributing

Feel free to contribute improvements:

1. **Performance**: Optimize AI algorithms or UI rendering
2. **Features**: Add new game modes or AI strategies
3. **Design**: Improve visual design or add animations
4. **Accessibility**: Enhance keyboard navigation or screen reader support

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Original 2048 game by Gabriele Cirulli
- Inspired by classic sliding puzzle games
- Built with modern web technologies for optimal performance

---

**Enjoy playing 2048 with your AI assistant! 🎮🤖**
