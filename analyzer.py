"""
Analyzer module - Pipeline utama untuk analisis kandidat karyawan
"""

import pandas as pd
from typing import Dict, List, Optional
import config
import services
from ai_analyzer import get_analyzer


def analyze_candidates(
    df: pd.DataFrame,
    keyword: str,
    enable_scraping: bool = False,
    use_mock_models: bool = False,
    progress_callback=None
) -> pd.DataFrame:
    """
    Pipeline utama untuk menganalisis kandidat karyawan
    
    Args:
        df: DataFrame berisi data karyawan
        keyword: Kata kunci untuk analisis relevansi
        enable_scraping: Jika True, coba scraping posting dari sosial media
        use_mock_models: Jika True, gunakan mock models untuk testing
        progress_callback: Function callback untuk update progress (opsional)
        
    Returns:
        pd.DataFrame: DataFrame hasil analisis dengan kolom tambahan
    """
    
    # Detect kolom-kolom penting
    columns = services.detect_columns(df)
    
    if not columns['name_col']:
        raise ValueError("Kolom nama tidak ditemukan dalam file!")
    
    # Initialize AI analyzer
    analyzer = get_analyzer(use_mock_models=use_mock_models)
    
    # Prepare results list
    results = []
    
    total_rows = len(df)
    
    # Iterasi setiap kandidat
    for idx, row in df.iterrows():
        try:
            # Update progress
            if progress_callback:
                progress_callback(idx + 1, total_rows)
            
            # Extract basic info
            name = row[columns['name_col']]
            if pd.isna(name) or not str(name).strip():
                continue
            
            name = str(name).strip()
            
            # Extract position and unit if available
            position = None
            if columns['position_col'] and columns['position_col'] in row:
                position = row[columns['position_col']]
                if not pd.isna(position):
                    position = str(position).strip()
            
            unit = None
            if columns['unit_col'] and columns['unit_col'] in row:
                unit = row[columns['unit_col']]
                if not pd.isna(unit):
                    unit = str(unit).strip()
            
            # Get social media links
            social_links = []
            
            # Check if social media column exists in data
            if columns['social_col'] and columns['social_col'] in row:
                existing_links = services.extract_social_links_from_text(
                    str(row[columns['social_col']])
                )
                social_links.extend(existing_links)
            
            # If no social links found, search for them
            search_performed = False
            if not social_links:
                social_links = services.find_social_media_links(
                    name, 
                    max_results=config.MAX_SEARCH_RESULTS
                )
                search_performed = True
            
            # Collect texts for analysis
            texts = []
            
            # Add text from text/bio column if exists
            if columns['text_col'] and columns['text_col'] in row:
                text_content = row[columns['text_col']]
                if not pd.isna(text_content):
                    texts.append(services.clean_text(
                        str(text_content), 
                        max_length=config.MAX_TEXT_LENGTH
                    ))
            
            # Try to fetch posts from social media if enabled
            if enable_scraping and social_links:
                for link in social_links[:2]:  # Limit to 2 profiles
                    posts = services.fetch_public_posts_from_url(
                        link, 
                        limit=config.MAX_POSTS_PER_ACCOUNT
                    )
                    for post in posts:
                        if post:
                            texts.append(services.clean_text(
                                post, 
                                max_length=config.MAX_TEXT_LENGTH
                            ))
            
            # If no texts collected, create fallback text
            if not texts:
                fallback_text = services.create_fallback_text(name, position, unit)
                texts.append(fallback_text)
            
            # Perform sentiment analysis
            sentiment_label, sentiment_score = analyzer.analyze_sentiment(texts)
            
            # Perform relevance analysis with reasoning
            relevance_score, relevance_reasoning = analyzer.calculate_relevance_with_reasoning(
                texts, keyword, name, position, unit
            )
            
            # Prepare preview text
            preview_text = texts[0][:200] + "..." if texts and len(texts[0]) > 200 else (texts[0] if texts else "")
            
            # Generate overall reasoning for this candidate
            overall_reasoning = _generate_candidate_reasoning(
                name, position, unit, relevance_score, sentiment_label, 
                sentiment_score, len(texts), search_performed, relevance_reasoning
            )
            
            # Compile result
            result = {
                'Name': name,
                'Position': position if position else '-',
                'Unit': unit if unit else '-',
                'Social Media': ', '.join(social_links) if social_links else 'Not found',
                'Social Media Count': len(social_links),
                'Search Performed': 'Yes' if search_performed else 'No',
                'Sentiment Label': sentiment_label,
                'Sentiment Score': round(sentiment_score, 3),
                'Relevance Score': round(relevance_score, 3),
                'Relevance Reasoning': relevance_reasoning,
                'Overall Reasoning': overall_reasoning,
                'Text Preview': preview_text,
                'Texts Analyzed': len(texts)
            }
            
            results.append(result)
            
        except Exception as e:
            import traceback
            print(f"\n❌ Error processing {name if 'name' in locals() else 'unknown'}:")
            print(f"   Error: {str(e)}")
            print(f"   Traceback: {traceback.format_exc()}")
            continue
    
    # Convert to DataFrame
    if not results:
        print(f"\n⚠️ DEBUG INFO:")
        print(f"   Total rows processed: {total_rows}")
        print(f"   Detected columns: {columns}")
        print(f"   DataFrame columns: {df.columns.tolist()}")
        print(f"   First row sample: {df.iloc[0].to_dict() if len(df) > 0 else 'No data'}")
        raise ValueError("Tidak ada kandidat yang berhasil dianalisis! Check error messages above.")
    
    results_df = pd.DataFrame(results)
    
    # Sort by relevance score (descending)
    results_df = results_df.sort_values('Relevance Score', ascending=False).reset_index(drop=True)
    
    return results_df


