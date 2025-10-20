#!/usr/bin/env python3
"""
Comprehensive PDF Analysis for Flames CC Cricket Dashboard
Analyzes all PDF formats in both Old Data and New Data folders
"""

import os
import json
import re
from pathlib import Path
import fitz  # PyMuPDF

def analyze_pdf_structure(pdf_path):
    """Analyze the structure and content of a PDF file"""
    try:
        doc = fitz.open(pdf_path)
        analysis = {
            "filename": os.path.basename(pdf_path),
            "pages": doc.page_count,
            "text_samples": [],
            "structure_analysis": {},
            "extractable_data": {}
        }
        
        # Extract text from first few pages
        for page_num in range(min(3, doc.page_count)):
            page = doc[page_num]
            text = page.get_text()
            analysis["text_samples"].append({
                "page": page_num + 1,
                "text_preview": text[:500] + "..." if len(text) > 500 else text
            })
            
            # Look for common cricket scorecard patterns
            patterns = {
                "match_date": r"(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})",
                "team_names": r"(Flames|vs|VS)",
                "scores": r"(\d{1,3}/\d{1,2})",
                "overs": r"(\d{1,2}\.\d)",
                "player_names": r"([A-Z][a-z]+\s+[A-Z][a-z]+)",
                "innings": r"(1st\s+Innings|2nd\s+Innings|First\s+Innings|Second\s+Innings)"
            }
            
            for pattern_name, pattern in patterns.items():
                matches = re.findall(pattern, text, re.IGNORECASE)
                if matches:
                    analysis["extractable_data"][pattern_name] = matches[:5]  # First 5 matches
        
        doc.close()
        return analysis
        
    except Exception as e:
        return {
            "filename": os.path.basename(pdf_path),
            "error": str(e),
            "pages": 0,
            "text_samples": [],
            "structure_analysis": {},
            "extractable_data": {}
        }

def categorize_pdf_format(analysis):
    """Categorize PDF based on its structure and content"""
    filename = analysis["filename"]
    text_samples = analysis.get("text_samples", [])
    
    # Check filename patterns
    if "Spartans" in filename or "Alpha" in filename:
        return "spartan_format"
    
    # Check content patterns
    full_text = " ".join([sample.get("text_preview", "") for sample in text_samples])
    
    if "Full Scorecard" in full_text or "FLAMES" in full_text.upper():
        return "full_scorecard_format"
    elif "AllStar" in full_text or "CricketScore" in full_text:
        return "allstar_format"
    elif "CricHeroes" in full_text or "cricheroes" in full_text.lower():
        return "cricheroes_format"
    else:
        return "unknown_format"

def main():
    print("Flames CC - Comprehensive PDF Analysis")
    print("=" * 50)
    
    # Define paths
    old_data_path = Path("Flames/Old Data")
    new_data_path = Path("Flames/New data")
    
    all_analyses = []
    format_categories = {}
    
    # Analyze Old Data folder
    if old_data_path.exists():
        print(f"\nAnalyzing Old Data folder: {old_data_path}")
        old_pdfs = list(old_data_path.glob("*.pdf"))
        print(f"Found {len(old_pdfs)} PDFs in Old Data")
        
        for pdf_file in old_pdfs:
            print(f"  Analyzing: {pdf_file.name}")
            analysis = analyze_pdf_structure(pdf_file)
            analysis["folder"] = "Old Data"
            analysis["format_type"] = categorize_pdf_format(analysis)
            all_analyses.append(analysis)
            
            # Categorize by format
            format_type = analysis["format_type"]
            if format_type not in format_categories:
                format_categories[format_type] = []
            format_categories[format_type].append(analysis["filename"])
    
    # Analyze New Data folder
    if new_data_path.exists():
        print(f"\nAnalyzing New Data folder: {new_data_path}")
        new_pdfs = list(new_data_path.glob("*.pdf"))
        print(f"Found {len(new_pdfs)} PDFs in New Data")
        
        for pdf_file in new_pdfs[:10]:  # Sample first 10 for analysis
            print(f"  Analyzing: {pdf_file.name}")
            analysis = analyze_pdf_structure(pdf_file)
            analysis["folder"] = "New data"
            analysis["format_type"] = categorize_pdf_format(analysis)
            all_analyses.append(analysis)
            
            # Categorize by format
            format_type = analysis["format_type"]
            if format_type not in format_categories:
                format_categories[format_type] = []
            format_categories[format_type].append(analysis["filename"])
    
    # Generate summary
    print(f"\nAnalysis Summary:")
    print(f"Total PDFs analyzed: {len(all_analyses)}")
    print(f"Format categories found: {len(format_categories)}")
    
    for format_type, files in format_categories.items():
        print(f"  {format_type}: {len(files)} files")
        if len(files) <= 5:
            for file in files:
                print(f"    - {file}")
        else:
            for file in files[:3]:
                print(f"    - {file}")
            print(f"    ... and {len(files) - 3} more")
    
    # Save detailed analysis
    with open("comprehensive_pdf_analysis.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": {
                "total_pdfs": len(all_analyses),
                "format_categories": format_categories,
                "analysis_date": str(Path.cwd())
            },
            "detailed_analyses": all_analyses
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nDetailed analysis saved to: comprehensive_pdf_analysis.json")
    
    # Create format-specific sample files
    for format_type, files in format_categories.items():
        if files:
            sample_file = files[0]
            print(f"\nSample file for {format_type}: {sample_file}")
    
    return format_categories, all_analyses

if __name__ == "__main__":
    try:
        format_categories, analyses = main()
        print("\nAnalysis complete!")
        
        # Show next steps
        print("\nNext Steps:")
        print("1. Review comprehensive_pdf_analysis.json")
        print("2. Create extractors for each format type")
        print("3. Extract data from all PDFs")
        print("4. Build comprehensive database")
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        import traceback
        traceback.print_exc()
