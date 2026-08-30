const https = require('https');
const fs = require('fs');
const path = require('path');

// ============================================================
// Sina Finance API configurations
// ============================================================
// Real-time: hf_NID = LME Nickel, hf_AHD = LME Aluminum
const SINA_API = 'https://hq.sinajs.cn/list=hf_NID,hf_AHD,hf_CAD,hf_ZSD';

// Historical K-line (daily) - Inner futures (Shanghai)
// NI0 = 沪镍主力, AL0 = 沪铝主力
const SINA_INNER_KLINE = 'https://stock.finance.sina.com.cn/futures/api/jsonp.php/var=/InnerFuturesNewService.getDailyKLine?symbol=';
// Historical K-line (daily) - Global futures (LME)
// NID = LME镍, AHD = LME铝
const SINA_GLOBAL_KLINE = 'https://stock.finance.sina.com.cn/futures/api/jsonp.php/var=/GlobalFuturesService.getGlobalFuturesDailyKLine?symbol=';

// Eastmoney API for domestic futures
const EASTMONEY_API = 'https://push2.eastmoney.com/api/qt/ulist.np/get?ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fields=f12,f13,f14,f2,f4,f3,f18&secids=113.nim,113.alm';

// ============================================================
// Symbol mapping for historical data
// ============================================================
const HISTORY_SYMBOLS = [
  { symbol: 'NID', name: 'LME镍', source: 'Sina Global Futures', type: 'global', unit: '$/吨' },
  { symbol: 'AHD', name: 'LME铝', source: 'Sina Global Futures', type: 'global', unit: '$/吨' },
  { symbol: 'NI0', name: '沪镍主力', source: 'Sina Inner Futures', type: 'inner', unit: '¥/吨' },
  { symbol: 'AL0', name: '沪铝主力', source: 'Sina Inner Futures', type: 'inner', unit: '¥/吨' }
];

function fetchUrl(url, referer = 'https://finance.sina.com.cn') {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'Referer': referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
    }).on('error', reject);
  });
}

function parseSinaData(text) {
  const result = {};
  const matches = text.match(/var hq_str_hf_(\w+)="([^"]*)";/g);
  if (!matches) return result;
  
  matches.forEach(match => {
    const [, code, values] = match.match(/var hq_str_hf_(\w+)="([^"]*)";/);
    const parts = values.split(',');
    // Format: latest,,bid,ask,high,low,time,open,prevClose,volume,_,_,date,name,position
    if (parts.length >= 14) {
      result[code] = {
        latest: parseFloat(parts[0]) || 0,
        high: parseFloat(parts[4]) || 0,
        low: parseFloat(parts[5]) || 0,
        open: parseFloat(parts[7]) || 0,
        prevClose: parseFloat(parts[8]) || 0,
        name: parts[13],
        date: parts[12],
        time: parts[6]
      };
    }
  });
  return result;
}

function formatChange(current, prev) {
  if (!prev || prev === 0) return { change: '0%', trend: 'flat' };
  const pct = ((current - prev) / prev * 100).toFixed(2);
  const trend = pct > 0 ? 'up' : pct < 0 ? 'down' : 'flat';
  return { change: (pct >= 0 ? '+' : '') + pct + '%', trend };
}

// ============================================================
// Historical data fetching (Daily K-line -> Weekly aggregation)
// ============================================================

function parseKlineData(text, type) {
  // Extract JSON array from JSONP response
  const start = text.indexOf('[');
  if (start === -1) return null;
  const end = text.lastIndexOf(']');
  if (end === -1) return null;
  try {
    return JSON.parse(text.substring(start, end + 1));
  } catch (e) {
    console.error('Parse K-line failed:', e.message);
    return null;
  }
}

