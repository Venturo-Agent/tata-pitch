#!/usr/bin/env python3
# 一次性頁面產生器：以 index.html 的 header/footer 為母版，產出各分頁靜態 HTML。
# 之後若改 header/footer，改 index.html 再重跑此腳本即可同步。
import re, pathlib

root = pathlib.Path("/Users/williamchien/Projects/agency/tata-pitch")
src = (root / "index.html").read_text(encoding="utf-8")

header = src[: src.index("<!-- ============ Hero")]
footer = src[src.index("<!-- ============ Footer"):]

def make(slug, title, desc, content, extra_js=""):
    page = header + content + footer
    page = page.replace(
        "<title>台北市旅行商業同業公會 TATA｜凝聚旅行產業力量</title>",
        f"<title>{title}</title>")
    page = re.sub(
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{desc}">', page, count=1)
    if extra_js:
        page = page.replace('<script src="assets/js/main.js"></script>',
                            f'<script src="assets/js/main.js"></script>\n<script src="{extra_js}"></script>')
    (root / slug).write_text(page, encoding="utf-8")
    print("written", slug)

def hero(crumb, h1, lead):
    return f"""
<section class="page-hero">
  <div class="wrap">
    <p class="page-hero__crumb"><a href="index.html">首頁</a> ／ {crumb}</p>
    <h1>{h1}</h1>
    <p class="page-hero__lead">{lead}</p>
  </div>
</section>
"""

import calendar as _cal
def mini_cal(y, m, single=(), rng=()):
    """產生一個小月曆 HTML：single=單日活動、range=連續活動日"""
    cal = _cal.Calendar(firstweekday=6)
    weeks = cal.monthdayscalendar(y, m)
    head = "".join(f"<th>{d}</th>" for d in ["日","一","二","三","四","五","六"])
    body = ""
    for wk in weeks:
        tds = ""
        for d in wk:
            if d == 0:
                tds += "<td></td>"
            elif d in single:
                tds += f'<td class="is-event">{d}</td>'
            elif d in rng:
                tds += f'<td class="is-range">{d}</td>'
            else:
                tds += f"<td>{d}</td>"
        body += f"<tr>{tds}</tr>"
    return f'<div class="mini-cal"><h3>{y} 年 {m} 月</h3><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'



TEAM_SECTION = pathlib.Path("/tmp/tata-audit/team-section.html").read_text(encoding="utf-8")
TEAM_INNER = TEAM_SECTION[TEAM_SECTION.index('<div class="wrap">'):TEAM_SECTION.rindex('</section>')]
TEAM_INNER = TEAM_INNER.replace('<div class="wrap">', '', 1)
TEAM_INNER = TEAM_INNER.rsplit('</div>', 1)[0]
TEAM_INNER = TEAM_INNER.replace('<h2>領航團隊</h2>', '<h2 class="sub-title" style="margin-top:3.5rem">領航團隊</h2>')

# ---------------- about.html ----------------
about = hero("公會介紹", "台灣旅行產業的核心力量",
    "台北市旅行商業同業公會自 1969 年成立，凝聚超過 1,400 家會員旅行社，推動台灣觀光競爭力、產業數位轉型與國際合作。") + """
<section class="page-section page-section--paper anchor-block" id="intro">
  <div class="wrap">
    <h2 class="sub-title">公會簡介</h2>
    <p class="sub-lead">台北市旅行商業同業公會自 1969 年成立，致力凝聚旅行業界力量，提升台灣觀光競爭力，並積極推動產業數位轉型與國際合作。超過半世紀的產業深耕，TATA 是台灣最大的旅行產業組織，也是業者最堅實的後盾。</p>
    <div class="ruled-list ruled-list--2col" style="margin-top:2.5rem">
      <div class="ruled-item"><span class="ruled-item__no">01</span><div><h3>凝聚產業力量</h3><p>整合超過 1,400 家旅行社，形成台灣最強大的旅遊產業共同體，共同面對市場挑戰。</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">02</span><div><h3>提升觀光競爭力</h3><p>透過 TTE 旅展、教育訓練及政策倡議，全面提升台灣觀光產業的國際競爭力。</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">03</span><div><h3>推動數位轉型</h3><p>導入 AI 技術與數位工具，協助旅行業者實現智能化營運，接軌全球數位旅遊趨勢。</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">04</span><div><h3>促進國際交流</h3><p>積極參與國際旅遊組織，連結全球夥伴，拓展台灣旅遊業的國際視野與商機。</p></div></div>
    </div>
  </div>
</section>

<section class="page-section anchor-block chairman-sec" id="chairman">
  <div class="wrap">
    <h2 class="sub-title">理事長介紹</h2>
    <div class="chairman-intro" style="display:grid;grid-template-columns:320px 1fr;gap:3rem;align-items:start;margin-top:1.5rem">
      <figure style="margin:0"><img src="assets/img/chairman.jpg" alt="台北市旅行商業同業公會理事長" style="width:100%;border-radius:12px;display:block"></figure>
      <div>
    <p class="sub-lead" style="font-size:1.3rem;color:var(--ink);font-weight:500">「深耕旅行產業，開創數位新局。」</p>
    <p class="sub-lead">理事長深耕旅行產業逾三十年，帶領公會推動數位轉型與國際布局，串連十八個專業委員會，與超過 1,400 家會員旅行社共同打造台灣旅遊生態圈。</p>
    <dl style="margin-top:2rem;border-top:2px solid var(--navy-900)">
      <div class="def-row"><dt>公會歷史</dt><dd>55+ 年（1969 年成立）</dd></div>
      <div class="def-row"><dt>產業資歷</dt><dd>深耕旅行產業逾 30 年</dd></div>
      <div class="def-row"><dt>督導編制</dt><dd>18 個專業委員會</dd></div>
    </dl>
      </div>
    </div>
  </div>
</section>

""" + TEAM_SECTION + """


<section class="page-section page-section--paper anchor-block" id="org">
  <div class="wrap">
    <h2 class="sub-title">公會組織</h2>
    <p class="sub-lead">公會以會員大會為最高權力機構，下設理事會、監事會與秘書處，並依業務領域設置專業委員會。</p>
    <div class="org-tree" style="margin-top:2.5rem">
      <div class="org-tree__root">會員大會</div>
      <div class="org-tree__stem"></div>
      <div class="org-tree__row">
        <div class="org-tree__node"><h3>理事會</h3><p>會務決策與執行監督，理事長對外代表公會</p></div>
        <div class="org-tree__node"><h3>監事會</h3><p>督導會務與財務，守護會員權益</p></div>
        <div class="org-tree__node"><h3>秘書處</h3><p>日常會務執行，串連各委員會運作</p></div>
        <div class="org-tree__node"><h3>18 個專業委員會</h3><p>涵蓋各旅遊業務領域的專業分工</p></div>
      </div>
    </div>
    """ + TEAM_INNER + """
  </div>
</section>

<section class="page-section anchor-block" id="committees">
  <div class="wrap">
    <h2 class="sub-title">專業委員會</h2>
    <p class="sub-lead">十八個專業委員會涵蓋旅行產業各業務領域，由業界資深實務者擔任主委，推動專業分工與政策倡議。（以下為示範編制，正式名單以公會公告為準）</p>
    <div class="ruled-list ruled-list--2col" style="margin-top:2.5rem">
      <div class="ruled-item"><span class="ruled-item__no">01</span><div><h3>國際線業務委員會</h3><p>出境旅遊市場與國際線業務發展</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">02</span><div><h3>兩岸業務委員會</h3><p>兩岸旅遊交流與業務推動</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">03</span><div><h3>國民旅遊委員會</h3><p>國內旅遊市場與在地體驗開發</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">04</span><div><h3>入境旅遊委員會</h3><p>來台旅客接待與國際市場開拓</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">05</span><div><h3>票務委員會</h3><p>航空票務實務與同業協調</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">06</span><div><h3>領隊導遊委員會</h3><p>領隊導遊考照輔導與權益維護</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">07</span><div><h3>教育訓練委員會</h3><p>從業人員培訓課程規劃</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">08</span><div><h3>數位發展委員會</h3><p>AI 工具導入與數位服務平台</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">09</span><div><h3>法規委員會</h3><p>旅行業法規研究與政策建議</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">10</span><div><h3>會員服務委員會</h3><p>入會申請、年費與會員權益</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">11</span><div><h3>財務委員會</h3><p>公會財務規劃與預算監督</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">12</span><div><h3>公共關係委員會</h3><p>媒體關係與產業形象</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">13</span><div><h3>旅展籌備委員會</h3><p>TTE 台北國際旅展籌劃執行</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">14</span><div><h3>青年發展委員會</h3><p>青年創業與新世代人才培育</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">15</span><div><h3>永續旅遊委員會</h3><p>永續觀光與 ESG 實踐</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">16</span><div><h3>電子商務委員會</h3><p>線上銷售與數位行銷</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">17</span><div><h3>郵輪旅遊委員會</h3><p>郵輪市場與包船業務</p></div></div>
      <div class="ruled-item"><span class="ruled-item__no">18</span><div><h3>觀光推廣委員會</h3><p>城市觀光行銷與國際推廣</p></div></div>
    </div>
  </div>
</section>

<section class="page-section page-section--paper anchor-block" id="secretariat">
  <div class="wrap">
    <h2 class="sub-title">秘書處</h2>
    <dl style="margin-top:1.5rem;border-top:2px solid var(--navy-900)">
      <div class="def-row"><dt>會址</dt><dd>台北市中山區四平街 20 號 6 樓</dd></div>
      <div class="def-row"><dt>電話</dt><dd><a href="tel:+886225312191">(02) 2531-2191</a></dd></div>
      <div class="def-row"><dt>電子郵件</dt><dd><a href="mailto:service@tata.org.tw">service@tata.org.tw</a></dd></div>
      <div class="def-row"><dt>服務時間</dt><dd>週一至週五 08:30–17:30</dd></div>
    </dl>
    <p style="margin-top:2rem"><a href="contact.html" class="btn btn--gold">聯絡秘書處</a></p>
  </div>
</section>
"""
make("about.html", "公會介紹｜台北市旅行商業同業公會 TATA",
     "TATA 公會簡介、理事長介紹、公會組織、十八個專業委員會與秘書處聯絡資訊。", about)

# ---------------- news.html ----------------
NEWS = [
    ("2026-06-15", "event", "活動消息", "2026 TTE 台北國際旅展 正式啟動報名！", "年度最盛大旅遊展覽即將登場，超過 200 個攤位，匯集全球旅遊品牌，歡迎旅行社會員踴躍報名參展。"),
    ("2026-06-12", "guild", "公會訊息", "AI 數位轉型工作坊 第三期報名開始", "協助業者導入 AI 行程規劃、智能客服與自動化行銷工具，名額有限。"),
    ("2026-06-10", "industry", "產業資訊", "觀光署公布 2026 上半年入境旅客統計", "上半年入境旅客持續回溫，東北亞與東南亞市場成長最為顯著。"),
    ("2026-06-08", "official", "公會公文", "115 年度第二次理監事聯席會議紀錄", "會議紀錄已建檔，會員如需調閱請洽秘書處。"),
    ("2026-06-05", "media", "新聞媒體", "TATA 與新加坡旅遊業協會簽署 MOU", "雙方將就會展旅遊、人才交流與數位轉型展開深度合作。"),
    ("2026-06-01", "guild", "公會訊息", "2026 年度會費繳納公告", "請各會員旅行社於期限內完成年度會費繳納，線上繳費系統同步開放。"),
    ("2026-05-28", "tourism", "觀光新訊", "台灣燈會觀光效益評估出爐", "大型節慶活動帶動周邊住宿與交通需求，旅行同業可提前布局。"),
    ("2026-05-22", "event", "活動消息", "日韓旅遊業者 B2B 採購商談 開放報名", "與日韓業者面對面洽談，創造最新合作機會。"),
    ("2026-05-18", "official", "公會公文", "轉知觀光署修正旅行業管理規則部分條文", "相關條文修正內容與因應建議，請會員業者留意。"),
    ("2026-05-15", "industry", "產業資訊", "航空票價與燃油附加費趨勢分析", "國際油價波動對票價結構的影響評估，提供業者訂價參考。"),
    ("2026-05-10", "media", "新聞媒體", "本會理事長接受媒體專訪：談台灣觀光下一個十年", "從數位轉型到永續旅遊，台灣旅行產業的關鍵布局。"),
    ("2026-05-06", "tourism", "觀光新訊", "郵輪旅遊市場回溫，基隆港泊位需求創新高", "郵輪復甦帶動包船與岸上觀光商機。"),
]
rows = "\n".join(
    f'''      <a href="{'doc.html' if c == 'official' else 'news.html'}" class="news-row" data-cat="{c}">
        <span class="news-row__date">{d}</span>
        <span class="news-row__cat">{t}</span>
        <span class="news-row__title">{ti}<span class="m-sub" style="font-weight:400;color:var(--muted);font-size:0.85rem;display:block;margin-top:2px">{de}</span></span>
        <span class="news-row__arrow">→</span>
      </a>''' for (d, c, t, ti, de) in NEWS)
news = hero("最新消息", "最新消息", "公會訊息、公文、活動消息與產業資訊，一手掌握旅行產業脈動。") + f"""
<section class="page-section page-section--paper">
  <div class="wrap">
    <div class="filter-pills" id="newsPills">
      <button type="button" data-cat="all" class="is-active">全部</button>
      <button type="button" data-cat="guild">公會訊息</button>
      <button type="button" data-cat="official">公會公文</button>
      <button type="button" data-cat="event">活動消息</button>
      <button type="button" data-cat="media">新聞媒體</button>
      <button type="button" data-cat="industry">產業資訊</button>
      <button type="button" data-cat="tourism">觀光新訊</button>
    </div>
    <div id="newsList">
{rows}
    </div>
  </div>
</section>
<script>
(function () {{
  var pills = document.querySelectorAll("#newsPills button");
  var rows = document.querySelectorAll("#newsList .news-row");
  function apply(cat) {{
    pills.forEach(function (b) {{ b.classList.toggle("is-active", b.dataset.cat === cat); }});
    rows.forEach(function (r) {{ r.style.display = (cat === "all" || r.dataset.cat === cat) ? "" : "none"; }});
  }}
  pills.forEach(function (b) {{ b.addEventListener("click", function () {{ apply(b.dataset.cat); }}); }});
  var q = new URLSearchParams(location.search).get("cat");
  if (q && document.querySelector('#newsPills button[data-cat="' + q + '"]')) apply(q);
}})();
</script>
"""
make("news.html", "最新消息｜台北市旅行商業同業公會 TATA",
     "TATA 公會訊息、公會公文、活動消息、新聞媒體、產業資訊與觀光新訊。", news)

# ---------------- events.html ----------------
EVENTS = [
    ("tte", "旅展", "11<span>月</span>", "06<i>–09</i>", "2026-11-06 ～ 11-09", "2026 TTE 台北國際旅展", "台北世界貿易中心", "500 / 600 人已報名 · 名額剩餘 100 位", "0.83", "2026-11-06", "2026-11-09"),
    ("training", "教育訓練", "08<span>月</span>", "21", "2026-08-21", "AI 數位轉型工作坊 第三期", "TATA 公會大樓", "28 / 40 人已報名 · 名額剩餘 12 位", "0.70", "2026-08-21", "2026-08-21"),
    ("forum", "產業論壇", "09<span>月</span>", "18", "2026-09-18", "2026 台灣旅遊業永續發展峰會", "台大醫院國際會議中心", "180 / 250 人已報名 · 名額剩餘 70 位", "0.72", "2026-09-18", "2026-09-18"),
    ("b2b", "B2B 商談會", "10<span>月</span>", "15<i>–16</i>", "2026-10-15 ～ 10-16", "日韓旅遊業者 B2B 採購商談", "圓山大飯店", "62 / 80 人已報名 · 名額剩餘 18 位", "0.78", "2026-10-15", "2026-10-16"),
]
PIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
ev_rows = "\n".join(
    f'''      <li class="event-row" data-cat="{cat}">
        <div class="event-row__date"><span class="event-row__month">{mon}</span><span class="event-row__day">{day}</span></div>
        <div class="event-row__main">
          <p class="event-row__meta"><span class="tag tag--gold">{tag}</span>{datestr}</p>
          <h3>{title}</h3>
          <p class="event-row__venue">{PIN}{venue}</p>
        </div>
        <div class="event-row__reg">
          <div class="progress" style="--p:{p}"><span class="progress__track"><span class="progress__fill"></span></span>
            <p class="progress__text">{reg}</p></div>
          <p class="event-row__count" data-start="{ds}" data-end="{de}"></p>
        </div>
        <div class="event-row__actions">
          <a href="contact.html#join" class="btn btn--ghost-gold">立即報名</a>
        </div>
      </li>''' for (cat, tag, mon, day, datestr, title, venue, reg, p, ds, de) in EVENTS)
events = hero("活動專區", "活動專區", "近期活動、教育訓練、產業論壇、B2B 商談——每月精彩活動不間斷。") + f"""
<section class="page-section page-section--navy">
  <div class="wrap">
    <div class="filter-pills" id="evPills">
      <button type="button" data-cat="all" class="is-active">全部</button>
      <button type="button" data-cat="tte">旅展</button>
      <button type="button" data-cat="training">教育訓練</button>
      <button type="button" data-cat="forum">產業論壇</button>
      <button type="button" data-cat="b2b">B2B 商談會</button>
    </div>
    <ul class="event-list" id="evList" style="list-style:none">
{ev_rows}
    </ul>
  </div>
</section>

<section class="page-section anchor-block" id="tte">
  <div class="wrap">
    <h2 class="sub-title">TTE 台北國際旅展</h2>
    <p class="sub-lead">年度最盛大的旅遊展覽，超過 200 個攤位，匯集全球旅遊品牌。TTE 台北國際旅展由本會主辦，是台灣旅行產業與消費者之間最大的年度橋樑，也是會員旅行社年度最重要的曝光與銷售舞台。</p>
    <div class="info-grid" style="margin-top:2rem">
      <div class="info-card"><span class="info-card__tag">200+</span><h3>參展攤位</h3><p>匯集全球旅遊品牌、航空公司、飯店與觀光局。</p></div>
      <div class="info-card"><span class="info-card__tag">2026-11-06 ～ 11-09</span><h3>展期</h3><p>台北世界貿易中心，為期四天。</p></div>
      <div class="info-card"><span class="info-card__tag">會員優先</span><h3>參展報名</h3><p>會員旅行社享有攤位優先選位與報名優惠。</p></div>
    </div>
    <p style="margin-top:2rem"><a href="contact.html#join" class="btn btn--gold">洽詢參展</a></p>
  </div>
</section>

<section class="page-section page-section--paper anchor-block" id="calendar">
  <div class="wrap">
    <h2 class="sub-title">活動月曆</h2>
    <div class="cal-split" style="margin-top:1.5rem">
      <div class="mini-cals">
        """ + mini_cal(2026, 8, single=(21,)) + """
        """ + mini_cal(2026, 9, single=(18,)) + """
        """ + mini_cal(2026, 10, rng=(15, 16)) + """
        """ + mini_cal(2026, 11, rng=(6, 7, 8, 9)) + """
      </div>
      <div class="cal-rows">
        <div class="cal-row"><div class="cal-row__date">08.21<small>週五</small></div><div><h3>AI 數位轉型工作坊 第三期</h3><p>教育訓練 · TATA 公會大樓</p></div><a href="contact.html#join" class="btn btn--gold">報名</a></div>
        <div class="cal-row"><div class="cal-row__date">09.18<small>週五</small></div><div><h3>2026 台灣旅遊業永續發展峰會</h3><p>產業論壇 · 台大醫院國際會議中心</p></div><a href="contact.html#join" class="btn btn--gold">報名</a></div>
        <div class="cal-row"><div class="cal-row__date">10.15<small>週四–五</small></div><div><h3>日韓旅遊業者 B2B 採購商談</h3><p>B2B 商談會 · 圓山大飯店 · 10/15–10/16</p></div><a href="contact.html#join" class="btn btn--gold">報名</a></div>
        <div class="cal-row"><div class="cal-row__date">11.06<small>週五–一</small></div><div><h3>2026 TTE 台北國際旅展</h3><p>旅展 · 台北世界貿易中心 · 11/06–11/09</p></div><a href="contact.html#join" class="btn btn--gold">報名</a></div>
      </div>
    </div>
  </div>
</section>
<script>
(function () {{
  var pills = document.querySelectorAll("#evPills button");
  var rows = document.querySelectorAll("#evList .event-row");
  function apply(cat) {{
    pills.forEach(function (b) {{ b.classList.toggle("is-active", b.dataset.cat === cat); }});
    rows.forEach(function (r) {{ r.style.display = (cat === "all" || r.dataset.cat === cat) ? "" : "none"; }});
  }}
  pills.forEach(function (b) {{ b.addEventListener("click", function () {{ apply(b.dataset.cat); }}); }});
  var q = new URLSearchParams(location.search).get("cat");
  if (q && document.querySelector('#evPills button[data-cat="' + q + '"]')) apply(q);
}})();
</script>
"""
make("events.html", "活動專區｜台北市旅行商業同業公會 TATA",
     "TATA 近期活動、TTE 台北國際旅展、教育訓練、產業論壇、B2B 商談會與活動月曆。", events)

# ---------------- services.html ----------------
SVC = [
    ("ai-service", "AI 客服", "24 小時智能客服", "24 小時智能客服，即時解答會員法規、活動、會務問題。結合公會知識庫與 AI 問答，會員隨時提問、即時獲得正確解答，秘書處服務量能倍增。"),
    ("ai-secretary", "AI 會員秘書", "一站式 AI 賦能服務", "AI 行程規劃、智能客服、自動化行銷、影音剪輯——一站式 AI 賦能服務平台，協助會員旅行社以最低成本導入最新 AI 工具。"),
    ("newsletter", "電子月刊", "每月產業精華直送信箱", "TATA 電子月刊每月出刊，精選產業動態、法規更新、活動預告與會員故事，直送會員信箱。"),
    ("podcast", "Podcast", "旅遊產業深度對話", "TATA Podcast 邀請產業領袖、學者與實務者深度對談，從 AI 革命到市場趨勢，隨時隨地掌握旅行產業脈動。Spotify、Apple Podcast、Google Podcast、SoundOn 同步上架。"),
    ("video", "影音中心", "活動花絮 × 會員故事", "旅展精彩回顧、會員轉型故事、教育訓練精華片段，以影音記錄產業的每一步前進。"),
]
svc_blocks = "\n".join(
    f'''<section class="page-section{' page-section--paper' if i % 2 else ''} anchor-block" id="{sid}">
  <div class="wrap">
    <h2 class="sub-title">{name}</h2>
    <p class="sub-lead" style="font-size:1.15rem;color:var(--ink);font-weight:500">{tag}</p>
    <p class="sub-lead">{desc}</p>
    <p style="margin-top:1.5rem"><a href="contact.html" class="btn btn--gold">洽詢開通</a></p>
  </div>
</section>''' for i, (sid, name, tag, desc) in enumerate(SVC))
services = hero("數位服務", "數位服務", "AI 客服、電子月刊、Podcast、影音中心、AI 會員秘書——TATA 的數位服務平台，協助會員接軌全球數位旅遊趨勢。") + svc_blocks
make("services.html", "數位服務｜台北市旅行商業同業公會 TATA",
     "TATA 數位服務：AI 客服、AI 會員秘書、電子月刊、Podcast、影音中心。", services)

# ---------------- partners.html ----------------
partners = hero("異業合作", "異業合作", "攜手全球頂尖航空、飯店、郵輪品牌及觀光機構，共同打造台灣旅遊生態圈。") + """
<section class="page-section page-section--paper">
  <div class="wrap">
    <h2 class="sub-title">國際合作夥伴</h2>
    <p class="sub-lead">航空公司、飯店集團、郵輪公司與觀光機構，與 TATA 長期攜手。（以下為合作類別示範名單）</p>
    <div class="info-grid" style="margin-top:2rem">
      <div class="info-card"><span class="info-card__tag">航空公司（10）</span><h3>華航 · 長榮 · 星宇 · 台虎</h3><p>中華航空、長榮航空、星宇航空、台灣虎航、日本航空、全日本空輸、新加坡航空、國泰航空、韓亞航空、大韓航空。</p></div>
      <div class="info-card"><span class="info-card__tag">飯店集團（8）</span><h3>晶華 · 君悅 · 萬豪 · 希爾頓</h3><p>晶華酒店、君悅大飯店、萬豪國際、希爾頓集團、洲際酒店、凱悅集團、四季酒店、香格里拉。</p></div>
      <div class="info-card"><span class="info-card__tag">郵輪 · 觀光機構</span><h3>郵輪公司與各國觀光局</h3><p>國際郵輪品牌與各國觀光推廣機構，共同開發台灣出境與入境市場。</p></div>
    </div>
  </div>
</section>

<section class="page-section anchor-block" id="ad">
  <div class="wrap contact2">
    <div class="contact2__info">
      <h2 class="sub-title">廣告刊登</h2>
      <p class="sub-lead">在 TATA 官網、月刊、電子報觸及台灣最大旅行業受眾群體——超過 1,400 家旅行社的決策者與從業人員。</p>
      <dl style="margin-top:1.5rem;border-top:2px solid var(--navy-900)">
        <div class="def-row"><dt>官網橫幅</dt><dd>首頁與消息頁版位，月曝光另計</dd></div>
        <div class="def-row"><dt>電子月刊</dt><dd>每月直送全體會員信箱</dd></div>
        <div class="def-row"><dt>活動贊助</dt><dd>旅展、論壇、教育訓練現場曝光</dd></div>
      </dl>
      <h2 class="sub-title anchor-block" id="proposal" style="margin-top:3rem">合作提案</h2>
      <p class="sub-lead">科技、金融、保險、法律等異業品牌，歡迎提出合作構想。提案經秘書處初審後，將安排與相關委員會進一步洽談。</p>
      <dl style="margin-top:1.5rem;border-top:2px solid var(--navy-900)">
        <div class="def-row"><dt>提案流程</dt><dd>送出提案 → 秘書處初審 → 委員會洽談</dd></div>
        <div class="def-row"><dt>回覆時程</dt><dd>五個工作天內回覆</dd></div>
      </dl>
    </div>
    <form class="contact2__form" action="partners.html#proposal" method="get">
      <div class="field"><label for="p-name">公司名稱</label><input id="p-name" type="text" placeholder="請輸入公司名稱"></div>
      <div class="field"><label for="p-person">聯絡人</label><input id="p-person" type="text" placeholder="請輸入聯絡人姓名"></div>
      <div class="field"><label for="p-mail">Email</label><input id="p-mail" type="email" placeholder="name@example.com"></div>
      <div class="field"><label for="p-type">合作類型</label><select id="p-type"><option>廣告刊登</option><option>異業合作</option><option>活動贊助</option><option>其他</option></select></div>
      <div class="field"><label for="p-msg">合作構想</label><textarea id="p-msg" placeholder="請簡述您的合作構想"></textarea></div>
      <div><button type="submit" class="btn btn--gold">送出提案</button><p class="form-note">示範站表單尚未串接後端，正式站將串接秘書處收件流程。</p></div>
    </form>
  </div>
</section>
"""
make("partners.html", "異業合作｜台北市旅行商業同業公會 TATA",
     "TATA 國際合作夥伴、廣告刊登與異業合作提案。", partners)

# ---------------- contact.html ----------------
contact = hero("聯絡我們", "聯絡我們", "週一至週五 08:30–17:30，秘書處竭誠為您服務。") + """
<section class="page-section page-section--paper">
  <div class="wrap contact2">
    <div class="contact2__info">
      <h2 class="sub-title">聯絡我們</h2>
      <p class="sub-lead">無論是入會申請、活動報名、法規諮詢或合作提案，秘書處都竭誠為您服務。週一至週五 08:30–17:30，來電或來信都可以。</p>
      <p class="contact2__meta">
        <a href="mailto:service@tata.org.tw">service@tata.org.tw</a><i></i><a href="tel:+886225312191">(02) 2531-2191</a><i></i>台北市中山區四平街 20 號 6 樓
      </p>
      <div class="contact2__map" aria-hidden="true">
        <div class="contact2__map-frame">
        <img class="contact2__map-img" src="assets/img/world-dots.svg" alt="">
        <div class="cpin">
          <span class="cpin__label">我們在這裡 · 台北</span>
          <span class="cpin__beam"></span>
          <span class="cpin__ring"></span>
          <span class="cpin__ring cpin__ring--2"></span>
          <span class="cpin__ring cpin__ring--3"></span>
          <span class="cpin__dot"></span>
        </div>
        </div>
      </div>
    </div>
    <form class="contact2__form" action="contact.html" method="get">
      <div class="field"><label for="c-name">姓名</label><input id="c-name" type="text" placeholder="請輸入姓名"></div>
      <div class="field"><label for="c-mail">Email</label><input id="c-mail" type="email" placeholder="name@example.com"></div>
      <div class="field"><label for="c-comp">公司／旅行社名稱</label><input id="c-comp" type="text" placeholder="請輸入公司或旅行社名稱"></div>
      <div class="field"><label for="c-msg">訊息內容</label><textarea id="c-msg" placeholder="請輸入您想洽詢的內容"></textarea></div>
      <div><button type="submit" class="btn btn--gold">送出訊息</button><p class="form-note">示範站表單尚未串接後端，正式站將串接秘書處收件流程。</p></div>
    </form>
  </div>
</section>

<section class="page-section page-section--paper anchor-block" id="join">
  <div class="wrap" style="max-width:760px">
    <h2 class="sub-title">入會申請</h2>
    <p class="sub-lead">加入超過 1,400 家旅行社的行列，享受完整公會資源與服務。填寫下列資料，秘書處將於三個工作天內與您聯繫。</p>
    <form class="form-grid" style="margin-top:2rem" action="contact.html#join" method="get">
      <div class="field"><label for="j-comp">公司名稱</label><input id="j-comp" type="text" placeholder="請輸入旅行社公司名稱"></div>
      <div class="field"><label for="j-tax">統一編號</label><input id="j-tax" type="text" placeholder="請輸入統一編號"></div>
      <div class="field"><label for="j-boss">負責人</label><input id="j-boss" type="text" placeholder="請輸入負責人姓名"></div>
      <div class="field"><label for="j-tel">聯絡電話</label><input id="j-tel" type="tel" placeholder="02-0000-0000"></div>
      <div class="field is-full"><label for="j-mail">Email</label><input id="j-mail" type="email" placeholder="name@example.com"></div>
      <div class="field is-full"><label for="j-msg">備註</label><textarea id="j-msg" placeholder="其他想說明的事項（選填）"></textarea></div>
      <div class="is-full"><button type="submit" class="btn btn--gold">送出申請</button><p class="form-note">示範站表單尚未串接後端，正式站將串接秘書處收件流程。</p></div>
    </form>
  </div>
</section>
"""
make("contact.html", "聯絡我們｜台北市旅行商業同業公會 TATA",
     "聯絡 TATA 秘書處：會址、電話、電子郵件、線上聯絡與入會申請。", contact)

# ---------------- members.html ----------------
members = hero("會員名錄", "會員名錄", "超過 1,400 家會員旅行社的公開名錄，可依公司名稱、行政區、營業範圍搜尋篩選。（公開商業名錄，非私人個資）") + """
<section class="page-section page-section--paper">
  <div class="wrap">
    <div class="members-toolbar">
      <input type="search" id="mSearch" placeholder="搜尋公司名稱、負責人、電話…" aria-label="搜尋會員">
      <select id="mDistrict" aria-label="依行政區篩選"><option value="">全部行政區</option></select>
      <select id="mScope" aria-label="依營業範圍篩選"><option value="">全部營業範圍</option></select>
      <span class="members-count" id="mCount"></span>
    </div>
    <div class="table-wrap">
      <table class="member-table">
        <thead><tr><th>公司名稱</th><th>行政區</th><th>營業範圍</th><th>電話</th><th>入會日期</th><th>網站</th></tr></thead>
        <tbody id="mRows"></tbody>
      </table>
    </div>
    <div class="pager" id="mPager"></div>
  </div>
</section>
"""
make("members.html", "會員名錄｜台北市旅行商業同業公會 TATA",
     "TATA 會員旅行社公開名錄，1,400+ 家會員可依名稱、行政區、營業範圍搜尋篩選。", members,
     extra_js="assets/js/members.js")


# ---------------- doc.html（公文閱讀頁） ----------------
doc = hero("公會公文", "公會公文", "公文全文線上閱讀，附件可直接下載，不再只是一個 PDF 分頁。") + """
<section class="page-section page-section--paper">
  <div class="wrap" style="max-width:820px">
    <a class="doc-back" href="news.html?cat=official">← 返回公文列表</a>
    <article class="doc-sheet">
      <p class="doc-sheet__no">發文字號：旅北市商字第 1150608 號</p>
      <h1>115 年度第二次理監事聯席會議紀錄</h1>
      <dl class="doc-sheet__meta">
        <div class="def-row"><dt>發文日期</dt><dd>2026 年 6 月 8 日</dd></div>
        <div class="def-row"><dt>公文類別</dt><dd>會議紀錄</dd></div>
        <div class="def-row"><dt>聯絡窗口</dt><dd>秘書處 (02) 2531-2191</dd></div>
      </dl>
      <h3>主旨</h3>
      <p>檢送本會 115 年度第二次理監事聯席會議紀錄乙份，請查照。</p>
      <h3>說明</h3>
      <p>一、本次會議於 115 年 6 月 5 日下午二時假本會會議室召開，由理事長親自主持，應出席理監事 27 人，實際出席 24 人，符合法定開會人數。</p>
      <p>二、重要決議事項：（一）通過 2026 TTE 台北國際旅展籌備進度報告；（二）通過 AI 數位轉型服務平台第二期預算；（三）通過新入會會員資格審查名單；（四）追認本會 115 年度第一季財務報表。</p>
      <p>三、會員如需調閱完整會議紀錄或提案列入下次議程，請於每月 20 日前以書面或電子郵件洽秘書處辦理。</p>
      <div class="doc-attach">
        <span>附件：115年度第二次理監事聯席會議紀錄.pdf</span>
        <button type="button" class="btn btn--gold">下載 PDF</button>
      </div>
      <p class="form-note" style="margin-top:1rem">示範站公文內容為示意，正式站由後台發布、附件自動上傳。</p>
    </article>
  </div>
</section>
"""
make("doc.html", "公會公文｜台北市旅行商業同業公會 TATA",
     "TATA 公會公文線上閱讀：發文字號、主旨、說明與附件下載。", doc)

# ---------------- legal.html ----------------
legal = hero("法務資訊", "隱私政策與使用條款", "本頁為設計提案示範（Redesign Concept），非 TATA 官方網站。") + """
<section class="page-section page-section--paper">
  <div class="wrap" style="max-width:760px">
    <h2 class="sub-title">隱私政策</h2>
    <p class="sub-lead">本示範站不蒐集、不儲存任何使用者個人資料。頁面中的表單僅為設計展示，送出的資料不會傳輸或保存。正式網站上線前，應依個人資料保護法訂定完整隱私政策，載明資料蒐集之目的、利用範圍、保存期限與當事人權利。</p>
    <h2 class="sub-title anchor-block" id="terms" style="margin-top:3rem">使用條款</h2>
    <p class="sub-lead">本示範站內容（含文字、圖片、數據）僅供重新設計提案展示使用，部分內容為示意性質，正式資訊以台北市旅行商業同業公會官方公告為準。未經許可，不得轉載或作其他用途。</p>
  </div>
</section>
"""
make("legal.html", "隱私政策與使用條款｜台北市旅行商業同業公會 TATA",
     "TATA 示範站隱私政策與使用條款。", legal)

print("ALL DONE")
