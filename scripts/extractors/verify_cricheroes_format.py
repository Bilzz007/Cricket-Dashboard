#!/usr/bin/env python3
"""
Verify that all PDFs are CricHeroes format
"""

import os
import PyPDF2
import re

def verify_all_cricheroes():
    """Verify all PDFs are CricHeroes format"""
    
    print("=== VERIFYING ALL PDFs ARE CRICHEROES FORMAT ===\n")
    
    pdf_folder = "Flames/Scorecards"
    
    if not os.path.exists(pdf_folder):
        print(f"Folder not found: {pdf_folder}")
        return
    
    # Get all PDFs
    all_pdfs = [f for f in os.listdir(pdf_folder) if f.endswith('.pdf')]
    
    print(f"Total PDFs to check: {len(all_pdfs)}\n")
    
    cricheroes_pdfs = []
    non_cricheroes_pdfs = []
    error_pdfs = []
    
    # Check each PDF
    for i, pdf_file in enumerate(all_pdfs):
        pdf_path = os.path.join(pdf_folder, pdf_file)
        
        # Show progress
        if i % 10 == 0:
            print(f"Checking {i+1}/{len(all_pdfs)}...")
        
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                if len(pdf_reader.pages) > 0:
                    # Extract text from first page
                    first_page_text = pdf_reader.pages[0].extract_text()
                    
                    # Check for CricHeroes indicators
                    cricheroes_indicators = [
                        'cricheroes.com',
                        'cricHeroes',
                        'CricHeroes',
                        'Match Details',
                        'Best Performances'
                    ]
                    
                    is_cricheroes = any(indicator in first_page_text for indicator in cricheroes_indicators)
                    
                    if is_cricheroes:
                        cricheroes_pdfs.append(pdf_file)
                    else:
                        non_cricheroes_pdfs.append(pdf_file)
                        print(f"\n  NON-CRICHEROES: {pdf_file}")
                        print(f"  First 300 chars: {first_page_text[:300]}")
                else:
                    error_pdfs.append(pdf_file)
                    print(f"\n  ERROR (No pages): {pdf_file}")
                    
        except Exception as e:
            error_pdfs.append(pdf_file)
            print(f"\n  ERROR reading {pdf_file}: {e}")
    
    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    print(f"\nTotal PDFs checked: {len(all_pdfs)}")
    print(f"CricHeroes format: {len(cricheroes_pdfs)} ({len(cricheroes_pdfs)*100//len(all_pdfs)}%)")
    print(f"Non-CricHeroes format: {len(non_cricheroes_pdfs)}")
    print(f"Errors: {len(error_pdfs)}")
    
    if non_cricheroes_pdfs:
        print(f"\nNON-CRICHEROES PDFs:")
        for pdf in non_cricheroes_pdfs:
            print(f"  - {pdf}")
    
    if error_pdfs:
        print(f"\nERROR PDFs:")
        for pdf in error_pdfs:
            print(f"  - {pdf}")
    
    if len(cricheroes_pdfs) == len(all_pdfs):
        print("\n*** ALL PDFs ARE CRICHEROES FORMAT! ***")
        print("We can proceed with creating a single CricHeroes extractor.")
    elif len(non_cricheroes_pdfs) > 0:
        print(f"\n*** WARNING: {len(non_cricheroes_pdfs)} PDFs are NOT CricHeroes format ***")
        print("These need to be reviewed.")
    
    return {
        "total": len(all_pdfs),
        "cricheroes": len(cricheroes_pdfs),
        "non_cricheroes": len(non_cricheroes_pdfs),
        "errors": len(error_pdfs),
        "non_cricheroes_list": non_cricheroes_pdfs,
        "error_list": error_pdfs
    }

if __name__ == "__main__":
    verify_all_cricheroes()
