#!/usr/bin/env python3
"""
Crawl Vietnamese legal documents from official sources.
Sources: vanban.chinhphu.vn, thuvienphapluat.vn, luatvietnam.vn, baohiemxahoi.gov.vn
"""

import json
import time
import re
import os
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from urllib.parse import urljoin, urlparse
import hashlib

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Installing dependencies...")
    os.system("pip install requests beautifulsoup4 lxml")
    import requests
    from bs4 import BeautifulSoup

CACHE_DIR = Path("data/private_cache/vbpq")
CACHE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "vi-VN,vi;q=0.9,en;q=0.8",
}

@dataclass
class LegalDocument:
    source_id: str
    docid: str
    ky_hieu: str
    loai: str
    co_quan: str
    ngay_ban_hanh: str
    ngay_hieu_luc: str
    trich_yeu: str
    url: str
    pdf_local: str
    chars: int
    status: str
    linh_vuc: str
    tags: List[str]
    replaced_by: Optional[str] = None
    expired_on: Optional[str] = None
    effective_date: Optional[str] = None
    source_type: Optional[str] = None
    issuing_authority: Optional[str] = None
    document_number: Optional[str] = None
    gazette_number: Optional[str] = None
    pages: Optional[int] = None
    content: Optional[str] = None
    content_hash: Optional[str] = None

class LegalCrawler:
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a page with retries."""
        for attempt in range(3):
            try:
                resp = self.session.get(url, timeout=30)
                resp.raise_for_status()
                resp.encoding = 'utf-8'
                return resp.text
            except Exception as e:
                print(f"  Attempt {attempt+1} failed for {url}: {e}")
                time.sleep(self.delay * (attempt + 1))
        return None
    
    def download_pdf(self, pdf_url: str, local_path: Path) -> bool:
        """Download PDF file."""
        try:
            resp = self.session.get(pdf_url, stream=True, timeout=60)
            resp.raise_for_status()
            with open(local_path, 'wb') as f:
                for chunk in resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            print(f"  PDF download failed: {e}")
            return False
    
    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using pypdf."""
        try:
            import pypdf
            reader = pypdf.PdfReader(str(pdf_path))
            texts = []
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    texts.append(text)
            return "\n".join(texts)
        except Exception as e:
            print(f"  PDF text extraction failed: {e}")
            return ""
    
    def parse_vanban_detail(self, html: str, docid: str) -> Dict:
        """Parse vanban.chinhphu.vn detail page."""
        soup = BeautifulSoup(html, 'html.parser')
        
        # Extract metadata from the page
        result = {"docid": docid}
        
        # Find the main content area
        main = soup.find('div', class_='main-content') or soup.find('div', id='content') or soup
        
        # Extract tables with metadata
        tables = main.find_all('table')
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                th = row.find('th')
                td = row.find('td')
                if th and td:
                    key = th.get_text(strip=True).lower()
                    value = td.get_text(strip=True)
                    if 'ký hiệu' in key or 'số hiệu' in key:
                        result['ky_hieu'] = value
                    elif 'loại' in key:
                        result['loai'] = value
                    elif 'cơ quan' in key:
                        result['co_quan'] = value
                    elif 'ngày ban hành' in key or 'ngày ký' in key:
                        result['ngay_ban_hanh'] = value
                    elif 'ngày hiệu lực' in key:
                        result['ngay_hieu_luc'] = value
                    elif 'trích yếu' in key or 'tên văn bản' in key:
                        result['trich_yeu'] = value
        
        # Extract PDF link
        pdf_links = main.find_all('a', href=re.compile(r'\.pdf$', re.I))
        if pdf_links:
            result['pdf_url'] = urljoin("https://vanban.chinhphu.vn", pdf_links[0]['href'])
        
        return result
    
    def crawl_docid(self, docid: str) -> Optional[LegalDocument]:
        """Crawl a single document by docid."""
        url = f"https://vanban.chinhphu.vn/?pageid=27160&docid={docid}"
        print(f"Crawling {url}...")
        
        html = self.fetch_page(url)
        if not html:
            return None
        
        meta = self.parse_vanban_detail(html, docid)
        
        # Download PDF if available
        pdf_local = None
        content = ""
        if 'pdf_url' in meta:
            pdf_path = CACHE_DIR / f"{docid}.pdf"
            if self.download_pdf(meta['pdf_url'], pdf_path):
                pdf_local = str(pdf_path)
                content = self.extract_text_from_pdf(pdf_path)
        
        # Build LegalDocument
        doc = LegalDocument(
            source_id=f"{meta.get('ky_hieu', '').replace('/', '_').replace('.', '_')}_{meta.get('ngay_ban_hanh', '').split('-')[-1]}".lower(),
            docid=docid,
            ky_hieu=meta.get('ky_hieu', ''),
            loai=meta.get('loai', ''),
            co_quan=meta.get('co_quan', ''),
            ngay_ban_hanh=meta.get('ngay_ban_hanh', ''),
            ngay_hieu_luc=meta.get('ngay_hieu_luc', ''),
            trich_yeu=meta.get('trich_yeu', ''),
            url=url,
            pdf_local=pdf_local or "",
            chars=len(content),
            status="active_verified",
            linh_vuc="",
            tags=[],
            content=content,
            content_hash=hashlib.sha256(content.encode()).hexdigest() if content else None
        )
        
        return doc


def load_legal_database() -> Dict:
    """Load the legal database JSON."""
    with open("data/legal_database.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_legal_database(db: Dict):
    """Save the legal database JSON."""
    with open("data/legal_database.json", "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def main():
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent))
    
    db = load_legal_database()
    
    # Print current status
    print(f"Current sources: {len(db['sources'])}")
    print(f"Missing critical categories: {list(db['missing_critical'].keys())}")
    
    # Print missing documents count
    total_missing = sum(len(cat['documents']) for cat in db['missing_critical'].values())
    print(f"Total missing critical documents: {total_missing}")
    
    for cat_name, cat in db['missing_critical'].items():
        print(f"  {cat_name} ({cat['priority']}): {len(cat['documents'])} docs")
        for doc in cat['documents']:
            print(f"    - {doc['ky_hieu']} ({doc['doc_number']})")


if __name__ == "__main__":
    main()