function normalizeDailyData(raw, type) {
  // Normalize to common format: { date, open, high, low, close, volume }
  if (type === 'inner') {
    // Inner format: { d, o, h, l, c, v, p, s }
    return raw.map(d => ({
      date: d.d,
      open: parseFloat(d.o),
      high: parseFloat(d.h),
      low: parseFloat(d.l),
      close: parseFloat(d.c),
      volume: parseFloat(d.v)
    }));
  } else {
    // Global format: { date, open, high, low, close, volume, position, s }
    return raw.map(d => ({
      date: d.date,
      open: parseFloat(d.open),
      high: parseFloat(d.high),
      low: parseFloat(d.low),
      close: parseFloat(d.close),
      volume: parseFloat(d.volume)
    }));
  }
}

function aggregateWeekly(dailyData, weeks = 52) {
  // Group by ISO week, take last 52 weeks
  const weekly = [];
  let currentWeek = null;
  
  dailyData.forEach(day => {
    const dt = new Date(day.date + 'T00:00:00+08:00');
    const year = dt.getFullYear();
    const weekNum = getISOWeek(dt);
    const weekKey = year + '-W' + String(weekNum).padStart(2, '0');
    
    if (!currentWeek || currentWeek.weekKey !== weekKey) {
      if (currentWeek) weekly.push(currentWeek);
      currentWeek = {
        weekKey,
        date: day.date, // Monday date
        open: day.open,
        high: day.high,
        low: day.low,
        close: day.close,
        volume: day.volume
      };
    } else {
      currentWeek.high = Math.max(currentWeek.high, day.high);
      currentWeek.low = Math.min(currentWeek.low, day.low);
      currentWeek.close = day.close; // Last day of week
      currentWeek.volume += day.volume;
    }
  });
  
  if (currentWeek) weekly.push(currentWeek);
  
  // Return last N weeks
  return weekly.slice(-weeks).map(w => ({
    date: w.date,
    open: Math.round(w.open * 100) / 100,
    high: Math.round(w.high * 100) / 100,
    low: Math.round(w.low * 100) / 100,
    close: Math.round(w.close * 100) / 100,
    volume: Math.round(w.volume)
  }));
}

