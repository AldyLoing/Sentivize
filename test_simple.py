"""
Script sederhana untuk testing komponen aplikasi tanpa Streamlit
"""

import pandas as pd
import config
import services
from ai_analyzer import get_analyzer

def test_file_reading():
    """Test membaca file sample"""
    print("\n" + "="*50)
    print("TEST 1: File Reading")
    print("="*50)
    
    try:
        df = pd.read_csv('sample_data.csv')
        print(f"✅ File berhasil dibaca")
        print(f"   Total baris: {len(df)}")
        print(f"   Kolom: {', '.join(df.columns)}")
        return df
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_column_detection(df):
    """Test deteksi kolom"""
    print("\n" + "="*50)
    print("TEST 2: Column Detection")
    print("="*50)
    
    try:
        # Normalize columns
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        cols = services.detect_columns(df)
        print("✅ Kolom terdeteksi:")
        for key, value in cols.items():
            print(f"   {key}: {value if value else 'Tidak ditemukan'}")
        return cols
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_social_search():
    """Test pencarian sosial media"""
    print("\n" + "="*50)
    print("TEST 3: Social Media Search")
    print("="*50)
    
    test_name = "Budi Santoso"
    print(f"Mencari profil untuk: {test_name}")
    
    try:
        links = services.find_social_media_links(test_name, max_results=2)
        if links:
            print(f"✅ Ditemukan {len(links)} link:")
            for link in links:
                print(f"   - {link}")
        else:
            print("⚠️  Tidak ada link ditemukan (mungkin rate limited)")
        return links
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

def test_ai_mock_mode():
    """Test AI analyzer dalam mock mode"""
    print("\n" + "="*50)
    print("TEST 4: AI Analyzer (Mock Mode)")
    print("="*50)
    
    try:
        analyzer = get_analyzer(use_mock_models=True)
        
        # Test texts
        texts = [
            "Saya sangat tertarik dengan isu lingkungan dan keberlanjutan.",
            "Pengalaman saya dalam pengelolaan limbah sangat baik.",
            "Passionate about environmental sustainability."
        ]
        
        keyword = "lingkungan"
        
        print(f"Analyzing {len(texts)} texts dengan keyword: '{keyword}'")
        
        # Sentiment analysis
        sentiment_label, sentiment_score = analyzer.analyze_sentiment(texts)
        print(f"✅ Sentiment: {sentiment_label} (score: {sentiment_score:.3f})")
        
        # Relevance analysis
        relevance_score = analyzer.calculate_relevance(texts, keyword)
        print(f"✅ Relevance: {relevance_score:.3f}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_text_processing():
    """Test text cleaning dan processing"""
    print("\n" + "="*50)
    print("TEST 5: Text Processing")
    print("="*50)
    
    try:
        # Test clean_text
        dirty_text = "  This  is   a   text   with   extra   spaces  "
        clean = services.clean_text(dirty_text)
        print(f"✅ Clean text: '{clean}'")
        
        # Test extract links
        text_with_links = "Check my profile: https://linkedin.com/in/test and https://instagram.com/test"
        links = services.extract_social_links_from_text(text_with_links)
        print(f"✅ Extracted {len(links)} links: {links}")
        
        # Test fallback text
        fallback = services.create_fallback_text("John Doe", "Manager", "IT")
        print(f"✅ Fallback text: '{fallback}'")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def test_full_pipeline():
    """Test pipeline lengkap dengan sample data"""
    print("\n" + "="*50)
    print("TEST 6: Full Pipeline (Mock Mode)")
    print("="*50)
    
    try:
        import analyzer as analyzer_module
        
        # Load sample data
        df = pd.read_csv('sample_data.csv')
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        
        # Limit to 3 candidates for testing
        df_small = df.head(3).copy()
        
        print(f"Analyzing {len(df_small)} candidates...")
        
        results_df = analyzer_module.analyze_candidates(
            df=df_small,
            keyword="lingkungan",
            enable_scraping=False,
            use_mock_models=True,
            progress_callback=lambda c, t: print(f"   Progress: {c}/{t}")
        )
        
        print(f"\n✅ Analisis selesai!")
        print(f"   Total kandidat: {len(results_df)}")
        print(f"\nTop 3 by Relevance:")
        top3 = results_df.nlargest(3, 'Relevance Score')[['Name', 'Relevance Score', 'Sentiment Label']]
        print(top3.to_string(index=False))
        
        # Save results
        filename = analyzer_module.save_results_to_excel(results_df, 'test_hasil.xlsx')
        print(f"\n✅ Hasil disimpan ke: {filename}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "🔍 SENTIVIZE - TEST SUITE ".center(50, "="))
    print("Testing komponen aplikasi...\n")
    
    results = []
    
    # Test 1: File reading
    df = test_file_reading()
    results.append(df is not None)
    
    if df is not None:
        # Test 2: Column detection
        cols = test_column_detection(df)
        results.append(cols is not None)
        
        # Test 3: Social search (optional, may fail due to rate limiting)
        test_social_search()  # Not added to results due to rate limiting
        
        # Test 4: AI mock mode
        ai_ok = test_ai_mock_mode()
        results.append(ai_ok)
        
        # Test 5: Text processing
        text_ok = test_text_processing()
        results.append(text_ok)
        
        # Test 6: Full pipeline
        pipeline_ok = test_full_pipeline()
        results.append(pipeline_ok)
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✅ All tests passed!")
        print("\n🎉 Aplikasi siap digunakan!")
        print("   Jalankan: streamlit run app.py")
    else:
        print(f"⚠️  Some tests failed. Check errors above.")
    
    print("\n")

if __name__ == "__main__":
    main()
