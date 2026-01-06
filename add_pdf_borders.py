"""
PDF Border Addition Tool

This program adds white borders to PDF pages and resizes them to specified dimensions.
It preserves the text layer and maintains quality without compression.

Requirements:
    pip install PyMuPDF

Usage:
    python add_pdf_borders.py input.pdf output.pdf
"""

import sys
from pymupdf import pymupdf

def add_borders_to_pdf(input_path, output_path, target_width_inches=5.91,
                       target_height_inches=9.08, top_margin_inches=0.3,
                       left_margin_inches=0.3, right_margin_inches=0.3):
    """
    Add white borders to PDF pages and resize to target dimensions.

    Args:
        input_path: Path to input PDF file
        output_path: Path to output PDF file
        target_width_inches: Target page width in inches (default: 5.91)
        target_height_inches: Target page height in inches (default: 9.08)
        top_margin_inches: Top margin in inches (default: 0.3)
        left_margin_inches: Left margin in inches (default: 0.3)
        right_margin_inches: Right margin in inches (default: 0.3)
    """

    # Convert inches to points (1 inch = 72 points)
    POINTS_PER_INCH = 72

    target_width = target_width_inches * POINTS_PER_INCH
    target_height = target_height_inches * POINTS_PER_INCH
    top_margin = top_margin_inches * POINTS_PER_INCH
    left_margin = left_margin_inches * POINTS_PER_INCH
    right_margin = right_margin_inches * POINTS_PER_INCH

    print(f"Processing PDF: {input_path}")
    print(
        f"Target dimensions: {target_width_inches}\" × {target_height_inches}\" ({target_width:.2f} × {target_height:.2f} points)")
    print(f"Margins - Top: {top_margin_inches}\", Left: {left_margin_inches}\", Right: {right_margin_inches}\"")

    # Open input PDF
    input_doc = pymupdf.open(input_path)
    total_pages = len(input_doc)
    print(f"Total pages: {total_pages}")

    # Create output PDF
    output_doc = pymupdf.open()

    # Process each page
    for page_num in range(total_pages):
        print(f"Processing page {page_num + 1}/{total_pages}...", end="\r")

        # Get original page
        original_page = input_doc[page_num]
        original_rect = original_page.rect

        # Calculate bottom margin to reach target height
        # bottom_margin = target_height - top_margin - original_height
        # But we want to position content at top with fixed top margin

        # Create new page with target dimensions
        new_page = output_doc.new_page(width=target_width, height=target_height)

        #new_page = output_doc.new_page(width=original_rect.width, height=original_rect.height)

        # Calculate the position to place the original content
        # Content should be offset by left_margin and top_margin
        left_margin = (target_width - original_rect.width)/2

        target_rect = pymupdf.Rect(
            left_margin,
            top_margin,
            left_margin + original_rect.width,
            top_margin + original_rect.height
        )

        print(target_rect)

        # Show the original page on the new page at the calculated position
        new_page.show_pdf_page(target_rect, input_doc, page_num)

    print(f"\nProcessing complete. Saving to: {output_path}")

    # Save output PDF without compression to maintain quality
    output_doc.save(
        output_path,
        garbage=4,  # Maximum garbage collection
        deflate=True,  # Use deflate compression (lossless)
        deflate_images=False,  # Don't compress images
        deflate_fonts=False,  # Don't compress fonts
    )

    output_doc.close()
    input_doc.close()

    print(f"Successfully saved: {output_path}")
    print(f"Output file size: {get_file_size_mb(output_path):.2f} MB")


def get_file_size_mb(filepath):
    """Get file size in megabytes."""
    import os
    return os.path.getsize(filepath) / (1024 * 1024)


def main():
    """Main entry point for command-line usage."""
    if len(sys.argv) < 3:
        print("Usage: python add_pdf_borders.py <input.pdf> <output.pdf>")
        print("\nOptional arguments:")
        print("  --width <inches>      Target page width (default: 5.91)")
        print("  --height <inches>     Target page height (default: 9.08)")
        print("  --top <inches>        Top margin (default: 0.3)")
        print("  --left <inches>       Left margin (default: 0.3)")
        print("  --right <inches>      Right margin (default: 0.3)")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    # Parse optional arguments
    kwargs = {}
    i = 3
    while i < len(sys.argv):
        if sys.argv[i] == "--width" and i + 1 < len(sys.argv):
            kwargs["target_width_inches"] = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--height" and i + 1 < len(sys.argv):
            kwargs["target_height_inches"] = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--top" and i + 1 < len(sys.argv):
            kwargs["top_margin_inches"] = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--left" and i + 1 < len(sys.argv):
            kwargs["left_margin_inches"] = float(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--right" and i + 1 < len(sys.argv):
            kwargs["right_margin_inches"] = float(sys.argv[i + 1])
            i += 2
        else:
            print(f"Unknown argument: {sys.argv[i]}")
            sys.exit(1)

    try:
        add_borders_to_pdf(input_path, output_path, **kwargs)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()