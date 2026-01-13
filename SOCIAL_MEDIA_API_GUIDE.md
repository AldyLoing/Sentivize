# 📊 Social Media Intelligence API - Complete Guide

## 🎯 **Apa itu Instagram Statistics API?**

API ini adalah **analytics platform untuk influencer marketing dan brand monitoring**, BUKAN people search tool atau social media scraper umum.

### **Database Karakteristik:**
- **5+ juta accounts** (influencer, brands, businesses)
- **Instagram**: Open business accounts only (bukan personal accounts)
- **Facebook**: Public pages only (bukan personal user accounts)
- **YouTube, Twitter, TikTok, Telegram**: Supported untuk public creators/influencers
- Update frequency: High priority (daily), Average (weekly-monthly), Low (few times/year)

---

## ⚠️ **PENTING: Kenapa Akun Tidak Ditemukan?**

### **API Limitation by Design:**

```
❌ TIDAK TERDETEKSI:
- Akun personal biasa (1-5K followers)
- Private accounts
- Akun baru tanpa analytics history
- Akun tanpa engagement metrics yang significant

✅ TERDETEKSI:
- Influencer (5000+ followers)
- Business accounts
- Verified accounts
- Creator accounts dengan public analytics
```

### **Contoh Real Test:**

| Username | Followers | Result | Reason |
|----------|-----------|--------|---------|
| `@therock` | 397M | ✅ **200 OK** | Influencer terindeks penuh |
| `@aldy_loing` | ~500-1K | ❌ **404 Not Found** | Akun personal, bukan influencer |
| `@cristiano` | 600M+ | ✅ **200 OK** | Athlete/influencer |

**Ini bukan bug, tapi design API!**

---

## 📦 **Supported Platforms:**

| Platform | Status | Coverage |
|----------|--------|----------|
| **Instagram** | ✅ Full Support | Business accounts with analytics |
| **Twitter/X** | ✅ Full Support | Public accounts with metrics |
| **TikTok** | ✅ Full Support | Creator accounts |
| **YouTube** | ⚠️ In Progress | Public channels |
| **Facebook** | ⚠️ In Progress | Public pages only |
| **Telegram** | ⚠️ In Progress | Public channels |

---

## 📊 **Metrics yang Tersedia:**

### **Basic Info:**
- `usersCount` - Followers count
- `screenName` - Username
- `name` - Profile name
- `description` - Bio
- `verified` - Verification status
- `isBlocked` - Account blocked
- `isClosed` - Account private/closed
- `type` - influencer | business

### **Engagement Metrics:**
- `avgER` - Average Post Engagement Rate (0-1)
- `avgInteractions` - Average interactions per post (likes+comments+shares)
- `avgViews` - Average views per post
- `avgLikes` - Average likes per post
- `avgComments` - Average comments per post

### **Quality Metrics:**
- `qualityScore` - Quality indicator (0-1)
  - Compared to similar accounts
  - Considers: audience quality, engagement, growth, regularity, bot percentage
- `pctFakeFollowers` - Percentage of fake followers (0-1)

### **Demographics (Account Owner):**
- `country` - Account country
- `countryCode` - Country code
- `city` - Account city
- `gender` - m | f
- `age` - Age range (0_18, 18_21, 21_24, 24_27, 27_30, 30_35, 35_45, 45_100)
- `categories` - Account categories

### **Audience Demographics:**
- `membersTypes` - Audience types distribution:
  - `real` - Real followers
  - `suspicious` - Suspicious accounts
  - `massfollowers` - Mass followers
  - `influencer` - Influencer followers
- `countries` - Top audience countries with percentages
- `genders` - Audience gender distribution (m/f with %)
- `ages` - Audience age groups with percentages
- `membersReachability` - Audience by follower count ranges

### **Reach & Growth:**
- `toMentions180d` - Times mentioned by others (6 months)
- `toMentionsCommunities180d` - Number of accounts that mentioned
- `toMentionsViews180d` - Total reach of mentions
- `fromMentions180d` - Times mentioning others
- `fromMentionsCommunities180d` - Number of accounts mentioned
- `fromMentionsViews180d` - Total reach of posts with mentions
- `pctUsersCount180d` - Follower growth % (6 months)

### **Contact & Timestamps:**
- `contactEmail` - Contact email (if public)
- `timeStatistics` - Last update of basic info
- `timePostsLoaded` - Last update of posts

---

## 🔍 **API Methods Available:**

### **1. Profile by URL** (Currently Implemented)
```python
url = "https://www.instagram.com/therock"
response = api.get(f"{base_url}/community", params={"url": url})
```

**Supported URLs:**
- Instagram: `https://www.instagram.com/username`
- YouTube: `https://www.youtube.com/@channel` or `/channel/ID`
- Twitter: `https://twitter.com/username`
- TikTok: `https://www.tiktok.com/@username`
- Facebook: `https://www.facebook.com/pagename` or `/pageID`
- Telegram: `https://t.me/channel`

### **2. Profile by ID** (Fast Lookup)
```python
response = api.get(f"{base_url}/profile", params={"cid": unique_id})
```

### **3. Search** (Advanced Filters)
```python
response = api.get(f"{base_url}/search", params={
    "q": "keyword",
    "minUsersCount": 10000,
    "maxUsersCount": 1000000,
    "minER": 0.02,
    "maxFakeFollowers": 0.15,
    "audienceLocations": "ID",  # Indonesia
    "socialTypes": "INST,TT,YT"
})
```