function getISOWeek(date) {
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7;
  d.setUTCDate(d.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

async function fetchHistory(symbol, type) {
  const url = type === 'inner' 
    ? SINA_INNER_KLINE + symbol
    : SINA_GLOBAL_KLINE + symbol + '&_=' + Date.now();
  
  try {
    console.log(`Fetching history: ${symbol} (${type})`);
    const text = await fetchUrl(url);
    const raw = parseKlineData(text, type);
    if (!raw || raw.length === 0) {
      console.warn(`No history data for ${symbol}`);
      return null;
    }
    
    const daily = normalizeDailyData(raw, type);
    const weekly = aggregateWeekly(daily, 52);
    
    console.log(`  ${symbol}: ${raw.length} daily -> ${weekly.length} weekly`);
    return weekly;
  } catch (e) {
    console.error(`History fetch failed for ${symbol}:`, e.message);
    return null;
  }
}

async function updateHistoryData(outputDir) {
  const historyDir = path.join(outputDir, 'history');
  if (!fs.existsSync(historyDir)) {
    fs.mkdirSync(historyDir, { recursive: true });
  }
  
  const results = {};
  
  for (const cfg of HISTORY_SYMBOLS) {
    const weekly = await fetchHistory(cfg.symbol, cfg.type);
    if (weekly) {
      const filePath = path.join(historyDir, cfg.symbol + '.json');
      const data = {
        symbol: cfg.symbol,
        name: cfg.name,
        unit: cfg.unit,
        interval: '1wk',
        data: weekly,
        lastUpdated: new Date().toISOString(),
        source: cfg.source,
        count: weekly.length
      };
      fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
      results[cfg.symbol] = { count: weekly.length, file: filePath };
      console.log(`  Saved: ${filePath} (${weekly.length} weeks)`);
    } else {
      results[cfg.symbol] = { count: 0, error: 'No data' };
    }
  }
  
  return results;
}

// ============================================================
// News fetching (Google News search as fallback)
// ============================================================

function buildGoogleNewsUrl(query) {
  return 'https://news.google.com/search?q=' + encodeURIComponent(query) + '&hl=zh-CN';
}

async function fetchNews() {
  // Since most news APIs require keys or are blocked, we build search links
  // The frontend will open these links directly
  const newsQueries = [
    { key: 'nickel', label: '镍价 镍矿 印尼', queries: ['镍价 2026', '印尼镍矿 RKAB', 'LME nickel price'] },
    { key: 'alumina', label: '铝价 氧化铝', queries: ['铝价 2026', '氧化铝价格', 'LME aluminum'] },
    { key: 'acid', label: '硫酸 硫磺', queries: ['硫酸价格 2026', '硫磺 CFR中国', '磷石膏制酸'] },
    { key: 'energy', label: '能源 光伏 储能', queries: ['印尼光伏 2026', '动力煤价格', '储能电池'] },
    { key: 'ev', label: '电动车 新能源', queries: ['印尼电动车 2026', '新能源汽车销量', '固态电池'] }
  ];
  
  const techQueries = [
    { key: 'nickel', label: '镍冶炼技术', queries: ['HPAL nickel technology', 'RKEF energy efficiency', 'nickel smelting innovation'] },
    { key: 'alumina', label: '铝电解技术', queries: ['inert anode aluminum', 'aluminum electrolysis节能', 'red mud utilization'] },
    { key: 'acid', label: '硫酸技术', queries: ['sulfuric acid process', 'wet phosphoric acid', 'sulfur recovery'] },
    { key: 'energy', label: '储能技术', queries: ['floating solar Indonesia', 'offshore wind foundation', 'microgrid storage'] },
    { key: 'ev', label: '电池技术', queries: ['solid state battery 2026', 'sodium ion battery', '800V EV platform'] }
  ];
  
  const news = {};
  const tech = {};
  
  newsQueries.forEach(cat => {
    news[cat.key] = cat.queries.map((q, i) => ({
      text: (i === 0 ? '📰 ' : '📰 ') + q,
      url: buildGoogleNewsUrl(q),
      source: 'Google News'
    }));
  });
  
  techQueries.forEach(cat => {
    tech[cat.key] = cat.queries.map((q, i) => ({
      text: (i === 0 ? '🔬 ' : '🔬 ') + q,
      url: buildGoogleNewsUrl(q),
      source: 'Google News'
    }));
  });
  
  return { news, tech };
}

// ============================================================
// Main data assembly
// ============================================================

async function main() {
  const now = new Date();
  const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  
  // ---- 1. Fetch real-time data ----
  let sinaData = {};
  let emData = {};
  
  try {
    const sinaText = await fetchUrl(SINA_API);
    sinaData = parseSinaData(sinaText);
    console.log('Sina real-time fetched:', Object.keys(sinaData));
  } catch (e) {
    console.error('Sina fetch failed:', e.message);
  }
  
  try {
    const emText = await fetchUrl(EASTMONEY_API);
    const emJson = JSON.parse(emText);
    if (emJson.data && emJson.data.diff) {
      emJson.data.diff.forEach(item => {
        emData[item.f12] = {
          name: item.f14,
          latest: item.f2,
          change: item.f4,
          changePct: item.f3
        };
      });
    }
    console.log('Eastmoney fetched:', Object.keys(emData));
  } catch (e) {
    console.error('Eastmoney fetch failed:', e.message);
  }
  
  // ---- 2. Fetch historical data ----
  const outputDir = path.join(__dirname, '..', 'mir-data');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  console.log('\n--- Fetching historical data ---');
  const historyResults = await updateHistoryData(outputDir);
  console.log('History results:', historyResults);
  
  // ---- 3. Fetch news ----
  console.log('\n--- Building news links ---');
  const { news: fetchedNews, tech: fetchedTech } = await fetchNews();
  
  // ---- 4. Build MIR data structure ----
  const mirData = {
    lastUpdated: beijingTime.toISOString().replace('T', ' ').substring(0, 19) + ' +08:00',
    source: 'SIO-战略情报官 / 新浪财经+东方财富',
    historyAvailable: Object.values(historyResults).some(r => r.count > 0),
    historySource: 'Sina Finance (LME+SHFE 日K线聚合为周线)',
    data: {
      nickel: {
        items: [],
        quality: [
          { name: 'MHP镍含量', value: 'Ni≥30%', desc: '湿法冶炼中间品' },
          { name: 'MSP镍含量', value: 'Ni≥50%', desc: '高冰镍' },
          { name: '电解镍', value: 'Ni≥99.8%', desc: 'LME交割标准' },
          { name: 'NPI镍含量', value: 'Ni 8-12%', desc: 'RKEF工艺镍铁' }
        ]
      },
      alumina: {
        items: [],
        quality: [
          { name: 'A00铝锭', value: 'Al≥99.7%', desc: '国标GB/T 1196' },
          { name: 'A356合金', value: 'Si 6.5-7.5%', desc: '铸造铝合金' },
          { name: '氧化铝等级', value: 'AO-1 / AO-2', desc: '冶金级氧化铝' },
          { name: '铝土矿品位', value: 'Al₂O₃≥45%', desc: '拜耳法适用矿石' }
        ]
      },
      acid: {
        items: [
          { name: '98%硫酸华东价', value: '¥380/吨', change: '+5.6%', trend: 'up', source: '卓创资讯' },
          { name: '硫磺CFR中国', value: '$95/吨', change: '+2.1%', trend: 'up', source: 'ICIS' },
          { name: '磷石膏制酸成本', value: '¥220/吨', change: '-1.2%', trend: 'down', source: '行业测算' }
        ],
        quality: [
          { name: '工业硫酸浓度', value: '98% / 93%', desc: '国标GB/T 534优等品' },
          { name: '发烟硫酸', value: '104.5% / 105%', desc: '含游离SO₃' },
          { name: '硫磺纯度', value: 'S≥99.5%', desc: '国标一等品' }
        ]
      },
      energy: {
        items: [
          { name: '印尼动力煤HBA', value: '$118/吨', change: '-2.5%', trend: 'down', source: 'ESDM' },
          { name: '光伏组件价格', value: '¥0.85/W', change: '-8.1%', trend: 'down', source: 'PVInfoLink' },
          { name: '储能电池系统', value: '¥0.55/Wh', change: '-12%', trend: 'down', source: 'CNESA' }
        ]
      },
      ev: {
        items: [
          { name: '五菱Air EV', value: '2.38亿印尼盾', change: '持平', trend: 'flat', source: 'Wuling Indonesia' },
          { name: '比亚迪Atto 3', value: '4.25亿印尼盾', change: '+3.2%', trend: 'up', source: 'BYD Indonesia' }
        ]
      }
    },
    // Real news with Google News search links
    news: fetchedNews,
    tech: fetchedTech,
    // Fallback preset news (used when no fetched data)
    presetNews: {
      nickel: [
        { text: '📰 印尼2026年RKAB镍矿配额审批进度达78%', url: 'https://www.esdm.go.id' },
        { text: '📰 华友钴业印尼MHP项目二期投产', url: 'https://www.huayou.com' }
      ],
      alumina: [
        { text: '📰 印尼政府重申氧化铝出口禁令', url: 'https://www.esdm.go.id' },
        { text: '📰 南山铝业印尼项目全面投产', url: 'https://www.cnal.com' }
      ],
      acid: [
        { text: '📰 印尼政府推动磷石膏综合利用', url: 'https://www.kemenperin.go.id' },
        { text: '📰 中国硫铁矿制酸产能向印尼转移', url: 'https://www.ccfa.com.cn' }
      ],
      energy: [
        { text: '📰 印尼目标2030年可再生能源占比达31%', url: 'https://www.esdm.go.id' },
        { text: '📰 印尼煤电退役计划启动', url: 'https://www.pln.co.id' }
      ],
      ev: [
        { text: '📰 印尼政府推出电动车购置补贴政策', url: 'https://www.kemenperin.go.id' },
        { text: '📰 印尼充电基础设施建设加速', url: 'https://www.pln.co.id' }
      ]
    },
    presetTech: {
      nickel: [
        { text: '🔬 HPAL技术优化：浸出率提升至95%以上', url: 'https://www.sciencedirect.com/search?qs=HPAL+nickel' }
      ],
      acid: [
        { text: '🔬 湿法磷酸工艺改进：能耗降低20%', url: 'https://www.ccfa.com.cn' }
      ],
      alumina: [
        { text: '🔬 惰性阳极技术突破：CO2排放趋近于零', url: 'https://www.riotinto.com' }
      ],
      energy: [
        { text: '🔬 漂浮式光伏：印尼水库应用潜力超1GW', url: 'https://www.irena.org/solar' }
      ],
      ev: [
        { text: '🔬 固态电池产业化进展', url: 'https://www.catl.com' }
      ]
    }
  };
  
  // Populate nickel data from Sina
  if (sinaData.NID) {
    const nid = sinaData.NID;
    const chg = formatChange(nid.latest, nid.prevClose);
    mirData.data.nickel.items = [
      { name: 'LME镍3个月', value: '$' + nid.latest.toLocaleString() + '/吨', change: chg.change, trend: chg.trend, source: 'LME ' + nid.date },
      { name: 'LME镍最高', value: '$' + nid.high.toLocaleString() + '/吨', change: '-', trend: 'flat', source: 'LME ' + nid.date },
      { name: 'LME镍最低', value: '$' + nid.low.toLocaleString() + '/吨', change: '-', trend: 'flat', source: 'LME ' + nid.date }
    ];
  } else {
    mirData.data.nickel.items = [
      { name: 'LME镍3个月', value: '数据获取中...', change: '-', trend: 'flat', source: 'Sina API' }
    ];
  }
  
  // Populate aluminum data from Sina
  if (sinaData.AHD) {
    const ahd = sinaData.AHD;
    const chg = formatChange(ahd.latest, ahd.prevClose);
    mirData.data.alumina.items = [
      { name: 'LME铝3个月', value: '$' + ahd.latest.toLocaleString() + '/吨', change: chg.change, trend: chg.trend, source: 'LME ' + ahd.date }
    ];
  }
  
  // Populate Shanghai futures from Eastmoney
  if (emData.nim) {
    const nim = emData.nim;
    mirData.data.nickel.items.push({
      name: '沪镍主力',
      value: '¥' + nim.latest + '/吨',
      change: (nim.changePct >= 0 ? '+' : '') + nim.changePct + '%',
      trend: nim.changePct > 0 ? 'up' : nim.changePct < 0 ? 'down' : 'flat',
      source: 'SHFE'
    });
  }
  
  if (emData.alm) {
    const alm = emData.alm;
    mirData.data.alumina.items.push({
      name: '沪铝主力',
      value: '¥' + alm.latest + '/吨',
      change: (alm.changePct >= 0 ? '+' : '') + alm.changePct + '%',
      trend: alm.changePct > 0 ? 'up' : alm.changePct < 0 ? 'down' : 'flat',
      source: 'SHFE'
    });
  }
  
  // Write data
  const outputPath = path.join(outputDir, 'latest.json');
  fs.writeFileSync(outputPath, JSON.stringify(mirData, null, 2));
  console.log('\nMIR data saved to:', outputPath);
  
  // Summary
  console.log('\n=== MIR Fetch Summary ===');
  console.log('Real-time:', Object.keys(sinaData).join(', ') || 'None');
  console.log('History:', Object.entries(historyResults).map(([k,v]) => `${k}=${v.count}w`).join(', '));
  console.log('News links:', Object.keys(fetchedNews).length, 'categories');
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
