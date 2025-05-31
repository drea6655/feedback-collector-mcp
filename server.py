# Interactive Feedback MCP
# Developed by Fábio Ferreira (https://x.com/fabiomlferreira)
# Inspired by/related to dotcursorrules.com (https://dotcursorrules.com/)
import os
import sys
import json
import tempfile
import subprocess
import base64

from typing import Annotated, Dict, List, Any, Optional

from pydantic import Field

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.utilities.types import Image as MCPImage

# The log_level is necessary for Cline to work: https://github.com/jlowin/fastmcp/issues/81
mcp = FastMCP("Interactive Feedback MCP", log_level="ERROR")

def launch_feedback_ui(project_directory: str, summary: str) -> dict:
    # Create a temporary file for the feedback result
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        output_file = tmp.name

    try:
        # Get the path to feedback_ui.py relative to this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        feedback_ui_path = os.path.join(script_dir, "feedback_ui.py")

        # Run feedback_ui.py as a separate process
        # NOTE: There appears to be a bug in uv, so we need
        # to pass a bunch of special flags to make this work
        args = [
            sys.executable,
            "-u",
            feedback_ui_path,
            "--project-directory", project_directory,
            "--prompt", summary,
            "--output-file", output_file
        ]
        result = subprocess.run(
            args,
            check=False,
            shell=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            close_fds=True
        )
        if result.returncode != 0:
            raise Exception(f"Failed to launch feedback UI: {result.returncode}")

        # Read the result from the temporary file
        with open(output_file, 'r') as f:
            result = json.load(f)
        os.unlink(output_file)
        return result
    except Exception as e:
        if os.path.exists(output_file):
            os.unlink(output_file)
        raise e

def first_line(text: str) -> str:
    return text.split("\n")[0].strip()

def convert_to_mcp_images(images_data: List[Dict[str, str]]) -> List[MCPImage]:
    """
    Convert image data to a list of MCPImage objects
    
    Args:
        images_data: List of dictionaries containing image data
        
    Returns:
        List of MCPImage objects
    """
    result_images = []
    
    for img_data in images_data:
        try:
            # Extract image data - this should be base64 encoded
            base64_data = img_data.get('data', '')
            mime_type = img_data.get('mime_type', 'image/png')
            
            if not base64_data:
                continue
                
            # Get format from mime_type
            format = mime_type.split('/')[-1] if '/' in mime_type else 'png'
            
            # Decode base64 to binary data before passing to MCPImage
            binary_data = base64.b64decode(base64_data)
            
            # Create MCPImage object with binary data
            result_images.append(MCPImage(data=binary_data, format=format))
            
        except Exception as e:
            print(f"Error converting image: {e}")
    
    return result_images

@mcp.tool()
def interactive_feedback(
    project_directory: Annotated[str, Field(description="Full path to the project directory")],
    summary: Annotated[str, Field(description="Short, one-line summary of the changes")],
) -> Dict[str, Any]:
    """
    Interactive tool for collecting user feedback. AI can report completed work, and users can provide text and image feedback.
    
    Args:
        summary: AI's report on the completed work.
        
    Returns:
        User feedback content or instructions. Users can provide text and image feedback; please follow the instructions carefully.
    """
    # Get user feedback
    result = launch_feedback_ui(first_line(project_directory), first_line(summary))
    
    feedback_items = []

    from mcp.types import TextContent
    feedback_items.append(TextContent(
        type="text", 
        text=f"feedback_text：{result.get('interactive_feedback', '')}"
    ))

    # Add image feedback
    if 'images' in result and result['images']:
        mcp_images = convert_to_mcp_images(result['images'])
        for image_data in mcp_images:
            feedback_items.append(image_data)
        
    return feedback_items

if __name__ == "__main__":
    # For testing, try running just the feedback UI directly
    # try:
    #     print("Testing feedback UI...")
    #     test_result = launch_feedback_ui(os.getcwd(), "test")
    #     print(test_result)
    #     print("Feedback UI test successful")
    # except Exception as e:
    #     print(f"Error testing feedback UI: {e}")
    
    print("Starting MCP server...")
    mcp.run()
