"""Docstring generation functionality for bartste-prompts."""

from typing import List, Optional
import subprocess
import pathlib
from aider_chat import AiderChat

class DocstringGenerator:
    """Handles docstring generation for files."""
    
    def __init__(self, conventions_file: Optional[str] = None):
        self.conventions = self._load_conventions(conventions_file)
        self.aider = AiderChat()
        
    def _load_conventions(self, path: Optional[str]) -> str:
        """Load conventions from file if provided."""
        if not path:
            return ""
            
        try:
            return pathlib.Path(path).read_text()
        except Exception as e:
            print(f"Warning: Could not load conventions file: {e}")
            return ""
        
    def get_unstaged_files(self) -> List[str]:
        """Get list of unstaged files from git."""
        result = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            capture_output=True,
            text=True
        )
        return result.stdout.splitlines()
        
    def generate_docstrings(self, files: List[str]) -> None:
        """Generate docstrings for given files."""
        if not files:
            files = self.get_unstaged_files()
            
        for file in files:
            self._process_file(file)
            
    def _process_file(self, file_path: str) -> None:
        """Process a single file to add docstrings."""
        # Determine language based on file extension
        lang = self._get_language(file_path)
        
        # Get appropriate prompt based on language and style
        prompt = self._get_prompt(lang)
        
        # Use aider to add docstrings
        self.aider.process_file(file_path, prompt)
        
    def _get_language(self, file_path: str) -> str:
        """Get programming language from file extension."""
        ext = file_path.split(".")[-1].lower()
        return {
            "py": "python",
            "js": "javascript",
            "ts": "typescript",
            "java": "java",
            "go": "go",
            "rs": "rust",
            "rb": "ruby",
            # Add more extensions as needed
        }.get(ext, "unknown")
        
    def _get_prompt(self, language: str) -> str:
        """Get the appropriate prompt based on language and conventions."""
        prompt = f"""
Add appropriate docstrings to all {language} functions, classes and methods that are missing them.
Follow standard conventions for {language} code.

Key requirements:
- Only add docstrings where they are missing
- Maintain existing code style
- Keep docstrings concise but informative
- Include type information where appropriate

{self.conventions}
"""
        return prompt.strip()