### **4. Feed** (Get Posts)
```python
response = api.get(f"{base_url}/feed", params={
    "cid": unique_id,
    "from": "01.01.2025",
    "to": "31.12.2025",
    "type": "posts"  # posts | ads | stories | mentions
})
```

### **5. Retrospective** (Historical Stats)
```python
response = api.get(f"{base_url}/retrospective", params={
    "cid": unique_id,
    "from": "01.01.2025",
    "to": "31.12.2025"
})
```

---

## 🎯 **Best Practices untuk HR:**

### **✅ DO:**
1. **Gunakan sebagai bonus intelligence**
   - Jika ketemu → analyze metrics (fake followers, engagement, quality)
   - Jika tidak ketemu → NORMAL, bukan red flag

2. **Minta username langsung saat interview**
   - "Apakah Anda memiliki akun Instagram/LinkedIn/Twitter?"
   - Verifikasi manual lebih akurat

3. **Fokus pada quality metrics (jika terdeteksi):**
   - Quality Score > 0.7 = Excellent
   - Fake Followers < 15% = Good
   - Engagement Rate > 2% = Active audience

### **❌ DON'T:**
1. **Jangan jadikan requirement**
   - Tidak semua kandidat punya social media influencer
   - Akun personal biasa tidak akan terdeteksi

2. **Jangan anggap "not found" sebagai red flag**
   - API hanya untuk influencer/business accounts
   - Regular accounts dengan <5K followers tidak terindeks

3. **Jangan rely 100% pada automated search**
   - Username di CV mungkin berbeda
   - Kandidat bisa menggunakan nickname

---

## 📈 **Interpretation Guide:**

### **Quality Score (0-1):**
- **0.8 - 1.0**: Elite influencer, top-tier content
- **0.6 - 0.8**: High-quality account, good engagement
- **0.4 - 0.6**: Average account
- **0.2 - 0.4**: Below average, possible issues
- **0.0 - 0.2**: Low quality, high bot percentage

### **Fake Followers % (0-1):**
- **0% - 10%**: ✅ Excellent, natural growth
- **10% - 20%**: ⚠️ Acceptable, common range
- **20% - 30%**: ⚠️ Warning, investigate further
- **30%+**: 🚨 Red flag, likely purchased followers

### **Engagement Rate (ER):**
- **5%+**: 🌟 Excellent engagement
- **2-5%**: ✅ Good engagement
- **1-2%**: ⚠️ Average
- **<1%**: 🚨 Low engagement, possible fake followers

### **Audience Types:**
- **Real > 70%**: ✅ Healthy audience
- **Real 50-70%**: ⚠️ Acceptable but monitor
- **Real < 50%**: 🚨 Questionable audience quality
- **Suspicious > 30%**: 🚨 High bot/fake percentage

---

## 🔧 **Implementation Status:**

### **✅ Completed:**
- Instagram search with full metrics extraction
- Twitter/X search implementation
- TikTok search implementation
- Comprehensive reporting with all metrics
- Username variation generation (30+ patterns)
- Confidence scoring system
- Quality metrics display (fake followers, ER, quality score)
- Demographics display (account & audience)
- Growth & reach metrics

### **⚠️ In Progress:**
- YouTube search (endpoint ready, needs testing)
- Facebook search (endpoint ready, needs testing)
- Telegram search (endpoint ready, needs testing)

### **📋 Planned:**
- Feed analysis (recent posts)
- Historical analysis (Retrospective)
- Advanced search with filters
- Activity timing analysis

---

## 🎓 **Example Use Cases:**

### **Use Case 1: Social Media Manager Position**
```
Kandidat: Sarah Marketing
Instagram Found: @sarahmarketingpro
- Followers: 15K
- Engagement Rate: 3.5%
- Quality Score: 0.75
- Fake Followers: 8%
- Account Type: Business

✅ Decision: Good fit! 
   Active professional presence, authentic engagement
```

### **Use Case 2: Entry-Level Position**
```
Kandidat: Budi Fresh Graduate
Instagram: Not Found

✅ Decision: Normal! 
   Kandidat tidak aktif di social media atau akun personal biasa
   Minta username saat interview jika diperlukan
```

### **Use Case 3: Influencer Marketing Role**
```
Kandidat: Rina Influencer
Instagram Found: @rinabeauty
- Followers: 250K
- Engagement Rate: 0.8%
- Quality Score: 0.35
- Fake Followers: 42%
- Suspicious Audience: 38%

⚠️ Decision: RED FLAG!
   High fake followers, low engagement, purchased followers likely
```

---

## 📞 **Support & Resources:**

- **RapidAPI Documentation**: https://rapidapi.com/artemlipko/api/instagram-statistics-api/
- **API Endpoint**: `instagram-statistics-api.p.rapidapi.com`
- **Rate Limits**: Depends on subscription tier
- **Historical Data**: Last 2 years of metrics available

---

## 💡 **Key Takeaway:**

> **"API ini adalah tool untuk analyze influencer metrics, bukan untuk spy kandidat. Gunakan dengan bijak sebagai supplementary intelligence, bukan requirement."**

**Not finding an account ≠ Problem**  
**Finding an account = Bonus data untuk validate fit**

---

**Updated:** December 2025  
**Version:** 2.0 - Full Metrics Implementation
