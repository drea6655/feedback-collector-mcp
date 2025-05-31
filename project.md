# 專案架構與功能概述

## 1. 專案簡介
本專案 **Interactive Feedback MCP** 是一個 MCP（Model Context Protocol）伺服器，旨在為如 Cursor、Cline 及 Windsurf 等 AI 輔助開發工具提供人機協作（human-in-the-loop）工作流程。它允許用戶執行指令、檢視輸出結果，並直接向 AI 提供回饋，提升 AI 輔助開發的效率與品質。

## 2. 高層架構

- **MCP 伺服器（server.py）：**
  - 基於 `fastmcp` 框架建構。
  - 提供名為 `interactive_feedback` 的工具，啟動回饋 UI 並回傳用戶回饋及指令日誌。
  - 負責 AI 助理與回饋 UI 之間的溝通。

- **回饋 UI（feedback_ui.py）：**
  - 使用 PySide6（Qt for Python）開發。
  - 提供圖形化介面，讓用戶：
    - 檢視指令輸出/日誌。
    - 輸入並提交回饋。
    - 設定指令與 UI 偏好（每個專案以 QSettings 儲存）。
  - 支援深色模式及平台專屬 UI 增強。

- **設定管理：**
  - 透過 Qt 的 QSettings 進行每個專案的設定（指令、自動執行、UI 狀態、視窗幾何資訊）。
  - 設定儲存於平台專屬位置（如 macOS 的 plist、Windows 的 registry）。

- **相依套件：**
  - Python 3.11+
  - fastmcp（MCP 伺服器框架）
  - psutil（程序管理）
  - pyside6（UI 框架）

## 3. 功能說明

- **互動式回饋流程：**
  - AI 助理呼叫 `interactive_feedback` 工具，傳入專案目錄及變更摘要。
  - 伺服器啟動回饋 UI，讓用戶檢閱日誌並提供回饋。
  - 回饋與日誌回傳給 AI 助理做進一步處理。

- **指令執行：**
  - 用戶可於 UI 設定並執行自訂指令。
  - 指令輸出即時顯示，並記錄日誌供檢閱。

- **用戶設定：**
  - 用戶可針對每個專案儲存偏好指令與 UI 設定。
  - UI 支援切換指令區塊、深色模式及視窗狀態持久化。

## 4. 檔案結構

- `server.py`：主要 MCP 伺服器，提供回饋工具。
- `feedback_ui.py`：基於 PySide6 的回饋與指令執行 UI。
- `pyproject.toml`：專案中繼資料與相依套件。
- `README.md`：文件與使用說明。
- `images/`：UI 圖片/截圖。
- `.github/`：GitHub 相關檔案（如 workflow、圖片）。

## 5. 使用方式

- 以 `uv run server.py` 啟動伺服器。
- 於 Cursor、Cline 或 Windsurf 設定 MCP 伺服器連線。
- 透過 UI 互動式提供回饋並管理指令。

---

本文件簡要說明了 Interactive Feedback MCP 專案的架構與功能。 