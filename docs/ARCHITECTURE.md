# TATA 示範站 — 後台與 API 架構交接文件

> 目的：這份文件讓接手開發者（或公會資訊廠商）能在不重做的前提下，把目前的靜態示範站升級成「有後台、有資料庫」的正式站。
> 現況：純靜態站（HTML/CSS/JS，無 build step），資料放在 `assets/data/*.json`。
> 共識（William 2026-07-22）：會員名錄等公開資料未來放 **Supabase**（不放 Google Sheets）。

## 1. 站點地圖（Site Map）

| 頁面 | 檔案 | 內容來源（現況） | 未來資料表 |
|---|---|---|---|
| 首頁 | `index.html` | 寫死在 HTML | 各表彙整 |
| 公會介紹 | `about.html` | 寫死在 HTML | `pages`（靜態內容） |
| 最新消息 | `news.html` | 寫死在 HTML＋前端篩選 | `news` |
| 活動專區 | `events.html` | 寫死在 HTML（倒數由 data 屬性計算） | `events` |
| 數位服務 | `services.html` | 寫死在 HTML | `pages` |
| 異業合作 | `partners.html` | 寫死在 HTML＋提案表單 | `partners`、`inquiries` |
| 會員名錄 | `members.html` | `assets/data/members.json`（1,459 筆） | `members` |
| 聯絡我們 | `contact.html` | 表單 ×3（聯絡、入會、提案） | `inquiries` |
| 公文閱讀頁 | `doc.html` | 寫死在 HTML（公文結構：字號/主旨/說明/附件） | `news`（body 呈現＋attachment 欄位） |
| 法務 | `legal.html` | 寫死在 HTML | — |

共用母版：header/footer 與 `index.html` 相同；若需修改，改 `index.html` 後重跑 `tools/genpages.py`（見第 6 節）。

## 2. 現況資料流

```
tata_members.csv（爬蟲產出，travel/同業名錄-TATA/）
  → tools/csv 轉 JSON（已執行）
  → assets/data/members.json（700KB，1,459 筆，含 meta/cities/scopes/members）
  → members.html 的 assets/js/members.js 前端 fetch → 搜尋/篩選/分頁（每頁 50 筆）
```

**API-ready 設計**：`members.js` 只依賴 JSON 的形狀（`{ meta, cities, scopes, members[] }`）。未來只要把 `DATA_URL` 從 `assets/data/members.json` 換成 Supabase REST endpoint，前端不用改。

### members 物件欄位（= 未來 API 回應形狀）

| 欄位 | 型別 | 說明 |
|---|---|---|
| `id` | int | 流水號 |
| `name` / `name_en` | text | 公司中英文名稱 |
| `boss` / `rep` | text | 負責人、會員代表（含職稱字串） |
| `address` | text | 中文地址 |
| `city` / `district` | text | 由地址解析（篩選用） |
| `phone` / `fax` | text | |
| `join_date` | text | 入會年月日（原始字串，如「1970 年 10 月 31 日」） |
| `reg_no` / `tax_id` | text | 註冊編號、統一編號 |
| `scope` | text | 甲種／乙種／綜合旅行業 |
| `email` / `website` | text | |

## 3. Supabase 資料表設計（提案，尚未建立）

> ⚠️ 建表屬高風險操作，由 William 或 Claude 執行；此處僅為規格。

```sql
-- 會員名錄（公開資料）
create table members (
  id          bigint generated always as identity primary key,
  name        text not null,
  name_en     text,
  boss        text,
  rep         text,
  address     text,
  city        text,
  district    text,
  phone       text,
  fax         text,
  join_date   text,           -- 保留原始字串；如需排序另加 join_on date
  reg_no      text,
  tax_id      text,
  scope       text,           -- 甲種旅行業 / 乙種旅行業 / 綜合旅行業
  email       text,
  website     text,
  is_active   boolean default true,
  updated_at  timestamptz default now()
);
create index on members (district);
create index on members (scope);

-- 最新消息
create table news (
  id          bigint generated always as identity primary key,
  category    text not null,  -- guild/official/event/media/industry/tourism
  title       text not null,
  summary     text,
  body        text,
  published_on date not null,
  is_hot      boolean default false
);

-- 活動
create table events (
  id          bigint generated always as identity primary key,
  category    text not null,  -- tte/training/forum/b2b
  title       text not null,
  venue       text,
  starts_on   date not null,
  ends_on     date not null,
  capacity    int,
  registered  int default 0
);

-- 各種詢問（聯絡、入會、合作提案、廣告）
create table inquiries (
  id          bigint generated always as identity primary key,
  kind        text not null,  -- contact/join/proposal/ad
  payload     jsonb not null, -- 表單欄位原樣存入
  created_at  timestamptz default now(),
  handled     boolean default false
);
```

