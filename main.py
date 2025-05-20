# -*- coding: utf-8 -*-

import os
import sys

class FixedPromptTerminal:
    def __init__(self, prompt='> '):
        self.prompt = prompt
        self.output_buffer = []
        self._setup_terminal()
        self._display_welcome()

    def _setup_terminal(self):
        """Initialize and Setup Terminal"""
        if os.name == 'nt':
            # If Windows, Enable Virtual Terminal Sequences and ANSI sequences.
            os.system('')  # Enable ANSI sequences.

    def _get_terminal_size(self):
        """Get Terminal Screen size, Maybe work on Windows and Linux and MacOS X. But not sure."""
        try:
            size = os.get_terminal_size()
            return size.lines, size.columns
        except:
            return 25, 80  # Failsafe Default size for Terminal (80x25).

    def _clear_screen(self):
        """Clear screen and Move cursor to top left"""
        sys.stdout.write('\033[2J')  # Clear Screen
        sys.stdout.write('\033[H')  # Move cursor to top left.
        sys.stdout.flush()

    def _move_cursor_to_bottom(self):
        """Move cursor to bottom of Terminal"""
        rows, _ = self._get_terminal_size()
        sys.stdout.write(f'\033[{rows};1H')  # Move cursor to Last line and First column.
        sys.stdout.flush()

    def _display_output(self):
        """Display Output"""
        rows, cols = self._get_terminal_size()
        max_output_rows = rows - 1  # Keep last line for Prompt.

        # Calculate Display Ranges.
        start_idx = max(0, len(self.output_buffer) - max_output_rows)
        visible_output = self.output_buffer[start_idx:]

        self._clear_screen()
        print('\n'.join(visible_output))
        self._move_cursor_to_bottom()
        print(self.prompt, end='', flush=True)

    def add_output(self, text):
        """Add new output to Stdout area"""
        lines = str(text).split('\n')
        self.output_buffer.extend(lines)
        self._display_output()

    def _display_welcome(self):
        """Display Welcome Messages"""
        self.add_output("CLI Console")
        self.add_output("Type '/exit' or '/quit' to quit, '/clear' to clear screen.")

    def run(self):
        """Main Loop"""
        while True:
            try:
                # Display prompt and Get user input.
                self._move_cursor_to_bottom()
                sys.stdout.write(self.prompt)
                sys.stdout.flush()

                # Get user input.
                user_input = input()

                # Handle special commands.
                if user_input.lower() in ('/exit', '/quit'):
                    break

                if user_input.lower() == '/clear':
                    self.output_buffer = []
                    self._clear_screen()
                    self._display_output()
                    continue

                # Stdout <- User input Results.
                self.add_output(f"$ {user_input}") # User input contents.
                self.add_output(f"Result of '{user_input}'") # User input execution results. Can Modify this.

            except KeyboardInterrupt:
                self.add_output("^C")
                # If you want to exit on press Ctrl+C, Comment the previous line, Then uncomment the next line.
                # break
            except EOFError:
                break
            except Exception as e:
                self.add_output(f"Error: {str(e)}")


if __name__ == "__main__":
    terminal = FixedPromptTerminal()
    terminal.run()
