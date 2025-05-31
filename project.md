# Project Structure and Functionality Overview

## 1. Project Introduction
This project, **Interactive Feedback MCP**, is an MCP (Model Context Protocol) server designed to provide human-in-the-loop workflows for AI-assisted development tools such as Cursor, Cline, and Windsurf. It allows users to execute commands, view output results, and provide feedback directly to AI, enhancing the efficiency and quality of AI-assisted development.

## 2. High-Level Architecture

- **MCP Server (server.py):**
  - Built on the `fastmcp` framework.
  - Provides a tool named `interactive_feedback`, which launches the feedback UI and returns user feedback and command logs.
  - Responsible for communication between the AI assistant and the feedback UI.

- **Feedback UI (feedback_ui.py):**
  - Developed using PySide6 (Qt for Python).
  - Provides a graphical interface that allows users to:
    - View command output/logs.
    - Input and submit feedback.
    - Configure command and UI preferences (stored for each project using QSettings).
  - Supports dark mode and platform-specific UI enhancements.

- **Configuration Management:**
  - Uses Qt's QSettings for per-project settings (commands, automatic execution, UI state, window geometry).
  - Settings are stored in platform-specific locations (e.g., plist on macOS, registry on Windows).

- **Dependencies:**
  - Python 3.11+
  - fastmcp (MCP server framework)
  - psutil (process management)
  - pyside6 (UI framework)

## 3. Functionality Description

- **Interactive Feedback Process:**
  - The AI assistant calls the `interactive_feedback` tool, providing the project directory and change summary.
  - The server launches the feedback UI, allowing the user to review logs and provide feedback.
  - Feedback and logs are returned to the AI assistant for further processing.

- **Command Execution:**
  - Users can configure and execute custom commands through the UI.
  - Command output is displayed in real-time and logged for review.

- **User Configuration:**
  - Users can save preferred commands and UI settings for each project.
  - The UI supports toggling the command section, dark mode, and persistent window state.

## 4. File Structure

- `server.py`: Main MCP server providing feedback tools.
- `feedback_ui.py`: PySide6-based UI for feedback and command execution.
- `pyproject.toml`: Project metadata and dependencies.
- `README.md`: Documentation and usage instructions.
- `images/`: UI images/screenshots.
- `.github/`: GitHub-related files (e.g., workflow, images).

## 5. Usage

- Start the server with `uv run server.py`.
- Configure the MCP server connection in Cursor, Cline, or Windsurf.
- Interact with the UI to provide feedback and manage commands.

---

This document briefly describes the architecture and functionality of the Interactive Feedback MCP project. 