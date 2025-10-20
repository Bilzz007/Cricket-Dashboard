#!/usr/bin/env python3
"""
Organize project structure like Streamlit
Clean up unnecessary files and create proper folder structure
"""

import os
import shutil

def organize_project():
    """Organize project into clean folder structure"""
    
    print("=== ORGANIZING PROJECT STRUCTURE ===\n")
    
    # Define folder structure
    folders = {
        "assets": ["css", "js"],
        "data": ["raw", "processed"],
        "scripts": ["extractors", "processors"],
        "docs": []
    }
    
    # Create folders
    print("Creating folder structure...")
    for folder, subfolders in folders.items():
        os.makedirs(folder, exist_ok=True)
        for subfolder in subfolders:
            os.makedirs(os.path.join(folder, subfolder), exist_ok=True)
    
    # Move files to appropriate locations
    print("\nMoving files to organized structure...")
    
    # Move CSS files
    css_files = ["advanced_styles.css", "flames_styles.css", "squad_styles_addon.css"]
    for f in css_files:
        if os.path.exists(f):
            shutil.move(f, f"assets/css/{f}")
            print(f"  Moved {f} -> assets/css/")
    
    # Move JS files
    js_files = ["advanced_script.js", "flames_script.js", "squad_manager.js"]
    for f in js_files:
        if os.path.exists(f):
            shutil.move(f, f"assets/js/{f}")
            print(f"  Moved {f} -> assets/js/")
    
    # Move processed data files
    data_files = [
        "dashboard_data.json",
        "cricket_database_cricheroes.json",
        "extraction_summary.json"
    ]
    for f in data_files:
        if os.path.exists(f):
            shutil.move(f, f"data/processed/{f}")
            print(f"  Moved {f} -> data/processed/")
    
    # Move extractor scripts
    extractor_scripts = [
        "extract_cricheroes_comprehensive.py",
        "verify_cricheroes_format.py",
        "reanalyze_pdf_formats.py"
    ]
    for f in extractor_scripts:
        if os.path.exists(f):
            shutil.move(f, f"scripts/extractors/{f}")
            print(f"  Moved {f} -> scripts/extractors/")
    
    # Move processor scripts
    processor_scripts = [
        "prepare_dashboard_data.py",
        "integrate_advanced_dashboard.py"
    ]
    for f in processor_scripts:
        if os.path.exists(f):
            shutil.move(f, f"scripts/processors/{f}")
            print(f"  Moved {f} -> scripts/processors/")
    
    # Move documentation
    doc_files = [
        "VERIFICATION_REPORT.txt",
        "FLAMES_MATCHES.txt",
        "RAFTAAR_MATCHES.txt",
        "COMPLETE_MATCH_LIST.txt"
    ]
    for f in doc_files:
        if os.path.exists(f):
            shutil.move(f, f"docs/{f}")
            print(f"  Moved {f} -> docs/")
    
    # Delete temporary/unnecessary files
    print("\nDeleting unnecessary files...")
    temp_files = [
        "analyze_cricheroes_structure.py",
        "analyze_pdf_formats.py",
        "check_fielding_data.py",
        "check_more_formats.py",
        "create_complete_standalone.py",
        "create_final_dashboard.py",
        "create_match_list.py",
        "create_verification_report.py",
        "debug_pdf_content.py",
        "extract_format1_comprehensive.py",
        "extract_format1_fielding_simple.py",
        "extract_format1_final.py",
        "extract_format1_friendly.py",
        "extract_format1_improved.py",
        "extract_format1_with_fielding.py",
        "extract_all_cricheroes.py",
        "remove_excel_data.py",
        "player_name_mapper.py",
        # JSON files that are intermediate/temporary
        "clean_cricket_database.json",
        "cleaned_excel_data.json",
        "complete_20overs_database.json",
        "complete_4050overs_database.json",
        "complete_excel_database.json",
        "comprehensive_cricket_database.json",
        "comprehensive_pdf_analysis.json",
        "dashboard_cricket_data.json",
        "detailed_match_statistics.json",
        "excel_extraction_results.json",
        "format1_comprehensive_extraction.json",
        "format1_fielding_analysis.json",
        "format1_final_extraction.json",
        "format1_friendly_improved.json",
        "format1_friendly_sample.json",
        "format1_with_fielding.json",
        "matches_20overs_cleaned.json",
        "matches_4050overs_cleaned.json",
        "specific_sheets_extraction.json",
        "test_13 - 26-Sep-21 -  CLASSIC XI KARACHI VS Flames.json",
        "test_Scorecard_10640768.json",
        "20overs_column_structure.json",
        "4050overs_column_structure.json",
        "flames_squad_cleaned.json",
        "flames_squad.json",
        # Text files
        "cricheroes_structure.txt",
        "format1_verification_report.txt",
        "match_lists_output.txt",
        # Markdown files that are not needed
        "EXCEL_DATA_SUMMARY.md",
        "EXTRACTED_DATA_VERIFICATION.md",
        "SQUAD_MANAGEMENT.md"
    ]
    
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
            print(f"  Deleted {f}")
    
    print("\n=== PROJECT ORGANIZATION COMPLETE ===")
    print("\nNew Structure:")
    print("  assets/")
    print("    css/      - All CSS files")
    print("    js/       - All JavaScript files")
    print("  data/")
    print("    raw/      - Raw PDF scorecards")
    print("    processed/- Processed JSON data")
    print("  scripts/")
    print("    extractors/ - PDF extraction scripts")
    print("    processors/ - Data processing scripts")
    print("  docs/")
    print("    - Documentation and reports")
    print("  index.html or flames_dashboard.html - Main dashboard")
    print("  README.md - Project documentation")

if __name__ == "__main__":
    organize_project()

