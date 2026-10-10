from pathlib import Path
import html, urllib.parse
root=Path(__file__).resolve().parent
out=root/'dist'
navlinks=[('/acquisitions/','Acquisitions'),('/#business-development','Business Development'),('/#portfolio-management','Portfolio Management'),('/our-businesses/','Businesses & Relationships'),('/robert-ritch/','Robert Ritch')]
def shell(slug,title,desc,body):
    route='/' if slug=='' else '/'+slug+'/'
    nav=''.join('<a href="'+s+'"'+(' aria-current="page"' if s==route else '')+'>'+t+'</a>' for s,t in navlinks)
    footer=''.join('<a href="/'+s+'/">'+t+'</a>' for s,t in [('lock-equity','Lock Equity'),('resources','Resources & Referrals'),('our-businesses','Businesses & Relationships'),('privacy','Privacy')])
    favicon='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="3" fill="#101f2d"/><text x="4" y="22" font-family="Georgia" font-size="18" fill="#b9deef">RV</text></svg>'
    seo='<meta name="robots" content="noindex,follow">' if slug in ['404','thank-you'] else '<link rel="canonical" href="https://ritchventures.com'+route+'">'
    return f'''<!doctype html><html lang="en" data-delivery="netlify"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{html.escape(title)} | Ritch Ventures</title><meta name="description" content="{html.escape(desc)}">{seo}<link rel="icon" href="data:image/svg+xml,{urllib.parse.quote(favicon)}"><link rel="stylesheet" href="/style.css"><script src="/site.js" defer></script></head><body><header><nav aria-label="Main navigation"><a class="brand" href="/"><span>RV</span>Ritch Ventures</a>{nav}<a class="button" href="/contact/?type=acquisition">Discuss an Acquisition</a></nav></header><main>{body}</main><footer><div class="wrap"><strong>Ritch Ventures</strong><p class="small">Ritch Ventures acquires, develops and manages businesses.</p><div class="footer-links">{footer}<a href="https://robertritch.com/">RobertRitch.com</a></div><p class="small">Independent providers fulfill their own services unless otherwise agreed. Relevant ownership, affiliate and referral-compensation relationships are disclosed. Project responsibilities are agreed for each engagement.</p><p class="small">© 2026 Ritch Ventures</p></div></footer></body></html>'''
def hero(kicker,title,text,cta='Discuss a Business Opportunity',href='/contact/?type=business'):
    return '<section class="hero"><div class="wrap"><p class="eyebrow">'+kicker+'</p><h1>'+title+'</h1><p>'+text+'</p><div class="actions"><a class="button" href="'+href+'">'+cta+'</a></div></div></section>'
def section(title,text):return '<section class="wrap section"><h2>'+title+'</h2>'+text+'</section>'
def card(title,text,cta,href):return '<article class="card"><h3>'+title+'</h3>'+text+'<a class="button" href="'+href+'">'+cta+'</a></article>'
pages={}
from final_content import apply
apply(pages,hero,section,card)
out.mkdir(exist_ok=True)
for slug,(title,desc,body) in pages.items():
    target=out/slug/'index.html' if slug not in ('','404') else out/('404.html' if slug=='404' else 'index.html')
    target.parent.mkdir(exist_ok=True,parents=True);target.write_text(shell(slug,title,desc,body))
(out/'style.css').write_text((root/'style-reference.css').read_text())
(out/'site.js').write_text((root/'site-script.js').read_text())
(out/'_redirects').write_text('/investors-move /our-businesses/ 301\n/investors-move/ /our-businesses/ 301\n/media-data /our-businesses/ 301\n/media-data/ /our-businesses/ 301\n')
(out/'_headers').write_text('/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  X-Frame-Options: SAMEORIGIN\n')
routes=['/' if s=='' else '/'+s+'/' for s in pages if s not in ['404','thank-you']]
(out/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://ritchventures.com/sitemap.xml\n')
(out/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>https://ritchventures.com'+s+'</loc></url>' for s in sorted(routes))+'</urlset>')
(root/'netlify.toml').write_text('[build]\n  publish = "dist"\n')
print('Built',len(pages),'Netlify-ready pages.')
