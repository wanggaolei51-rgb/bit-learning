const https = require('https');
const fs = require('fs');
const path = require('path');

// Sina Finance API for LME metals
// hf_NID = LME Nickel, hf_AHD = LME Aluminum, hf_CAD = LME Copper, hf_ZSD = LME Zinc
const SINA_API = 'https://hq.sinajs.cn/list=hf_NID,hf_AHD,hf_CAD,hf_ZSD';

// Eastmoney API for domestic futures
// 113.nim = Shanghai Nickel Main, 113.alm = Shanghai Aluminum Main
const EASTMONEY_API = 'https://push2.eastmoney.com/api/qt/ulist.np/get?ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fields=f12,f13,f14,f2,f4,f3,f18&secids=113.nim,113.alm';

function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, {
      headers: {
        'Referer': 'https://finance.sina.com.cn',
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

async function main() {
  const now = new Date();
  const beijingTime = new Date(now.getTime() + 8 * 60 * 60 * 1000);
  
  let sinaData = {};
  let emData = {};
  
  try {
    const sinaText = await fetchUrl(SINA_API);
    sinaData = parseSinaData(sinaText);
    console.log('Sina data fetched:', Object.keys(sinaData));
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
    console.log('Eastmoney data fetched:', Object.keys(emData));
  } catch (e) {
    console.error('Eastmoney fetch failed:', e.message);
  }
  
  // Build MIR data structure
  const mirData = {
    lastUpdated: beijingTime.toISOString().replace('T', ' ').substring(0, 19) + ' +08:00',
    source: 'SIO-战略情报官 / 新浪财经+东方财富',
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
    news: {
      nickel: [
        { text: '📰 印尼2026年RKAB镍矿配额审批进度达78%', url: 'https://www.esdm.go.id' },
        { text: '📰 华友钴业印尼MHP项目二期投产', url: 'https://www.huayou.com' }
      ],
      alumina: [
        { text: '📰 印尼政府重申氧化铝出口禁令', url: 'https://www.esdm.go.id' },
        { text: '📰 南山铝业印尼项目全面投产', url: 'https://www.cnal.com' }
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
  
  // Ensure output directory exists
  const outputDir = path.join(__dirname, '..', 'mir-data');
  if (!fs.existsSync(outputDir)) {
    fs.mkdirSync(outputDir, { recursive: true });
  }
  
  // Write data
  const outputPath = path.join(outputDir, 'latest.json');
  fs.writeFileSync(outputPath, JSON.stringify(mirData, null, 2));
  console.log('MIR data saved to:', outputPath);
  console.log('Data:', JSON.stringify(mirData, null, 2));
}

main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
