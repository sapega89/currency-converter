"""Menu handler for following Single Responsibility Principle."""

# Import Tuple for return type annotation
from typing import Tuple

# Import DTO for menu item
from dtos import MenuItemDTO

# Import menu option enumeration
from enums import MenuOption

# Import text messages for menu
from messages import (
    MENU_CHANGE_RATE_DESCRIPTION,
    MENU_CONVERT_DESCRIPTION,
    MENU_EXIT_DESCRIPTION,
)


class MenuHandler:
    """Class for working with application menu."""

    def __init__(self, output_handler) -> None:
        # Save output handler for displaying menu
        # output_handler will be used for displaying menu to user
        self._output = output_handler

    def get_menu_items(self) -> Tuple[MenuItemDTO, ...]:
        """
        Returns menu items.

        Returns:
            Tuple[MenuItemDTO, ...]: Tuple of menu items (immutable list)
        """
        # Return tuple of three menu items
        return (
            # First item: currency conversion
            # MenuItemDTO creates object with option and description
            MenuItemDTO(MenuOption.CONVERT, MENU_CONVERT_DESCRIPTION),
            # Second item: rate change
            MenuItemDTO(MenuOption.CHANGE_RATE, MENU_CHANGE_RATE_DESCRIPTION),
            # Third item: application exit
            MenuItemDTO(MenuOption.EXIT, MENU_EXIT_DESCRIPTION),
        )

    def display_menu(self) -> None:
        """Displays menu to user."""
        # Get list of menu items
        menu_items = self.get_menu_items()
        # Pass menu items to output handler for display
        # Output handler knows how to format and display menu
        self._output.print_menu(menu_items)