**RLS 建議**：`members`／`news`／`events` 開 anon 唯讀（公開資料）；`inquiries` 只開 insert、不開 select（前台只能投、不能讀）；後台用 authenticated 角色全權。

## 4. API 契約（REST，Supabase PostgREST 直接可用）

| 用途 | 現況 | 未來 endpoint |
|---|---|---|
| 會員列表 | `GET assets/data/members.json` | `GET /rest/v1/members?select=*&order=name` |
| 依行政區篩選 | 前端 filter | `GET /rest/v1/members?district=eq.中山區` |
| 關鍵字搜尋 | 前端 filter | `GET /rest/v1/members?name=ilike.*關鍵字*` |
| 消息列表 | 寫死 | `GET /rest/v1/news?order=published_on.desc` |
| 活動列表 | 寫死 | `GET /rest/v1/events?order=starts_on.asc` |
| 表單送出 | 無（示範） | `POST /rest/v1/inquiries`（body: `{kind, payload}`） |

前端只需一隻共用 wrapper（帶 `apikey` header 的 fetch）；金鑰用 anon public key（RLS 保護），值放部署環境變數，不進 git。

> 公文呈現原則（William 2026-07-23）：公文**一律有內容頁**（doc.html 式：字號、主旨、說明、附件下載鈕），不得讓使用者點了公文直接開一個 PDF 分頁。

## 5. 後台（Admin）規劃

**最小可行後台**（建議直接利用 Supabase 生態，不自刻）：
1. **第一階段**：用 Supabase Dashboard 的 Table Editor 當後台——消息、活動、名錄的新增編輯已足用，零開發。
2. **第二階段**（若要給秘書處非技術人員用）：做一個受密碼保護的 `/admin/` 靜態頁（Supabase Auth email 登入），提供：消息 CRUD、活動 CRUD、inquiries 收件匣（標記已處理）、名錄 CSV 匯入。
3. **名錄更新工作流**：`travel/同業名錄-TATA/scrape_tata.py` 重撈（有禮貌延遲，勿改猛）→ 轉 JSON → upsert 進 `members`（以 `tax_id` 為唯一鍵）。

**表單通知**：`inquiries` 新增時用 Supabase Database Webhook → 打 LINE/Email 通知秘書處（生態內已有 LINE bot 基礎可借鑑）。

## 6. 維運備忘

- **改共用 header/footer**：改 `index.html` → 重跑 `tools/genpages.py` 重新產出 8 個分頁（腳本目前在 `/tmp/tata-audit/genpages.py`，建議移入 `tools/` 並納入版控）。
- **圖片與影片來源**：見 `CREDITS.txt`（全部 Wikimedia Commons / Pexels 免費授權）。hero 影片為 480p 免費素材，升級時同路徑替換即可。
- **理監事照片與名單**：目前為 Pexels 示意肖像（CREDITS.txt 有註明），正式站需換真實照片與姓名。
- **委員會名單**：`about.html#committees` 的 18 個名稱為合理推測的示範編制，正式名單以公會公告為準。
- **消息/活動資料**：目前為示範文案（日期已調整為 2026 下半年讓倒數有效），正式站由 `news`/`events` 表驅動。
- **設計規範**：見 `DESIGN.md`（深藍金、全站黑體 Noto Sans TC、圓角 ≤12px、禁彩虹色）。策略文件見 `PRODUCT.md`。
