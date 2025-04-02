"""Docstring generation functionality for bartste-prompts."""

from typing import List
import subprocess
from aider_chat import AiderChat

class DocstringGenerator:
    """Handles docstring generation for files."""
    
    def __init__(self, style: str = "google"):
        self.style = style
        self.aider = AiderChat()
        
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
        """Get the appropriate prompt based on language and style."""
        base_prompt = f"Add {self.style} style docstrings to all {language} "
        base_prompt += "functions, classes and methods that are missing them. "
        base_prompt += "Follow all standard conventions for the language."
        
        if language == "python":
            if self.style == "google":
                base_prompt += " Use Google style docstrings with type hints."
            elif self.style == "numpy":
                base_prompt += " Use NumPy style docstrings."
            elif self.style == "rest":
                base_prompt += " Use reStructuredText style docstrings."
        
        return base_prompt