def _generate_candidate_reasoning(
    name: str,
    position: Optional[str],
    unit: Optional[str],
    relevance_score: float,
    sentiment_label: str,
    sentiment_score: float,
    texts_count: int,
    search_performed: bool,
    relevance_reasoning: str
) -> str:
    """
    Generate detailed reasoning untuk kandidat
    
    Args:
        name: Nama kandidat
        position: Jabatan kandidat
        unit: Unit kerja kandidat
        relevance_score: Skor relevansi
        sentiment_label: Label sentiment
        sentiment_score: Skor sentiment
        texts_count: Jumlah teks yang dianalisis
        search_performed: Apakah pencarian dilakukan
        relevance_reasoning: Alasan relevansi dari AI
        
    Returns:
        str: Reasoning lengkap
    """
    reasons = []
    
    # 1. Relevance reasoning
    if relevance_score >= 0.7:
        reasons.append(f"✅ **Sangat Relevan** (Score: {relevance_score:.3f})")
        reasons.append(f"   {relevance_reasoning}")
    elif relevance_score >= 0.5:
        reasons.append(f"⚠️ **Cukup Relevan** (Score: {relevance_score:.3f})")
        reasons.append(f"   {relevance_reasoning}")
    else:
        reasons.append(f"⚪ **Kurang Relevan** (Score: {relevance_score:.3f})")
        reasons.append(f"   {relevance_reasoning}")
    
    # 2. Position relevance
    if position and position != '-':
        reasons.append(f"💼 **Jabatan:** {position}")
        if unit and unit != '-':
            reasons.append(f"🏢 **Unit:** {unit}")
    
    # 3. Sentiment analysis
    if sentiment_label == config.SENTIMENT_POSITIVE:
        reasons.append(f"😊 **Sentiment Positif** (Score: {sentiment_score:.3f})")
        reasons.append(f"   Menunjukkan attitude dan komunikasi yang baik")
    elif sentiment_label == config.SENTIMENT_NEGATIVE:
        reasons.append(f"😟 **Sentiment Negatif** (Score: {sentiment_score:.3f})")
        reasons.append(f"   Perlu evaluasi lebih lanjut terhadap konten")
    else:
        reasons.append(f"😐 **Sentiment Netral** (Score: {sentiment_score:.3f})")
        reasons.append(f"   Konten profesional dan objektif")
    
    # 4. Data sources
    reasons.append(f"📊 **Data Analisis:** {texts_count} teks dianalisis")
    if search_performed:
        reasons.append(f"🔍 Pencarian social media dilakukan")
    
    return "\n".join(reasons)
    
    return results_df


def save_results_to_excel(results_df: pd.DataFrame, filename: str = None) -> str:
    """
    Simpan hasil analisis ke file Excel
    
    Args:
        results_df: DataFrame hasil analisis
        filename: Nama file output (default: config.OUTPUT_FILENAME)
        
    Returns:
        str: Path file yang disimpan
    """
    if filename is None:
        filename = config.OUTPUT_FILENAME
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Write main results
            results_df.to_excel(writer, sheet_name='Hasil Analisis', index=False)
            
            # Create summary sheet
            summary_data = {
                'Metric': [
                    'Total Kandidat',
                    'Rata-rata Relevance Score',
                    'Rata-rata Sentiment Score',
                    'Jumlah Positive Sentiment',
                    'Jumlah Negative Sentiment',
                    'Jumlah Neutral Sentiment',
                    'Kandidat dengan Social Media',
                    'Kandidat tanpa Social Media'
                ],
                'Value': [
                    len(results_df),
                    round(results_df['Relevance Score'].mean(), 3),
                    round(results_df['Sentiment Score'].mean(), 3),
                    len(results_df[results_df['Sentiment Label'] == config.SENTIMENT_POSITIVE]),
                    len(results_df[results_df['Sentiment Label'] == config.SENTIMENT_NEGATIVE]),
                    len(results_df[results_df['Sentiment Label'] == config.SENTIMENT_NEUTRAL]),
                    len(results_df[results_df['Social Media Count'] > 0]),
                    len(results_df[results_df['Social Media Count'] == 0])
                ]
            }
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        return filename
        
    except Exception as e:
        raise Exception(f"Error saving to Excel: {str(e)}")


def get_analysis_summary(results_df: pd.DataFrame) -> Dict:
    """
    Generate summary statistics dari hasil analisis
    
    Args:
        results_df: DataFrame hasil analisis
        
    Returns:
        Dict: Dictionary berisi summary statistics
    """
    summary = {
        'total_candidates': len(results_df),
        'avg_relevance': results_df['Relevance Score'].mean(),
        'avg_sentiment': results_df['Sentiment Score'].mean(),
        'sentiment_distribution': results_df['Sentiment Label'].value_counts().to_dict(),
        'top_candidates': results_df.head(5)[['Name', 'Relevance Score']].to_dict('records'),
        'social_media_coverage': {
            'with_social': len(results_df[results_df['Social Media Count'] > 0]),
            'without_social': len(results_df[results_df['Social Media Count'] == 0])
        }
    }
    
    return summary
